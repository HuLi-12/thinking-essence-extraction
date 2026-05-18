# Test Prompts for thinking-essence-extraction

本文件包含用于验证 skill 是否稳定生效的测试用例。
每个测试包含：输入 prompt、合格标准、不合格示例。

---

## Test 1：1×1 卷积的本质

### 输入

```text
用本质变量抽取分析：1×1 卷积的本质是什么？
```

### 合格标准

- [ ] 必须说明 1×1 conv 在**每个空间位置**上做的是 **C_in → C_out 的通道线性投影**
- [ ] 必须给出变量：kernel size = 1×1, params = C_in × C_out, 空间分辨率不变
- [ ] 必须区分参数量与 FLOPs：参数量只取决于 C_in × C_out，与 H×W 无关
- [ ] 不能只说"调整通道数"——必须说清楚"怎么调整"
- [ ] 必须有代价交换：以失去空间特征交互为代价换取通道间的全连接组合

### 不合格示例

```text
1×1 卷积可以调整通道数，实现跨通道的信息交互，增强特征表达能力。
```

> 问题：没有变量、没有参数公式、没有代价、把"信息交互"当解释。

---

## Test 2：下采样后增加通道

### 输入

```text
用本质变量抽取分析：为什么下采样后通常增加通道？
```

### 合格标准

- [ ] 必须区分 H×W 下降带来的多重影响（计算量下降、激活内存下降）
- [ ] 必须说到"用空间预算换通道容量"
- [ ] 必须提到参数量和 FLOPs 的变化关系
- [ ] 必须说到 decoder 需要补偿空间损失
- [ ] 必须给出可验证实验

### 不合格示例

```text
下采样后语义增强，所以增加通道来匹配语义复杂度。
```

> 问题："语义增强"是结果不是原因，"语义复杂度"不可度量。

---

## Test 3：ASPP dilation 改小后部分提升但整体下降

### 输入

```text
用本质变量抽取分析：DeepLabV3+ 中 ASPP dilation 从 (6,12,18) 改为 (3,6,9) 后，
barren 类提升 0.6% 但 road 类下降 0.5%，整体 mIoU 下降 0.3%，为什么？
```

### 合格标准

- [ ] 必须说到 ERF（有效感受野）变化与目标尺度的对齐关系
- [ ] 必须给出 sampling density（采样密度）的变化
- [ ] 必须区分大目标和小目标受不同 dilation 的影响
- [ ] 必须给出类别级验证实验（class-wise IoU / scale bucket）
- [ ] Evidence Level 区分清晰：哪些是结构事实、哪些是推断、哪些是假设

### 不合格示例

```text
Dilation 改小后，对大目标的上下文捕获不足，但对小目标更友好。
因此大目标类下降，小目标类上升。
```

> 问题："上下文捕获不足"和"更友好"都是不可度量的说辞，没有给出 ERF、采样密度等变量。

---

## Test 4：Decoder 设计是否合理

### 输入

```text
用本质变量抽取分析这个 decoder 设计：
1×1 conv (reduce 48→C) → 3×3 conv (C→C) → 4× upsampling → concat with res2 → 3×3 conv → 4× upsampling
这个设计在 LoveDA 上有没有问题？瓶颈可能在哪？
```

### 合格标准

- [ ] 必须分析梯度路径长度和上采样倍数的分配
- [ ] 必须指出 low-level feature（res2）与 high-level feature 的对齐问题
- [ ] 必须分析 1×1 reduce 的信息瓶颈
- [ ] 必须给出代价交换
- [ ] 必须给出可验证假设

### 不合格示例

```text
这个 decoder 设计合理，能恢复空间细节，提升分割精度。
```

> 问题：没有变量分析、没有具体瓶颈判断、没有给出可验证预测。

---

## Test 5：ResNet-50 vs ResNet-101

### 输入

```text
用本质变量抽取分析：ResNet-50 和 ResNet-101 在 LoveDA 上的表现接近，
几乎没有收益。为什么更深的网络在 LoveDA 上不带来提升？
```

### 合格标准

- [ ] 必须分析 ERF 与 LoveDA 目标尺度的匹配关系
- [ ] 必须提到 BN 稳定性对少样本类别的影响
- [ ] 必须区分参数量、FLOPs、有效容量的差异
- [ ] 必须给出 Evidence Level 区分
- [ ] 必须给出可验证实验（scale bucket / BN statistics / gradient norm）

### 不合格示例

