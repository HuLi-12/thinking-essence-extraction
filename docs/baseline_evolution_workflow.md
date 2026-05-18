# Baseline Evolution Workflow

当需要对 baseline 进行进化设计时，按照以下流程进行。

---

## Workflow Overview

```text
baseline 缺陷诊断
→ 变量瓶颈定位
→ 文献/模块搜索
→ 模块适配判断
→ 最小验证实验
→ 结果反馈进化
```

---

## Step 1: Baseline Profile

记录当前状态：

```text
当前架构：
当前 mIoU：
关键瓶颈（基于已有实验或分析）：
```

---

## Step 2: Defect Hypothesis

从 Defect Taxonomy（`docs/baseline_defect_taxonomy.md`）中选取最可能的缺陷类型。
每个缺陷必须附带证据或推断：

```text
缺陷类型：
证据/推断：
瓶颈变量：
```

**规则**：
- 至少列出 2 个候选缺陷，但不要超过 4 个
- 每个缺陷必须有独立证据（不是同一个现象的不同表述）
- 区分结构事实与待验证假设（遵守 Evidence Level Rule）

---

## Step 3: Candidate Module Pool

针对每个缺陷，从 Module Cards（`docs/module_cards.md`）或文献搜索中选取候选模块。
每个模块必须包含：

```text
对应缺陷：
修改变量：
引入位置：
代价估算（参数量/FLOPs/显存）：
最小验证实验：
```

**规则**：
- 每个缺陷至少推荐 1 个模块，但不要超过 3 个
- 优先选择改动最小的方案
- 标注代价估算为经验估计（参看 Module Cards 中的 Estimation Warning）

### Literature/Module Search Rule

搜索文献或模块时，遵守以下规则。

#### Search Around Variables, Not Vague Concepts

错误搜索方向：

```text
特征融合模块
语义增强方法
多尺度上下文
```

正确搜索方向：

```text
解决 boundary 定位精度的模块
控制 ERF 与目标尺度对齐的结构
处理 class imbalance / class confusion 的 loss
能增加 feature 类间距离的正则方法
浅层梯度衰减问题的辅助训练结构
```

#### Map Module to Defect

找到候选模块后，必须回答：

- 这个模块解决了我的哪类缺陷？
- 它改变了哪个具体变量（C, H, W, dilation, loss weight, gradient path...）？
- 它在原论文中被验证解决的是什么场景下的问题（大目标、小目标、边界、类混淆）？
- 它的引入代价是什么（参数量、FLOPs、activation memory、训练稳定性）？

#### Reject Without Verification

以下情况直接拒绝引入：

- "在 XX 数据集上 SOTA" 但没有说明解决了什么具体变量
- 只给了整体指标，没有类别级或尺度级分析
- 模块复杂度远大于当前 baseline 的瓶颈复杂度

#### Search Priority

按以下优先级从高到低搜索：

1. 直接改变当前瓶颈变量的模块（如 boundary loss → B-IoU 下降）
2. 对当前架构改动最小的方案（增量改动优先于重构）
3. 在类似数据分布上验证过的方案（遥感优先于通用视觉）
4. 有公开源码和预训练权重的方案

#### Evidence Record

查找资料后必须记录以下字段。禁止只因为 "SOTA" 或 "论文新" 就加入候选池。

```text
方法名称：
论文年份/来源：
是否有公开代码：
是否有预训练权重：
验证数据集：
是否与当前 baseline 同任务/同尺度/同输入分辨率：
是否控制 Params / FLOPs：
核心提升来自哪个变量：
是否有 class-wise / scale-wise / boundary 指标：
可复现实验入口：
```

---

## Step 4: Experiment Priority

设计实验序列，按优先级排列。

### P0 — Must Verify

必须优先验证的瓶颈假设。控制 1 个变量，最快出结果。

```text
实验设计：
预期收益：
资源成本：
```

### P1 — Core Improvement

如果 P0 验证通过后的下一步改进。

```text
实验设计：
预期收益：
```

### P2 — Enhancement

锦上添花，前提是 P0/P1 通过。

```text
实验设计：
预期收益：
```

---

## Step 5: Result Feedback Rule

根据实验结果决定下一步。

```text
如果观察到 [指标变化 A]：
→ 说明 [假设 B] 成立
→ 下一步做 [实验 C]

如果观察到 [指标变化 D]：
→ 说明 [假设 E] 不成立
→ 切换到 [备选路线 F]

如果观察到 [异常现象 G]：
→ 回到 Defect Hypothesis 重新诊断
```

---

## Reference

- Defect Taxonomy: `docs/baseline_defect_taxonomy.md`
- Module Cards: `docs/module_cards.md`
- Evolution Examples: `examples/baseline_evolution_examples.md`
- Variable Cards: `docs/variable_cards.md`
- Variable Interaction Cards: `docs/variable_cards.md` (Interaction Cards section)
