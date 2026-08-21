"""Authenticated, per-game Streamable HTTP MCP server."""

from __future__ import annotations

import secrets
import socket
import threading
import time
from typing import Annotated, Any, Literal

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from prolong_agent.environment.game_session import GameSessionController

MAX_BATCH_ACTIONS = 20


class SubmittedAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal[
        "ACTION1",
        "ACTION2",
        "ACTION3",
        "ACTION4",
        "ACTION5",
        "ACTION6",
        "ACTION7",
        "RESET",
    ]
    x: Annotated[int, Field(strict=True, ge=0, le=63)] | None = None
    y: Annotated[int, Field(strict=True, ge=0, le=63)] | None = None

    @model_validator(mode="after")
    def validate_coordinates(self) -> SubmittedAction:
        coordinate_fields = self.model_fields_set & {"x", "y"}
        if self.action == "ACTION6" and coordinate_fields != {"x", "y"}:
            raise ValueError("ACTION6 requires x and y")
        if self.action != "ACTION6" and coordinate_fields:
            raise ValueError(f"{self.action} does not accept coordinates")
        return self


class BearerAuthMiddleware:
    def __init__(self, app: Any, token: str) -> None:
        self.app = app
        self._expected = f"Bearer {token}".encode()

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope.get("type") == "http":
            headers = dict(scope.get("headers", []))
            supplied = headers.get(b"authorization", b"")
            if not secrets.compare_digest(supplied, self._expected):
                await send(
                    {
                        "type": "http.response.start",
                        "status": 401,
                        "headers": [
                            (b"content-type", b"application/json"),
                            (b"www-authenticate", b"Bearer"),
                        ],
                    }
                )
                await send(
                    {
                        "type": "http.response.body",
                        "body": b'{"error":"unauthorized"}',
                    }
                )
                return
        await self.app(scope, receive, send)


