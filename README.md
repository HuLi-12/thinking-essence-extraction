# Thinking Essence Extraction / 本质变量抽取

强制技术分析落到**变量、机制链、代价交换、可验证实验**的 agent skill package。
支持一键安装到 **Codex CLI** 和 **Claude Code**。

---

## Quick Install

### Codex CLI

```bash
# 从本仓库安装到当前项目
curl -sL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_codex.sh | bash

# 或手动复制
cp AGENTS.md /path/to/your-project/
cp -r .codex /path/to/your-project/
```

安装后，在项目根目录运行：

```bash
codex "用本质变量抽取分析：DeepLabV3+ 的 ASPP 是什么原理？"
```

### Claude Code

```bash
# 从本仓库安装到当前项目
curl -sL https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.sh | bash

# 或手动复制
cp CLAUDE.md /path/to/your-project/
cp -r .claude /path/to/your-project/
```

安装后，在项目根目录运行：

```bash
claude "用本质变量抽取分析：DeepLabV3+ 的 ASPP 是什么原理？"
```

### Manual Prompt

将 `SKILL.md` 全文作为 system prompt：

```text
你是一个严格遵循本质变量抽取的分析助手。
规则如下：[粘贴 SKILL.md 全文]

请用本质变量抽取分析：[你的技术问题]
```

### Windows (PowerShell)

```powershell
# Codex
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_codex.ps1) }"

# Claude
iex "& { $(irm https://raw.githubusercontent.com/HuLi-12/thinking-essence-extraction/master/install/install_claude.ps1) }"
```

---

## What This Does

```text
你不是在得到一个"解释工具"，
而是在得到一个"强制分析落到 4 个核心要素的执行框架"：

1. 变量表    → 什么变量变了（直接/衍生/观测/隐藏）
2. 机制链    → 变量如何通过结构约束传导到结果
3. 代价交换  → 拿什么换什么（没有免费的改进）
4. 可验证    → 如何实验证伪这个解释
```

安装后，你的 agent（Codex 或 Claude）会在相关技术讨论中自动使用这个框架，
拒绝"增强语义信息""提升表达能力""捕获上下文"等不可证伪的解释。

---

## Directory Structure

```
thinking-essence-extraction/
├── SKILL.md                      # 主技能文件（执行规则入口）
├── AGENTS.md                     # Codex agent 清单
├── CLAUDE.md                     # Claude 项目级入口
├── README.md                     # 本文件
├── CHANGELOG.md                  # 版本历史
├── CONTRIBUTING.md               # 贡献规范
├── LICENSE                       # 许可证
│
├── .claude/
│   └── skills/
│       └── thinking-essence-extraction/
│           └── SKILL.md          # Claude Code 自动发现路径
│
├── .codex/
│   └── skills/
│       └── thinking-essence-extraction/
│           ├── SKILL.md          # Codex skill 副本
│           ├── docs/             # 变量卡片、缺陷分类、模块卡片
│           ├── examples/         # 领域分析案例
│           └── evals/            # 测试检查点
│
├── docs/
│   ├── variable_cards.md                 # 14 张变量卡片 + 9 组交互卡片
│   ├── anti_patterns.md                  # 5 组错误→修正对照
│   ├── baseline_defect_taxonomy.md       # 10 类 baseline 缺陷
│   ├── module_cards.md                   # 15 个模块卡片
│   └── baseline_evolution_workflow.md    # Baseline 进化工作流
│
├── examples/
│   ├── remote_sensing_segmentation_examples.md  # 遥感分割分析（4个）
│   ├── engineering_design_examples.md           # 工程设计分析（6个）
│   └── baseline_evolution_examples.md           # Baseline 进化示例（2个）
│
├── evals/
│   ├── test_prompts.md              # 14 个测试用例
│   ├── checkpoints.json             # JSON 评分检查点
│   └── expected_checkpoints.md      # 预期输出描述
│
├── install/
│   ├── install.sh                   # Unix 全量安装
│   ├── install.ps1                  # Windows 全量安装
│   ├── install_codex.sh             # Codex 专用（Unix）
│   ├── install_codex.ps1            # Codex 专用（Windows）
│   ├── install_claude.sh            # Claude 专用（Unix）
│   ├── install_claude.ps1           # Claude 专用（Windows）
│   └── verify_installation.py       # 安装验证脚本
│
├── scripts/
│   ├── validate_skill_package.py    # 包完整性验证
│   ├── check_response_against_checkpoints.py  # 测试评分
│   └── sync_claude_skill.py         # .claude 同步
│
└── .github/workflows/
    ├── validate.yml                 # CI 自动验证
    └── release.yml                  # Release 打包

> 完整结构以 `scripts/validate_skill_package.py` 中 `REQUIRED_FILES` 为准。
```

---

## Capabilities

| 场景 | 类型 | 说明 |
|------|------|------|
| Concept Essence | Type A | 1×1 卷积、下采样、skip connection 等概念本质 |
| Architecture Review | Type B | Decoder、ASPP、backbone 结构审查 |
| Experiment Diagnosis | Type C | mIoU 下降、模块无效、类别冲突诊断 |
| Innovation Review | Type D | 论文创新点评价（5 维判断） |
| Engineering Design | Type E | 缓存、索引、并发、架构设计分析 |
| Baseline Evolution | Type F | Baseline 缺陷诊断→模块搜索→实验序列设计 |

---

## Verification

安装后验证是否生效：

```bash
# Codex
codex "用本质变量抽取分析：1×1 卷积的本质是什么？"

# Claude
claude "用本质变量抽取分析：1×1 卷积的本质是什么？"
```

如果回答包含变量表（C_in, C_out, kernel size）、机制链、代价交换、可验证实验，
则安装成功。如果回答只说了"调整通道数，增强特征表达能力"，则未生效。

### 自动化验证

```bash
# 验证安装完整性
python install/verify_installation.py /path/to/target-project

# 运行完整测试集
python scripts/check_response_against_checkpoints.py "Test 1" "<response text>"
```

---

## Development

```bash
# 克隆后验证包完整性
python scripts/validate_skill_package.py

# 同步 .claude 副本
python scripts/sync_claude_skill.py

# 运行测试评分
python scripts/check_response_against_checkpoints.py "Test 1" "<response>"
```

---

## License

MIT
