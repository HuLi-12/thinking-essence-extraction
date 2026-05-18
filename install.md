# Install

## 推荐方式：复制完整 skill 文件夹

```bash
# 克隆仓库
git clone https://github.com/HuLi-12/thinking-essence-extraction.git
cd thinking-essence-extraction

# === Codex CLI ===

# 全局安装
cp -R skills/thinking-essence-extraction ~/.codex/skills/

# 项目级安装
cp -R skills/thinking-essence-extraction /path/to/project/.codex/skills/

# Codex 项目入口（可选）
cp wrappers/codex/AGENTS.md /path/to/project/AGENTS.md

# === Claude Code ===

# 安装 skill
cp -R skills/thinking-essence-extraction /path/to/project/.claude/skills/

# 使用 subagent wrapper（可选）
cp wrappers/claude/subagent.md /path/to/project/

# 或配置为 slash command（高级）
# 将 wrappers/claude/command.md 中的 JSON 加入 ~/.claude/commands.json
```

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
