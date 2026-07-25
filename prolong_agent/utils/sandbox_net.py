"""Secure-by-default sandbox networking.

Agent containers run on an --internal docker network (no direct internet,
host, or metadata access) and reach their LLM API only through a squid
allowlist proxy. The proxy container is attached to both the internal
network and the default bridge so it alone has egress.

Opt out with CODEX_DOCKER_NETWORK=host / CLAUDE_DOCKER_NETWORK=host.
"""
import logging
import subprocess

log = logging.getLogger(__name__)

INTERNAL_NETWORK = "rgb-internal"

_ensured: set[str] = set()


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), capture_output=True, text=True)


def ensure_secure_network(proxy_name: str, proxy_image: str, build_dir: str) -> None:
    """Idempotently create the internal network and start the egress proxy."""
    if proxy_name in _ensured:
        return
    if _run("docker", "network", "inspect", INTERNAL_NETWORK).returncode != 0:
        r = _run("docker", "network", "create", "--internal", INTERNAL_NETWORK)
        if r.returncode != 0 and "already exists" not in r.stderr:
            raise RuntimeError(f"could not create docker network {INTERNAL_NETWORK}: {r.stderr}")
    state = _run("docker", "inspect", "-f", "{{.State.Running}}", proxy_name)
    if state.returncode != 0 or state.stdout.strip() != "true":
        _run("docker", "rm", "-f", proxy_name)
        r = _run("docker", "run", "-d", "--restart", "unless-stopped",
                 "--name", proxy_name, proxy_image)
        if r.returncode != 0:
            raise RuntimeError(
                f"could not start egress proxy {proxy_name!r}. Build it first:\n"
                f"  docker build -t {proxy_image} {build_dir}\n"
                f"or opt out of the sandbox lockdown with *_DOCKER_NETWORK=host.\n{r.stderr}")
        c = _run("docker", "network", "connect", INTERNAL_NETWORK, proxy_name)
        if c.returncode != 0 and "already exists" not in c.stderr:
            raise RuntimeError(f"could not attach {proxy_name} to {INTERNAL_NETWORK}: {c.stderr}")
        log.info("started egress proxy %s on %s", proxy_name, INTERNAL_NETWORK)
    _ensured.add(proxy_name)
