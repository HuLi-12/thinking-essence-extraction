---
name: thinking-essence-extraction
version: 1.4.0
description: >
  当用户分析技术概念、神经网络模块、论文方法、实验失效、架构设计或工程方案，
  且要求直击本质、拒绝表层解释时使用。该技能强制分析落到变量、机制链、
  代价交换和可验证实验上，避免"增强语义信息""提升表达能力"等不可证伪解释。
---

# Thinking Essence Extraction / 本质变量抽取

## Core Rule

你必须使用本质变量抽取方式分析技术问题。

核心目标不是讲一个顺滑的解释，而是识别：

1. 哪些变量真正变化；
2. 变量变化如何通过结构约束传导到结果；
3. 这个设计用什么代价换取什么收益；
4. 这个解释如何被实验验证或证伪。

凡是不能落到变量、机制链、代价交换、实验验证的解释，全部视为表层解释。

---

## Problem Type Router

在分析前先判断问题类型，以此决定输出重点。但**不要在最终回答中机械展示这个判断过程**。

### Type A: Concept Essence
解释概念本质。适用于：
- 1×1 卷积本质是什么？
- 下采样后为什么增加通道？
- 为什么 ResNet 要加 shortcut？

输出重点：变量变化、机制链、代价交换。

### Type B: Architecture Review
审查模块或网络结构设计。适用于：
- 这个 decoder 设计合理吗？
- 这个 ASPP 改法是否有效？
- 这个融合方式优于 concatenation 吗？

输出重点：瓶颈是否对齐、代价是否可接受、是否破坏预训练、替代方案对比。

### Type C: Experiment Diagnosis
分析实验失效或指标异常。适用于：
- 为什么 A 类提升但整体 mIoU 下降？
- 为什么模块加上去没效果？
- 为什么两个有效模块组合后无效？

输出重点：class-wise IoU、混淆矩阵、失败链、最小验证实验。

### Type D: Innovation Review
评价论文创新点。适用于：
- 这个方法能不能作为硕士创新点？
- 这个模块是不是堆模块？
- 这个改进的边际贡献是什么？

输出重点：新变量、新约束、新机制、可证伪性、参数量公平性。

### Type E: Engineering Design
分析工程或代码设计。适用于：
- 为什么要加缓存？
- 为什么用 ThreadLocal 而不用参数传递？
- 为什么唯一索引要包含 deleted 列？

输出重点：数据流、状态变量、一致性约束、失败边界、工程代价。

### Type F: Baseline Evolution
规划设计 baseline 进化路线。适用于：
- 当前 baseline 的瓶颈在哪？
- 应该查什么资料、补什么模块？
- 魔改方案设计的实验序列是什么？

输出重点：缺陷假设、瓶颈变量、可改造位置、候选模块池、实验优先级、结果反馈规则。

---

## Core Output Requirements

无论使用哪种输出模式，以下 4 项绝对不能省略：

```text
变量表
机制链
代价交换
可验证实验
```

### Full Mode（默认）
适用于架构审查、论文方法分析（Type B / D）。
包含以下 8 项：

```text
【常见说法】
【问题】
【真正变化的变量】
【本质一句话】
【机制链】
【代价交换】
【可验证】
【对当前模块的启发】
```

### Compact Mode
适用于概念解释、简单机制问题（Type A）。
包含以下 5 项：

```text
【真正变化的变量】
【本质一句话】
【机制链】
【代价交换】
【可验证】
```

极简回答也必须保留 4 项核心要素，只是可以压缩篇幅。

---

## Output Mode Rule

根据问题复杂度选择输出模式，但不能省略变量表、机制链、代价交换、可验证实验四个核心要素。

### Compact Mode
适用于概念解释、简单机制问题（Type A）。
输出结构：
```text
【真正变化的变量】
【本质一句话】
【机制链】
【代价交换】
【可验证】
```

### Full Mode（默认）
适用于架构审查、论文方法分析（Type B / D）。
输出标准 8 段模板（见 Core Output Requirements / Full Mode）。

### Diagnosis Mode
适用于实验失败、指标异常、模块无效（Type C）。
使用 Failure Diagnosis Template 替代标准模板。

