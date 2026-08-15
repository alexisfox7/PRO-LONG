"""Environment package."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseEnv(ABC):
    @abstractmethod
    def reset(self, task: dict | None = None) -> dict:
        pass

    @abstractmethod
    def step(self, action: Any) -> tuple[dict, float, bool]:
        pass

    def close(self):
        return


from prolong_agent.environment.arcagi3 import ArcAgi3Env

__all__ = ["BaseEnv", "ArcAgi3Env"]
