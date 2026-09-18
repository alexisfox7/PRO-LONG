import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { execFile, spawn } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { promisify } from "node:util";
import { initProject } from "../src/init.js";
import { getProjectStatus } from "../src/status.js";
import { uninstallProject } from "../src/uninstall.js";

async function temporaryProject(): Promise<string> {
  const root = await mkdtemp(path.join(tmpdir(), "prolong-test-"));
  await mkdir(path.join(root, ".git"));
  return root;
}

async function runRuntime(root: string, event: object): Promise<{ stdout: string; stderr: string; code: number | null }> {
  return new Promise((resolve, reject) => {
    const child = spawn(
      process.execPath,
      [path.join(root, ".prolong/runtime.mjs"), "--prolong-hook", "codex"],
      { cwd: root },
    );
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => { stdout += String(chunk); });
    child.stderr.on("data", (chunk) => { stderr += String(chunk); });
    child.on("error", reject);
    child.on("close", (code) => resolve({ stdout, stderr, code }));
    child.stdin.end(JSON.stringify(event));
  });
}

test("init, status, runtime, and uninstall form an idempotent lifecycle", async () => {
  const root = await temporaryProject();
  try {
    await writeFile(path.join(root, "AGENTS.md"), "# Existing agent rules\n", "utf8");
    await writeFile(path.join(root, "CLAUDE.md"), "# Existing Claude rules\n", "utf8");
    await writeFile(path.join(root, ".gitignore"), "coverage/\n", "utf8");
    await mkdir(path.join(root, ".codex"), { recursive: true });
    await writeFile(path.join(root, ".codex/hooks.json"), JSON.stringify({
      hooks: { SessionStart: [{ hooks: [{ type: "command", command: "echo existing" }] }] },
    }), "utf8");
    await mkdir(path.join(root, ".claude"), { recursive: true });
    await writeFile(path.join(root, ".claude/settings.json"), JSON.stringify({ permissions: { allow: ["Read"] } }), "utf8");

    const clients = ["codex", "claude-code", "opencode", "pi", "hermes"] as const;
    await initProject({ root, clients: [...clients] });
    const initialized = await initProject({ root, clients: [...clients] });
    const hermesFiles = initialized.manifest.files.filter((file) => file.path.startsWith(".hermes/"));
    assert.deepEqual(hermesFiles.map((file) => [file.path, file.mode]), [
      [".hermes/plugins/prolong/plugin.yaml", "owned"],
      [".hermes/plugins/prolong/__init__.py", "owned"],
    ]);

    const status = await getProjectStatus(root);
    assert.equal(status.initialized, true);
    assert.equal(status.healthy, true);
    assert.deepEqual(
      status.clients.filter((client) => clients.includes(client.name)).map((client) => client.installed),
      [true, true, true, true, true],
    );

    const codexConfig = JSON.parse(await readFile(path.join(root, ".codex/hooks.json"), "utf8"));
    assert.equal(codexConfig.hooks.SessionStart.length, 2, "existing hook plus one PRO-LONG hook");
    assert.equal(codexConfig.hooks.Stop.length, 1, "re-running init does not duplicate hooks");
    const claudeConfig = JSON.parse(await readFile(path.join(root, ".claude/settings.json"), "utf8"));
    assert.deepEqual(claudeConfig.permissions, { allow: ["Read"] });

    const runtime = await runRuntime(root, {
      session_id: "session-1",
      hook_event_name: "UserPromptSubmit",
      prompt: "remember this decision",
    });
    assert.equal(runtime.code, 0);
    assert.equal(runtime.stdout, "{}");
    assert.equal(runtime.stderr, "");
    const entries = (await readFile(path.join(root, ".prolong/log.jsonl"), "utf8")).trim().split("\n");
    assert.equal(entries.length, 1);
    assert.deepEqual(JSON.parse(entries[0]!), {
      timestamp: JSON.parse(entries[0]!).timestamp,
      client: "codex",
      sessionId: "session-1",
      type: "user_prompt",
      content: {
        session_id: "session-1",
        hook_event_name: "UserPromptSubmit",
        prompt: "remember this decision",
      },
    });

    await runRuntime(root, {
      session_id: "session-1",
      hook_event_name: "PostToolUse",
      tool_input: { command: "rg decision .prolong/log.jsonl" },
      tool_response: entries[0],
    });
    const afterSelfRead = (await readFile(path.join(root, ".prolong/log.jsonl"), "utf8")).trim().split("\n");
    assert.equal(afterSelfRead.length, 1, "reading the memory log must not copy it back into itself");

    const result = await uninstallProject({ root });
    assert.deepEqual(result.warnings, []);
    assert.match(await readFile(path.join(root, "AGENTS.md"), "utf8"), /Existing agent rules/);
    assert.doesNotMatch(await readFile(path.join(root, "AGENTS.md"), "utf8"), /prolong:start/);
    assert.match(await readFile(path.join(root, "CLAUDE.md"), "utf8"), /Existing Claude rules/);
    assert.equal(await readFile(path.join(root, ".prolong/log.jsonl"), "utf8").then(() => true), true);
    await assert.rejects(readFile(path.join(root, ".prolong/runtime.mjs"), "utf8"), { code: "ENOENT" });
    for (const file of hermesFiles) {
      await assert.rejects(readFile(path.join(root, file.path), "utf8"), { code: "ENOENT" });
    }

    const preservedCodex = JSON.parse(await readFile(path.join(root, ".codex/hooks.json"), "utf8"));
    assert.equal(preservedCodex.hooks.SessionStart.length, 1);
    assert.equal(preservedCodex.hooks.SessionStart[0].hooks[0].command, "echo existing");
    const preservedClaude = JSON.parse(await readFile(path.join(root, ".claude/settings.json"), "utf8"));
    assert.deepEqual(preservedClaude, { permissions: { allow: ["Read"] } });
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

for (const [client, relativePath, comment] of [
  ["opencode", ".opencode/plugins/prolong.ts", "//"],
  ["hermes", ".hermes/plugins/prolong/__init__.py", "#"],
  ["hermes", ".hermes/plugins/prolong/plugin.yaml", "#"],
] as const) {
  test(`uninstall preserves a modified owned adapter file: ${relativePath}`, async () => {
    const root = await temporaryProject();
    try {
      await initProject({ root, clients: [client] });
      const pluginPath = path.join(root, relativePath);
      await writeFile(pluginPath, `${await readFile(pluginPath, "utf8")}\n${comment} local change\n`, "utf8");

      const result = await uninstallProject({ root, purge: true });
      assert.equal(result.warnings.length, 2);
      assert.match(result.warnings[0]!, /Preserved modified file/);
      assert.match(result.warnings[1]!, /runtime.mjs/);
      assert.match(await readFile(pluginPath, "utf8"), /local change/);
      await readFile(path.join(root, ".prolong/runtime.mjs"), "utf8");
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });
}

test("invalid existing hook JSON fails before creating managed files", async () => {
  const root = await temporaryProject();
  try {
    await mkdir(path.join(root, ".codex"), { recursive: true });
    await writeFile(path.join(root, ".codex/hooks.json"), "{ definitely not json", "utf8");

    await assert.rejects(initProject({ root, clients: ["codex"] }), /Cannot safely update/);
    await assert.rejects(readFile(path.join(root, ".prolong/runtime.mjs"), "utf8"), { code: "ENOENT" });
    await assert.rejects(readFile(path.join(root, "AGENTS.md"), "utf8"), { code: "ENOENT" });
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("Hermes is detected from its project directory", async () => {
  const root = await temporaryProject();
  try {
    await mkdir(path.join(root, ".hermes"));
    const result = await initProject({ root });
    assert.match(result.detected.join(","), /hermes/);
    assert.match(await readFile(path.join(root, ".hermes/plugins/prolong/plugin.yaml"), "utf8"), /name: prolong/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("Hermes callbacks record events without copying history or interrupting the session", async () => {
  const root = await temporaryProject();
  try {
    await initProject({ root, clients: ["hermes"] });
    const script = String.raw`
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("prolong", root / ".hermes/plugins/prolong/__init__.py")
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)
hooks = {}
plugin.register(SimpleNamespace(register_hook=hooks.__setitem__))
events = [
    ("on_session_start", {"model": "test-model", "platform": "cli"}),
    ("pre_llm_call", {"user_message": "remember this decision"}),
    ("pre_tool_call", {"tool_name": "terminal", "args": {"command": "echo hello"}}),
    ("post_tool_call", {"tool_name": "terminal", "args": {"command": "echo hello"}, "result": "hello", "status": "success"}),
    ("post_llm_call", {"assistant_response": "decision saved"}),
    ("on_session_end", {"completed": True}),
]
assert set(hooks) == {name for name, _ in events}
for name, payload in events:
    assert hooks[name](session_id="hermes-session", task_id="task-1", turn_id="turn-1",
                       conversation_history=[{"content": "historical-only"}], future_field=True,
                       **payload) is None

log = root / ".prolong/log.jsonl"
history = log.read_text()
for name in ("pre_tool_call", "post_tool_call"):
    assert hooks[name](session_id="hermes-session", tool_name="terminal",
                       args={"command": "rg decision .prolong/log.jsonl"}, result=history) is None
assert log.read_text() == history
hooks["post_llm_call"](session_id="hermes-session", assistant_response="retrieved",
                      conversation_history=[{"role": "tool", "content": history}])
before_failure = log.read_text()
(root / ".prolong/runtime.mjs").unlink()
assert hooks["pre_llm_call"](user_message="runtime missing") is None
assert log.read_text() == before_failure
`;
    const { stdout, stderr } = await promisify(execFile)("python3", ["-B", "-c", script, root], { timeout: 10000 });
    assert.equal(stdout, "");
    assert.equal(stderr, "");
    const log = await readFile(path.join(root, ".prolong/log.jsonl"), "utf8");
    const entries = log.trim().split("\n").map((line) => JSON.parse(line));
    assert.deepEqual(entries.map((entry) => entry.type), [
      "session_start", "user_prompt", "tool_call", "tool_result", "assistant_message", "session_end", "assistant_message",
    ]);
    assert.ok(entries.every((entry) => entry.client === "hermes" && entry.sessionId === "hermes-session"));
    assert.equal(entries[1].content.user_message, "remember this decision");
    assert.deepEqual(entries[2].content.tool_input, { command: "echo hello" });
    assert.equal(entries[3].content.result, "hello");
    assert.equal(entries[4].content.assistant_response, "decision saved");
    assert.equal(entries[5].content.completed, true);
    assert.doesNotMatch(log, /historical-only|conversation_history|future_field/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
