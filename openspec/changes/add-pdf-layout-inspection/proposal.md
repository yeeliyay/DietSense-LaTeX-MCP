# Add PDF Layout Inspection

## Why
The MCP can compile LaTeX and return logs but cannot yet inspect a particular PDF page visually. Users want to say `Table II overflows on page 3` and have a tool supply the right page preview and diagnostics for an AI-assisted fix.

## What Changes
- Render requested compiled PDF pages to PNG previews for the client.
- Return locations of compiler warnings and relevant source hints when available.
- Keep the modify/approve/compile/inspect loop explicit; no automatic Git push.
- Add tests for invalid pages, missing PDF, and untrusted paths.

## Capabilities
### New
- `pdf-layout-inspection`: a read-only view of compiled PDF pages and related diagnostics.
### Modified
- `latex-build`: expose compiled artifact location in a way clients can safely consume.

## Impact
Affects `server.py`, a proposed PDF rendering helper, tests, documentation, and optionally the local LaTeX toolchain. No behavior changes to existing editing and Git tools until implemented.

## Status
Proposal only. The PDF inspection MCP tool is **NOT implemented** in this package.
