import path from "node:path";
import { hasManagedBlock } from "./blocks.js";
import { createAdapters } from "./clients/index.js";
import { LOG_PATH } from "./constants.js";
import { fileSize, readText, sha256 } from "./io.js";
import { loadManifest } from "./manifest.js";
import type { ProjectStatus } from "./types.js";
import { CLIENT_NAMES } from "./types.js";

export async function getProjectStatus(rootInput: string): Promise<ProjectStatus> {
  const root = path.resolve(rootInput);
  const manifest = await loadManifest(root);
  const adapters = createAdapters(root, manifest);
  const clients = await Promise.all(CLIENT_NAMES.map((name) => adapters[name].status()));
  const common: ProjectStatus["common"] = [];

  if (manifest !== null) {
    for (const file of manifest.files.filter((candidate) =>
      candidate.path === ".prolong/runtime.mjs"
      || candidate.path.startsWith(".agents/skills/prolong/")
      || candidate.path === "AGENTS.md"
      || candidate.path === ".gitignore"
    )) {
      const content = await readText(path.join(root, file.path));
      if (file.mode === "block") {
        const healthy = hasManagedBlock(content);
        common.push({ path: file.path, healthy, detail: healthy ? "managed block present" : "managed block missing" });
      } else {
        const healthy = content !== null && sha256(content) === file.sha256;
        common.push({ path: file.path, healthy, detail: healthy ? "installed" : "missing or modified" });
      }
    }
  }

  const installedClients = new Set(manifest?.clients ?? []);
  const relevantClientsHealthy = clients
    .filter((client) => installedClients.has(client.name))
    .every((client) => client.healthy);
  const healthy = manifest !== null
    && common.length >= 5
    && common.every((item) => item.healthy)
    && relevantClientsHealthy;

  return {
    root,
    initialized: manifest !== null,
    healthy,
    ...(manifest === null ? {} : { packageVersion: manifest.packageVersion }),
    logPath: path.join(root, LOG_PATH),
    logBytes: await fileSize(path.join(root, LOG_PATH)),
    common,
    clients,
  };
}

export function formatStatus(status: ProjectStatus): string {
  const lines = [
    `PRO-LONG ${status.initialized ? (status.healthy ? "is healthy" : "needs attention") : "is not initialized"}`,
    `Project: ${status.root}`,
    `Log: ${status.logPath} (${status.logBytes} bytes)`,
  ];
  if (status.initialized) {
    lines.push(`Version: ${status.packageVersion ?? "unknown"}`);
  }
  for (const client of status.clients) {
    const state = client.installed ? (client.healthy ? "ok" : "broken") : (client.detected ? "detected" : "not detected");
    lines.push(`- ${client.name}: ${state} — ${client.detail}`);
  }
  return `${lines.join("\n")}\n`;
}
