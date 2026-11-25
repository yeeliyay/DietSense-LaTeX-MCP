# AI editing policy for Claude / Codex

- Treat `project/main.tex` as the source of truth. Never invent citations, metrics or experimental outcomes.
- Read the relevant section first. Prefer `preview_section_edit` to broad edits.
- Show the diff and **request explicit user approval** before calling `apply_section_edit`.
- After a change, compile and inspect diagnostics. If errors appear, repair only the relevant scope.
- Do not edit packages, `\documentclass`, figures or bibliography unless the user specifically requests it.
- Never commit or push to GitHub or Overleaf without explicit user consent.
- Never print credentials or store Overleaf Git tokens in this repository.
- If a request involves remote Overleaf, explain the Git integration prerequisite and confirm before push.

## OpenSpec change control

- Read `openspec/config.yaml` and existing `openspec/specs/` before making non-trivial behavior changes.
- For new features, first create/review `openspec/changes/<change-name>/` proposal, design, delta specs, and tasks.
- Do not imply a proposed feature is already implemented.
- Preserve the user approval gate before edits and Git/Overleaf pushes.
- Keep specs, tests, and docs synchronized after an approved implementation.
