from __future__ import annotations

import asyncio

import httpx2
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.server.mcpserver.exceptions import ToolError

from conftest import FakeEnv, observation
from prolong_agent.environment.mcp_game import GameMcpServer


async def _mcp_call(server, tool, arguments):
    async with httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {server.token}"},
        trust_env=False,
    ) as http:
        async with streamable_http_client(server.local_url, http_client=http) as streams:
            async with ClientSession(*streams[:2]) as session:
                await session.initialize()
                return await session.call_tool(tool, arguments)


def test_mcp_requires_the_per_game_bearer_token(make_controller):
    controller, _ = make_controller()
    with GameMcpServer(controller) as server:
        async def requests():
            async with httpx2.AsyncClient(trust_env=False) as client:
                missing = await client.post(server.local_url, json={})
                wrong = await client.post(
                    server.local_url,
                    headers={"Authorization": "Bearer wrong"},
                    json={},
                )
                return missing, wrong

        missing, wrong = asyncio.run(requests())
        assert missing.status_code == 401
        assert wrong.status_code == 401
        result = asyncio.run(_mcp_call(server, "current_board", {}))
        assert result.structured_content["game_id"] == "test-game"


def test_parallel_game_servers_are_isolated(make_controller):
    first, _ = make_controller(game_id="first")
    second, _ = make_controller(game_id="second")
    with GameMcpServer(first) as one, GameMcpServer(second) as two:
        async def cross_token():
            async with httpx2.AsyncClient(
                headers={"Authorization": f"Bearer {one.token}"}, trust_env=False
            ) as client:
                return await client.post(two.local_url, json={})

        assert asyncio.run(cross_token()).status_code == 401
        assert asyncio.run(_mcp_call(one, "current_board", {})).structured_content["game_id"] == "first"
        assert asyncio.run(_mcp_call(two, "current_board", {})).structured_content["game_id"] == "second"


def test_tool_schemas_and_current_board_shape(make_controller):
    controller, _ = make_controller(max_actions=12)
    with GameMcpServer(controller) as server:
        async def schemas():
            async with httpx2.AsyncClient(
                headers={"Authorization": f"Bearer {server.token}"}, trust_env=False
            ) as http:
                async with streamable_http_client(server.local_url, http_client=http) as streams:
                    async with ClientSession(*streams[:2]) as session:
                        await session.initialize()
                        return await session.list_tools()

        tools = {tool.name: tool for tool in asyncio.run(schemas()).tools}
        assert set(tools) == {"current_board", "submit_actions"}
        assert tools["current_board"].input_schema["properties"] == {}
        assert tools["current_board"].input_schema["type"] == "object"
        actions_schema = tools["submit_actions"].input_schema["properties"]["actions"]
        assert actions_schema["type"] == "array"
        assert actions_schema["minItems"] == 1
        assert actions_schema["maxItems"] == 20
        action_definition = next(iter(tools["submit_actions"].input_schema["$defs"].values()))
        assert action_definition["additionalProperties"] is False
        assert "plan" not in action_definition["properties"]
        assert "rationale" not in action_definition["properties"]
        board = server.current_board()
        assert board["state"] == "PLAYING"
        assert board["remaining_actions"] == 12
        assert board["board"] == ["00", "00"]


@pytest.mark.parametrize("bad", [
    [],
    [{"action": "ACTION1"}] * 21,
    [{"action": "NOPE"}],
    [{"action": "ACTION4"}],
    [{"action": "ACTION1", "plan": "because"}],
    [{"action": "ACTION1", "x": 1}],
    [{"action": "ACTION6"}],
    [{"action": "ACTION6", "x": -1, "y": 2}],
    [{"action": "ACTION6", "x": 1, "y": 64}],
    [{"action": "ACTION6", "x": True, "y": 2}],
])
def test_malformed_or_unavailable_batches_are_rejected_atomically(make_controller, bad):
    controller, env = make_controller()
    server = GameMcpServer(controller)
    with pytest.raises(ToolError):
        server.submit_actions(bad)
    assert env.calls == []


def test_entire_batch_is_validated_before_execution(make_controller):
    controller, env = make_controller()
    server = GameMcpServer(controller)
    with pytest.raises(ToolError):
        server.submit_actions([
            {"action": "ACTION1"},
            {"action": "ACTION6", "x": 100, "y": 1},
        ])
    assert env.calls == []


def test_immediate_execution_and_score_change_flush(make_controller):
    env = FakeEnv(scripted=[
        observation(score=0, fill=1),
        observation(score=1, fill=2),
        observation(score=1, fill=3),
    ])
    controller, env = make_controller(env=env)
    result = GameMcpServer(controller).submit_actions([
        {"action": "ACTION1"},
        {"action": "ACTION2"},
        {"action": "ACTION1"},
    ])
    assert result["submitted_count"] == 3
    assert result["executed_count"] == 2
    assert result["stop_reason"] == "score_changed"
    assert result["observation"]["score"] == 1
    assert result["observation"]["board"] == ["22", "22"]
    assert len(env.calls) == 2


def test_win_stops_batch(make_controller):
    env = FakeEnv(scripted=[observation(state="WIN", score=1)])
    controller, env = make_controller(env=env)
    result = GameMcpServer(controller).submit_actions([
        {"action": "ACTION1"}, {"action": "ACTION2"}
    ])
    assert result["executed_count"] == 1
    assert result["stop_reason"] == "win"
    assert result["observation"]["state"] == "WIN"


def test_game_over_stops_and_automatically_resets(make_controller):
    env = FakeEnv(scripted=[
        observation(state="GAME_OVER"),
        observation(state="NOT_FINISHED", fill=4),
    ])
    controller, env = make_controller(env=env)
    result = GameMcpServer(controller).submit_actions([
        {"action": "ACTION1"}, {"action": "ACTION2"}
    ])
    assert result["executed_count"] == 1
    assert result["automatic_actions"] == ["RESET"]
    assert result["stop_reason"] == "game_over_reset"
    assert result["observation"]["state"] == "PLAYING"
    assert len(env.calls) == 2


def test_action_budget_stops_batch(make_controller):
    controller, env = make_controller(max_actions=2)
    result = GameMcpServer(controller).submit_actions([
        {"action": "ACTION1"}, {"action": "ACTION2"}, {"action": "ACTION1"}
    ])
    assert result["executed_count"] == 2
    assert result["stop_reason"] == "action_budget_exhausted"
    assert result["observation"]["remaining_actions"] == 0
    assert len(env.calls) == 2
