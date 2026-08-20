import path from "node:path";
import { commandExists } from "../project.js";
import { hasManagedBlock, upsertManagedBlock } from "../blocks.js";
import { INSTRUCTIONS_BLOCK } from "../constants.js";
import { pathExists, readText, removePath, writeText } from "../io.js";
import { readJsonObject, writeJsonObject, type JsonObject } from "../json.js";
import type { ClientStatus, InstallManifest } from "../types.js";
import type { ClientAdapter, ManagedPath } from "./client.js";
import { isProlongHookGroup, removeBlockFile, removeEmptyHooksContainer } from "./shared.js";

const CONFIG_PATH = ".claude/settings.json";
const INSTRUCTIONS_PATH = "CLAUDE.md";
const EVENTS = ["SessionStart", "UserPromptSubmit", "PostToolUse", "Stop", "SessionEnd"] as const;

function handler(): JsonObject {
  return {
    type: "command",
    command: "node",
    args: ["${CLAUDE_PROJECT_DIR}/.prolong/runtime.mjs", "--prolong-hook", "claude-code"],
    timeout: 3,
  };
}

function installHooks(config: JsonObject): void {
  const hooks = typeof config.hooks === "object" && config.hooks !== null && !Array.isArray(config.hooks)
    ? config.hooks as JsonObject
    : {};
  config.hooks = hooks;
  for (const event of EVENTS) {
    const groups = Array.isArray(hooks[event]) ? hooks[event] as unknown[] : [];
    hooks[event] = [
      ...groups.filter((group) => !isProlongHookGroup(group, "claude-code")),
      { hooks: [handler()] },
    ];
  }
}

function removeHooks(config: JsonObject): void {
  const hooks = typeof config.hooks === "object" && config.hooks !== null && !Array.isArray(config.hooks)
    ? config.hooks as JsonObject
    : null;
  if (hooks === null) {
    return;
  }
  for (const event of EVENTS) {
    if (!Array.isArray(hooks[event])) {
      continue;
    }
    const remaining = (hooks[event] as unknown[]).filter((group) => !isProlongHookGroup(group, "claude-code"));
    if (remaining.length === 0) {
      delete hooks[event];
    } else {
      hooks[event] = remaining;
    }
  }
  removeEmptyHooksContainer(config);
}

export class ClaudeCodeAdapter implements ClientAdapter {
  readonly name = "claude-code" as const;

  constructor(private readonly root: string) {}

  async detect(): Promise<boolean> {
    return await commandExists("claude") || await pathExists(path.join(this.root, ".claude"));
  }

  async install(): Promise<ManagedPath[]> {
    const configTarget = path.join(this.root, CONFIG_PATH);
    const config = await readJsonObject(configTarget);
    installHooks(config);
    await writeJsonObject(configTarget, config);

    const instructionsTarget = path.join(this.root, INSTRUCTIONS_PATH);
    await writeText(instructionsTarget, upsertManagedBlock(await readText(instructionsTarget), INSTRUCTIONS_BLOCK));
    return [
      { path: CONFIG_PATH, mode: "merged" },
      { path: INSTRUCTIONS_PATH, mode: "block" },
    ];
  }

  async status(): Promise<ClientStatus> {
    const detected = await this.detect();
    try {
      const config = await readJsonObject(path.join(this.root, CONFIG_PATH));
      const hooks = typeof config.hooks === "object" && config.hooks !== null && !Array.isArray(config.hooks)
        ? config.hooks as JsonObject
        : {};
      const hooksInstalled = EVENTS.every((event) =>
        Array.isArray(hooks[event]) && (hooks[event] as unknown[]).some((group) => isProlongHookGroup(group, "claude-code"))
      );
      const instructionsInstalled = hasManagedBlock(await readText(path.join(this.root, INSTRUCTIONS_PATH)));
      const installed = hooksInstalled && instructionsInstalled;
      return {
        name: this.name,
        detected,
        installed,
        healthy: installed,
        detail: installed ? "5 lifecycle hooks and CLAUDE.md pointer installed" : "hooks or CLAUDE.md pointer are missing",
      };
    } catch (error) {
      return { name: this.name, detected, installed: false, healthy: false, detail: (error as Error).message };
    }
  }

  async uninstall(_manifest: InstallManifest | null): Promise<string[]> {
    const configTarget = path.join(this.root, CONFIG_PATH);
    if (await pathExists(configTarget)) {
      const config = await readJsonObject(configTarget);
      removeHooks(config);
      if (Object.keys(config).length === 0) {
        await removePath(configTarget);
      } else {
        await writeJsonObject(configTarget, config);
      }
    }
    await removeBlockFile(this.root, INSTRUCTIONS_PATH);
    return [];
  }
}
