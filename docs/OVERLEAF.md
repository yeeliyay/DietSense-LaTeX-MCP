# Overleaf Git Bridge (optional)

This repository is primarily a **local-first** MCP editor. It does not log in through Overleaf's private web endpoints.

1. Check whether the owner of the Overleaf project has access to Git Integration.
2. Obtain the project's official Git URL from its Overleaf menu and clone it with Git into a **separate directory**.
3. In your local clone, assign `overleaf` as the remote name (if the clone starts with `origin`, rename using `git remote rename origin overleaf`).
4. Set `LATEX_PROJECT_ROOT` to the clone path in the Claude configuration. Do not mix the GitHub server-code repo with your Overleaf document Git history.
5. `git_sync_status()` to review changes. `git_fetch_remote('overleaf')` to fetch remote updates. Review/diff and merge manually (do not blindly overwrite collaborator edits).
6. Preview and apply a local LaTeX change via MCP, compile, then use your usual terminal to commit. After explicit approval, `git_push_to_overleaf('overleaf', True)` pushes your current branch to the Overleaf remote.

**Important:** A GitHub push and an Overleaf push are separate operations. Do not embed tokens in tracked files or invoke a remote push on behalf of another user without consent. GitHub's repo URL is not an Overleaf remote URL.
