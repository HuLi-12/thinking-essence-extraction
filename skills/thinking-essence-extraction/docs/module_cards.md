# Module Cards

每个模块按统一模板描述：解决的缺陷、改变的变量、插入位置、代价、最小验证实验、失败信号。

---

## Estimation Warning

模块卡中的 Params / FLOPs / 显存代价为**经验估计，不是结构事实**。

正式实验前必须使用实际代码统计：

- params
- FLOPs / MACs
- activation memory
- training memory
- inference latency

不要把模块卡中的代价估算当成最终实验结论。实际代价取决于具体实现、输入尺寸、框架算子效率。

---

## 1. Deformable Convolution

**对应缺陷**：Spatial Detail Recovery Failure（细长结构断裂、不规则目标覆盖差）

**修改变量**：
- 直接：conv 采样位置从固定网格变为可学习 offset
- 衍生：有效感受野变为自适应形状（不再限定为矩形）、采样点密度分布变为可学习的空间分布

**引入位置**：backbone 最后 1-2 个 stage，或 decoder 的 3×3 conv

**代价估算**：
- 参数量增加：offset 网络（额外 3×3 conv，输出 2×N 个 offset），约 5-10% 参数增加
- FLOPs：offset 计算 + 非规则采样 ≈ 1.5-2× 普通卷积
- 显存：offset feature map 需要额外存储

**最小验证**：
- 在 baseline 上只替换 backbone 最后一个 stage 的 3×3 conv 为 deformable conv
- 对比细长结构类（road, fence）的 IoU 提升

**失败信号**：
- 如果 road IoU 不提升 → 说明当前 bottleneck 不在采样位置固定性
- 如果 offset 可视化显示 offset 幅度接近于 0 → 说明 model 没有学会自适应，需检查 offset 网络初始化

**参考论文**：Deformable Convolutional Networks (Dai et al., ICCV 2017), Deformable DETR (Zhu et al., ICLR 2021)

---

## 2. Boundary Loss / Contour-aware Loss

**对应缺陷**：Boundary Quality Deficiency（边界模糊、锯齿、B-IoU gap 大）

**修改变量**：
- 直接：loss 函数中增加 boundary 区域的惩罚项
- 衍生：boundary 像素的 gradient norm 上升、模型在边界区域的优化权重增加

**引入位置**：在主 loss 旁增加辅助 loss

**代价估算**：
- 参数量：无额外参数
- FLOPs：计算 boundary mask（通常用 Sobel 或 dilation 差集）≈ 可忽略
- 需要调优 boundary loss weight（建议初始 α=0.1）

**最小验证**：
- 对比有/无 boundary loss 的 B-IoU
- 可视化 boundary 区域的 confidence 变化

**失败信号**：
- 如果 B-IoU 不提升 → 模型 boundary 问题可能来自 feature 分辨率不足，而非 loss 信号不足
- 如果 mIoU 明显下降 → boundary loss weight 过大，内部区域一致性被破坏

---

## 3. Dice Loss / IoU Loss

**对应缺陷**：Class Confusion（混淆类对）、Loss Signal Insufficiency（少样本类梯度弱）

**修改变量**：
- 直接：loss 从 pixel-wise CE 改为 region-wise Dice（直接优化 IoU）
- 衍生：少样本类的 gradient norm 相对上升、大类的 gradient norm 相对下降

**引入位置**：替代或与交叉熵联合（CE + λ × Dice）

**代价估算**：
- 参数量：无
- FLOPs：少，需计算每类的 intersection/union
- 训练稳定性：Dice loss 在早期训练时梯度可能不稳定（预测接近 0 时）
- 需调优 λ（建议 λ=0.5 起步）

**最小验证**：
- 在混淆类对上比较 CE vs CE+Dice 的 IoU
- 监控少样本类的 gradient norm 变化

**失败信号**：
- 如果所有类同步下降 → Dice loss 权重过大抑制了 CE 的贡献
- 如果只是少样本类提升但多数类下降 → 固定 λ 调整不充分

---

## 4. Focal Loss

**对应缺陷**：Loss Signal Insufficiency（hard example 贡献弱）、Class Imbalance

