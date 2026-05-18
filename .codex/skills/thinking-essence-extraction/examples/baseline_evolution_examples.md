# Baseline Evolution 示例

---

## 示例 1：DeepLabV3+ ResNet-101 LoveDA baseline 进化

### Baseline Profile

```text
当前架构：DeepLabV3+（ResNet-101 backbone，ASPP (6,12,18)，简单 2-layer decoder）
当前 mIoU：~49.5%（LoveDA 验证集）
关键瓶颈：road/building 混淆（IoU ~55% vs ~80% 多数类），边界 B-IoU 低（~38%），细长结构断裂
```

### Defect Hypothesis

| 缺陷类型 | 证据 | 瓶颈变量 |
|---------|------|---------|
| Class Confusion (3) | road↔building 互相误分率 > 25% | feature space 类间距离不足 |
| Boundary Quality (1) | B-IoU 比 mIoU 低 ~11.5 个点 | decoder 梯度路径仍偏长 |
| Spatial Detail Recovery (2) | <32px 目标 recall < 50% | 下采样 4× 后小目标 feature 衰减严重 |
| Large Region Consistency (10) | road 中心区域预测出现空洞 | ERF 被 dilation 采样间隙切割 |

### Candidate Module Pool

#### Module 1: Prototype Learning（针对 Class Confusion）
- **修改变量**：feature space 中的类间距离
- **引入位置**：decoder 输出后、分类 head 前
- **代价**：参数量无关，FLOPs 增加 C×H×W 的相似度计算
- **最小验证**：在 road↔building 上单独计算 IoU，看混淆是否下降

#### Module 2: Boundary Loss（针对 Boundary Quality）
- **修改变量**：boundary 区域的 gradient norm
- **引入位置**：主 loss + 0.1 × boundary loss
- **代价**：无参数增加，需调优 α
- **最小验证**：B-IoU 是否从 ~38% 提升到 42%+

#### Module 3: Deformable Convolution（针对 Spatial Detail）
- **修改变量**：conv 采样位置的自适应性
- **引入位置**：backbone 最后一个 stage
- **代价**：参数量 +5-10%，FLOPs +50-100%
- **最小验证**：细长结构类（road, fence）的 IoU

### Experiment Priority

#### P0：验证 feature space 是否真的是瓶颈
```text
实验设计：
1. 训练一个简单分类器 probe：用当前 backbone 提取 feature → 训练 linear classifier 区分 road/building
2. 如果 probe 精度不高（<70%），说明 feature 本身已不可分 → 需要 contrastive learning
3. 如果 probe 精度高（>90%），说明 feature 可分但 decoder/classifier 未有效利用 → 瓶颈在 decoder

预期收益：明确了真正瓶颈位置，避免在错误方向上投入
资源成本：仅需冻结 backbone 提取 feature 训练 linear probe，不需要完整重新训练，适合 P0 快速验证
```

#### P1：确认 bottleneck 后执行对应改进
```text
场景 A：feature 不可分（probe < 70%）
  方案：增加 Prototype Loss（CE + 0.1 × contrastive loss）
  预期：road/building IoU 各提升 2-3%

场景 B：feature 可分但分类器没用好（probe > 90%）
  方案：替换 decoder 为 MLP decoder + Coordinate Attention
  预期：road/building 边界提升 1-2%
```

#### P2：边界质量与一致性增强
```text
实验设计：
1. 在 P1 基础上增加 boundary loss（α=0.1）
2. 将 decoder 的 3×3 conv 替换为 deformable conv

预期收益：
  场景 A+B 下：B-IoU 再提升 2-3%，整体 mIoU +1-2%
```

### Result Feedback Rule

```text
如果 P0 probe accuracy > 90%：
→ 说明 bottleneck 不是 feature 可分性
→ Class Confusion 问题转 decoder / classification head 改进
→ 跳过 Prototype Learning，直接进入 P1 场景 B

如果 boundary loss 后 B-IoU 提升但 mIoU 下降：
→ boundary loss weight α 偏大，内部一致性被破坏
→ 降低 α 至 0.05 或 0.01 重试

如果 deformable conv offset 可视化显示 offset ≈ 0：
→ 模型没有利用自适应采样能力
→ 检查 offset 网络初始化（用 0 初始化会抑制梯度）
```

---

## 示例 2：轻量级 baseline 快速提升

### Baseline Profile

```text
当前架构：DeepLabV3+（MobileNetV2 backbone, ASPP (6,12,18), simple decoder）
当前 mIoU：~45.2%（LoveDA 验证集）
关键瓶颈：整体容量不足，特别是少样本类（water mIoU ~25%，forest ~30%），边界质量差
```

### Defect Hypothesis

| 缺陷类型 | 证据 | 瓶颈变量 |
|---------|------|---------|
| Optimization Instability (4) | 不同 seed 下 water/forest IoU 波动 > 5% | BN 统计量在少样本类上不稳定 |
| Loss Signal Insufficiency (8) | 少样本类的 gradient norm 比多数类低 3-5 倍 | CE loss 偏向多样本类 |
| Computation Redundancy (6) | MobileNetV2 本身已轻量，但 ASPP 3 branch 占用了 40% 参数 | ASPP 分支有效利用率低 |

### Candidate Module Pool

#### Module 1: Dice Loss（针对 Loss Signal）
- **修改变量**：loss 从 CE 改为 CE + Dice
- **代价**：无参数增加

#### Module 2: GroupNorm（针对 Optimization Instability）
- **修改变量**：BN → GN
- **注意**：替换所有 BN 可能破坏预训练权重，建议先替换 decoder + ASPP 的 BN

#### Module 3: ASPP pruning（针对 Computation Redundancy）
- **修改变量**：3 branch → 2 branch（去掉 dilation=6）
- **依据**：dilation=6 与 dilation=3 的 ERF 重叠度高

### Experiment Priority

```text
P0（验证优化不稳定性假设）：
  实验：freeze backbone BN + 只训练 decoder/ASPP + Dice Loss
  预期：water/forest IoU 波动从 5% 降到 2%，均值提升 2-3%
  资源成本：仅需 freeze backbone BN + 调 loss 配置，不需要修改网络结构

P1（验证 ASPP 冗余假设）：
  实验：如果 P0 通过，移除 dilation=6 branch（控制总参数可比）
  预期：mIoU 不降甚至微升（因为少参数后同等 epoch 训练更充分）
  资源成本：需要完整训练 1 个实验，但分支删除后训练速度更快

P2（边界增强）：
  实验：P0 + P1 通过后，增加 boundary loss
  预期：B-IoU 提升 2-3%
```

### Result Feedback Rule

```text
如果 P0 无效（water/forest 无提升）：
→ 假设错误：瓶颈不是 BN 稳定性，也不是 loss 信号
→ 应该是模型容量不足——少样本类需要更多参数来建模
→ 转向增大 backbone 容量而非改进训练策略
```
