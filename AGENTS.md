## Issue Tracking

This project uses **bd (Beads)** for workflow tracking.
Run `bd prime` for workflow context, or install hooks with `bd hooks install` for auto-injection.

Quick reference:
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create work
- `bd update <id> --claim` - Claim work
- `bd close <id>` - Complete work
- `bd sync` - Sync workflow state

Gastown note:
- when inside a Gastown rig, use `gt prime` for role context and `gt sling` for delegation
- `bd` remains the source of truth for workflow state