**修改变量**：
- 直接：调整每个像素的 loss 权重，使 hard example（预测概率低）权重增大
- 衍生：easy example 的 loss 贡献被抑制（γ 控制的衰减）、gradient norm 分布向 hard example 偏移

**引入位置**：替代交叉熵 loss

**代价估算**：
- 参数量：无
- FLOPs：可忽略
- 需要调优 γ（建议 γ=2 起步）和 α（类别平衡权重）

**最小验证**：
- 统计 easy vs hard example 的 loss 贡献比例变化
- 对比边界像素和内部像素的 gradient norm 分布

**失败信号**：
- 如果只是整体 loss 下降但 mIoU 不变 → γ 过大，easy example 贡献不足
- 如果噪声区域被放大 → hard example 中包含大量标注噪声

---

## 5. Non-local / Self-Attention

**对应缺陷**：Large Region Consistency Failure（大面积均匀区域预测不一致）
Class Confusion（缺乏全局上下文约束）

**修改变量**：
- 直接：在 feature map 上计算所有位置间的 pairwise affinity
- 衍生：ERF 从局部扩展为全局（全图）、远距离同类像素的 feature 被拉近

**引入位置**：backbone 最后一层输出之后、ASPP 之前或替换 ASPP

**代价估算**：
- 参数量：1×1 reduce + non-local 本身 ≈ 少量参数
- FLOPs：H×W×H×W 的矩阵乘法是 O(N²) → 高分辨率输入下不可承受
- 改进版本只采样关键点（如 criss-cross、axial attention）

**最小验证**：
- 在 low-resolution feature（stride=16 或 32）上应用 non-local
- 对比 homogeneous 区域（road、building 屋顶）的 IoU

**失败信号**：
- 如果 mIoU 不提升 → 当前 baseline 的 ERF 已经覆盖主要目标尺度
- 如果小目标下降 → non-local 在全局自注意力中稀释了局部细节

---

## 6. Coordinate Attention

**对应缺陷**：Spatial Detail Recovery Failure（位置敏感目标的定位偏差）

**修改变量**：
- 直接：在 attention 中保留位置编码（坐标信息）
- 衍生：模型在 feature 变换过程中保留精确的空间位置感知

**引入位置**：backbone 各 stage 之后或 decoder 融合之前

**代价估算**：
- 参数量：少量（两个 1×1 conv + 两个 pooling）
- FLOPs：低（相比 non-local），仅对长宽方向做 pooling

**最小验证**：
- 对比有/无 coordinate attention 在位置敏感任务（道路拓扑、屋顶轮廓）上的 IoU

**失败信号**：
- 如果无提升 → 当前 backbone 的位置编码（positional implicit）已经足够
- 如果 baseline 已有 SE 模块 → Coordinate Attention 可能带来额外收益

**参考论文**：Coordinate Attention for Efficient Mobile Network Design (Hou et al., CVPR 2021)

---

## 7. GroupNorm + Weight Standardization

**对应缺陷**：Optimization Instability（BN 在少样本类上不稳定、小 batch 训练）

**修改变量**：
- 直接：归一化方式：BN（跨 batch 归一化）→ GN（跨通道分组归一化）
- 衍生：训练时不再依赖 batch 统计量 → 小 batch 和少样本类的训练稳定
- 推理时不需要 running_mean/running_var → 消除训练/推理不一致

**引入位置**：替换 backbone 和 decoder 中所有 BN 层

**代价估算**：
- 参数量：几乎相同（GN 无 learnable scale/bias 外的额外参数）
- FLOPs：GN 计算量略低于 BN（不需要跨样本统计）
- 训练时验证时行为一致，减少训练/推理 gap

**最小验证**：
- 替换最后 2 个 stage 的 BN 为 GN
- 对比 water, forest 等少样本类的 IoU 稳定性和均值

**失败信号**：
- 如果所有类同步下降 → backbone 预训练权重依赖 BN 统计量，替换后破坏了预训练特征分布
- 解决方案：渐进替换（先替换 decoder，再替换深层 stage）

---

