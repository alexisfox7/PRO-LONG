from __future__ import annotations

from conftest import FakeEnv, observation
from prolong_agent.environment.runner import InteractiveMcpGameRunner
from prolong_agent.metrics.structures import Status


def test_zero_progress_calls_end_as_agent_stalled(tmp_path):
    calls = []

    def agent(run_dir, action_num, **kwargs):
        calls.append((run_dir, action_num, kwargs))
        return {"meta": {"input_tokens": 1, "output_tokens": 1}}

    runner = InteractiveMcpGameRunner(
        env=FakeEnv(initial=observation(state="NOT_FINISHED")),
        game_id="stall",
        agent_name="fake",
        max_actions_per_game=20,
        prompts_log_path=tmp_path / "stall" / "logs.txt",
        agent=agent,
        agent_retries=2,
    )
    metrics = runner.run()
    assert metrics.status == Status.AGENT_STALLED
    assert len(calls) == 2
    assert calls[0][1] == calls[1][1] == 0
    assert "mcp_url" in calls[0][2]
    assert "mcp_token" in calls[0][2]


def test_early_exit_resumes_same_live_session(tmp_path):
    env = FakeEnv(initial=observation(state="NOT_FINISHED"))
    seen = []

    def agent(run_dir, action_num, **kwargs):
        seen.append((run_dir, action_num, kwargs["mcp_url"], kwargs["mcp_token"]))
        runner._session.execute_action({"name": "ACTION1", "data": {}})
        if len(seen) == 2:
            runner._session.arc_state = type(runner._session.arc_state).WIN
        return {"meta": {}}

    runner = InteractiveMcpGameRunner(
        env=env,
        game_id="resume",
        agent_name="fake",
        max_actions_per_game=10,
        prompts_log_path=tmp_path / "resume" / "logs.txt",
        agent=agent,
        agent_retries=3,
    )
    runner.run()
    assert len(seen) == 2
    assert seen[0][0] == seen[1][0]
    assert seen[0][2:] == seen[1][2:]
    assert seen[1][1] == seen[0][1] + 1
