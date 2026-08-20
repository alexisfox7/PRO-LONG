import path from "node:path";
import { commandExists } from "../project.js";
import { pathExists, removePath } from "../io.js";
import { readJsonObject, writeJsonObject, type JsonObject } from "../json.js";
import type { ClientStatus, InstallManifest } from "../types.js";
import type { ClientAdapter, ManagedPath } from "./client.js";
import { isProlongHookGroup, removeEmptyHooksContainer } from "./shared.js";

const CONFIG_PATH = ".codex/hooks.json";
const EVENTS = ["SessionStart", "UserPromptSubmit", "PostToolUse", "Stop", "SessionEnd"] as const;
const COMMAND = 'node "$(git rev-parse --show-toplevel)/.prolong/runtime.mjs" --prolong-hook codex';

function handler(): JsonObject {
  return {
    type: "command",
    command: COMMAND,
    commandWindows: 'node "$(git rev-parse --show-toplevel)\\.prolong\\runtime.mjs" --prolong-hook codex',
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
      ...groups.filter((group) => !isProlongHookGroup(group, "codex")),
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
    const remaining = (hooks[event] as unknown[]).filter((group) => !isProlongHookGroup(group, "codex"));
    if (remaining.length === 0) {
      delete hooks[event];
    } else {
      hooks[event] = remaining;
    }
  }
  removeEmptyHooksContainer(config);
}

export class CodexAdapter implements ClientAdapter {
  readonly name = "codex" as const;

  constructor(private readonly root: string) {}

  async detect(): Promise<boolean> {
    return await commandExists("codex") || await pathExists(path.join(this.root, ".codex"));
  }

  async install(): Promise<ManagedPath[]> {
    const target = path.join(this.root, CONFIG_PATH);
    const config = await readJsonObject(target);
    installHooks(config);
    await writeJsonObject(target, config);
    return [{ path: CONFIG_PATH, mode: "merged" }];
  }

  async status(): Promise<ClientStatus> {
    const detected = await this.detect();
    try {
      const config = await readJsonObject(path.join(this.root, CONFIG_PATH));
      const hooks = typeof config.hooks === "object" && config.hooks !== null && !Array.isArray(config.hooks)
        ? config.hooks as JsonObject
        : {};
      const installed = EVENTS.every((event) =>
        Array.isArray(hooks[event]) && (hooks[event] as unknown[]).some((group) => isProlongHookGroup(group, "codex"))
      );
      return {
        name: this.name,
        detected,
        installed,
        healthy: installed,
        detail: installed ? "5 lifecycle hooks installed" : "hooks are missing",
      };
    } catch (error) {
      return { name: this.name, detected, installed: false, healthy: false, detail: (error as Error).message };
    }
  }

  async uninstall(_manifest: InstallManifest | null): Promise<string[]> {
    const target = path.join(this.root, CONFIG_PATH);
    if (!await pathExists(target)) {
      return [];
    }
    const config = await readJsonObject(target);
    removeHooks(config);
    if (Object.keys(config).length === 0) {
      await removePath(target);
    } else {
      await writeJsonObject(target, config);
    }
    return [];
  }
}
