# Claude Subagent: Thinking Essence Extraction

A Claude Code subagent that enforces essence variable extraction methodology.

## Usage

Add this to your project's `CLAUDE.md`:

```markdown
## Subagents

Use `thinking-essence-extraction` for technical analysis.
See `.claude/skills/thinking-essence-extraction/` for the full skill definition.
```

## Install

```bash
# 1. Copy the skill folder
cp -R skills/thinking-essence-extraction .claude/skills/

# 2. (Optional) Reference in CLAUDE.md
```

## What this does

When invoked, this subagent forces analysis to land on:

1. **Variables** — What actually changes (C, H, W, dilation, gradient path, etc.)
2. **Mechanism Chain** — How changes propagate through structural constraints
3. **Cost Trade-off** — What is sacrificed for what gain
4. **Verifiable Experiment** — How to empirically test the explanation

The subagent reads the full skill definition from `.claude/skills/thinking-essence-extraction/SKILL.md`.
