# Variable Cards

常用技术变量的定义、影响和常见误区。
用于快速定位分析中涉及的变量，避免概念混淆。

---

## H / W

**定义**：feature map 的空间高度和宽度。

**谁直接改变它**：stride > 1 的卷积或 pooling、downsampling layer、input resolution。

**影响链**：
- `H×W` 是 FLOPs 和 activation memory 的乘数因子
- H/W 减半 → FLOPs 和 activation memory 约降为 1/4（对 channel-wise 操作）
- H/W 减半 → 空间细节丢失 → boundary 定位精度下降
- H/W 减半 → 有效感受野的相对覆盖比例增大

**常见误区**：
- 认为 H/W 下降 "减少参数量" → 实际上卷积参数量是 `C_out × C_in × K_h × K_w`，与 H/W 无关；减少的是 FLOPs 和 activation memory
- 认为 H/W 下降一定会损失信息 → 取决于下采样方式（stride conv 可学习，max pooling 不可学习）

---

## C（通道数）

**定义**：feature map 的通道维度。

**谁直接改变它**：卷积的输出通道数、全连接层维度、通道重排操作。

**影响链**：
- `C` 增大 → 后续卷积参数量按 `C_out × C_in` 增加（二次增长）
- `C` 增大 → channel basis 数量增加 → 理论特征组合容量 ↑
- `C` 增大 → activation memory 线性增加
- `C` 增大 → 每个空间位置的信息密度上升 → 但可能引入冗余

**常见误区**：
- "C 增加 = 语义增强" → C 只是通道基数增加，不保证学到的基向量更有语义
- "C 越大越好" → 过大的 C 在数据不足时导致过拟合，且 C 增大受 activation memory 约束
- 混淆参数量和 FLOPs：C 翻倍使下一层参数量翻倍（权重增加），FLOPs 翻倍（计算增加），但本层 activation memory 只增加输出部分

---

## Params（参数量）

**定义**：模型中可训练参数的总数。

**计算公式**（卷积层）：
- `Params = C_out × (C_in × K_h × K_w + 1)`（含 bias）
- 全连接层：`Params = input_dim × output_dim + output_dim`

**谁影响它**：
- 卷积层参数量主要由 C 决定（`C_out × C_in × K_h × K_w`），K 和 C 各贡献二次增长
- kernel size 7×7 的一层 ≈ 49×(C_in×C_out) 参数，3×3 一层 ≈ 9×(C_in×C_out)
- 对参数更敏感的是 C（二次影响），而不是 K 或 H/W

**常见误区**：
- "参数量增加 = 过拟合风险高" → 需要结合数据量和正则化强度判断
- "参数量不变则公平对比" → 参数量一致但结构不同，ERF、梯度路径、激活分布可能完全不同
- 认为参数量是计算开销的唯一指标 → activation memory、FLOPs、memory bandwidth 可能更关键

---

## FLOPs（浮点运算数）

**定义**：模型前向传播所需的浮点运算次数，衡量计算负载。

**计算公式**（卷积层）：
- `FLOPs = 2 × C_out × C_in × K_h × K_w × H × W`
- 约等于 `Params × 2 × H × W`（近似）

**谁影响它**：
- H/W 是线性乘数：H/W 翻倍 → FLOPs 翻倍
- C 是二次影响：输入和输出 C 同时翻倍 → FLOPs 变 4 倍
- K 是二次影响：K_h/K_w 翻倍 → FLOPs 变 4 倍

**常见误区**：
- "FLOPs 是推理速度的代理指标" → 实际推理速度取决于 memory bandwidth、算子实现、硬件特性
- 混淆 FLOPs 与参数量：大 kernel 小 C（如 7×7, 64 dims）≈ 小 kernel 大 C（如 3×3, 256 dims）在 FLOPs 上可能相当，但参数量和 ERF 完全不同

---

## Activation Memory（激活内存）

**定义**：前向传播中存储所有中间 feature map 所需的内存（训练时需保留至反向传播）。

**计算公式**（单层）：
- `Activation Memory ≈ Σ(B × C × H × W × dtype_size)` 对所有中间 feature map
- 训练时需保留所有中间激活用于反向传播，因此是 **层数 × 每层尺寸**

