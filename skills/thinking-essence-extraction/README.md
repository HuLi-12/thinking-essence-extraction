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

## 最小调用示例

```text
输入：用本质变量抽取分析 1×1 卷积的核心作用。

预期输出框架：
1. 变量表：C_in, C_out, 1×1 卷积核 (weight), 逐点非线性映射
2. 机制链：1×1 卷积核在 H×W 空间滑动 → 每个空间位置做 C_in→C_out 全连接映射
   → 本质是跨通道特征重组合（跨通道线性/非线性映射），不改变空间结构
3. 代价交换：参数量 O(C_in×C_out) 显著低于 3×3 的 O(9×C_in×C_out)；
   失去空间感受野（1×1 不聚合空间邻域信息）
4. 可验证实验：对比 1×1 卷积与 3×3 卷积在分类任务（纯语义，空间不重要）
   与分割任务（空间细节重要）上的表现差异
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
