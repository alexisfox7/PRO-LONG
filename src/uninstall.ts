import path from "node:path";
import { createAdapters } from "./clients/index.js";
import { LOG_PATH, MANIFEST_PATH, RUNTIME_PATH, SKILL_METADATA_PATH, SKILL_PATH } from "./constants.js";
import { pathExists, removeEmptyParents, removePath } from "./io.js";
import { loadManifest } from "./manifest.js";
import { readTemplate } from "./templates.js";
import { CLIENT_NAMES } from "./types.js";
import { removeBlockFile, removeOwnedFile } from "./clients/shared.js";

export interface UninstallOptions {
  root: string;
  purge?: boolean;
}

export interface UninstallResult {
  root: string;
  purged: boolean;
  warnings: string[];
}

export async function uninstallProject(options: UninstallOptions): Promise<UninstallResult> {
  const root = path.resolve(options.root);
  const manifest = await loadManifest(root);
  const adapters = createAdapters(root, manifest);
  const warnings: string[] = [];

  for (const client of CLIENT_NAMES) {
    warnings.push(...await adapters[client].uninstall(manifest));
  }

  await removeBlockFile(root, "AGENTS.md");
  await removeBlockFile(root, "CLAUDE.md");
  await removeBlockFile(root, ".gitignore");

  let preserveRuntime = warnings.length > 0;
  if (preserveRuntime) {
    warnings.push(`Preserved ${RUNTIME_PATH} because a modified adapter still imports it`);
  } else {
    const runtimeWarning = await removeOwnedFile(root, RUNTIME_PATH, manifest, await readTemplate("runtime.mjs"));
    if (runtimeWarning !== null) {
      warnings.push(runtimeWarning);
      preserveRuntime = true;
    }
  }

  const ownedFiles: Array<[string, string]> = [
    [SKILL_PATH, "prolong/SKILL.md"],
    [SKILL_METADATA_PATH, "prolong/agents/openai.yaml"],
  ];
  for (const [relativePath, template] of ownedFiles) {
    const warning = await removeOwnedFile(root, relativePath, manifest, await readTemplate(template));
    if (warning !== null) {
      warnings.push(warning);
    }
  }

  if (options.purge === true) {
    if (preserveRuntime) {
      await removePath(path.join(root, LOG_PATH));
      await removePath(path.join(root, MANIFEST_PATH));
    } else {
      await removePath(path.join(root, ".prolong"), true);
    }
  } else {
    await removePath(path.join(root, MANIFEST_PATH));
    await removeEmptyParents(path.join(root, ".prolong"), root);
  }

  for (const directory of [
    ".agents/skills/prolong/agents",
    ".agents/skills/prolong",
    ".agents/skills",
    ".agents",
    ".codex",
    ".claude",
    ".opencode/plugins",
    ".opencode",
    ".pi/extensions",
    ".pi",
  ]) {
    const target = path.join(root, directory);
    if (await pathExists(target)) {
      await removeEmptyParents(target, root);
    }
  }

  return { root, purged: options.purge === true, warnings };
}
