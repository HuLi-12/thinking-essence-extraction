# Thinking Essence Extraction / 本质变量抽取

强制技术分析落到**变量、机制链、代价交换、可验证实验**的技能单元。

## 用法

将此文件夹整体复制到你的 Codex 或 Claude 的 skills 目录：

```bash
# Codex (全局安装)
cp -R skills/thinking-essence-extraction ~/.codex/skills/

# Codex (项目级)
cp -R skills/thinking-essence-extraction .codex/skills/

# Claude (需要 subagent wrapper，见 wrappers/claude/)
```

## 结构

```
thinking-essence-extraction/
├── README.md          # 本文件
├── SKILL.md           # 主技能文件（执行规则）
├── docs/              # 参考文档
│   ├── variable_cards.md               # 变量卡片（14张 + 9组交互）
│   ├── anti_patterns.md                # 错误→修正对照（5组）
│   ├── baseline_defect_taxonomy.md     # baseline 缺陷分类（10类）
│   ├── module_cards.md                 # 模块卡片（15个）
│   └── baseline_evolution_workflow.md  # baseline 进化工作流
├── examples/          # 领域分析案例
│   ├── remote_sensing_segmentation_examples.md   # 遥感分割（4个）
│   ├── engineering_design_examples.md            # 工程设计（6个）
│   └── baseline_evolution_examples.md            # baseline 进化（2个）
└── evals/             # 测试检查点
    ├── test_prompts.md       # 14 个测试用例
    ├── checkpoints.json      # JSON 评分检查点
    └── expected_checkpoints.md
```

## 能力

| 类型 | 场景 | 说明 |
|------|------|------|
| Type A | Concept Essence | 1×1 卷积、下采样、skip connection 等概念本质 |
| Type B | Architecture Review | Decoder、ASPP、backbone 结构审查 |
| Type C | Experiment Diagnosis | mIoU 下降、模块无效、类别冲突诊断 |
| Type D | Innovation Review | 论文创新点评价（5 维判断） |
| Type E | Engineering Design | 缓存、索引、并发、架构设计分析 |
| Type F | Baseline Evolution | Baseline 缺陷诊断→模块搜索→实验序列设计 |