## 8. Feature Pyramid Network (FPN) / Multi-scale Fusion

**对应缺陷**：Spatial Detail Recovery Failure（多尺度目标同时存在时顾此失彼）

**修改变量**：
- 直接：多尺度 feature（P2-P5）被融合到同一表示中
- 衍生：小目标的高分辨率特征保留完整梯度路径、大目标的语义特征参与决策

**引入位置**：backbone 后、预测 head 前

**代价估算**：
- 参数量：1×1 conv + top-down 通路，约 backbone 参数的 10-20%
- FLOPs：取决于融合的特征层数

**最小验证**：
- 对比 baseline（单层 feature 直接上采样）vs FPN 的多尺度尺度 mIoU
- 分别统计 <16px, 16-64px, >64px 的收益

**失败信号**：
- 如果小目标不提升 → 说明不是多尺度问题，而是小目标本身的 feature response 不足
- 如果大目标下降 → FPN 的高分辨率分支引入了噪声

---

## 9. Online Hard Example Mining (OHEM)

**对应缺陷**：Loss Signal Insufficiency（简单像素主导梯度，hard example 欠训练）

**修改变量**：
- 直接：只对 loss 最高的前 k% 像素回传梯度（而非全部像素）
- 衍生：hard pixel 的梯度贡献占比上升、easy pixel 的梯度被截断

**引入位置**：在 loss 计算后、反向传播前

**代价估算**：
- 参数量：无
- FLOPs：需排序 loss（O(NlogN)），高分辨率下可能略慢
- 显存：全部像素的 loss 仍需要前向计算

**最小验证**：
- 对比有/无 OHEM 在边界像素和内部像素上的 gradient norm 分布
- 分别在 easy/hard pixel subset 上计算 IoU

**失败信号**：
- 如果整体 mIoU 下降 → k 太小，丢失了大量正常梯度信号
- 如果只是边界提升但内部一致性下降 → OHEM 让模型过度关注边界噪声

---

## 10. Knowledge Distillation

**对应缺陷**：Optimization Instability（小模型容量不足）、Class Confusion

**修改变量**：
- 直接：额外 loss 使 student 输出分布接近 teacher
- 衍生：student 模型学到 teacher 软化的类别关系（如 road↔building 的相似度结构）

**引入位置**：训练时增加蒸馏 loss

**代价估算**：
- 参数量：需要额外 teacher 模型的前向计算
- FLOPs：训练成本约翻倍，推理成本不变
- 需要预训练 teacher 模型

**最小验证**：
- 用小 backbone（如 ResNet-18）作为 student，用大模型（ResNet-101）作为 teacher
- 对比 student 直接训练 vs KD 训练的 mIoU

**失败信号**：
- 如果 KD 无效 → teacher 的软化输出中类别关系不可迁移（teacher 本身过拟合）
- 如果 student 反而不如直接训练 → temperature 参数或 loss weight 不匹配

---

## 11. Data Augmentation (CutMix / MixUp / RandAug)

**对应缺陷**：Optimization Instability（数据量不足、过拟合）
Domain/Distribution Shift（泛化性差）

**修改变量**：
- 直接：训练样本从"原图"变为"多种变换后的图像"
- 衍生：有效数据分布变广、各数据点之间的独立性下降（正则化效应）

**引入位置**：数据加载阶段

**代价估算**：
- 参数量：无
- FLOPs：无（训练时预处理阶段）
- 训练速度：可能在数据加载阶段变慢（取决于 augmentation 复杂度）

**最小验证**：
- 对比 baseline vs +CutMix 的 val mIoU 和 train/val loss gap
- 分别对比少样本类的 IoU

**失败信号**：
- 如果训练 loss 不下降 → augmentation 过于激进，破坏了图像结构
- 如果 val 不提升但 train loss 更高 → augmentation 强度适当，但模型容量不足

---

## 12. Class-balanced Sampling / Weighted Sampling

**对应缺陷**：Optimization Instability（类别严重不平衡——水、森林样本量远少于 road、building）

