# LaTeX Build Specification

## Purpose
Diagnose the document locally without silently changing or publishing it.

## Requirements

### Requirement: Explicit LaTeX compilation
The server SHALL provide an MCP tool to compile the configured LaTeX entry point and report success, errors, and relevant warnings.

#### Scenario: Compilation warning
- **WHEN** LaTeX compilation reports an overfull box
- **THEN** the result includes the warning so the AI client can suggest an edit

### Requirement: No automatic remote publishing
The server SHALL NOT push edited LaTeX files to a remote repository as a side effect of compilation.

#### Scenario: Successful PDF build
- **WHEN** compilation succeeds
- **THEN** the server reports the local result without initiating Git push
