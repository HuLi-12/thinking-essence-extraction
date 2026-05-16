# 遥感分割领域分析样例库

本文件提供遥感图像分割场景下的本质变量抽取分析示例，覆盖 DeepLabV3+、ASPP、decoder、LoveDA 等常见场景。

---

## 示例 1：ASPP dilation 改小后部分类别提升但整体 mIoU 下降

**问题背景**：DeepLabV3+ 中将 ASPP branch 的 dilation 从 (6,12,18) 改为 (3,6,9)，
建物/道路等大尺度类别 mIoU 上升 0.5-1%，但整体 mIoU 下降 0.3-0.5%。

**【常见说法】**
大 dilation 对小目标有负作用，改小 dilation 能改善小目标，但会损失大目标的上下文。

**【问题】**
"上下文"是模糊概念。大 dilation 到底改变了什么变量？改小 dilation 为什么部分类别提升？
损失了哪类信息的上下文？

**【真正变化的变量】**
- 直接变量：dilation rate ↓ → effective receptive field (ERF) ↓
- 衍生变量：
  - 采样稀疏度 ↓（小 dilation 在同尺寸 feature map 上采样点更密）
  - ASPP 输出的局部纹理密度 ↑
  - 远距离空间依赖性 ↓
  - 对大目标的覆盖连续性 ↓（当 dilation > 目标尺寸时，采样点可能全部落在背景上）

**【本质一句话】**
ASPP dilation 改小的本质是调整 ERF 与目标尺度之间的对齐关系：
小 dilation 对密集小目标提升局部采样密度，但降低了大目标的远距离像素关联覆盖；
类别级 mIoU 变化的背后是各类目标尺度分布与 ERF 之间的匹配度转移。

**【机制链】**
dilation (6,12,18) → (3,6,9)
→ ERF 中心区域采样密度 ↑，外围覆盖范围 ↓
→ road/building 等大面积类别：改小后外围远距离采样点减少 → 覆盖连续性下降 → 边界一致性下降 → 大目标边界类 mIoU 可能下降
→ agriculture/barren：目标斑块较小 → 大 dilation 采样点大量落在无关区域（噪声）→ 改小后采样噪声 ↓ → 小目标 mIoU 上升
→ 整体 mIoU 取决于两类变化的净效应

**【代价交换】**
以远距离空间依赖（大目标全局一致性）换取局部采样密度（小目标识别精度）；
净效果取决于数据集中大目标和小目标的像素比例。

**【可验证】**
1. 按目标尺度分桶统计 mIoU（<32px / 32-128px / >128px）—— 确认 mIoU 转移方向。
2. 可视化 ASPP 各 branch 的有效感受野（使用 stimulation method）—— 验证 ERF 是否确实收缩。
3. 对 road/building 做 boundary IoU（B-IoU）—— 验证边界质量是否下降。
4. 消融：只改大 dilation（12→18）看哪类受益，与改小结果对称吗？

**【对当前模块的启发】**
1. 固定 dilation 集合对多变尺度分布的数据集（如 LoveDA）有天然缺陷。
2. 改进方向：可学习的 dilation / 自适应尺度选择，而非固定多 branch。
3. 如果计算预算允许，加入更大 dilation 的额外 branch（如 dilation=24）可能比替换更鲁棒。
4. 评价时不能只看 mIoU，必须报告尺度类别分组结果。

---

## 示例 2：DeepLabV3+ 的 decoder 到底贡献了什么

**【常见说法】**
Decoder 把 encoder 下采样丢失的空间细节恢复回来。

**【问题】**
"空间细节"具体指什么？是边界精度还是纹理信息？decoder 是通过什么机制恢复的？
用简单上采样和用复杂 decoder 的差异在哪个变量上体现？

**【真正变化的变量】**
- 直接变量：decoder 结构复杂度（层数、通道数、融合策略）
- 衍生变量：
  - low-level feature 与 high-level feature 的梯度通路长度
  - 各层级的 gradient norm 更新量分布
  - 特征图的空间分辨率 → 最终输出对齐像素所需的插值距离
  - 边界区域的 cross-entropy loss 值（边界像素是否被"放弃"）
  - 类别间置信度差距（边界模糊 vs 类别混淆）

