import path from "node:path";
import { upsertManagedBlock } from "./blocks.js";
import {
  GITIGNORE_BLOCK,
  INSTRUCTIONS_BLOCK,
  LOG_PATH,
  PACKAGE_VERSION,
  RUNTIME_PATH,
  SKILL_METADATA_PATH,
  SKILL_PATH,
} from "./constants.js";
import { createAdapters } from "./clients/index.js";
import { writeOwnedFile } from "./clients/shared.js";
import { readText, writeText } from "./io.js";
import { readJsonObject } from "./json.js";
import { describeManagedFile, loadManifest, saveManifest } from "./manifest.js";
import { readTemplate } from "./templates.js";
import type { ClientName, InstallManifest, ManagedFile, ManagedFileMode } from "./types.js";
import { CLIENT_NAMES } from "./types.js";

export interface InitOptions {
  root: string;
  clients?: ClientName[];
}

export interface InitResult {
  root: string;
  clients: ClientName[];
  detected: ClientName[];
  manifest: InstallManifest;
}

export async function initProject(options: InitOptions): Promise<InitResult> {
  const root = path.resolve(options.root);
  const previousManifest = await loadManifest(root);
  const adapters = createAdapters(root, previousManifest);
  const detected = (await Promise.all(
    CLIENT_NAMES.map(async (name) => ({ name, detected: await adapters[name].detect() })),
  )).filter((result) => result.detected).map((result) => result.name);

  const requested = options.clients ?? detected;
  const clients = [...new Set([...(previousManifest?.clients ?? []), ...requested])];

  // Parse shared JSON configs before writing anything so malformed user files
  // cannot leave a partially initialized installation.
  if (clients.includes("codex")) {
    await readJsonObject(path.join(root, ".codex/hooks.json"));
  }
  if (clients.includes("claude-code")) {
    await readJsonObject(path.join(root, ".claude/settings.json"));
  }

  const runtime = await readTemplate("runtime.mjs");
  const skill = await readTemplate("prolong/SKILL.md");
  const skillMetadata = await readTemplate("prolong/agents/openai.yaml");
  await writeOwnedFile(root, RUNTIME_PATH, runtime, previousManifest, "PRO-LONG runtime");
  await writeOwnedFile(root, SKILL_PATH, skill, previousManifest);
  await writeOwnedFile(root, SKILL_METADATA_PATH, skillMetadata, previousManifest);

  const agentsPath = path.join(root, "AGENTS.md");
  await writeText(agentsPath, upsertManagedBlock(await readText(agentsPath), INSTRUCTIONS_BLOCK));

  const gitignorePath = path.join(root, ".gitignore");
  await writeText(gitignorePath, upsertManagedBlock(await readText(gitignorePath), GITIGNORE_BLOCK));

  const logTarget = path.join(root, LOG_PATH);
  if (await readText(logTarget) === null) {
    await writeText(logTarget, "");
  }

  const managedPaths: Array<{ path: string; mode: ManagedFileMode }> = [
    { path: RUNTIME_PATH, mode: "owned" },
    { path: SKILL_PATH, mode: "owned" },
    { path: SKILL_METADATA_PATH, mode: "owned" },
    { path: "AGENTS.md", mode: "block" },
    { path: ".gitignore", mode: "block" },
  ];
  for (const client of clients) {
    managedPaths.push(...await adapters[client].install());
  }

  const files: ManagedFile[] = [];
  for (const managed of managedPaths) {
    files.push(await describeManagedFile(root, managed.path, managed.mode));
  }

  const manifest: InstallManifest = {
    schemaVersion: 1,
    packageVersion: PACKAGE_VERSION,
    installedAt: new Date().toISOString(),
    clients,
    files,
  };
  await saveManifest(root, manifest);
  return { root, clients, detected, manifest };
}
