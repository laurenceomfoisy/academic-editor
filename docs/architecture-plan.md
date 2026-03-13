# Academic Editor Architecture Plan

## Core Principle

`academic-planner` is the planning front door for article design. `academic-writer` is the execution orchestrator. Together they turn a paper idea into a bead-tracked, subagent-driven writing workflow.

By default, specialist subagent use is mandatory rather than optional. `academic-writer` should only skip subagent invocation for pure copyediting or stylistic cleanup with no new substantive content.

By default, `bd` is the required workflow memory layer for substantive tasks. `academic-writer` should use a parent bead plus dependent child beads to manage long-horizon article work.

By default, this system follows a Gastown-inspired orchestration model: `academic-writer` acts as the Mayor, the paper acts as the convoy, and specialist subagents act as polecats connected by explicit handoffs.

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

- `academic-planner` - primary planning mentor
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
  - executes the approved plan
  - writes in LaTeX by default
  - enforces the article arc and KKV discipline
  - invokes specialist subagents when needed
  - integrates all sections into one paper voice
  - creates and manages a paper convoy in Gastown mode
  - delegates specialist work through `gt sling` in Gastown mode

- `academic-planner`
  - mentors the user through article design
  - sharpens the research question, contribution, and structure before drafting
  - produces a handoff blueprint for `academic-writer`
  - emits an explicit ready-to-transfer cue when execution should begin

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

- `data-analysis`
  - actually executes the empirical analysis
  - understands and wrangles raw data into tidy analysis-ready form
  - estimates models, runs diagnostics, and produces reproducible findings

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

1. `academic-planner` plans the paper and produces the blueprint
2. `academic-planner` emits an explicit ready transfer cue
3. `academic-writer` starts the execution workflow from the approved blueprint
4. `paper-architect` proposes the manuscript arc
5. `literature-finder` retrieves sources into `docs/literature/`
6. `literature-review` maps the field
7. `theory-hypotheses` builds stance and hypotheses
8. `data-methods` writes design and code support
9. `data-analysis` executes the empirical analysis
10. `dataviz-editor` proposes the figure strategy
11. `ggplot-visualizer` builds grayscale figures
12. `results-writer` writes the empirical narrative
13. `discussion-limitations` interprets and bounds claims
14. `conclusion-writer` writes the ending
15. `paper-architect` assembles the LaTeX paper
16. `reviewer-2` pressure-tests the manuscript

Each step should correspond to a bead-backed convoy task and end with a structured handoff to the next specialist role.

## Implementation Notes

- The literature pipeline already exists and currently stores project-local outputs in `docs/literature/` when run from a project root.
- `academic-writer` should automatically trigger literature retrieval when new literature claims are needed, but only after planning and query approval.
- `academic-planner` should remain pre-workflow and should not create beads itself.
- `academic-writer` should create the bead structure after receiving an approved plan.
- `data-methods` and `data-analysis` should remain distinct: one designs the empirical strategy, the other executes it.
- `literature-finder` and `literature-review` should be separated conceptually even if they initially share tooling.
- `academic-writer` should support partial workflows too, such as writing only a methods section or revising only a conclusion.
- Figure production should be split between strategy (`dataviz-editor`) and implementation (`ggplot-visualizer`).
- The default article style assumes LaTeX assembly and grayscale figures unless the user specifies otherwise.
- `bd` should track the workflow state for all substantive full-paper and single-section tasks.
- OpenCode projects should prefer the lean Beads integration style: short repo instructions plus `bd prime` as dynamic workflow context.
- In Gastown mode, `gt convoy`, `gt sling`, `gt handoff`, and `gt resume` should be part of the actual execution workflow, not just conceptual guidance.
