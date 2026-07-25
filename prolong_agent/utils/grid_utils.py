"""Grid formatting utilities."""
from __future__ import annotations

_ASCII_PALETTE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1EG[]?-_+~<>i!lI;:,\"^`'. "


def format_grid_ascii(grid: list[list[int]], mode: str = "ascii") -> str:
    """Format a grid of 4-bit values (0-15) as text.

    Modes:
        ascii  — map to ASCII palette characters (default)
        hex    — single hex digit per cell (0-9, a-f)
        num    — space-separated decimal numbers
    """
    if not grid:
        return "(empty grid)"
    if mode == "hex":
        lines = []
        for row in grid:
            lines.append("".join(f"{max(0, min(15, int(v))):x}" for v in row))
        return "\n".join(lines)
    elif mode == "num":
        lines = []
        for row in grid:
            lines.append(" ".join(f"{max(0, min(15, int(v))):2d}" for v in row))
        return "\n".join(lines)
    else:  # ascii
        palette = _ASCII_PALETTE
        n = len(palette)
        lines = []
        for row in grid:
            chars = []
            for v in row:
                idx = min(int((max(0, min(15, int(v))) / 16) * (n - 1)), n - 1)
                chars.append(palette[idx])
            lines.append("".join(chars))
        return "\n".join(lines)