### Innovation Mode
适用于创新点评价（Type D）。
使用 Innovation Review Rule 输出格式。

### Evolution Mode
适用于 Baseline Evolution（Type F）。
使用 Baseline Evolution Workflow 模板。

---

## Forbidden Phrases

禁止将以下话术作为未展开的最终解释：

```text
增强语义信息
提升表达能力
加强特征融合
捕获上下文信息
提高鲁棒性
改善特征表示
```

这些话不是完全不能出现，但只有在它们被立刻还原为具体变量时才允许使用。

错误示例：

```text
这个模块增强了语义信息。
```

合格示例：

```text
这个模块不是抽象地"增强语义信息"，而是通过增大有效感受野、
改变 dilation 采样间隔、扩大低分辨率特征的上下文覆盖范围，
以局部采样密度下降为代价，换取更大区域的一致性建模。
```

---

## Variable Table Rule

变量表必须按四类组织，避免变量混在一起：

### Direct Variables
由设计改动直接改变的变量。
例如：C, dilation, kernel size, stride, branch number, loss weight。

### Derived Variables
由直接变量引发的连锁变化。
例如：ERF, sampling density, activation memory, gradient path length, feature map scale。

### Observed Metrics
实验中实际观察到的指标。
例如：mIoU, class-wise IoU, B-IoU, loss curve, confusion matrix。

### Hidden Variables
可能影响结果但当前没有直接观测的变量。
例如：feature separability, BN stability, gradient conflict, pretrained weight damage。

输出示例：

```text
【真正变化的变量】

直接变量：
- dilation rate: 12 → 6

衍生变量：
- ERF 缩小
- 局部采样密度上升
- 远距离依赖覆盖下降

观测指标：
- barren IoU 上升 0.8%
- road IoU 下降 0.5%
- overall mIoU 下降 0.3%

隐藏变量（待验证）：
- 类间 feature distance 是否缩小
- 边界区域 gradient norm 是否增加
```

---

## Evidence Level Rule

分析时必须区分三类内容，**不要把 Hypothesis 写成 Fact**：

### 1. Structural Fact
由网络结构、公式、代码、数学直接确定的事实。
标志词：改变、增加、减少、等于。

例如：
- H×W 下采样 2 倍后，feature map 尺寸减半
- dilation 从 6 增加到 12，采样间隔扩大
- FLOPs = H×W×C_in×C_out×K_h×K_w

### 2. Mechanism Inference
基于 Structural Fact 推出的合理机制，但尚未被本实验验证。
标志词：意味着、导致、可能、推测。

例如：
- dilation 增大 → 局部采样密度下降（这是空间几何关系，属于合理推断）
- 通道增多 → 特征组合能力增强（这是容量推理，但不是直接观测）

### 3. Verifiable Hypothesis
需要特定实验设计来验证的主张。
标志词：如果…那么…、假设、待验证。

例如：
- 如果 road/building 下降来自边界一致性受损，则 B-IoU 应下降
- 如果 ASPP small branch 有效是因为局部采样密度提升，则 3×3 conv 在小 dilation 区间的行为应类似

输出格式：

```text
结构事实：
- dilation 从 6/12/18 改为 3/6/9，ERF 范围缩小

机制推断：
- 局部采样密度提升，远距离依赖覆盖下降
- 小目标的采样噪声减少

待验证假设：
- road/building 的 mIoU 下降来自边界一致性受损 → 需要 B-IoU 验证
- barren 的提升来自采样噪声减少 → 需要对比 barren 在大小 dilation 下的输出稳定性
```

---

## Mechanism Chain Rule

机制链必须使用箭头表示：

```text
变量变化 → 约束变化 → 代价转移 → 结果变化
```

不允许跳链。

错误示例：

```text
ASPP 捕获多尺度上下文 → 提升分割效果
```

合格示例：

```text
dilation rate 增大
→ 采样间隔变大
→ effective receptive field 扩大
→ 局部采样密度下降
→ 大区域类别一致性增强
→ thin object / boundary 的局部细节可能下降
→ class-wise IoU 出现类别间转移
```

---

## Cost Trade-off Rule

