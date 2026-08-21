from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from prolong_agent.environment.game_session import GameSessionController


def observation(
    *,
    game_id: str = "test-game",
    state: str = "NOT_FINISHED",
    score: int = 0,
    actions: list[int] | None = None,
    fill: int = 0,
) -> dict:
    return {
        "game_id": game_id,
        "state": state,
        "score": score,
        "frame": [[[fill, fill], [fill, fill]]],
        "available_actions": actions if actions is not None else [1, 2, 6],
        "guid": f"guid-{game_id}",
    }


class FakeEnv:
    def __init__(self, initial: dict | None = None, scripted: list[dict] | None = None) -> None:
        self.initial = initial or observation()
        self.scripted = list(scripted or [])
        self.calls: list[dict] = []
        self.last = deepcopy(self.initial)

    def reset(self, task=None):
        self.last = deepcopy(self.initial)
        return deepcopy(self.last)

    def step(self, action):
        self.calls.append(action)
        if self.scripted:
            self.last = deepcopy(self.scripted.pop(0))
        return deepcopy(self.last), 0.0, False


@pytest.fixture
def make_controller(tmp_path: Path):
    def factory(*, env: FakeEnv | None = None, max_actions: int = 500, game_id="test-game"):
        env = env or FakeEnv(observation(game_id=game_id))
        controller = GameSessionController(
            env=env,
            game_id=game_id,
            agent_name="test-agent",
            max_actions=max_actions,
            trace_path=tmp_path / game_id / "logs.txt",
            log_post_board=True,
        )
        controller.start()
        return controller, env

    return factory
