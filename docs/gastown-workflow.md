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
2. the article is tracked as a convoy-like parent bead plus dependent child beads in `bd`
3. `bd` is the source of truth for workflow state
4. `gt` is the dispatch layer for specialist work when inside a Gastown rig
5. specialist subagents produce structured handoffs
6. recovery comes from `gt prime`, `gt ready` or `gt resume`, and `bd ready` plus bead inspection

Lean integration rule:
- keep repo instructions short
- let `bd prime` provide current Beads workflow context
- let `gt prime` provide current Gastown role context

For a new paper, `academic-writer` should automatically create the convoy root and its standard child beads once the paper plan is agreed.

## If You Are In a Gastown Workspace

Recommended recovery steps:

```bash
gt prime
gt ready
bd ready
bd show <parent-bead>
```

Recommended mental model:

- `academic-writer` coordinates the convoy
- each specialist subagent is a polecat role
- the active bead determines which polecat runs next

## Operational Dispatch Loop

Inside a Gastown rig, `academic-writer` should:

1. recover with `gt prime`
2. inspect ready work with `bd ready --json`
3. choose the highest-priority ready bead
4. map the bead to the correct specialist role
5. delegate with `gt sling`
6. wait for the structured handoff
7. update bead state in `bd`
8. repeat until no substantive ready work remains

Suggested role mapping:

- manuscript architecture -> `paper-architect`
- literature retrieval -> `literature-finder`
- literature review -> `literature-review`
- theory and hypotheses -> `theory-hypotheses`
- data and methods -> `data-methods`
- data analysis -> `data-analysis`
- dataviz strategy -> `dataviz-editor`
- ggplot figures -> `ggplot-visualizer`
- results writing -> `results-writer`
- discussion and limitations -> `discussion-limitations`
- conclusion -> `conclusion-writer`
- reviewer-2 pressure test -> `reviewer-2`

## If You Are Not In a Gastown Workspace

Use the same philosophy through `bd` alone:

- one parent bead per paper
- child beads for architecture, literature, theory, methods, figures, results, discussion, conclusion, review
- explicit handoff payloads between stages
- direct subagent invocation instead of `gt sling`

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
