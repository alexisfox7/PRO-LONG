export const CLIENT_NAMES = ["codex", "claude-code", "opencode", "pi"] as const;

export type ClientName = (typeof CLIENT_NAMES)[number];
export type ManagedFileMode = "owned" | "merged" | "block";

export interface ManagedFile {
  path: string;
  mode: ManagedFileMode;
  sha256: string;
}

export interface InstallManifest {
  schemaVersion: 1;
  packageVersion: string;
  installedAt: string;
  clients: ClientName[];
  files: ManagedFile[];
}

export interface ClientStatus {
  name: ClientName;
  detected: boolean;
  installed: boolean;
  healthy: boolean;
  detail: string;
}

export interface ProjectStatus {
  root: string;
  initialized: boolean;
  healthy: boolean;
  packageVersion?: string;
  logPath: string;
  logBytes: number;
  common: Array<{
    path: string;
    healthy: boolean;
    detail: string;
  }>;
  clients: ClientStatus[];
}

export function isClientName(value: string): value is ClientName {
  return (CLIENT_NAMES as readonly string[]).includes(value);
}
