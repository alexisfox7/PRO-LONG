import { createHash, randomUUID } from "node:crypto";
import { mkdir, readFile, rename, rm, rmdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";

export async function pathExists(target: string): Promise<boolean> {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

export async function readText(target: string): Promise<string | null> {
  try {
    return await readFile(target, "utf8");
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

export async function writeText(target: string, content: string): Promise<void> {
  await mkdir(path.dirname(target), { recursive: true });
  const temporary = `${target}.${randomUUID()}.tmp`;
  await writeFile(temporary, content, "utf8");
  await rename(temporary, target);
}

export async function removePath(target: string, recursive = false): Promise<void> {
  await rm(target, { force: true, recursive });
}

export function sha256(content: string): string {
  return createHash("sha256").update(content).digest("hex");
}

export async function fileSize(target: string): Promise<number> {
  try {
    return (await stat(target)).size;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") {
      return 0;
    }
    throw error;
  }
}

export async function removeEmptyParents(start: string, stop: string): Promise<void> {
  let current = path.resolve(start);
  const boundary = path.resolve(stop);

  while (current.startsWith(`${boundary}${path.sep}`) && current !== boundary) {
    try {
      await rmdir(current);
    } catch {
      return;
    }
    current = path.dirname(current);
  }
}
