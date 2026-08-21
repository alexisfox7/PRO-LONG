"""Game loop that drives the action queue through an ARC-AGI-3 environment."""

import json
import logging
import time
from pathlib import Path
from typing import Optional

from arcengine import GameState as ArcGameState

from prolong_agent.agent import ActionQueue, QueueExhausted
from prolong_agent.environment import ArcAgi3Env
from prolong_agent.environment.game_session import GameSessionController
from prolong_agent.environment.mcp_game import GameMcpServer
from prolong_agent.metrics.structures import GameMetrics, Status
from prolong_agent.utils import action_metadata

log = logging.getLogger(__name__)

_RETRY_NUDGE = (
    "Your previous response did not produce a valid /workspace/actions.json. "
    "Please write one with the shape {\"actions\": [...]}."
)


class GameRunner:
    """Runs a game using an agent and its queued actions."""

    def __init__(
        self,
        *,
        env: ArcAgi3Env,
        game_id: str,
        agent_name: str,
        max_actions_per_game: int,
        run_index: int = 1,
        tags: Optional[list[str]] = None,
        prompts_log_path: Optional[Path] = None,
        agent=None,
        log_post_board: bool = False,
        agent_retries: int = 5,
        agent_kwargs: Optional[dict] = None,
    ) -> None:
        self.env = env
        self.game_id = game_id
        self.agent_name = agent_name
        self.max_actions_per_game = max_actions_per_game
        self.run_index = run_index
        self.tags = tags
        self.prompts_log_path = prompts_log_path
        self.agent = agent
        self.log_post_board = log_post_board
        self.agent_retries = agent_retries
        self._session = GameSessionController(
            env=env,
            game_id=game_id,
            agent_name=agent_name,
            max_actions=max_actions_per_game,
            run_index=run_index,
            tags=tags,
            trace_path=prompts_log_path,
            log_post_board=log_post_board,
            grid_mode=(agent_kwargs or {}).get("grid_mode", "hex"),
        )
        self._state = self._session.state
        self._queue = ActionQueue()
        self._last_cost: float = 0.0
        self._last_agent_duration: float = 0.0
        self._usage = self._session.usage
        self._recent_actions: list[str] = []

    def _next_action(self) -> dict:
        obs = self._state.last_observation or {}
        state = obs.get("state", "NOT_PLAYED")

        if state in ("NOT_PLAYED", "GAME_OVER") and self._state.last_executed_action != "RESET":
            return {"name": "RESET", "data": {}, "obs_text": "Game Over, starting new game.", "action_text": ""}

        use_queued = bool(self._queue and not self._queue.score_changed)
        if not use_queued:
            self._queue.score_changed = False

        if use_queued and self._queue:
            action = self._queue.pop()
            # Guard against double-RESET or RESET-after-WIN triggering full_reset.
            _reset_unsafe = action.get("name") == "RESET" and (
                self._state.last_executed_action == "RESET"
                or state == "WIN"
            )
            if _reset_unsafe:
                _reason = ("duplicate RESET" if self._state.last_executed_action == "RESET"
                           else f"RESET while state={state}")
                log.warning(
                    "inserting ACTION7 no-op before %s (%d queued remaining)",
                    _reason, len(self._queue),
                )
                self._queue.push_front(action)
                action = {
                    "name": "ACTION7",
                    "data": {},
                    "obs_text": "",
                    "action_text": f"[injected ACTION7 no-op before {_reason}]",
                }
            label = f"plan step {self._queue.plan_index}/{self._queue.plan_total}"
            action["obs_text"] = ""
            action["action_text"] = f"[queued {label}]"

            log.info("queue drain -> %s (%s, %d remaining)",
                     action.get("name"), label, len(self._queue))
            return action

        log.info("queue empty — need a new plan from the agent")
        raise QueueExhausted("Queue empty, no actions from agent")


    def _build_action_metadata(self, action_dict: dict, action_num: int) -> str:
        """ARC reasoning-field JSON for one action. Full stats on batch heads;
        light stub on queued drains so replay analysis has per-action data."""
        meta = action_dict.get("batch_meta")
        name = action_dict.get("name", "?")
        data = action_dict.get("data", {})
        act_str = (f"ACTION6({data.get('x',0)},{data.get('y',0)})"
                   if name == "ACTION6" else name)
        aggregate = {
            "agent_calls": self._usage["calls"],
            "actions": action_num + 1,
            "input_tokens": self._usage["in"],
            "output_tokens": self._usage["out"],
            "cache_read_tokens": self._usage["cache_read"],
            "cost_usd": round(self._usage["cost"], 4),
        }
        if meta and action_dict.get("batch_head"):
            payload = action_metadata.build(
                output=meta.get("output", ""),
                input_tokens=meta.get("input_tokens", 0),
                cached_tokens=meta.get("cached_tokens", 0),
                output_tokens=meta.get("output_tokens", 0),
                reasoning_tokens=meta.get("reasoning_tokens", 0),
                cost_usd=meta.get("call_cost_usd", 0.0),
                commands=meta.get("commands"),
                plan={"step": f"{self._queue.plan_index}/{self._queue.plan_total}",
                      "action": act_str},
                aggregate=aggregate,
                model=meta.get("model", ""),
            )
        else:
            payload = action_metadata.build(
                output=f"queued plan step {self._queue.plan_index}/{self._queue.plan_total}: {act_str}",
                plan={"step": f"{self._queue.plan_index}/{self._queue.plan_total}",
                      "action": act_str},
                aggregate=aggregate,
            )
        try:
            return json.dumps(payload, separators=(",", ":"))
        except Exception:
            return f"Action: {name}"

    def _wait_for_plan(self, action_num, score, level):
        backoff = 30
        while True:
            for attempt in range(self.agent_retries):
                nudge = _RETRY_NUDGE if attempt else ""
                log.info(
                    "agent attempt %d/%d action=%d nudge=%s",
                    attempt + 1, self.agent_retries, action_num, bool(nudge),
                )
                if self._call_agent(action_num, score, retry_nudge=nudge, level_num=level):
                    return
                log.warning("agent attempt %d/%d failed", attempt + 1, self.agent_retries)

            log.warning(
                "all %d agent attempts failed at action %d — sleeping %ds "
                "before retrying (will not close scorecard)",
                self.agent_retries, action_num, backoff,
            )
            time.sleep(backoff)
            backoff = min(backoff * 2, 300)

    def _remember_action(self, action):
        name = action.get("name", "?")
        if name == "ACTION6":
            data = action.get("data", {})
            name = f"ACTION6({data.get('x', 0)},{data.get('y', 0)})"
        self._recent_actions.append(name)

    def _write_current_board(self, score, action_num):
        if not self.prompts_log_path:
            return
        board_path = self.prompts_log_path.parent / "current_board.txt"
        grid = self._state.render_board(include_animation=False)
        with open(board_path, "w", encoding="utf-8") as output:
            output.write(f"Score: {score}\nAction: {action_num}\n\n")
            if grid:
                output.write(f"[CURRENT BOARD STATE]\n{grid}\n")

    def _append_post_action_board(self):
        if not self.prompts_log_path:
            return
        grid = self._state.render_board()
        if not grid:
            return
        for _ in range(3):
            try:
                with open(self.prompts_log_path, "a", encoding="utf-8") as output:
                    output.write(f"[POST-ACTION BOARD STATE]\n{grid}\n\n")
                return
            except PermissionError:
                time.sleep(0.5)
        log.warning("failed to write board state after 3 retries (PermissionError)")

    def _record_usage(self, meta):
        return self._session.record_usage(meta)

    def run(self) -> GameMetrics:
        try:
            self._queue.reset()
            self._session.start()
            self._available_action_names = self._session.available_action_names
            log.info("[%s] Available actions: %s", self.game_id, ", ".join(self._available_action_names))
            self._write_current_board(self._session.arc_score, 0)

            while not self._session.exhausted:
                try:
                    action_dict = self._next_action()
                except QueueExhausted:
                    log.info("queue exhausted at action %d — calling agent", self._session.total_actions)
                    self._wait_for_plan(
                        self._session.total_actions,
                        self._session.arc_score,
                        self._session.level_num,
                    )
                    action_dict = self._next_action()

                action_dict["action_metadata"] = self._build_action_metadata(
                    action_dict, self._session.total_actions
                )
                action_dict["plan_step"] = (
                    f"{self._queue.plan_index}/{self._queue.plan_total}"
                    if self._queue.plan_total else None
                )
                self._remember_action(action_dict)
                outcome = self._session.execute_action(action_dict)
                self._available_action_names = self._session.available_action_names
                self._queue.check_score(self._session.arc_score)

                if outcome.state == ArcGameState.WIN:
                    break

        except QueueExhausted as e:
            log.info("[%s Run %d] Episode ended (queue exhausted): %s", self.game_id, self.run_index, e)
            self._session.metrics.status = Status.QUEUE_EXHAUSTED

        except Exception as e:
            self._session.metrics.status = Status.ERROR
            self._session.metrics.error_message = str(e)
            self._session.attempt_metrics.status = Status.ERROR
            self._session.level_metrics.status = Status.ERROR
            log.error("[%s Run %d] Exception: %s", self.game_id, self.run_index, e, exc_info=True)
        return self._session.finalize()

    def _call_agent(self, action_num: int, arc_score: int, retry_nudge: str = "",
                    level_num: int = 1) -> bool:
        if not self.agent:
            return False
        if self.prompts_log_path and not self.log_post_board:
            self._append_post_action_board()

        self._write_current_board(arc_score, action_num)

        kwargs = {
            "score": arc_score,
            "level": level_num,
            "last_actions": ", ".join(self._recent_actions[-5:]) if self._recent_actions else "none",
            "available_actions_list": list(self._available_action_names),
            "available_actions": ", ".join(self._available_action_names),
        }

        t0 = time.time()
        result = self.agent(self.prompts_log_path, action_num, retry_nudge=retry_nudge, **kwargs)
        self._last_agent_duration = time.time() - t0
        if not result:
            log.warning("agent returned None at action %d (%.1fs)", action_num, self._last_agent_duration)
            return False

        self._last_cost = result.get("cost", self._last_cost)
        self._state.set_external_hint(result["hint"])
        self._state.set_persistent_hint(result["plan"])

        actions = result.get("actions", [])
        meta = self._record_usage(result.get("meta"))
        if actions:
            if self._queue.load(actions, batch_meta=meta):
                log.info("agent at action %d: loaded %d actions", action_num, len(actions))
                return True
            log.warning("agent at action %d: queue rejected the actions", action_num)
            return False

        log.warning("agent at action %d: no actions from actions.json", action_num)
        return False

