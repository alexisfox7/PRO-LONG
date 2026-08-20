import { BLOCK_END, BLOCK_START } from "./constants.js";

function escapeRegex(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const BLOCK_PATTERN = new RegExp(
  `${escapeRegex(BLOCK_START)}[\\s\\S]*?${escapeRegex(BLOCK_END)}\\n?`,
  "m",
);

export function hasManagedBlock(content: string | null): boolean {
  return content !== null && BLOCK_PATTERN.test(content);
}

export function upsertManagedBlock(content: string | null, block: string): string {
  if (content === null || content.trim() === "") {
    return `${block}\n`;
  }
  if (hasManagedBlock(content)) {
    const updated = content.replace(BLOCK_PATTERN, `${block}\n`);
    return updated.endsWith("\n") ? updated : `${updated}\n`;
  }
  return `${content.trimEnd()}\n\n${block}\n`;
}

export function removeManagedBlock(content: string | null): string | null {
  if (content === null || !hasManagedBlock(content)) {
    return content;
  }
  const updated = content
    .replace(BLOCK_PATTERN, "")
    .replace(/\n{3,}/g, "\n\n")
    .trimEnd();
  return updated === "" ? "" : `${updated}\n`;
}
