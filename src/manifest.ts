import path from "node:path";
import { MANIFEST_PATH } from "./constants.js";
import { readText, sha256, writeText } from "./io.js";
import type { InstallManifest, ManagedFile, ManagedFileMode } from "./types.js";

export async function loadManifest(root: string): Promise<InstallManifest | null> {
  const content = await readText(path.join(root, MANIFEST_PATH));
  if (content === null) {
    return null;
  }
  try {
    const parsed = JSON.parse(content) as InstallManifest;
    if (parsed.schemaVersion !== 1 || !Array.isArray(parsed.clients) || !Array.isArray(parsed.files)) {
      throw new Error("unsupported manifest schema");
    }
    return parsed;
  } catch (error) {
    throw new Error(`Cannot read ${MANIFEST_PATH}: ${(error as Error).message}`);
  }
}

export async function saveManifest(root: string, manifest: InstallManifest): Promise<void> {
  await writeText(path.join(root, MANIFEST_PATH), `${JSON.stringify(manifest, null, 2)}\n`);
}

export async function describeManagedFile(
  root: string,
  relativePath: string,
  mode: ManagedFileMode,
): Promise<ManagedFile> {
  const content = await readText(path.join(root, relativePath));
  if (content === null) {
    throw new Error(`Expected managed file ${relativePath} to exist`);
  }
  return { path: relativePath, mode, sha256: sha256(content) };
}

export function manifestFile(manifest: InstallManifest | null, relativePath: string): ManagedFile | undefined {
  return manifest?.files.find((file) => file.path === relativePath);
}
