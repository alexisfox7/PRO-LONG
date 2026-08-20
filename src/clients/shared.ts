import path from "node:path";
import { removeManagedBlock } from "../blocks.js";
import { manifestFile } from "../manifest.js";
import { readText, removeEmptyParents, removePath, sha256, writeText } from "../io.js";
import type { InstallManifest } from "../types.js";

export function isProlongHookGroup(value: unknown, client: string): boolean {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const hooks = (value as { hooks?: unknown }).hooks;
  if (!Array.isArray(hooks)) {
    return false;
  }
  return hooks.some((hook) => {
    if (typeof hook !== "object" || hook === null) {
      return false;
    }
    const candidate = hook as { command?: unknown; args?: unknown };
    const command = typeof candidate.command === "string" ? candidate.command : "";
    const args = Array.isArray(candidate.args) ? candidate.args.join(" ") : "";
    return `${command} ${args}`.includes(".prolong/runtime.mjs")
      && `${command} ${args}`.includes(client);
  });
}

export async function writeOwnedFile(
  root: string,
  relativePath: string,
  content: string,
  manifest: InstallManifest | null,
  generatedMarker?: string,
): Promise<void> {
  const target = path.join(root, relativePath);
  const current = await readText(target);
  const owned = manifestFile(manifest, relativePath)?.mode === "owned";
  const generated = generatedMarker !== undefined && current?.includes(generatedMarker) === true;

  if (current !== null && current !== content && !owned && !generated) {
    throw new Error(`Refusing to overwrite existing ${relativePath}; move it aside or uninstall it first.`);
  }
  await writeText(target, content);
}

export async function removeOwnedFile(
  root: string,
  relativePath: string,
  manifest: InstallManifest | null,
  expectedContent?: string,
): Promise<string | null> {
  const target = path.join(root, relativePath);
  const current = await readText(target);
  if (current === null) {
    return null;
  }

  const managed = manifestFile(manifest, relativePath);
  const unchanged = managed?.mode === "owned" && managed.sha256 === sha256(current);
  const exactFallback = expectedContent !== undefined && expectedContent === current;
  if (!unchanged && !exactFallback) {
    return `Preserved modified file ${relativePath}`;
  }

  await removePath(target);
  await removeEmptyParents(path.dirname(target), root);
  return null;
}

export async function removeBlockFile(root: string, relativePath: string): Promise<void> {
  const target = path.join(root, relativePath);
  const current = await readText(target);
  const updated = removeManagedBlock(current);
  if (updated === null) {
    return;
  }
  if (updated === "") {
    await removePath(target);
    return;
  }
  await writeText(target, updated);
}

export function removeEmptyHooksContainer(config: Record<string, unknown>): void {
  const hooks = config.hooks;
  if (typeof hooks !== "object" || hooks === null || Array.isArray(hooks)) {
    return;
  }
  if (Object.keys(hooks).length === 0) {
    delete config.hooks;
  }
}