class InteractiveMcpGameRunner:
    """Let a resumed coding-agent session operate the game through MCP."""

    def __init__(
        self,
        *,
        env: ArcAgi3Env,
        game_id: str,
        agent_name: str,
        max_actions_per_game: int,
        run_index: int = 1,
        tags: Optional[list[str]] = None,
        prompts_log_path: Path,
        agent=None,
        log_post_board: bool = True,
        agent_retries: int = 5,
        agent_kwargs: Optional[dict] = None,
    ) -> None:
        self.agent = agent
        self.agent_retries = max(1, agent_retries)
        self.run_dir = prompts_log_path.parent
        self._session = GameSessionController(
            env=env,
            game_id=game_id,
            agent_name=agent_name,
            max_actions=max_actions_per_game,
            run_index=run_index,
            tags=tags,
            trace_path=prompts_log_path,
            log_post_board=log_post_board,
            grid_mode=(agent_kwargs or {}).get("grid_mode", "hex"),
        )

    def run(self) -> GameMetrics:
        server: GameMcpServer | None = None
        try:
            self._session.start()
            if (
                self._session.arc_state in (ArcGameState.NOT_PLAYED, ArcGameState.GAME_OVER)
                and not self._session.exhausted
            ):
                reset = {"name": "RESET", "data": {}, "plan_step": "automatic"}
                reset["action_metadata"] = self._session.build_action_metadata(
                    reset,
                    output="MCP automatic initial RESET",
                    step=1,
                    total=1,
                )
                self._session.execute_action(reset)

            server = GameMcpServer(self._session).start()
            stalled_calls = 0
            while not self._session.won and not self._session.exhausted:
                before = self._session.total_actions
                nudge = (
                    "Use the MCP tools now and make progress on the live game."
                    if stalled_calls else ""
                )
                result = None
                if self.agent:
                    result = self.agent(
                        self.run_dir,
                        self._session.total_actions,
                        mcp_url=server.container_url,
                        mcp_token=server.token,
                        retry_nudge=nudge,
                    )
                if result:
                    self._session.record_usage(result.get("meta"))
                executed = self._session.total_actions - before
                if executed:
                    stalled_calls = 0
                else:
                    stalled_calls += 1
                    log.warning(
                        "MCP agent made no progress (%d/%d consecutive calls)",
                        stalled_calls,
                        self.agent_retries,
                    )
                    if stalled_calls >= self.agent_retries:
                        self._session.set_stalled()
                        break
        except Exception as exc:
            self._session.metrics.status = Status.ERROR
            self._session.metrics.error_message = str(exc)
            self._session.attempt_metrics.status = Status.ERROR
            self._session.level_metrics.status = Status.ERROR
            log.error("interactive MCP runner failed: %s", exc, exc_info=True)
        finally:
            if server:
                server.close()
        return self._session.finalize()
