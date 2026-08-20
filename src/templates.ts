import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const PACKAGE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

export async function readTemplate(relativePath: string): Promise<string> {
  return readFile(path.join(PACKAGE_ROOT, "templates", relativePath), "utf8");
}
