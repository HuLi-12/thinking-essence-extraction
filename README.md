# Thinking Essence Extraction / 本质变量抽取

强制技术分析落到变量、机制链、代价交换、可验证实验的技能包。

## 结构

```
thinking-essence-extraction/
├── SKILL.md                                    # 主技能文件（执行规则）
├── README.md                                   # 本文件
├── CHANGELOG.md                                # 版本历史
├── CONTRIBUTING.md                             # 贡献规范
├── LICENSE                                     # 许可证
├── .gitignore                                  # Git 忽略规则
├── examples/
│   ├── remote_sensing_segmentation_examples.md # 遥感分割领域正例（4个）
│   └── engineering_design_examples.md          # 工程设计领域正例（4个）
├── evals/
│   ├── test_prompts.md                         # 测试用例集（9个）
│   └── expected_checkpoints.md                 # 预期输出检查点
├── docs/
│   ├── anti_patterns.md                        # 错误→修正对照（5组）
│   └── variable_cards.md                       # 变量卡片（14张+7组交互）
└── scripts/
    ├── validate_skill_package.py               # 包完整性验证脚本
    └── check_response_against_checkpoints.py   # 测试评分脚本
```

## 核心设计

```text
1. 变量表    → 什么变量变了（直接/衍生/观测/隐藏）
2. 机制链    → 变量如何通过约束传导到结果
3. 代价交换  → 拿什么换什么
4. 可验证    → 如何实验证伪这个解释
```

## 使用方式

### Claude Code

本技能已配置为 Claude Code 可发现技能。
在会话中直接说：

> 用本质变量抽取分析：[你的技术问题]

### 其他场景

`SKILL.md` 可作为独立 prompt 模板用于 ChatGPT、Codex 或其他 LLM。

## 场景覆盖

- 神经网络模块分析（ASPP、decoder、attention 等）
- 实验失效诊断（mIoU 下降、类别冲突、模块无效）
- 论文创新点评价（新变量、新约束、新机制）
- 工程设计本质分析（缓存、索引、并发等）
- 概念本质解释（1×1 conv、下采样、skip connection 等）
