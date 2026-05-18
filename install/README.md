# Installation Guide

## Codex CLI

```bash
# One-line install
curl -fsSL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_codex.sh | bash

# Install to specific project
curl -fsSL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_codex.sh | bash -s /path/to/project
```

Installs:
- `AGENTS.md` — Codex agent manifest (project root)
- `.codex/skills/thinking-essence-extraction/` — Full skill package (SKILL.md, docs, examples, evals)

## Claude Code

```bash
# One-line install
curl -fsSL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.sh | bash

# Install to specific project
curl -fsSL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.sh | bash -s /path/to/project
```

Installs:
- `CLAUDE.md` — Claude project entry (project root)
- `.claude/skills/thinking-essence-extraction/` — Skill for auto-discovery (SKILL.md, docs, examples)

## Windows (PowerShell)

```powershell
# Codex
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_codex.ps1) }"

# Claude
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.ps1) }"

# Both
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install.ps1) }"
```

## Full Install (Codex + Claude)

```bash
# Unix
curl -fsSL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install.sh | bash

# Windows
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install.ps1) }"
```

## Manual Install

1. Clone the repo:
   ```bash
   git clone https://github.com/HuLi-12/thinking-essence-extraction.git
   ```
2. Copy files:
   ```bash
   # For Codex
   cp AGENTS.md /path/to/your-project/
   cp -r .codex /path/to/your-project/
   
   # For Claude
   cp CLAUDE.md /path/to/your-project/
   cp -r .claude /path/to/your-project/
   ```

## Verify Installation

```bash
# Verify both
python install/verify_installation.py /path/to/target-project

# Verify specific agent
python install/verify_installation.py /path/to/target-project --agent codex
python install/verify_installation.py /path/to/target-project --agent claude
```

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `curl: command not found` | curl not installed (Windows) | Use PowerShell script instead |
| `404` on download | Wrong branch name | Ensure `master` is the default branch |
| AGENTS.md missing after install | Script aborted mid-way | Re-run with `curl -fsSL` (note `-f` flag) |
| Skill not active in Claude | Wrong `.claude` path | Ensure `.claude/skills/.../SKILL.md` exists |
| Skill not active in Codex | Codex CLI outdated | Run `codex --version`, update if < 0.5 |
