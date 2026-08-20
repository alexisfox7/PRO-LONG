import type { ClientName, ClientStatus, InstallManifest, ManagedFileMode } from "../types.js";

export interface ManagedPath {
  path: string;
  mode: ManagedFileMode;
}

export interface ClientAdapter {
  readonly name: ClientName;
  detect(): Promise<boolean>;
  install(): Promise<ManagedPath[]>;
  status(): Promise<ClientStatus>;
  uninstall(manifest: InstallManifest | null): Promise<string[]>;
}
