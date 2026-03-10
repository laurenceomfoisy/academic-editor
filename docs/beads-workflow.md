# Beads Workflow

This project uses `bd` as the required workflow tracker for substantive `academic-writer` tasks.

## Why

`academic-writer` orchestrates many specialist subagents. A plain-text plan is not enough for long scientific article workflows. `bd` provides durable, dependency-aware workflow state.

## Rule

For any substantive article or section task, `academic-writer` should:

1. run from the project root
2. ensure `bd` is initialized
3. create a parent bead for the deliverable
4. create child beads for required workstreams
5. claim the active bead before work
6. update bead state as work progresses
7. use `bd ready` to pick the next unblocked step

Only trivial copyediting can skip this workflow.

## Full Article Bead Template

Recommended child beads:

- manuscript architecture
- literature retrieval
- literature review
- theory and hypotheses
- data and methods
- dataviz strategy
- ggplot figures
- results writing
- discussion and limitations
- conclusion
- reviewer-2 pressure test

## Suggested Commands

Initialize in the project root:

```bash
bd init
```

Create the parent bead:

```bash
bd create "Paper: <title or topic>" -p 0
```

Create children:

```bash
bd create "Manuscript architecture" -p 1
bd create "Literature retrieval" -p 1
bd create "Literature review" -p 1
bd create "Theory and hypotheses" -p 1
bd create "Data and methods" -p 1
bd create "Dataviz strategy" -p 1
bd create "ggplot figures" -p 1
bd create "Results writing" -p 1
bd create "Discussion and limitations" -p 1
bd create "Conclusion" -p 1
bd create "Reviewer-2 pressure test" -p 1
```

Wire dependencies:

```bash
bd dep add <literature-review> <literature-retrieval>
bd dep add <theory-hypotheses> <literature-review>
bd dep add <data-methods> <theory-hypotheses>
bd dep add <dataviz-strategy> <data-methods>
bd dep add <ggplot-figures> <dataviz-strategy>
bd dep add <results-writing> <ggplot-figures>
bd dep add <discussion-limitations> <results-writing>
bd dep add <conclusion> <discussion-limitations>
bd dep add <reviewer-2> <conclusion>
```

Claim and inspect:

```bash
bd update <id> --claim
bd show <id>
bd ready
```

## Mapping to Subagents

- manuscript architecture -> `paper-architect`
- literature retrieval -> `literature-finder`
- literature review -> `literature-review`
- theory and hypotheses -> `theory-hypotheses`
- data and methods -> `data-methods`
- dataviz strategy -> `dataviz-editor`
- ggplot figures -> `ggplot-visualizer`
- results writing -> `results-writer`
- discussion and limitations -> `discussion-limitations`
- conclusion -> `conclusion-writer`
- reviewer-2 pressure test -> `reviewer-2`

## Output Discipline

For substantive work, `academic-writer` should report:

- parent bead
- active bead
- subagents invoked
- what moved to done
- what remains blocked or ready