```text
LoveDA 场景简单，不需要太深的网络。
ResNet-101 在遥感场景上收益递减。
```

> 问题："场景简单"无定义，"收益递减"是现象不是解释。

---

## Test 6：模块无效归因

### 输入

```text
我在 DeepLabV3+ 的 ASPP 后面加了一个 frequency branch（DWT + 高频增强），
在 LoveDA 上完全没提升，反而 mIoU 下降了 0.2%。为什么？
```

### 合格标准

- [ ] 必须使用 Failure Diagnosis Template
- [ ] 必须给出 2-3 条互斥的失败链
- [ ] 必须给出最小验证实验
- [ ] 必须区分结构事实、推断和假设
- [ ] 必须说明"可能的原因"而非唯一断言

### 不合格示例

```text
Frequency branch 引入的噪声大于收益，所以没有提升。
```

> 问题：只有一个解释、没有证据分层、没有给出验证方法。

---

## Test 7：创新点判断

### 输入

```text
我想把 ASPP 中所有 dilation 改成可学习的参数（让网络自己学 dilation 值），
作为硕士论文的创新点，你觉得够不够？
```

### 合格标准

- [ ] 必须使用 Innovation Review Rule 的 5 个维度逐一判断
- [ ] 必须给出"成立的条件"和"不成立的风险"
- [ ] 必须有参数量/计算量的公平性分析
- [ ] 必须有可证伪预测

### 不合格示例

```text
可学习 dilation 是一个不错的创新点，能让网络自适应调整感受野。
```

> 问题：没有维度判断、没有风险分析、没有公平性检查。

---

## Test 8：工程设计——为什么唯一索引要包含 deleted

### 输入

```text
用本质变量抽取分析：MySQL 表中，为什么唯一索引要包含 deleted 列？
```

### 合格标准

- [ ] 必须使用 Type E: Engineering Design 重点
- [ ] 必须分析"软删除 vs 唯一约束"的矛盾
- [ ] 必须给出数据流和状态变量
- [ ] 必须给出一致性约束的代价权衡
- [ ] 必须说明失败边界（并发问题）

### 不合格示例

```text
防止重复数据，实现软删除。
```

> 问题：没有分析软删除与唯一约束的矛盾本质（逻辑删除导致同一条记录可插入多次），没有给出并发场景下的风险。

---

## Test 9：Evidence Level 强制检查

### 输入

```text
用本质变量抽取分析：在语义分割中，增加 ASPP 的 dilation 为什么能提升大目标的分割质量？
```

### 合格标准

- [ ] 必须明确区分结构事实、机制推断、待验证假设
- [ ] 结构事实：dilation 增大 → 采样间隔增大 → ERF 扩大（数学确定）
- [ ] 机制推断：大目标上采样点覆盖更全面（合理推断）
- [ ] 待验证假设：大目标 mIoU 提升来自远距离依赖覆盖（需要实验验证）
- [ ] 不能把推断写成事实（如"dilation 增大一定提升大目标"——取决于目标尺度与 ERF 的相对关系）

### 不合格示例

```text
Dilation 增大扩大了感受野，因此大目标的分割效果更好。
```

> 问题：没有区分"感受野扩大"（事实）和"效果更好"（需要验证的假设），也没有说明 ERF 超过目标尺度后可能引入噪声的边界条件。

---

---

## Test 10：Baseline Evolution——Defect Diagnosis

### 输入

```text
用 Baseline Evolution 分析我的 DeepLabV3+（ResNet-50）在 LoveDA 上的 baseline：
mIoU ~48%，road 和 building 互相误分严重，B-IoU 比 mIoU 低 10 个点。
请帮我分析当前的瓶颈在哪，下一步应该怎么改进。
```

### 合格标准

- [ ] 必须使用缺陷分类（从 Defect Taxonomy 中识别匹配的缺陷类型）
- [ ] 必须给出每类缺陷的证据（不能只说"可能是边界问题"）
- [ ] 必须推荐候选模块并说明每个模块改变了什么变量
- [ ] 必须给出实验优先级（P0 > P1 > P2）
- [ ] 必须给出结果反馈规则（如果观察到 X，则说明 Y）

### 不合格示例

```text
你的 baseline 主要问题是边界质量不好和类别混淆。建议加一个 attention 模块和
boundary loss。应该在 decoder 里改。
```

> 问题：没有缺陷类型匹配、没有具体变量分析、没有实验优先级、没有反馈规则。

---

## Test 11：Baseline Evolution——Module Selection

### 输入