**修改变量**：
- 直接：每个 epoch 中各类样本出现的频率（从自然分布 → 均匀分布或平方根分布）
- 衍生：少样本类的训练步数增加、多样本类的训练步数减少

**引入位置**：DataLoader 的采样器

**代价估算**：
- 参数量：无
- FLOPs：无
- 训练时间：少样本类图像被反复采样 → 可能过拟合；多样本类欠采样 → 信息丢失

**最小验证**：
- 对比自然采样 vs 平方根采样的各类 IoU 和 overall mIoU
- 监控少样本类的训练的 IoU 曲线是否波动减小

**失败信号**：
- 如果多样本类（road, building）大幅下降 → 欠采样导致信息丢失
- 如果少样本类过拟合 → 采样倍数过高，需要正则化

---

## 13. Large Kernel Convolution

**对应缺陷**：Large Region Consistency Failure（需要大范围上下文但 dilation 有 grid effect）
Decoder Bottleneck（decoder 中小卷积无法有效跨大区域融合）

**修改变量**：
- 直接：kernel size 从 3×3 扩大到 7×7 / 15×15 / 31×31
- 衍生：ERF 在单层内大幅扩展（不需要堆叠多层或使用 dilation）、参数量按 K² 增长

**引入位置**：ASPP 中原 3×3 conv 的替换、或 backbone 最后一个 stage

**代价估算**：
- 参数量：7×7 ≈ 49×C² vs 3×3 ≈ 9×C² → 约 5.4 倍
- FLOPs：同等倍数增长
- 可通过 depthwise large kernel 减轻（ConvNeXt, RepLKNet）

**最小验证**：
- 在 ASPP 中把 3×3 conv 替换为 7×7 depthwise conv（控制参数量）
- 对比 homogeneous 区域（road 中心、水体）的 IoU

**失败信号**：
- 如果小目标下降 → 大 kernel 过度平滑了细节
- 如果参数量增加但 mIoU 不升 → 当前 bottleneck 不是感受野范围

---

## 14. Adaptive / Learnable Dilation

**对应缺陷**：Class Confusion（不同类别需要不同的最优 dilation）
Large Region Consistency Failure（固定 dilation 无法同时覆盖全部尺度）

**修改变量**：
- 直接：dilation 从固定超参变为可学习的参数（或由输入动态预测）
- 衍生：各空间位置的 ERF 大小自适应变化、采样模式不再是全局统一

**引入位置**：替换 ASPP 中固定 dilation 的并行分支

**代价估算**：
- 参数量：中等（额外的小网络预测 dilation 或 offset）
- FLOPs：中等（取决于预测网络的复杂度）
- 训练稳定性：可学习的 dilation 初期可能不稳定

**最小验证**：
- 固定 dilation ASPP vs 可学习 dilation ASPP（控制总参数量）
- 分别统计小目标和大目标的 IoU 变化——是否按预期自适应调整

**失败信号**：
- 如果可学习 dilation 收敛到固定值 → 动态 dilation 对当前任务无必要
- 如果训练震荡 → 需要对 dilation 的梯度做 normalization 或 clamp

---

## 15. Prototype Learning / Contrastive Segmentation

**对应缺陷**：Class Confusion（类间 feature 距离不足）

**修改变量**：
- 直接：对每个类别维护一个可学习的 prototype（嵌入空间的聚类中心）
- 衍生：训练时将同类的像素 feature 拉向同类 prototype、推离异类 prototype
- 测试时用像素 feature 与各类 prototype 的距离作为分类依据

**引入位置**：在 decoder 输出 feature 后、分类 head 前

**代价估算**：
- 参数量：每个原型是一个 D 维向量，C 类 × D 维 ≈ 可忽略
- FLOPs：计算像素 feature 与各原型的相似度（C × H × W）
- 训练需要 contrastive loss，调优 temperature 和 margin

**最小验证**：
- 在易混淆类对（road↔building）上对比 CE baseline vs Prototype + CE
- 计算 feature space 的类间距离变化

**失败信号**：
- 如果混淆类不改善 → 当前 feature space 的 class boundary 本身已高度非线性
- 如果整体下降 → prototype 初始化或 temperature 不匹配
