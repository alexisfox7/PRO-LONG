"""ActionQueue: FIFO action drain with score-change flushing."""
from __future__ import annotations

import logging
from collections import deque

log = logging.getLogger(__name__)


class QueueExhausted(RuntimeError):
    pass


VALID_ACTIONS = frozenset({
    "ACTION1", "ACTION2", "ACTION3", "ACTION4",
    "ACTION5", "ACTION6", "ACTION7", "RESET",
})


class ActionQueue:

    def __init__(self) -> None:
        self._queue: deque[dict] = deque()
        self.plan_total: int = 0
        self.plan_index: int = 0
        self._last_score: int = 0
        self.score_changed: bool = False

    def clear(self) -> None:
        self._queue.clear()
        self.plan_total = 0
        self.plan_index = 0

    def reset(self) -> None:
        self.clear()
        self._last_score = 0
        self.score_changed = False

    def __len__(self) -> int:
        return len(self._queue)

    def __bool__(self) -> bool:
        return bool(self._queue)

    def pop(self) -> dict:
        action = self._queue.popleft()
        self.plan_index += 1
        return action

    def push_front(self, action: dict) -> None:
        self._queue.appendleft(action)
        if self.plan_index > 0:
            self.plan_index -= 1

    def snapshot(self) -> list[dict]:
        return [{"name": a.get("name"), "data": a.get("data", {})} for a in self._queue]

    def check_score(self, score: int) -> None:
        if score != self._last_score:
            if self._queue:
                log.info("score %d->%d: flushing %d queued actions",
                         self._last_score, score, len(self._queue))
                self.clear()
            self.score_changed = True
            self._last_score = score

    def load(self, actions: list[dict], batch_meta: dict | None = None) -> bool:
        if not actions:
            log.warning("ActionQueue.load: empty action list")
            return False

        self._queue.clear()
        for step in actions:
            name = step.get("name", "")
            if name not in VALID_ACTIONS:
                log.warning("skipping unrecognized action: %s", name)
                continue
            self._queue.append({
                "name": name,
                "data": step.get("data", {}),
                "obs_text": "",
                "action_text": "",
                "batch_meta": batch_meta,
                "batch_head": False,
            })
        if self._queue:
            self._queue[0]["batch_head"] = True

        self.plan_total = len(self._queue)
        self.plan_index = 0

        if not self._queue:
            log.warning("ActionQueue.load: no valid actions after filtering")
            return False

        log.info("loaded %d-step plan: %s",
                 self.plan_total,
                 [s.get("name") for s in actions])
        return True