**【本质一句话】**
DeepLabV3+ decoder 的本质是缩短 high-level feature 到像素级输出的梯度传递路径，
并建立可学习的 low-level → high-level 特征融合通路，
以此缓解 encoder 下采样对边界像素梯度信号的空间稀释。

**【机制链】**
Encoder 4×/8× 下采样
→ high-level feature 的定位信息退化为粗略网格
→ 对 boundary 像素，其监督信号需通过 8× 上采样回传 → 梯度被空间插值稀释
→ Decoder 引入 skip connection：在 4× 尺度融合 low-level feature
→ 保留边界梯度信号 → boundary 像素的梯度更新强度 ↑ → 边界 IoU ↑
→ 但若 low-level feature 本身含噪声（如原图渗漏），decoder 也会放大噪声 → 内部一致性可能下降

**【代价交换】**
以额外计算量（decoder conv + concat）和低层噪声放大为代价，换取边界梯度保留和定位精度；
decoder 越深，边界收益越快饱和，而噪声放大风险持续累积。

**【可验证】**
1. 对比有/无 decoder 的梯度回传强度（gradient norm at boundary pixels）—— 验证梯度保留假设。
2. 可视化 decoder 输出的 low-level 通路权重分布——模型是否真的在边界区域更依赖 low-level？
3. B-IoU 对比：with decoder vs without decoder vs simple upsampling。
4. 换不同的 decoder 深度（1 layer vs 3 layers vs MLP-like），看 B-IoU 的边际收益递减点。

**【对当前模块的启发】**
1. 简单的 1-2 层 decoder（如 DeepLabV3+ 原版）已经捕捉到大部分边界收益，加更深 decoder 收益有限。
2. 关键变量不是 decoder 有多复杂，而是 low-level feature 与 high-level feature 的对齐质量。
3. 如果 low-level feature 质量差（如输入噪声大或第一层 stride=4 太激进），decoder 反而有害。
4. 对于遥感场景（LoveDA 中边界类多），decoder 的价值比一般分割更大。

---

## 示例 3：LoveDA 上类别混淆的本质——为什么 road/building 和 barren 混淆

**【常见说法】**
类别外观相似，导致特征难以区分。

**【问题】**
"外观相似"是观察结果，不是机制解释。具体是哪个维度相似？颜色？纹理？形状？
模型在哪里把 road 预测成 building 了？什么变量决定了混淆程度？

**【真正变化的变量】**
- 直接变量：类别间的 feature space 距离（类间距离 / 类内距离 比值）
- 衍生变量：
  - 高分辨率特征层中 road/building 的纹理相似度（二者均为人造纹理，缺乏自然纹理）
  - 低分辨率特征层中二者位置邻近性（相邻像素大概率分属不同类别但共享上下文区域）
  - 上采样中的空间平滑效应（decoder 4× 上采样把相邻 road/building 像素的预测概率相互渗透）

**【本质一句话】**
Road/building 混淆的本质不是"外观相似"，而是在 feature space 中二者在纹理维度上高度重叠、
在语义维度上无法被感受野内的局部上下文有效分离，且 decoder 上采样的空间平滑效应进一步
模糊了它们的决策边界——这是一个**特征分辨力不足**与**空间自相关过强**的联合问题。

**【机制链】**
Road 与 building 共享人造纹理分布
→ 在 low-level feature 中二者激活模式高度相关
→ Encoder 下采样后空间分辨率下降，相邻 road/building 像素的比例变化特征丢失
→ ASPP 的 dilation 采样在同感受野内同时包含两类像素 → 输出 feature 的类间可分性下降
→ Decoder 4× 双线性上采样 + 卷积 → 相邻像素的 logit 互相平滑
→ 决策边界从锐利变为模糊 → 两类概率在边界处接近 0.5
→ 最终配置：boundary 区域大量错误预测

**【代价交换】**
以保持特征图分辨率（不进一步压缩混淆区域）来降低损失，但承受 FLOPs 上升、
训练不稳定等代价；另一个方向是以更复杂的 class-specific head 为代价换取类别解耦。