```text
我的 baseline 是 DeepLabV3+，在 LoveDA 上 road/building 混淆严重。
我找到两个候选方案：
A. 加 prototype learning（每个类学一个原型，用 feature 与原型距离分类）
B. 加 contrastive loss（在 decoder 输出上增加辅助 loss，拉大类间距离）
这两个方案解决的是同一个变量吗？哪个更值得先试？怎么验证？
```

### 合格标准

- [ ] 必须使用 Literature/Module Search Rule 分析两个方案改变了哪个变量
- [ ] 必须指出两个方案是否指向同一变量（feature space 类间距离）
- [ ] 必须给出选择依据（改动幅度、实现复杂度、可验证性）
- [ ] 必须给出最小验证实验，而不是"两个都试"

### 不合格示例

```text
两个方案都可以提升特征区分度。建议都试一下看哪个效果好。
```

> 问题：没有分析共享变量、没有选择逻辑、"都试一下"不是实验设计。

---

## Test 12：Baseline Evolution——Experiment Sequence Design

### 输入

```text
我计划对 DeepLabV3+ LoveDA baseline 做以下改进：
1. Decoder 替换为 MLP decoder（参考 SegFormer）
2. Boundary loss
3. 增加一个 non-local block

这三个改进的优先级应该怎么排？哪个最可能先出效果？怎么设计实验序列？
```

### 合格标准

- [ ] 必须分析每个改动的变量变化和代价
- [ ] 必须判断哪个改动和当前瓶颈最相关（不是随意排列）
- [ ] 必须设计 P0 > P1 > P2 实验序列
- [ ] 必须有反馈规则：如果某步无效，下一步怎么调整
- [ ] 必须有预期收益和失败信号的对应关系

### 不合格示例

```text
建议先加 non-local block，因为能捕获全局上下文，mIoU 应该能提升 1-2%。
然后加 MLP decoder 和 boundary loss。
```

> 问题：没有变量分析、没有设计 P0 验证瓶颈假设、没有反馈规则。


---

## Test 13：Literature/Module Search Evidence Record

### 输入

```text
我找到一个模块：Dual Attention Network（DANet），在 Cityscapes 上 SOTA。
它用 position attention + channel attention 并行融合。能不能用在
我的 DeepLabV3+ LoveDA baseline 上？
```

### 合格标准

- [ ] 必须按 Evidence Record 字段分析（公开代码、预训练权重、验证数据集）
- [ ] 必须指出 Cityscapes（驾驶场景）与 LoveDA（遥感）的数据分布差异
- [ ] 必须判断核心提升来自哪个变量（position attention 改变了什么？）
- [ ] 不能只因为 "SOTA" 就推荐加入

### 不合格示例

```text
DANet 在 Cityscapes 上效果很好，可以试试用在遥感上。
```

> 问题：没有 Evidence Record、没有考虑 domain gap、把 SOTA 当推荐理由。

---

## Test 14：Result Feedback——Module Retention Decision

### 输入

```text
我在 DeepLabV3+ 的 ASPP 后加了 non-local block，结果：
- mIoU 从 48.5% 升到 49.2%（+0.7%）
- 但 road IoU 从 72.3% 降到 70.1%（-2.2%）
- water IoU 从 21.5% 升到 25.8%（+4.3%）

我应该保留还是丢弃 non-local block？判断依据是什么？
```

### 合格标准

- [ ] 必须分析 mIoU 上升但类别间有升降的原因（不是简单看 mIoU）
- [ ] 必须给出保留/丢弃的判断规则（基于什么条件）
- [ ] 必须说明如果保留，需要怎么补偿下降的类
- [ ] 必须说明如果丢弃，是否尝试其他方案获得类似收益

### 不合格示例

```text
mIoU 提升 0.7%，应该保留 non-local block。
```

> 问题：只看 mIoU 汇总指标，没有分析类别间分配转移，没有补偿策略。


## 测试执行记录

| 测试编号 | 测试日期 | 结果 (PASS/FAIL) | 失败原因 | 修复动作 |
|----------|----------|-------------------|----------|----------|
| Test 1 | | | | |
| Test 2 | | | | |
| Test 3 | | | | |
| Test 4 | | | | |
| Test 5 | | | | |
| Test 6 | | | | |
| Test 7 | | | | |
| Test 8 | | | | |
| Test 9 | | | | |
| Test 10 | | | | |
| Test 11 | | | | |
| Test 12 | | | | |
| Test 13 | | | | |
| Test 14 | | | | |
