# Thinking Essence Extraction Skill

This project provides a **Thinking Essence Extraction** skill for Claude Code.

## Installation

The skill is auto-discovered from `.claude/skills/thinking-essence-extraction/SKILL.md`.

To install in a new project:

```bash
# Unix
curl -sL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.sh | bash

# Windows PowerShell
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.ps1) }"
```

## Usage

Once installed, Claude Code will use this skill when you ask technical analysis questions:

```
用本质变量抽取分析：DeepLabV3+ 的 ASPP 中不同 dilation 起了什么作用？
```

Or in English:

```
Use essence variable extraction to analyze: what role do different dilations play in DeepLabV3+'s ASPP?
```

## What it enforces

Every technical analysis will include:

1. **Variable Table** — Direct variables, derived variables, observed metrics, hidden variables
2. **Mechanism Chain** — Complete causal chain using `→` notation
3. **Cost Trade-off** — "At the cost of X, in exchange for Y, at risk of Z"
4. **Verifiable Hypothesis** — At least 1 falsifiable experiment design

## Reference files (installed path)

- `.claude/skills/thinking-essence-extraction/docs/variable_cards.md` — Variable definitions and interaction cards
- `.claude/skills/thinking-essence-extraction/docs/anti_patterns.md` — Common explanation errors
- `.claude/skills/thinking-essence-extraction/docs/baseline_defect_taxonomy.md` — 10 types of baseline defects
- `.claude/skills/thinking-essence-extraction/docs/module_cards.md` — 15 module analysis cards
- `.claude/skills/thinking-essence-extraction/docs/baseline_evolution_workflow.md` — Baseline evolution workflow
- `.claude/skills/thinking-essence-extraction/examples/remote_sensing_segmentation_examples.md` — Remote sensing examples
- `.claude/skills/thinking-essence-extraction/examples/engineering_design_examples.md` — Engineering design examples
- `.claude/skills/thinking-essence-extraction/examples/baseline_evolution_examples.md` — Baseline evolution examples
