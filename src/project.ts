import { access, stat } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";

async function exists(target: string): Promise<boolean> {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

export async function resolveProjectRoot(start = process.cwd()): Promise<string> {
  let current = path.resolve(start);

  while (true) {
    if (await exists(path.join(current, ".git"))) {
      return current;
    }

    const parent = path.dirname(current);
    if (parent === current) {
      return path.resolve(start);
    }
    current = parent;
  }
}

export async function commandExists(command: string): Promise<boolean> {
  const entries = (process.env.PATH ?? "").split(path.delimiter).filter(Boolean);
  const extensions = process.platform === "win32"
    ? (process.env.PATHEXT ?? ".EXE;.CMD;.BAT;.COM").split(";")
    : [""];

  for (const entry of entries) {
    for (const extension of extensions) {
      try {
        await access(path.join(entry, `${command}${extension}`), constants.X_OK);
        return true;
      } catch {
        // Keep searching PATH.
      }
    }
  }
  return false;
}
