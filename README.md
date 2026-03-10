# academic-editor

Private work-in-progress repository for a shareable OpenCode academic writing system oriented toward political science articles written in a classic KKV style.

## Purpose

This repository tracks the agent architecture, prompts, and literature retrieval tooling for an `academic-writer` workflow that:

- plans and writes papers in LaTeX
- follows a classic article arc: hook, research question, literature, theory, hypotheses, data and methods, results, discussion, limitations, conclusion
- enforces KKV-style inferential discipline
- retrieves and reads literature before making literature claims
- keeps article-level coherence through orchestration and review

## Current Contents

- `docs/` - architecture plans and implementation notes
- `opencode/agents/` - current agent prompts
- `opencode/opencode.json` - current OpenCode config snapshot
- `literature/` - literature retrieval pipeline source files

## Current Direction

The current build plan is to keep `academic-writer` as the primary orchestrator and add specialist subagents for literature retrieval, literature review, theory, methods, results, data visualization, discussion, conclusion, and paper-level LaTeX assembly.

## Status

Early private build. Not yet packaged for public installation.
