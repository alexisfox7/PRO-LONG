#!/usr/bin/env node

import { initProject } from "./init.js";
import { resolveProjectRoot } from "./project.js";
import { formatStatus, getProjectStatus } from "./status.js";
import { uninstallProject } from "./uninstall.js";
import { isClientName, type ClientName } from "./types.js";

const USAGE = `Usage:
  prolong init [--client codex,claude-code,opencode,pi]
  prolong status [--json]
  prolong uninstall [--purge]
`;

function optionValue(args: string[], flag: string): string | undefined {
  const index = args.indexOf(flag);
  if (index === -1) {
    return undefined;
  }
  const value = args[index + 1];
  if (value === undefined || value.startsWith("--")) {
    throw new Error(`${flag} requires a value`);
  }
  return value;
}

function parseClients(args: string[]): ClientName[] | undefined {
  const value = optionValue(args, "--client");
  if (value === undefined) {
    return undefined;
  }
  const values = value.split(",").map((entry) => entry.trim()).filter(Boolean);
  for (const client of values) {
    if (!isClientName(client)) {
      throw new Error(`Unknown client ${client}`);
    }
  }
  return values as ClientName[];
}

export async function runCli(args = process.argv.slice(2)): Promise<number> {
  const [command] = args;
  if (command === undefined || command === "--help" || command === "-h" || command === "help") {
    process.stdout.write(USAGE);
    return 0;
  }

  const root = await resolveProjectRoot();
  if (command === "init") {
    const clients = parseClients(args);
    const result = await initProject({ root, ...(clients === undefined ? {} : { clients }) });
    process.stdout.write(`Initialized PRO-LONG in ${result.root}\n`);
    process.stdout.write(`Clients: ${result.clients.length === 0 ? "none (skill only)" : result.clients.join(", ")}\n`);
    if (result.clients.length === 0) {
      process.stdout.write("No supported client was detected. Re-run with --client <name> to install its event adapter.\n");
    }
    process.stdout.write("Memory stays local at .prolong/log.jsonl.\n");
    return 0;
  }

  if (command === "status") {
    const status = await getProjectStatus(root);
    process.stdout.write(args.includes("--json") ? `${JSON.stringify(status, null, 2)}\n` : formatStatus(status));
    return status.healthy ? 0 : 1;
  }

  if (command === "uninstall") {
    const result = await uninstallProject({ root, ...(args.includes("--purge") ? { purge: true } : {}) });
    process.stdout.write(`Uninstalled PRO-LONG from ${result.root}.\n`);
    process.stdout.write(result.purged ? "Deleted the local log.\n" : "Preserved .prolong/log.jsonl; use --purge to delete it.\n");
    for (const warning of result.warnings) {
      process.stdout.write(`Warning: ${warning}\n`);
    }
    return 0;
  }

  throw new Error(`Unknown command ${command}\n\n${USAGE}`);
}

runCli().then(
  (code) => {
    process.exitCode = code;
  },
  (error: unknown) => {
    process.stderr.write(`prolong: ${(error as Error).message}\n`);
    process.exitCode = 1;
  },
);
