# academic-editor

Private work-in-progress repository for a shareable OpenCode academic writing system oriented toward political science articles written in a classic KKV style.

## Purpose

This repository tracks the agent architecture, prompts, and literature retrieval tooling for an `academic-planner` and `academic-writer` workflow that:

- plans and writes papers in LaTeX
- follows a classic article arc: hook, research question, literature, theory, hypotheses, data and methods, results, discussion, limitations, conclusion
- enforces KKV-style inferential discipline
- retrieves and reads literature before making literature claims
- keeps article-level coherence through orchestration and review
- supports a planning-first handoff from `academic-planner` to `academic-writer`

## Current Contents

- `docs/` - architecture plans and implementation notes
- `opencode/agents/` - current agent prompts
- `opencode/opencode.json` - current OpenCode config snapshot
- `literature/` - literature retrieval pipeline source files

## Workflow Tracking

This project uses `bd` as the required workflow tracker for substantive agent work. See `docs/beads-workflow.md`.

## Gastown Integration

This project also adopts the Gas Town coordination philosophy:

- `academic-writer` acts as the Mayor
- each paper is treated as a convoy
- specialist subagents act like polecats with durable roles
- workflow recovery should use `gt prime` when inside a Gastown workspace

For new papers, `academic-writer` should automatically create and manage the paper's bead or convoy structure when the workflow starts.

See `docs/gastown-workflow.md`.

## Current Direction

The current build uses `academic-planner` as the planning front door and `academic-writer` as the execution orchestrator, with a specialist subagent family for:

- manuscript architecture and LaTeX assembly
- literature retrieval
- literature review and field mapping
- theory and hypotheses
- data and methods
- data visualization strategy
- grayscale `ggplot` figure implementation
- results writing
- discussion and limitations
- conclusion writing
- severe top-journal style review

`academic-planner` ends with a structured handoff blueprint that `academic-writer` can execute directly.

## Status

Early private build. Not yet packaged for public installation.
