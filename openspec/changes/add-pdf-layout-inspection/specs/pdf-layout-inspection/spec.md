# PDF Layout Inspection Delta

## ADDED Requirements

### Requirement: Inspect a compiled PDF page
The server SHALL support retrieving a bounded, read-only visual preview of a specified page in an existing compiled project PDF.

#### Scenario: User reports a layout issue
- **WHEN** the client requests page 3 of an existing PDF
- **THEN** the server returns a page preview or a safe artifact reference usable by the MCP client

#### Scenario: Page out of range
- **WHEN** the requested page number is not present
- **THEN** the server returns an actionable error without modifying files

### Requirement: Preserve approval gate for proposed fixes
The server SHALL NOT apply a suggested LaTeX layout fix without explicit user consent.

#### Scenario: AI finds an overflowing table
- **WHEN** an AI client analyzes a rendered page and proposes a fix
- **THEN** the server provides a diff preview before any optional approved write
