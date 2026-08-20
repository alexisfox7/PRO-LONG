import { readText, writeText } from "./io.js";

export type JsonObject = Record<string, unknown>;

export async function readJsonObject(target: string): Promise<JsonObject> {
  const content = await readText(target);
  if (content === null || content.trim() === "") {
    return {};
  }
  try {
    const parsed: unknown = JSON.parse(content);
    if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
      throw new Error("expected a JSON object");
    }
    return parsed as JsonObject;
  } catch (error) {
    throw new Error(`Cannot safely update ${target}: ${(error as Error).message}`);
  }
}

export async function writeJsonObject(target: string, value: JsonObject): Promise<void> {
  await writeText(target, `${JSON.stringify(value, null, 2)}\n`);
}
