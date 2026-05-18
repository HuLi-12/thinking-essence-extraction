# Thinking Essence Extraction

本质变量抽取 — 强制技术分析落到变量、机制链、代价交换、可验证实验的 skill 集。

## Skills

| Skill | Status | Description |
|-------|--------|-------------|
| [thinking-essence-extraction](skills/thinking-essence-extraction/) | Stable | Essence variable extraction for technical analysis |

## Quick Install

```bash
# Clone the repo
git clone https://github.com/HuLi-12/thinking-essence-extraction.git
cd thinking-essence-extraction

# Ensure target dir exists, then copy the entire skill folder
mkdir -p ~/.codex/skills
cp -R skills/thinking-essence-extraction ~/.codex/skills/
```

> **不要只复制 SKILL.md。** SKILL.md 通过相对路径引用 docs/examples/evals，必须复制完整目录才能正常工作。

详细安装方式（全局/项目级、Codex/Claude、Windows）见 [install.md](install.md)。

## Repository Structure

```
thinking-essence-extraction/
├── README.md                          # 本文件（registry 索引）
├── install.md                         # 安装说明
├── CHANGELOG.md                       # 版本历史
├── CONTRIBUTING.md                    # 贡献规范
├── LICENSE                            # 许可证
│
├── skills/
│   └── thinking-essence-extraction/   # 技能本体（可复制单元）
│       ├── README.md
│       ├── SKILL.md
│       ├── docs/
│       ├── examples/
│       └── evals/
│
├── wrappers/
│   ├── codex/
│   │   └── AGENTS.md                  # Codex wrapper（全局/项目级）
│   └── claude/
│       ├── subagent.md                # Claude subagent wrapper
│       └── command.md                 # Claude slash command wrapper
│
├── scripts/
│   ├── validate_skill_package.py      # 包完整性验证
│   └── check_response_against_checkpoints.py  # 测试评分
│
└── .github/workflows/
    ├── validate.yml                   # CI 自动验证
    └── release.yml                    # Release 打包
```

## Usage Examples

```text
# Codex
codex "用本质变量抽取分析：1×1 卷积的本质是什么？"

# Claude (subagent)
claude "Use thinking-essence-extraction to analyze: 1×1 convolution essence"

# Claude (slash command)
/essence 用本质变量抽取分析：ASPP 中不同 dilation 起了什么作用？

# Manual / Other agents
Read skills/thinking-essence-extraction/SKILL.md for full methodology.
Apply Core Rule to any technical analysis question.
```

## Development

```bash
# 验证包完整性
python scripts/validate_skill_package.py

# 运行测试评分
python scripts/check_response_against_checkpoints.py "Test 1" "<response>"
```

## License

MIT
