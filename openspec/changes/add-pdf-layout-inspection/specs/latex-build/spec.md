# LaTeX Build Delta

## MODIFIED Requirements

### Requirement: Explicit LaTeX compilation
The server SHALL provide an MCP tool to compile the configured LaTeX entry point and report success, errors, relevant warnings, and a safe reference to the resulting local PDF when available.

#### Scenario: Compilation warning
- **WHEN** LaTeX compilation reports an overfull box
- **THEN** the result includes the warning and a safe PDF reference if a PDF was produced

#### Scenario: PDF not generated
- **WHEN** compilation fails without a PDF
- **THEN** the server reports diagnostic errors without inventing an artifact path
