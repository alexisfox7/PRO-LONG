// PRO-LONG runtime. Generated into a project's .prolong directory.
import { appendFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const logPath = path.join(projectRoot, ".prolong", "log.jsonl");

function eventType(event) {
  const name = String(event?.hook_event_name ?? event?.type ?? "event");
  const lower = name.toLowerCase();
  if (lower.includes("session") && (lower.includes("start") || lower.includes("created"))) return "session_start";
  if (lower.includes("session") && (lower.includes("end") || lower.includes("shutdown") || lower.includes("idle"))) return "session_end";
  if (lower.includes("prompt") || (lower.includes("message") && event?.message?.role === "user")) return "user_prompt";
  if (lower.includes("tool") && (lower.includes("result") || lower.includes("after") || lower.includes("end") || lower.includes("post"))) return "tool_result";
  if (lower.includes("tool")) return "tool_call";
  if (lower.includes("stop") || (lower.includes("message") && event?.message?.role === "assistant")) return "assistant_message";
  return name;
}

function json(value) {
  const seen = new WeakSet();
  return JSON.stringify(value, (_key, candidate) => {
    if (typeof candidate === "bigint") return candidate.toString();
    if (typeof candidate === "object" && candidate !== null) {
      if (seen.has(candidate)) return "[circular]";
      seen.add(candidate);
    }
    return candidate;
  });
}

export function record(client, event) {
  const type = eventType(event);
  if (type === "tool_call" || type === "tool_result") {
    const toolInput = event?.tool_input ?? event?.toolInput ?? event?.args ?? event?.input;
    if (json(toolInput)?.includes(".prolong/log.jsonl")) return;
  }
  const entry = {
    timestamp: new Date().toISOString(),
    client,
    sessionId: event?.session_id ?? event?.sessionID ?? event?.sessionId,
    type,
    content: event,
  };
  mkdirSync(path.dirname(logPath), { recursive: true });
  appendFileSync(logPath, `${json(entry)}\n`, { encoding: "utf8", flag: "a" });
}

async function main() {
  const client = process.argv[3] ?? "unknown";
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  record(client, input.trim() === "" ? {} : JSON.parse(input));
  process.stdout.write("{}");
}

if (process.argv[2] === "--prolong-hook") {
  main().catch((error) => {
    process.stderr.write(`PRO-LONG hook failed: ${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
  });
}
