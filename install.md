# Install

## 推荐方式：复制完整 skill 文件夹

```bash
# 克隆仓库
git clone https://github.com/HuLi-12/thinking-essence-extraction.git
cd thinking-essence-extraction

# === Codex CLI ===

# 全局安装
mkdir -p ~/.codex/skills
cp -R skills/thinking-essence-extraction ~/.codex/skills/

# 项目级安装
mkdir -p /path/to/project/.codex/skills
cp -R skills/thinking-essence-extraction /path/to/project/.codex/skills/

# Codex 项目入口（可选）
cp wrappers/codex/AGENTS.md /path/to/project/AGENTS.md

# === Claude Code ===

### 方式 A：项目级 skill 文件夹（推荐）

```bash
mkdir -p /path/to/project/.claude/skills
cp -R skills/thinking-essence-extraction /path/to/project/.claude/skills/
```

Claude Code 会自动发现 `.claude/skills/` 下的 skill 文件。

### 方式 B：用户级 subagent（多项目共享）

```bash
mkdir -p ~/.claude/agents
cp wrappers/claude/subagent.md ~/.claude/agents/thinking-essence-extraction.md
```

然后在项目 `CLAUDE.md` 中引用：

```markdown
## Subagents

Use `thinking-essence-extraction` for technical analysis of deep learning architectures.
```

### 方式 C：Slash command（快捷入口）

将 `wrappers/claude/command.md` 直接复制到 commands 目录：

```bash
mkdir -p ~/.claude/commands
cp wrappers/claude/command.md ~/.claude/commands/essence.md
```

用法：`/essence 用本质变量抽取分析：ASPP 中不同 dilation 起了什么作用？`

## 验证安装

```bash
# Codex
codex "用本质变量抽取分析：1×1 卷积的本质是什么？"

# Claude
claude "用本质变量抽取分析：1×1 卷积的本质是什么？"
```

回答应包含：变量表、机制链、代价交换、可验证实验。

## 辅助安装脚本

仓库 `install/` 目录提供了自动化脚本（非必需）：

```bash
# Unix
bash install/install.sh /path/to/project

# Windows PowerShell
powershell -File install/install.ps1 -Target "C:\path\to\project"
```

## 输入

```bash
# Codex
codex "[用本质变量抽取分析]你的技术问题"
```

## 注意事项

- **整个 skill 文件夹**才是安装单元，不要只复制 SKILL.md
- SKILL.md 通过相对路径引用 docs/examples/evals，复制完整目录才能正常工作
- AGENTS.md 是 Codex 项目级上下文，不是 skill 本体的一部分
- Claude 安装后需重启 Claude Code 才能自动发现