**【可验证】**
1. 计算 feature space 中 road/building/background 的 Fisher Discriminant Ratio 值。
2. 可视化 decoder 输出前最后一层 feature 的 T-SNE —— 看三类是否可分离。
3. 消融：在 boundary 区域加重采样（boundary-aware loss）—— 如果解释成立，B-IoU 应显著提升。
4. 如果混淆本质是"特征分辨力不足"，增加 ASPP 输出通道或使用更强的 decoder 应缓解而非消除混淆。

**【对当前模块的启发】**
1. 只用 DeepLabV3+ 的结构无法从根本上解决 road/building 混淆——因为它们在同一层次共享特征。
2. 可能的改进方向：分支网络（class-specific heads）、对比学习（拉大类间距离）、
   或增加一个 road/building 的二分类辅助头来强制 feature 分离。
3. 简单增加 ASPP 通道可能效果有限——瓶颈在 feature 分辨力，不是通道容量。

---

## 示例 4：在 LoveDA 上 backbone 从 ResNet-50 换成 ResNet-101 收益递减

**【常见说法】**
更深的网络有更强的表达能力，但 LoveDA 场景简单，不需要太深的 backbone。

**【问题】**
"场景简单"是什么意思？掉点具体发生在哪类图像上？ResNet-101 相对 ResNet-50 增加的层
在 LoveDA 上为什么没有带来预期收益？是优化失败还是数据量不足？

**【真正变化的变量】**
- 直接变量：网络深度（层数），参数量，FLOPs
- 衍生变量：
  - 有效感受野（ERF）—— 更深网络的 ERF 更大
  - 梯度回传路径长度 —— 深网络靠前层的梯度稳定性
  - 批量统计量稳定性 —— 深层网络在少样本类别上的 BN 参数估计偏差
  - 训练 loss 收敛速度 —— 深网络需要更多迭代才能拟合低频类别

**【本质一句话】**
ResNet-50 → ResNet-101 在 LoveDA 上的收益递减不是因为"场景简单"，
而是：增加的深度使 ERF 进一步增大，但 LoveDA 中小目标密集的区域 ERF 已经超出目标尺度，
继续增加 ERF 只带来额外噪声；同时，深层网络在少样本类别上的 BN 参数对 batch 波动更敏感。

**【机制链】**
ResNet：输出 stride = 32；ERF 随深度亚线性增长
→ LoveDA 大量 32-128px 小目标：ResNet-50 的 ERF 已覆盖目标及以上范围
→ ResNet-101 ERF 进一步增加 → 对 small target 来说感受野噪声区域 > 信号区域
→ Conv 权重更新以小目标信号为主？不，以图像中大尺度背景为主
→ 深层参数拟合 background bias → 小目标精度下降或不变
→ 同时，深层 BN 统计量（均值和方差）在低频类别的 batch 间漂移 → 训练不稳
→ 最终：小目标和低频类别无提升甚至下降 → mIoU 无改善

**【代价交换】**
以参数量翻倍、训练成本上升、小目标/低频类的梯度稀释为代价，
换取在大目标上极为有限的 ERF 扩展收益，在 LoveDA 场景下得不偿失。

**【可验证】**
1. 对比 ResNet-50 vs ResNet-101 在不同尺度桶上的 mIoU：确认收益只在大目标上出现。
2. 统计前向传播中 ERF 的实际大小（使用感受野评估方法）。
3. 监控低频类的 BN running_mean/running_var 的震荡程度。
4. 冻结 ResNet-101 的前 50 层（加载预训练不更新），只训练新增层——看是否缓解 BN 漂移。

**【对当前模块的启发】**
1. LoveDA 场景的"backbone 瓶颈"不在深度，而在 backbone 对小目标的 ERF 适配和 BN 稳定性。
2. 更有效的改进方向：用高分辨率 backbone（如 HRNet）、或设计尺度感知的特征增强。
3. 如果必须用 ResNet-101，建议 freeze BN 或使用 GroupNorm 替代 BN。
4. 参数量预算应该优先给 decoder/ASPP 而不是 backbone 深度。
