# Gastown Workflow

This project adopts the Gas Town philosophy for coordinating academic writing agents.

## Core Mapping

- Mayor -> `academic-writer`
- Polecats -> specialist subagents
- Convoy -> one paper or major deliverable
- Beads -> section or workstream tasks
- Hooks -> persistent artifacts in the project, especially LaTeX files, literature files, figures, and notes

## Practical Rule

When running a substantive article workflow:

1. `academic-writer` acts as the Mayor
2. the article is tracked as a convoy-like parent bead plus dependent child beads
3. specialist subagents produce structured handoffs
4. recovery comes from `gt prime` when available and `bd ready` plus bead inspection

For a new paper, `academic-writer` should automatically create the convoy root and its standard child beads once the paper plan is agreed.

## If You Are In a Gastown Workspace

Recommended recovery steps:

```bash
gt prime
bd ready
bd show <parent-bead>
```

Recommended mental model:

- `academic-writer` coordinates the convoy
- each specialist subagent is a polecat role
- the active bead determines which polecat runs next

## If You Are Not In a Gastown Workspace

Use the same philosophy through `bd` alone:

- one parent bead per paper
- child beads for architecture, literature, theory, methods, figures, results, discussion, conclusion, review
- explicit handoff payloads between stages

This means the user can simply switch to `academic-writer` and start the paper workflow. The agent should create and manage the convoy structure automatically.

## Required Handoff Contract

Every specialist subagent should return:

- bead id
- role
- status
- artifacts produced
- claims safe to reuse
- open risks
- next recommended bead or subagent

## Why This Helps

- reduces agent drift across long article sessions
- makes section transitions explicit
- enables recovery after interruption
- helps `academic-writer` coordinate many specialist roles without losing coherence
