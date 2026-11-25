# Architecture and design decisions

```mermaid
flowchart TD
    U[User: natural-language request] --> C[Claude / Codex MCP Client]
    C --> S[Python FastMCP stdio server]
    S --> E[LaTeX editing engine]
    E --> R[(Project main.tex)]
    E --> D[Preview unified diff + SHA256]
    D --> A{User approves?}
    A -- Yes --> B[Apply & backup]
    A -- No --> N[No modification]
    B --> L[pdfLaTeX compiler]
    L --> W[Warnings / PDF]
    S --> G[Optional Git bridge]
    G --> O[Overleaf Git remote - only by approval]
```

## Decisions
- Safe, narrow scope edits minimize accidental rewrites.
- SHA-256 base hash rejects stale previews.
- Backups are local and gitignored.
- Git push requires explicit user approval and an already clean Git tree.
- No direct remote access unless Git Bridge is separately configured.
- STDIO logs must go to stderr; writing debug strings to stdout can corrupt MCP protocol frames.
