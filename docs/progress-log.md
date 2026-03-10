# Progress Log

## Completed so far

- Created `academic-writer` as a primary OpenCode agent with KKV-oriented writing rules.
- Created `reviewer-2` as a severe political science reviewer subagent.
- Created `literature-review` as a literature retrieval and synthesis subagent.
- Built a literature retrieval pipeline with Google Scholar search, PDF retrieval attempts, and result tracking.
- Updated the pipeline so outputs are stored in the active project's `docs/literature/` folder.
- Updated `academic-writer` so it acts as a front-door planner and invokes literature retrieval after planning and query approval.

## Next build stones

1. Split `literature-finder` from `literature-review`.
2. Add `paper-architect` for LaTeX assembly and manuscript coherence.
3. Add `theory-hypotheses`.
4. Add `data-methods`.
5. Add `ggplot-visualizer`.
6. Add `dataviz-editor`.
7. Add `results-writer`.
8. Add `discussion-limitations`.
9. Add `conclusion-writer`.
10. Rework `academic-writer` to orchestrate the larger agent family.
