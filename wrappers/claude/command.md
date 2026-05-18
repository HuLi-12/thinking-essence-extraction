# Slash Command: /essence

A Claude Code slash command that invokes the Thinking Essence Extraction skill.

## Setup

Add to `~/.claude/commands.json` or `.claude/commands.json`:

```json
{
  "commands": {
    "essence": {
      "description": "Analyze with essence variable extraction",
      "prompt": "You are a strict essence variable extraction analyst.\n\nRead the skill from:\n.claude/skills/thinking-essence-extraction/SKILL.md\n\nNow analyze the following using the methodology:\n{{input}}"
    }
  }
}
```

## Usage

```
/essence 用本质变量抽取分析：ASPP 中不同 dilation 起了什么作用？
```

## Requirements

- Skill folder must be installed at `.claude/skills/thinking-essence-extraction/`
- Claude Code with commands.json support
