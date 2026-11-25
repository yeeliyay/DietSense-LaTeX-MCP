# OpenSpec integration (DietSense LaTeX MCP)

OpenSpec is **spec-driven development for the source repository**. It does not itself act as the Claude Desktop MCP server. Existing `server.py` continues to serve MCP tools.

## Windows prerequisites

1. Install Node.js meeting the **current** OpenSpec CLI requirement, see https://github.com/Fission-AI/OpenSpec (requirements may change).
2. Confirm `node --version` and `npm --version` in CMD/PowerShell.
3. Install: `npm install -g @fission-ai/openspec@latest`.
4. Confirm: `openspec --version` (or `openspec version`, depending on CLI version; use `openspec --help`).
5. Enter **repository root**: `cd /d D:\DietSense-LaTeX-MCP`.
6. Run `openspec init --tools claude` for Claude Code, or `openspec init --tools codex` for Codex; `openspec init` interactive can ask which supported client(s) you use. To commit project-scoped skills use `openspec init --scope project --tools claude` when supported by the installed version.
7. Restart or reload the chosen **coding assistant** and use the commands it prints.

> Claude Desktop MCP and Claude Code are different products. OpenSpec slash commands/skills are primarily for coding assistants like Claude Code. They will not magically appear in a plain Claude Desktop MCP chat merely because the MCP server was configured there. You can still ask Claude Desktop to read the tracked OpenSpec Markdown documents if an appropriate file-reading tool is available.

## Existing OpenSpec content

- `openspec/config.yaml`: project context and artifact drafting rules.
- `openspec/specs/`: baseline contracts for safe section editing, build, and Git sync.
- `openspec/changes/add-pdf-layout-inspection/`: **proposal only**, with proposal, design, tasks, and delta specs. It does not implement PDF page inspection.

## Suggested daily workflow

- `/opsx:explore` to clarify problems.
- `/opsx:propose add-pdf-layout-inspection` to plan or review an existing proposal.
- `openspec list`, `openspec validate add-pdf-layout-inspection` in terminal as supported by your CLI version.
- `/opsx:apply` after review (in the coding assistant).
- Run Python tests, inspect builds, and use `/opsx:archive` when accepted.

**Do not** run `/opsx:apply` in Windows CMD, and do not type `openspec init` in a Claude Desktop chat. The `openspec` CLI executes in a terminal; `/opsx:*` commands are for a supported AI coding client.

When OpenSpec CLI has not been run, this repo contains a *pre-written spec scaffold*, not proof that skill installation is complete.
