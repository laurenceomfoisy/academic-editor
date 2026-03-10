# Academic Editor Architecture Plan

## Core Principle

`academic-writer` is the front-door paper orchestrator. It plans the paper, keeps the argument coherent, delegates specialized work to subagents, integrates the sections into one LaTeX manuscript, and always ends with a `reviewer-2` pressure test.

By default, specialist subagent use is mandatory rather than optional. `academic-writer` should only skip subagent invocation for pure copyediting or stylistic cleanup with no new substantive content.

## Article Logic

The default article structure follows a classic KKV-oriented format:

1. Hook
2. Research question
3. Literature review
4. Theoretical stance
5. Hypotheses
6. Data and methods
7. Results
8. Discussion
9. Limitations
10. Conclusion

## Existing Agents

- `academic-writer` - primary orchestrator
- `paper-architect` - manuscript-level structure and LaTeX assembly subagent
- `literature-finder` - retrieval-first source acquisition subagent
- `literature-review` - literature mapping and synthesis subagent
- `theory-hypotheses` - theory and hypothesis formation subagent
- `data-methods` - methods and design subagent
- `dataviz-editor` - visualization strategy subagent
- `ggplot-visualizer` - grayscale figure implementation subagent
- `results-writer` - empirical prose subagent
- `discussion-limitations` - implication and limitations subagent
- `conclusion-writer` - ending and payoff subagent
- `reviewer-2` - severe journal-reviewer subagent

## Planned Agent Split

### Orchestration

- `academic-writer`
  - plans the paper with the user
  - writes in LaTeX by default
  - enforces the article arc and KKV discipline
  - invokes specialist subagents when needed
  - integrates all sections into one paper voice

- `paper-architect`
  - owns manuscript-level structure and LaTeX assembly
  - controls section ordering, figure placement, appendix logic, and cross-references
  - checks that the paper tells a coherent and interesting story

### Literature

- `literature-finder`
  - retrieves papers into `current_project/docs/literature/`
  - tracks found, downloaded, and accessible items

- `literature-review`
  - maps literatures, camps, debates, and approaches
  - identifies what different groups of researchers have argued and how they approached the question
  - must remain source-grounded in what it actually read

### Theory and Design

- `theory-hypotheses`
  - derives theoretical stance and hypotheses from the literature
  - spells out mechanisms, rival explanations, and scope conditions

- `data-methods`
  - writes transparent KKV-style methods sections
  - emphasizes identification, assumptions, measurement, threats to inference, and robustness
  - can code in Python for analysis workflows

### Results and Visualization

- `results-writer`
  - writes disciplined results prose
  - separates descriptive from causal claims
  - interprets evidence without overclaiming

- `ggplot-visualizer`
  - produces publication-quality figures in `ggplot`
  - uses grayscale by default
  - returns code, caption suggestions, and export guidance

- `dataviz-editor`
  - checks whether the figure set is diverse and narratively aligned
  - ensures visuals tell the story rather than repeating the same design
  - assigns rhetorical roles to each figure

### Endgame

- `discussion-limitations`
  - interprets implications for the field
  - writes highly transparent limitations that protect against overclaiming

- `conclusion-writer`
  - writes the condensed ending for the section most likely to be read
  - summarizes the core contribution, result, implication, and caution

- `reviewer-2`
  - pressure-tests the integrated manuscript before final output

## Workflow Vision

1. `academic-writer` plans the paper
2. `paper-architect` proposes the manuscript arc
3. `literature-finder` retrieves sources into `docs/literature/`
4. `literature-review` maps the field
5. `theory-hypotheses` builds stance and hypotheses
6. `data-methods` writes design and code support
7. `dataviz-editor` proposes the figure strategy
8. `ggplot-visualizer` builds grayscale figures
9. `results-writer` writes the empirical narrative
10. `discussion-limitations` interprets and bounds claims
11. `conclusion-writer` writes the ending
12. `paper-architect` assembles the LaTeX paper
13. `reviewer-2` pressure-tests the manuscript

## Implementation Notes

- The literature pipeline already exists and currently stores project-local outputs in `docs/literature/` when run from a project root.
- `academic-writer` should automatically trigger literature retrieval when new literature claims are needed, but only after planning and query approval.
- `literature-finder` and `literature-review` should be separated conceptually even if they initially share tooling.
- `academic-writer` should support partial workflows too, such as writing only a methods section or revising only a conclusion.
- Figure production should be split between strategy (`dataviz-editor`) and implementation (`ggplot-visualizer`).
- The default article style assumes LaTeX assembly and grayscale figures unless the user specifies otherwise.
