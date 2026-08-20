import type { InstallManifest, ClientName } from "../types.js";
import type { ClientAdapter } from "./client.js";
import { ClaudeCodeAdapter } from "./claude-code.js";
import { CodexAdapter } from "./codex.js";
import { OpenCodeAdapter } from "./opencode.js";
import { PiAdapter } from "./pi.js";

export function createAdapters(root: string, manifest: InstallManifest | null): Record<ClientName, ClientAdapter> {
  return {
    codex: new CodexAdapter(root),
    "claude-code": new ClaudeCodeAdapter(root),
    opencode: new OpenCodeAdapter(root, manifest),
    pi: new PiAdapter(root, manifest),
  };
}