任何设计都必须说明代价。

固定格式：

```text
以 [X] 为代价，换取 [Y]，风险是 [Z]。
```

示例：

```text
以空间分辨率下降为代价，换取更高的通道表达容量，
风险是边界和细长目标的定位能力下降。
```

---

## Verifiable Hypothesis Rule

每个解释至少给出 1 个可证伪实验。

优先使用：

```text
ablation study
Params / FLOPs 对比
activation memory 对比
class-wise IoU
boundary IoU
confusion matrix
feature visualization
gradient norm
loss curve
scale-bucket evaluation
```

格式：

```text
如果这个解释成立，应该观察到 [A]；
如果观察不到 [A]，说明 [B] 假设不成立。
```

---

## Internal Validators

以下模型只作为内部检查器，**不要在最终回答中机械列出**：

```text
First Principles：拆假设，找不可绕开的底层事实
Theory of Constraints：找真实瓶颈
Scientific Method：转可证伪假设
Inversion：假设无效，反推原因
Pre-mortem：预判如何失败
Red Team：审稿人攻击视角
```

除非用户明确要求，否则不要输出：

```text
从第一性原理看……
从约束理论看……
从红队视角看……
```

---

## Anti-pattern Self-check

回答前进行自查：

```text
是否把结果当解释？
是否把抽象名词当变量？
是否只讲了单变量，忽略连锁变量？
是否没有说明代价？
是否没有可证伪实验？
是否跳过了机制链中间环节？
是否堆砌思维模型而没有落到技术变量？
是否混淆了推断和事实？
```

任一项为是，则重写。

---

## Standard Output Template

```text
【常见说法】
写出常见但不够本质的解释。

【问题】
说明这个解释为什么只是结果描述，不是机制解释。

【真正变化的变量】
直接变量：
- ...

衍生变量：
- ...

观测指标：
- ...

隐藏变量（待验证）：
- ...

【本质一句话】
这个设计的本质不是 A，而是 B。

【机制链】
变量变化 → 约束变化 → 代价转移 → 结果变化

【代价交换】
以 X 为代价，换取 Y，风险是 Z。

【可验证】
1. 如果该解释成立，应该观察到什么？
2. 用什么实验或指标验证？
3. 如果没有观察到，说明哪个假设错误？

【对当前模块的启发】
给出对当前架构、实验、模块设计或论文创新点的指导。
```

---

## Failure Diagnosis Template

当用户分析实验失败、模块无效、mIoU 下降、类别指标异常时，使用以下模板替代标准模板中的部分内容：

### 1. Observed Phenomenon
描述实验现象，不要先解释。

### 2. Changed Variables
本次实验相对 baseline 改了哪些变量（按四类组织）。

### 3. Possible Failure Chains
至少给出 2-3 条互斥的失败假设链，每条链必须完整（变量 → 约束 → 代价 → 结果）。

### 4. Most Likely Bottleneck
判断最可能的瓶颈，但必须说明证据不足的部分。

### 5. Minimal Verification
给出最小验证实验（控制 1 个变量，最快出结果），而不是直接设计大方案。

### 6. Next Action
下一步优先跑什么实验、对比什么指标。

输出示例：

```text
【现象】
S2 加入 small-context ASPP 后 barren 提升 0.6%，但 road/building 下降 0.8%，mIoU 不升。

【失败链 1】
small dilation → 局部纹理采样密度 ↑ → barren 更易分离
→ 但 road/building 的连续边界采样变碎 → 边界一致性下降

【失败链 2】
新增分支参数量 ↑ → 同等 epoch 训练不充分
→ small branch 输出权重不稳定 → 融合后扰动原 ASPP 输出分布

【失败链 3】
small branch 与原 ASPP low-dilation branch 功能重叠
→ concat 后 1×1 bottleneck 压缩 → 有效信息被冗余信息挤掉

【最小验证】
1. 冻结新增 branch 的 fusion weight 为 0，只训练 backbone → 排除训练扰动
2. 可视化 branch 输出 activation → 是否与原 low-dilation branch 高度相关
3. 对比 road/building 的 boundary IoU → 验证边界一致性假设

【下一步】
优先跑最小验证 1 和 3，先排除新增分支扰动和边界一致性下降这两个假设。
```

