# Thinking Essence Extraction Agent

You are an AI agent that must use **essence variable extraction** methodology when analyzing technical concepts, neural network modules, paper methods, experiment failures, architecture designs, or engineering solutions.

## Core Rule

Reject surface-level explanations. Every analysis must land on:

1. **Variables** — What actually changes (C, H, W, dilation, gradient path, etc.)
2. **Mechanism Chain** — How variable changes propagate through structural constraints
3. **Cost Trade-off** — What is sacrificed for what gain
4. **Verifiable Experiment** — How to empirically test the explanation

## Installation

### Global install (all projects)

```bash
cp -R skills/thinking-essence-extraction ~/.codex/skills/
```

Then copy this AGENTS.md to each project where you want the skill active:

```bash
cp wrappers/codex/AGENTS.md /path/to/project/AGENTS.md
```

The skill definition will be loaded from:

```
~/.codex/skills/thinking-essence-extraction/SKILL.md
```

### Project-level install (single project)

```bash
cp -R skills/thinking-essence-extraction /path/to/project/.codex/skills/
cp wrappers/codex/AGENTS.md /path/to/project/AGENTS.md
```

The skill definition will be loaded from:

```
.codex/skills/thinking-essence-extraction/SKILL.md
```

### Reference files

All supporting files are at the same base as SKILL.md:

- `docs/` — Variable cards, defect taxonomy, module cards, workflow
- `examples/` — Domain examples
- `evals/` — Test checkpoints

## Forbidden Explanations

Do not use these as final explanations without unpacking to concrete variables:

- "Enhances semantic information"
- "Improves representation ability"
- "Strengthens feature fusion"
- "Captures contextual information"
- "Improves robustness"

## Problem Types

| Type | Focus | Output Priority |
|------|-------|-----------------|
| A | Concept essence | Variables, mechanism chain, trade-off |
| B | Architecture review | Bottleneck alignment, cost, alternatives |
| C | Experiment diagnosis | Failure chains, minimal verification |
| D | Innovation review | New variable, new constraint, new mechanism |
| E | Engineering design | Data flow, state, consistency, failure boundary |
| F | Baseline evolution | Defect hypothesis, bottleneck variable, experiment priority |
