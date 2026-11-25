# Git Synchronization Specification

## Purpose
Separate local paper editing from remote Git/Overleaf synchronization.

## Requirements

### Requirement: Push requires explicit consent
The server SHALL require explicit user authorization before attempting a remote push.

#### Scenario: Unapproved push
- **WHEN** the client requests a push without consent
- **THEN** the server refuses the remote update

### Requirement: Git credentials remain private
The system SHALL NOT place credentials or access tokens in tracked project files or tool output.

#### Scenario: Missing authentication
- **WHEN** the Git remote cannot authenticate
- **THEN** the operation returns a safe error without exposing secrets