---

## Innovation Review Rule

当用户询问某个模块是否适合作为论文创新点时，从以下 5 个维度判断：

### 1. New Variable
是否引入了新的可控变量，而不是只堆已有模块？
- 是：提出了一种新的结构参数或损失项
- 否：只是把 A 模块换成 B 模块，没有引入新变量

### 2. New Constraint
是否提出了新的结构约束、损失约束、类别约束或尺度约束？
- 是：对模型行为施加了之前没有的约束
- 否：只是增加了自由度（更多通道、更多层）

### 3. New Mechanism
是否能形成清晰的机制链，而不是只说"提升性能"？
- 是：能写出 X 变量 → Y 约束 → Z 结果的完整链路
- 否：跳过中间变量，直接说"因此效果更好"

### 4. Verifiable Prediction
是否能预测哪些类别、哪些场景、哪些指标会变？
- 是：能说清"A 类应该上升，B 类可能下降"
- 否：只说"整体性能提升"

### 5. Minimal Superiority
能否用简单的 baseline 排除"只是参数/计算更多"的嫌疑？
- 是：控制参数量公平对比，仍有优势
- 否：不控制参数量，无法排除计算量优势

输出格式：

```text
【创新点判断】
- 新变量：是/否 —— [判断依据]
- 新约束：是/否 —— [判断依据]
- 新机制：是/否 —— [判断依据]
- 可预测：是/否 —— [判断依据]
- 公平对比：是/否 —— [判断依据]

【成立的条件】
如果满足以下条件，该创新成立：...

【不成立的风险】
如果以下情况发生，该创新不成立：...

【建议】
...
```

---

## Literature/Module Search Rule

当为 baseline evolution 搜索文献或模块时，按照以下规则进行。

### 1. Search Around Variables, Not Vague Concepts

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

### 2. Map Module to Defect

找到一个候选模块后，必须回答：

- 这个模块解决了我的哪类缺陷？
- 它改变了哪个具体变量（C, H, W, dilation, loss weight, gradient path...）？
- 它在原论文中被验证解决的是什么场景下的问题（大目标、小目标、边界、类混淆）？
- 它的引入代价是什么（参数量、FLOPs、activation memory、训练稳定性）？

### 3. Reject Without Verification

以下情况直接拒绝引入：

- "在 XX 数据集上 SOTA" 但没有说明解决了什么具体变量
- 只给了整体指标，没有类别级或尺度级分析
- 模块复杂度远大于当前 baseline 的瓶颈复杂度

### 4. Search Priority

按以下优先级从高到低搜索：

1. 直接改变当前瓶颈变量的模块（如 boundary loss → B-IoU 下降）
2. 对当前架构改动最小的方案（增量改动优先于重构）
3. 在类似数据分布上验证过的方案（遥感优先于通用视觉）
4. 有公开源码和预训练权重的方案

### 5. Evidence Record

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


## Baseline Evolution Rule

当用户请求 baseline 魔改、网络结构进化、模块搜索、实验路线设计时，使用 Evolution Mode。

必须遵守以下流程：

```text
baseline 缺陷 → 瓶颈变量 → 候选模块 → 适配判断 → 最小实验 → 结果反馈
```

详细模板和搜索规则参考：

- `docs/baseline_evolution_workflow.md`
- `docs/baseline_defect_taxonomy.md`
- `docs/module_cards.md`
- `examples/baseline_evolution_examples.md`


---

## Domain Reference

分析遥感语义分割、DeepLabV3+、ASPP、decoder、LoveDA、mIoU、class-wise IoU 等问题时，参考：

- `examples/remote_sensing_segmentation_examples.md`
- `examples/baseline_evolution_examples.md`
- `docs/baseline_defect_taxonomy.md`
- `docs/module_cards.md`
- `docs/baseline_evolution_workflow.md`
- `docs/variable_cards.md`

分析工程设计问题时，参考：

- `examples/engineering_design_examples.md`

反例和错误分析参考：

- `docs/anti_patterns.md`

必须迁移分析结构，不机械复用结论。
