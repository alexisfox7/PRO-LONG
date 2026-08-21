"""Opt-in connectivity smoke tests for the two real agent images."""

from __future__ import annotations

import os
import subprocess
import uuid

import pytest

from prolong_agent.environment.mcp_game import GameMcpServer


IMAGES = (
    "prolong-agent/codex-sandbox:latest",
    "prolong-agent/claude-sandbox:latest",
)


@pytest.mark.container
@pytest.mark.parametrize("image", IMAGES)
def test_agent_container_reaches_short_lived_mcp(image, make_controller):
    if os.environ.get("RUN_CONTAINER_SMOKE") != "1":
        pytest.skip("set RUN_CONTAINER_SMOKE=1 to run Docker connectivity tests")
    if subprocess.run(
        ["docker", "image", "inspect", image], capture_output=True
    ).returncode:
        pytest.skip(f"build {image} before running the smoke test")

    network = f"prolong-mcp-test-{uuid.uuid4().hex[:10]}"
    subprocess.run(
        ["docker", "network", "create", "--internal", network],
        check=True,
        capture_output=True,
    )
    controller, _ = make_controller(game_id=image.split("/")[-1].split(":")[0])
    try:
        with GameMcpServer(controller) as server:
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "--network", network,
                    "--add-host", "host.docker.internal:host-gateway",
                    "--entrypoint", "curl",
                    image,
                    "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                    "-H", f"Authorization: Bearer {server.token}",
                    server.container_url,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert result.returncode == 0, result.stderr
            assert result.stdout not in {"000", "401"}
    finally:
        subprocess.run(
            ["docker", "network", "rm", network], capture_output=True, timeout=10
        )
