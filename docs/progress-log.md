# Progress Log

## Completed so far

- Created `academic-writer` as a primary OpenCode agent with KKV-oriented writing rules.
- Created `reviewer-2` as a severe political science reviewer subagent.
- Created `literature-review` as a literature retrieval and synthesis subagent.
- Built a literature retrieval pipeline with Google Scholar search, PDF retrieval attempts, and result tracking.
- Updated the pipeline so outputs are stored in the active project's `docs/literature/` folder.
- Updated `academic-writer` so it acts as a front-door planner and invokes literature retrieval after planning and query approval.
- Added `literature-finder` as a distinct retrieval-first subagent.
- Added `paper-architect` as a LaTeX and manuscript-coherence subagent.
- Updated the repo OpenCode config so the new subagents are registered.
- Updated `academic-writer` to orchestrate `paper-architect`, `literature-finder`, `literature-review`, and `reviewer-2`.
- Added `theory-hypotheses`.
- Added `data-methods`.
- Added `ggplot-visualizer`.
- Added `dataviz-editor`.
- Added `results-writer`.
- Added `discussion-limitations`.
- Added `conclusion-writer`.
- Expanded `academic-writer` so it can orchestrate the full article workflow end to end.
- Hardened `academic-writer` so specialist subagent invocation is mandatory by default, with a narrow copyediting exception.

## Next build stones

1. Pressure-test the full orchestration on a sample article workflow.
2. Add packaging or installation docs for reuse outside the local OpenCode config.
3. Refine prompts after live usage.
