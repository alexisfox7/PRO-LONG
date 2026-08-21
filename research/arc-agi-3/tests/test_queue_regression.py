from __future__ import annotations

from conftest import FakeEnv, observation
from prolong_agent.agent.action_queue import ActionQueue
from prolong_agent.environment.runner import GameRunner
from prolong_agent.metrics.structures import Status


def test_existing_queue_flushes_after_score_change():
    queue = ActionQueue()
    assert queue.load([
        {"name": "ACTION1", "data": {}},
        {"name": "ACTION2", "data": {}},
    ])
    queue.check_score(1)
    assert not queue
    assert queue.score_changed


def test_queued_runner_still_generates_metrics_and_private_trace(tmp_path):
    env = FakeEnv(scripted=[observation(state="WIN", score=1, fill=5)])

    def agent(log_path, action_num, **kwargs):
        assert log_path.name == "logs.txt"
        return {
            "hint": "test",
            "plan": "take one action",
            "actions": [{"name": "ACTION1", "data": {}}],
            "meta": {
                "output": "test",
                "input_tokens": 3,
                "output_tokens": 2,
                "cached_tokens": 0,
                "call_cost_usd": 0.01,
                "model": "fake",
            },
        }

    trace = tmp_path / "queued" / "logs.txt"
    metrics = GameRunner(
        env=env,
        game_id="queued",
        agent_name="fake",
        max_actions_per_game=5,
        prompts_log_path=trace,
        agent=agent,
        log_post_board=True,
    ).run()

    assert metrics.status == Status.COMPLETED_RUN
    assert metrics.run_total_actions == 1
    assert metrics.final_score == 1
    assert trace.exists()
    trace_text = trace.read_text()
    assert "INITIAL BOARD STATE" in trace_text
    assert "Tool Call: ACTION1" in trace_text
    assert "POST-ACTION BOARD STATE" in trace_text
