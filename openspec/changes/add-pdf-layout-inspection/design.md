# Design: PDF Layout Inspection

## Context
Current MCP already handles LaTeX read/edit/build, but it reports only textual diagnostics. PDF visual inspection requires page rendering and client-side model vision.

## Decisions
1. Render requested pages using an installed PDF renderer (e.g., PyMuPDF) with page bounds and size limits.
2. Keep read-only inspection distinct from approved mutation.
3. Restrict paths to build artifacts under the configured project root or a dedicated build directory.
4. Return image artifact metadata or MCP image content according to the supported FastMCP version; the AI client handles visual reasoning.
5. Never claim that compiler warnings alone prove visually correct layout.

## Alternatives
- Full browser automation of Overleaf: rejected for this feature due to remote session complexity.
- Fully automated iterative fixes: deferred pending safe review workflow.

## Risks
Untrusted PDFs, oversized rendering, path traversal, and inaccurate page-to-source mapping. Add page/size limits, error handling, tests, and explicit uncertainty.
