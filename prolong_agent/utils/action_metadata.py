"""Build ARC-AGI-3 reasoning-field metadata for each submitted action.

ARC renders a per-action ``reasoning`` field on the online replay viewer and
uses it for cost/analysis. The schema follows
``arcprize/arc-agi-3-benchmarking`` ActionMetadata: ``output``, ``reasoning``,
``usage`` (OpenAI ResponseUsage shape), ``cost``. Arbitrary extra fields are
allowed; we add ``commands``, ``plan``, and ``aggregate``. ARC rejects payloads
over 16 KB, so we truncate the text fields to fit.
"""
from __future__ import annotations

import json
from typing import Any

MAX_BYTES = 16_000            # ARC caps at 16,384; keep margin
_MARKER = "\n... truncated {n} chars ...\n"


def _sizeof(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, separators=(",", ":")).encode("utf-8"))


def _cap(text: str, keep: int) -> str:
    removed = len(text) - keep
    if removed <= 0:
        return text
    head = (keep + 1) // 2
    tail = keep // 2
    return text[:head] + _MARKER.format(n=removed) + (text[-tail:] if tail else "")


def _fit(payload: dict[str, Any]) -> dict[str, Any]:
    """Shrink the largest text field(s) until the payload is under MAX_BYTES."""
    text_fields = ("reasoning", "output")
    for _ in range(24):
        over = _sizeof(payload) - MAX_BYTES
        if over <= 0:
            return payload
        # find the longest text field and trim it by a bit more than `over`
        longest = max(text_fields, key=lambda k: len(payload.get(k) or ""))
        cur = payload.get(longest) or ""
        if not cur:
            # nothing left to trim in text; drop the heaviest extra field
            for k in ("commands", "aggregate", "plan"):
                if k in payload:
                    del payload[k]
                    break
            else:
                return payload
            continue
        payload[longest] = _cap(cur, max(0, len(cur) - over - 64))
    return payload


def build(
    *,
    output: str = "",
    reasoning: str = "",
    input_tokens: int = 0,
    cached_tokens: int = 0,
    output_tokens: int = 0,
    reasoning_tokens: int = 0,
    cost_usd: float = 0.0,
    commands: list[str] | None = None,
    plan: dict[str, Any] | None = None,
    aggregate: dict[str, Any] | None = None,
    model: str = "",
) -> dict[str, Any]:
    """Assemble one action's metadata dict, fitted under the ARC size cap."""
    total = input_tokens + output_tokens
    payload: dict[str, Any] = {
        "output": output or "",
        "usage": {
            "input_tokens": int(input_tokens),
            "input_tokens_details": {"cached_tokens": int(cached_tokens)},
            "output_tokens": int(output_tokens),
            "output_tokens_details": {"reasoning_tokens": int(reasoning_tokens)},
            "total_tokens": int(total),
        },
        "cost": {"total_cost": round(float(cost_usd), 6)},
    }
    if reasoning:
        payload["reasoning"] = reasoning
    if commands:
        payload["commands"] = commands[:8]
    if plan:
        payload["plan"] = plan
    if aggregate:
        payload["aggregate"] = aggregate
    if model:
        payload["model"] = model
    return _fit(payload)
