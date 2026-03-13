# academic-editor

OpenCode agent system for planning and writing political science articles in a classic KKV style.

This repo is designed so a user can say:

`install these agents: https://github.com/laurenceomfoisy/academic-editor`

and another coding agent should be able to install the full agent family into OpenCode from this repository.

## What This Repo Contains

- `opencode/opencode.json` - OpenCode agent registry
- `opencode/agents/` - all primary agent and subagent prompts
- `literature/` - literature retrieval pipeline source
- `docs/` - workflow, architecture, beads, and Gastown notes

## Primary Agents

### `academic-planner`

Planning front door.

- acts like a senior mentor in quantitative political science
- helps design the paper before drafting starts
- sharpens the hook, research question, contribution, literature positioning, theory, hypotheses, and design
- produces a structured handoff blueprint for `academic-writer`

### `academic-writer`

Execution front door.

- takes the approved plan from `academic-planner`
- automatically creates the paper bead or convoy structure for new papers
- delegates work to specialist subagents
- writes in LaTeX by default
- integrates outputs into one coherent manuscript
- ends with a `reviewer-2` pressure test

In Gastown mode, `academic-writer` should:

- initialize the project as a rig with `gt init` if needed
- create or manage a paper convoy
- delegate work with `gt sling`
- use `gt handoff` and `gt resume` for session continuity

## Subagent Roster

### Structure and Orchestration

- `paper-architect` - manuscript structure, LaTeX assembly, section order, and overall coherence

### Literature

- `literature-finder` - retrieves project-local papers into `docs/literature/`
- `literature-review` - reads and synthesizes accessible literature in a source-grounded way

### Theory and Design

- `theory-hypotheses` - derives theoretical stance, mechanisms, rival explanations, and hypotheses
- `data-methods` - writes transparent KKV-style methods sections and supports empirical work in Python
- `data-analysis` - executes the analysis, wrangles tidy data, and produces reproducible findings from provided or public data

### Visualization and Results

- `dataviz-editor` - designs the paper-level figure strategy and checks figure diversity
- `ggplot-visualizer` - produces grayscale publication-ready `ggplot` figures
- `results-writer` - turns model output, tables, and figures into disciplined results prose

### Interpretation and Ending

- `discussion-limitations` - writes implications and highly transparent limitations
- `conclusion-writer` - writes the final compact, high-payoff conclusion
- `reviewer-2` - pressure-tests the manuscript like a severe top-journal reviewer

## Typical Workflow

1. Start in `academic-planner`
2. Develop the article plan in classic KKV order:
   - hook
   - research question
   - literature camps
   - theoretical stance
   - hypotheses
   - data and methods
   - discussion logic
   - limitations
   - conclusion payoff
3. End with the `academic-planner` handoff blueprint
   - `Plan status: ready`
   - `Send me to academic-writer`
4. Switch to `academic-writer`
5. `academic-writer` automatically creates the new paper bead or convoy structure
6. `academic-writer` delegates to the specialist subagents in dependency order
7. `reviewer-2` pressure-tests the result before final output

## OpenCode Installation

### What Another Agent Should Do

If a user says:

`install these agents: https://github.com/laurenceomfoisy/academic-editor`

the installing agent should:

1. clone this repository locally
2. copy `opencode/opencode.json` into `~/.config/opencode/opencode.json`
3. copy every file in `opencode/agents/` into `~/.config/opencode/agents/`
4. verify that `~/.config/opencode/opencode.json` parses as valid JSON
5. report which primary agents and subagents were installed
6. if the target project uses Beads, run `bd setup opencode` in that project for native workflow integration

### Manual Install

```bash
git clone https://github.com/laurenceomfoisy/academic-editor.git
mkdir -p ~/.config/opencode/agents
cp academic-editor/opencode/opencode.json ~/.config/opencode/opencode.json
cp academic-editor/opencode/agents/*.md ~/.config/opencode/agents/
python -m json.tool ~/.config/opencode/opencode.json >/dev/null
```

### Beads-Native OpenCode Setup

For projects that use Beads, install the native OpenCode workflow pointer:

```bash
cd your-project
bd init
bd setup opencode
```

This repository now prefers the official `bd setup opencode` output over custom AGENTS boilerplate.
That keeps the OpenCode integration aligned with Beads defaults and lets `bd prime` provide the current workflow context dynamically.

For Gastown-native execution, initialize the project as a rig when needed:

```bash
gt init
```

### Installed OpenCode Agents

After installation, the OpenCode config should include:

- primary: `academic-planner`
- primary: `academic-writer`
- subagent: `paper-architect`
- subagent: `literature-finder`
- subagent: `literature-review`
- subagent: `theory-hypotheses`
- subagent: `data-methods`
- subagent: `data-analysis`
- subagent: `dataviz-editor`
- subagent: `ggplot-visualizer`
- subagent: `results-writer`
- subagent: `discussion-limitations`
- subagent: `conclusion-writer`
- subagent: `reviewer-2`

## Workflow Tracking

This project uses `bd` as the required workflow tracker for substantive work.

- `academic-planner` plans the paper but does not create beads
- `academic-writer` creates and manages the bead structure once the plan is approved
- new papers should start with an automatically created parent bead and standard child beads

See `docs/beads-workflow.md`.

## Gastown Integration

This project also adopts the Gas Town philosophy.

- `academic-writer` acts as the Mayor
- each paper is treated as a convoy
- specialist subagents act like polecats
- recovery should use `gt prime` when inside a Gastown workspace

Execution commands to prefer in Gastown mode:

- `gt convoy create`
- `gt sling`
- `gt handoff`
- `gt resume`
- `gt formula run kkv-article`

See `docs/gastown-workflow.md`.

## Literature Pipeline

The literature tooling lives in `literature/`.

Purpose:

- retrieve papers
- download accessible PDFs
- store outputs in the current project's `docs/literature/`
- support source-grounded literature review and writing

Note:

- article projects should be run from the project root so literature files land in `docs/literature/`

## Additional Requirements

Recommended tools:

- `bd` - required for bead-backed workflow tracking
- `gt` - recommended for Gastown-style recovery and orchestration

Some workflows also assume:

- Python available for the literature pipeline
- OpenCode configured at `~/.config/opencode/`

## Repo Access

Public repository:

- `https://github.com/laurenceomfoisy/academic-editor`

Any user or installing agent with standard GitHub access should be able to clone it and follow the install procedure above.
