FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl git nodejs npm bubblewrap \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @openai/codex@latest

RUN useradd -m -u 1000 -s /bin/bash sandbox

USER sandbox
WORKDIR /workspace

ENTRYPOINT ["codex"]
