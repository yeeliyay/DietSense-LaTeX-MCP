# Section Editing Specification

## Purpose
Provide safe, minimally scoped changes to the LaTeX paper through MCP tools.

## Requirements

### Requirement: Read and preview without mutation
The server SHALL allow reading supported LaTeX sections and previewing a unified diff without modifying the paper.

#### Scenario: Preview an Abstract revision
- **WHEN** the client requests a preview for a replacement Abstract
- **THEN** the server returns the expected diff without changing `project/main.tex`

### Requirement: Approved edits with recovery
The server SHALL require an explicit approval signal for an apply operation, check concurrent modifications, and preserve a recoverable backup.

#### Scenario: Concurrent edit detected
- **WHEN** `main.tex` changed after the preview or expected hash
- **THEN** the server rejects a stale apply rather than overwriting newer work

### Requirement: Scope boundaries
The server SHALL constrain file access to the configured project and SHALL avoid unrelated section edits.

#### Scenario: Unsafe path
- **WHEN** a client requests traversal outside the project root
- **THEN** the operation fails without accessing the outside path