**谁影响它**：
- H/W 是二次影响（空间维度减少使后续所有层的 H/W 均等比减小）
- 下采样层是 activation memory 的关键下降点
- batch size 是线性乘数

**常见误区**：
- "参数量最大的层最吃内存" → 实际上 activation memory 通常由 feature map 尺寸最大的层（即网络浅层）决定
- 下采样增加通道时，activation memory 不一定增加（H/W 降幅可能抵消 C 增幅）

---

## ERF（有效感受野）

**定义**：输入空间中每个输出像素实际依赖的区域大小，呈高斯分布（中心像素贡献最大，边缘衰减）。

**理论公式**：
- 理论 RF = `1 + Σ(K_i - 1) × Π(dilation_j)`（对前 i 层）
- 但有效 RF（高斯覆盖区域）≈ `O(√L)`（L 为层数），远小于理论 RF

**谁影响它**：
- dilation 率：直接扩大采样间隔
- depth：深层网络的 ERF 更大，但呈亚线性增长
- skip connection：在 ResNet 中，ERF 增长比 plain net 更慢（因梯度路径更短，浅层贡献保留）

**常见误区**：
- "理论 RF = 有效 RF" → 实际有效 RF 约为理论 RF 的 1/3 到 1/2
- "dilation 翻倍则 ERF 翻倍" → 只在单层上成立，多层累积后 ERF 增长受网络架构限制
- 认为 ERF 越大越好 → ERF 超过目标尺寸后增加噪声

---

## Dilation（空洞率）

**定义**：卷积采样点之间的间隔。dilation=1 为标准卷积，dilation=2 为隔一个像素采样。

**对变量的影响**：
- 保持参数量不变（kernel 权重数量不变）但扩大采样范围
- 不改变 FLOPs（采样点数相同）但改变采样位置
- 改变 ERF：dilation 翻倍使单层 RF 扩大约 2×(K-1)

**采样模式**：
- 大 dilation → 采样稀疏 → 覆盖范围大但局部密度低
- 小 dilation → 采样密集 → 局部细节好但覆盖范围小
- 过大 dilation → 采样点产生"grid effect"（棋盘状间隙）

**常见误区**：
- "dilation 越大语义越强" → dilation 只是采样间隔改变，不直接增强语义
- 忽略 dilation 对边界区域的采样的影响：大 dilation 在边界处采样点可能全部落在另一类区域

---

## Sampling Density（采样密度）

**定义**：在 feature map 的某个局部区域内，卷积核实际采样点的空间密集程度。

**与 dilation 的关系**：
- dilation = 1：K×K 区域内全部采样（100% 密度）
- dilation = 2：K×K 区域内隔点采样（约 25% 局部密度，取决于 K）
- dilation 越大 → 采样点越稀疏 → 等效于在每个局部区域使用更少的像素信息

**重要性**：
- 解释 ASPP 中大小 dilation 对目标尺度影响的核心变量
- 大 dilation 低采样密度 = 对细节不敏感，但对大范围模式有鲁棒性
- 小 dilation 高采样密度 = 保留局部纹理和边界的精确定位

**常见误区**：
- 混淆 sampling density 与 ERF：sampling density 关注的是"有多少点在一个局部"，ERF 关注的是"覆盖了多大范围"
- 认为 dilation 增大只影响感受野而不影响信息密度

---

## Gradient Path（梯度路径）

**定义**：损失函数的梯度从输出层传播到指定层所需经过的计算路径。

**路径构成**：
- 路径长度 = 经过的层数
- 路径中的非线性激活（ReLU 会截断负梯度）
- 路径中的乘法操作（注意力权重可能抑制某些路径）
- skip connection 创建"梯度高速公路"

**对训练的影响**：
- 长路径 → 梯度衰减或爆炸（vanishing/exploding gradient）
- skip connection → 输出层的梯度可直接到达浅层
- 辅助损失 → 为浅层提供独立于主路径的梯度源

**常见误区**：
- "ResNet 解决了梯度消失" → 缓解了深层网络的梯度衰减，但没有完全消除
- 只关注梯度大小不关注方向 → 梯度方向冲突（gradient conflict）对多任务学习的影响可能比梯度大小更关键

---

## Boundary IoU（B-IoU）

**定义**：仅计算目标边界区域（通常取距离真实边界 δ 像素范围内的区域）的 IoU。