class GameMcpServer:
    """Expose one controller through exactly two MCP tools."""

    def __init__(self, controller: GameSessionController) -> None:
        self.controller = controller
        self.token = secrets.token_urlsafe(32)
        self._lock = threading.Lock()
        self._mcp = MCPServer(
            "prolong-game",
            instructions="Inspect the current board and submit validated game actions.",
        )
        self._register_tools()
        self._socket: socket.socket | None = None
        self._server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None
        self.port: int | None = None

    @property
    def local_url(self) -> str:
        if self.port is None:
            raise RuntimeError("MCP server is not running")
        return f"http://127.0.0.1:{self.port}/mcp"

    @property
    def container_url(self) -> str:
        if self.port is None:
            raise RuntimeError("MCP server is not running")
        return f"http://host.docker.internal:{self.port}/mcp"

    def _register_tools(self) -> None:
        @self._mcp.tool(name="current_board", structured_output=True)
        def current_board() -> dict[str, Any]:
            """Return the live game observation and remaining action budget."""
            return self.current_board()

        @self._mcp.tool(name="submit_actions", structured_output=True)
        def submit_actions(
            actions: Annotated[
                list[SubmittedAction],
                Field(min_length=1, max_length=MAX_BATCH_ACTIONS),
            ],
        ) -> dict[str, Any]:
            """Validate and immediately execute a batch of one to twenty actions."""
            return self.submit_actions(actions)

    def current_board(self) -> dict[str, Any]:
        with self._lock:
            return self.controller.observation

    def submit_actions(
        self, actions: list[SubmittedAction | dict[str, Any]]
    ) -> dict[str, Any]:
        with self._lock:
            validated = self._validate_batch(actions)
            submitted = len(validated)
            executed = 0
            automatic_actions: list[str] = []
            stop_reason = "batch_complete"

            for index, action in enumerate(validated, start=1):
                if self.controller.exhausted:
                    stop_reason = "action_budget_exhausted"
                    break
                action["plan_step"] = f"{index}/{submitted}"
                action["action_metadata"] = self.controller.build_action_metadata(
                    action,
                    output=f"MCP submit_actions batch of {submitted}",
                    step=index,
                    total=submitted,
                )
                outcome = self.controller.execute_action(action)
                executed += 1

                if outcome.state.name == "WIN":
                    stop_reason = "win"
                    break
                if outcome.state.name == "GAME_OVER":
                    stop_reason = "game_over"
                    if not self.controller.exhausted:
                        reset = {
                            "name": "RESET",
                            "data": {},
                            "plan_step": "automatic",
                        }
                        reset["action_metadata"] = (
                            self.controller.build_action_metadata(
                                reset,
                                output="MCP automatic RESET after GAME_OVER",
                                step=1,
                                total=1,
                            )
                        )
                        self.controller.execute_action(reset)
                        automatic_actions.append("RESET")
                        stop_reason = "game_over_reset"
                    break
                if outcome.exhausted:
                    stop_reason = "action_budget_exhausted"
                    break
                if outcome.score_changed:
                    stop_reason = "score_changed"
                    break

            return {
                "submitted_count": submitted,
                "executed_count": executed,
                "automatic_actions": automatic_actions,
                "stop_reason": stop_reason,
                "observation": self.controller.observation,
            }

    def _validate_batch(self, actions: Any) -> list[dict[str, Any]]:
        if not isinstance(actions, list):
            raise ToolError("actions must be an array")
        if not 1 <= len(actions) <= MAX_BATCH_ACTIONS:
            raise ToolError("actions must contain 1 to 20 entries")

        available = set(self.controller.available_action_names)
        validated: list[dict[str, Any]] = []
        for index, entry in enumerate(actions):
            try:
                parsed = (
                    entry
                    if isinstance(entry, SubmittedAction)
                    else SubmittedAction.model_validate(entry)
                )
            except ValidationError as exc:
                message = exc.errors(include_url=False)[0]["msg"]
                raise ToolError(f"actions[{index}] is invalid: {message}") from exc

            name = parsed.action
            if name not in available:
                raise ToolError(f"actions[{index}].action {name} is unavailable")
            if name == "ACTION6":
                validated.append({"name": name, "data": {"x": parsed.x, "y": parsed.y}})
            else:
                validated.append({"name": name, "data": {}})
        return validated

    def start(self) -> GameMcpServer:
        if self._thread:
            return self
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", 0))
        sock.listen(128)
        self.port = sock.getsockname()[1]
        self._socket = sock

        security = TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=["127.0.0.1:*", "localhost:*", "host.docker.internal:*"],
            allowed_origins=[
                "http://127.0.0.1:*",
                "http://localhost:*",
                "http://host.docker.internal:*",
            ],
        )
        app = self._mcp.streamable_http_app(
            streamable_http_path="/mcp",
            json_response=True,
            stateless_http=True,
            transport_security=security,
            host="0.0.0.0",
        )
        config = uvicorn.Config(
            BearerAuthMiddleware(app, self.token),
            host="0.0.0.0",
            port=self.port,
            log_level="warning",
            access_log=False,
        )
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(
            target=self._server.run,
            kwargs={"sockets": [sock]},
            name=f"mcp-{self.controller.game_id}",
            daemon=True,
        )
        self._thread.start()
        deadline = time.monotonic() + 5
        while not self._server.started and self._thread.is_alive():
            if time.monotonic() >= deadline:
                self.close()
                raise RuntimeError("MCP server failed to start")
            time.sleep(0.01)
        if not self._server.started:
            self.close()
            raise RuntimeError("MCP server exited before startup completed")
        return self

    def close(self) -> None:
        if self._server:
            self._server.should_exit = True
        if self._thread:
            self._thread.join(timeout=5)
        if self._socket:
            try:
                self._socket.close()
            except OSError:
                pass
        self._thread = None
        self._server = None
        self._socket = None

    def __enter__(self) -> GameMcpServer:
        return self.start()

    def __exit__(self, *_: Any) -> None:
        self.close()
