"""Memory-condition selection shared by the research runners and agents."""

from __future__ import annotations

import warnings
from enum import Enum


class MemoryMode(str, Enum):
    FULL_LOG = "full-log"
    WINDOWED_LOG = "windowed-log"
    IN_PROMPT = "in-prompt"
    MCP_NO_LOG = "mcp-no-log"


def resolve_memory_mode(
    *,
    no_log: bool = False,
    in_prompt: bool = False,
    log_window: int | None = None,
) -> tuple[MemoryMode, int | None]:
    """Resolve public flags to one unambiguous internal memory condition."""
    if log_window is not None and log_window != -1 and log_window < 1:
        raise ValueError("--log-window must be -1 or a positive integer")

    selected = int(no_log) + int(in_prompt) + int(log_window is not None)
    if selected > 1:
        raise ValueError("--no-log, --in-prompt, and --log-window are mutually exclusive")

    if no_log:
        return MemoryMode.MCP_NO_LOG, None
    if in_prompt:
        return MemoryMode.IN_PROMPT, None
    if log_window == -1:
        warnings.warn(
            "--log-window -1 is deprecated; use --in-prompt instead",
            FutureWarning,
            stacklevel=2,
        )
        return MemoryMode.IN_PROMPT, None
    if log_window is not None:
        return MemoryMode.WINDOWED_LOG, log_window
    return MemoryMode.FULL_LOG, None