**计算公式**：
- `B-IoU = |G_δ ∩ P_δ| / |G_δ ∪ P_δ|`
- 其中 G_δ 和 P_δ 分别是真实和预测边界距离 δ 内的像素集合

**谁影响它**：
- decoder 结构（能否保留边界梯度）
- dilation 大小（大 dilation 可能导致边界采样点落在类外）
- loss 函数是否显式关注边界（如 boundary loss、Contour-aware loss）

**常见误区**：
- "mIoU 高则 B-IoU 也高" → 大目标在 mIoU 中占比高但对 B-IoU 不敏感
- B-IoU 比 mIoU 对 decoder 设计和 dilation 选择更敏感，通常是 decoder 改进的主要指标

---

## Class-wise IoU（类别级 IoU）

**定义**：每个语义类别单独计算的 IoU，反映模型在不同类别上的性能分布。

**分析价值**：
- 发现混淆对（road↔building、barren↔agriculture）
- 识别尺度偏好（大目标类 vs 小目标类的 IoU 差距）
- 定位改进的真实效果（全局 mIoU 上升但可能只是某一类的大幅提升掩盖了其他类的下降）

**常见误区**：
- "mIoU 上升 = 所有类都提升" → mIoU 是均值，单一类的大幅提升可掩盖其他类的下降
- 不结合 confusion matrix 看 class-wise IoU → 无法区分是"该类变强了"还是"该类被更大类吞并了"

---

## Feature Separability（特征可分性）

**定义**：不同类别在 feature space 中的可区分程度。

**常用度量**：
- Fisher Discriminant Ratio：`(μ₁ - μ₂)² / (σ₁² + σ₂²)`，类间距离 / 类内距离
- T-SNE / UMAP 可视化
- linear separability（用线性分类器在 feature 上做分类的准确率）

**谁影响它**：
- 损失函数（交叉熵鼓励可分性，contrastive loss 直接最大化类间距离）
- 特征维度（高维空间更容易线性可分离）
- 底层特征可分性通常低于高层（因为底层保留更多低级纹理）

**常见误区**：
- "类间距离越大越好" → 过大的类间距离可能意味着特征空间扭曲，损害泛化
- 只关注类间距离不关注类内方差 → 类内方差大的类别在高维空间中可能和相邻类重叠

---

## BN Stability（Batch Normalization 稳定性）

**定义**：BN 层的 running_mean / running_var 在训练和推理之间的行为稳定性。

**影响因素**：
- batch size：小 batch 下 BN 统计量波动大
- 类别分布不均衡：少样本类别出现在 batch 中的频率低 → BN 统计量偏向多数据类
- 冻结 backbone：fine-tuning 时冻结 BN 可避免预训练特征分布被少样本类别扰动

**典型问题**：
- 少样本类别（water、forest 等低频类）对应的激活分布不稳定 → BN 参数波动 → 推理时出现错误缩放
- 解决方式：GroupNorm 替代 BN，或 freeze BN + 只训练卷积层

**常见误区**：
- "BN 只是加速收敛" → BN 在少样本场景下可能损害性能
- 认为 BN 参数是微调中"无害的" → 预训练 BN 统计量在被少量新数据更新后可能偏离原始分布

---

## Pretrained Weight Preservation（预训练权重保持）

**定义**：在迁移学习或 fine-tuning 过程中，预训练权重被保留的有效程度。

**损伤因素**：
- 新增随机初始化的参数 → 这些参数输出随机值 → 反向传播时产生梯度 → 相邻层预训练权重参数被扰动
- 学习率过高 → 预训练权重被大幅度更新 → 失去预训练的特征提取能力
- 数据分布偏移 → 预训练特征不再适用 → 需要更新权重但又有遗忘风险

**典型问题**：
- 在 ASPP 后新增 branch → 新 branch 的随机初始化梯度回传到 backbone → backbone 预训练权重偏离
- 固定 backbone + 只训练 decoder 可避免此类问题，但限制了下游任务的适应能力

**常见误区**：
- "用预训练权重初始化就一定比随机初始化好" → 如果下游数据分布与预训练数据差异过大，预训练权重可能成为负迁移
- 认为 fine-tuning 只影响顶层权重 → 反向传播中浅层权重也会被更新（虽然更新量小于顶层）
