# Beads Workflow

This project uses `bd` as the required workflow tracker for substantive `academic-writer` tasks.

Preferred OpenCode integration style:
- keep repo-level instructions lean
- use the official `bd setup opencode` output in the target project
- rely on `bd prime` for current workflow context

## Why

`academic-writer` orchestrates many specialist subagents. A plain-text plan is not enough for long scientific article workflows. `bd` provides durable, dependency-aware workflow state.

Within the Gastown philosophy, these beads function as the convoy work units for the paper.

## Rule

For any substantive article or section task, `academic-writer` should:

1. run from the project root
2. ensure `bd` is initialized
3. create a parent bead for the deliverable
4. create child beads for required workstreams
5. claim the active bead before work
6. update bead state as work progresses
7. use `bd ready` to pick the next unblocked step

Recommended startup in an OpenCode project:

```bash
bd init
bd setup opencode
bd prime
```

Only trivial copyediting can skip this workflow.

For a new paper, `academic-writer` should create the bead structure automatically once the paper topic and scope are clear.

In Gastown mode, the bead structure should also be attached to a paper convoy.

## Full Article Bead Template

Recommended child beads:

- manuscript architecture
- literature retrieval
- literature review
- theory and hypotheses
- data and methods
- data analysis
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

## Automatic New-Paper Startup

When a user starts a new paper with `academic-writer`, the agent should create the full bead structure automatically.

Suggested script pattern:

```bash
PARENT=$(bd create "Paper: <title or topic>" -p 0 --type epic --silent)
ARCH=$(bd create "Manuscript architecture" -p 1 --parent "$PARENT" --silent)
RETRIEVE=$(bd create "Literature retrieval" -p 1 --parent "$PARENT" --silent)
LIT=$(bd create "Literature review" -p 1 --parent "$PARENT" --silent)
THEORY=$(bd create "Theory and hypotheses" -p 1 --parent "$PARENT" --silent)
METHODS=$(bd create "Data and methods" -p 1 --parent "$PARENT" --silent)
ANALYSIS=$(bd create "Data analysis" -p 1 --parent "$PARENT" --silent)
VIZPLAN=$(bd create "Dataviz strategy" -p 1 --parent "$PARENT" --silent)
FIGS=$(bd create "ggplot figures" -p 1 --parent "$PARENT" --silent)
RESULTS=$(bd create "Results writing" -p 1 --parent "$PARENT" --silent)
DISCUSS=$(bd create "Discussion and limitations" -p 1 --parent "$PARENT" --silent)
CONCLUDE=$(bd create "Conclusion" -p 1 --parent "$PARENT" --silent)
REVIEW=$(bd create "Reviewer-2 pressure test" -p 1 --parent "$PARENT" --silent)

bd dep add "$LIT" "$RETRIEVE"
bd dep add "$THEORY" "$LIT"
bd dep add "$METHODS" "$THEORY"
bd dep add "$ANALYSIS" "$METHODS"
bd dep add "$VIZPLAN" "$ANALYSIS"
bd dep add "$FIGS" "$VIZPLAN"
bd dep add "$RESULTS" "$ANALYSIS"
bd dep add "$RESULTS" "$FIGS"
bd dep add "$DISCUSS" "$RESULTS"
bd dep add "$CONCLUDE" "$DISCUSS"
bd dep add "$REVIEW" "$CONCLUDE"

bd update "$ARCH" --claim
bd ready
```

The first active bead should usually be `Manuscript architecture`.

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
bd create "Data analysis" -p 1
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
bd dep add <data-analysis> <data-methods>
bd dep add <dataviz-strategy> <data-analysis>
bd dep add <ggplot-figures> <dataviz-strategy>
bd dep add <results-writing> <data-analysis>
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
- data analysis -> `data-analysis`
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
