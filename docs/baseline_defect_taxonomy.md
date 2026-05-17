# Baseline Defect Taxonomy

Baseline 进化路线设计的起点是识别当前 baseline 的缺陷类型。
每个缺陷都对应一组可操作的变量开关和候选模块。

---

## 1. Boundary Quality Deficiency

**表现**：mIoU 尚可，但 B-IoU（boundary IoU）明显偏低（通常比 mIoU 低 5-10 个点以上）。
在类别边界处预测模糊、锯齿状、宽度不一致。

**相关变量**：
- 直接：decoder 梯度路径长度、上采样倍数、boundary loss weight
- 衍生：boundary pixel 的 gradient norm、low-level feature 利用率

**可查找模块**：
- Boundary loss / Contour-aware loss
- Decoder refinement module（DenseASPP, DMNet）
- Feature alignment module

**最小验证**：
- 计算当前模型的 B-IoU，确认 gap 大小
- 可视化 boundary 区域的 prediction confidence map
- 单纯增加 decoder 1-2 层后 B-IoU 是否改善

---

## 2. Spatial Detail Recovery Failure

**表现**：细长物体（road, fence, 电线杆等）断裂、稀疏小目标大量漏检。
下采样倍数越大，小目标特征在最后一层越弱。

**相关变量**：
- 直接：backbone 输出 stride、decoder 上采样倍数、skip connection 设计
- 衍生：小目标的 feature response magnitude、ERF 与目标尺度的比例

**可查找模块**：
- HRNet（高分辨率 backbone）
- Feature pyramid（FPN, PAN）
- Detail-enhanced decoder（UperNet）
- Multi-scale fusion（AFF, iAFF）

**最小验证**：
- 按尺度分桶统计 recall（<16px, 16-32px, 32-64px）
- 可视化 backbone 各层的小目标激活强度
- 对比 stride=8 vs stride=32 backbone 的小目标 mIoU

---

## 3. Class Confusion

**表现**：易混淆类别对（road↔building, barren↔agriculture）的 IoU 明显低于其他类。
Confusion matrix 显示这两类的互分错误占比高。

**相关变量**：
- 直接：feature space 中的类间距离 / 类内距离
- 衍生：分类器的线性可分性、confusion matrix 非对角线元素

**可查找模块**：
- Contrastive learning loss（SupCon, Triplet）
- Class-specific head
- Prototype learning
- Margin-based loss（AM-Softmax, CosFace）

**最小验证**：
- 计算混淆对在 feature space 中的 Fisher Discriminant Ratio
- 可视化最后一层 feature 的 T-SNE
- 在混淆对上单独计算 recall 和 precision

---

## 4. Optimization Instability

**表现**：训练 loss 震荡剧烈，val mIoU 波动大，不同 seed 的结果方差大。
少样本类别（water, forest）的 IoU 在不同 run 间差异显著。

**相关变量**：
- 直接：learning rate、batch size、BN 统计量稳定性
- 衍生：gradient norm 分布、loss landscape 平滑度、少样本类的 BN 参数漂移

**可查找模块**：
- GroupNorm + Weight Standardization
- Gradient clipping / gradient normalization
- Warmup schedule / cosine decay
- Lookahead optimizer / SAM
- EMA (Exponential Moving Average) teacher

**最小验证**：
- 统计少样本类别的 BN running_mean / running_var 的 batch 间方差
- 对比不同 seed 下少样本类别的 IoU 标准差
- Gradient norm histogram：查看是否有 exploding gradient

---

## 5. Pretrained Feature Damage

**表现**：模块加上后 mIoU 不升反降，或需要显著降低学习率才能微调。
新加模块收敛速度明显慢于 backbone。

**相关变量**：
- 直接：新增模块的梯度回传到 backbone 的距离和强度
- 衍生：backbone 参数与预训练权重的偏离程度（parameter shift）

**可查找模块**：
- 冻结 backbone 的 training strategy（freeze BN, differential lr）
- 增量式 integration（non-destructive insertion, residual addition）
- 适配器模块（Adapter-style tuning）

**最小验证**：
- 对比冻结 backbone vs 全部解冻的 mIoU
- 测量 backbone 参数的 L2 距离变化（相对于初始预训练权重）
- 在新增模块后的第一个 conv 处设置 gradient stop

---

## 6. Computation Redundancy

**表现**：Params / FLOPs 远高于同精度 baseline，或高分辨率输入下 OOM。
去除某个分支或减少通道后精度无明显下降。

**相关变量**：
- 直接：分支数、通道数、kernel size、dilation size
- 衍生：各分支输出的相关性、各通道的有效秩（effective rank）

**可查找模块**：
- Depthwise separable convolution
- Ghost module
- Pruning（结构化剪枝）
- 轻量上采样（CARAFE, DUpsampling）

**最小验证**：
- 逐一移除并行分支看 mIoU 下降量
- 计算各分支输出之间的 mutual information 或 correlation
- 计算 feature map 的 singular value 分布和 effective rank

---

## 7. Decoder Bottleneck

**表现**：增加 decoder 深度/复杂度后指标不提升，B-IoU 饱和；
或 low-level 特征引入后反而引入噪声。

**相关变量**：
- 直接：decoder 层数、通道数、上采样策略、融合方式
- 衍生：low-level 特征在 decoder 中的权重、噪声放大率

**可查找模块**：
- MLP decoder（SegFormer-style）
- Progressive upsampling decoder
- Attention-guided feature fusion
- 上采样方法替换：bilinear → CARAFE / PixelShuffle

**最小验证**：
- 固定 backbone 只替换 decoder 类型，对比 mIoU、B-IoU
- 可视化 decoder 各层输出的噪声比例
- 对比不同 decoder 深度的边际收益曲线

---

## 8. Loss Signal Insufficiency

**表现**：训练 loss 和 val loss 同步平坦，不再下降但 val mIoU 未达预期。
模型在 hard example（边界、小目标、遮挡）上普遍表现差。

**相关变量**：
- 直接：loss 函数结构（交叉熵、dice、focal 等）、loss weight
- 衍生：各类别的梯度信号强度、boundary 区域的 loss 贡献比例

**可查找模块**：
- Dice Loss / IoU Loss
- Focal Loss
- Boundary-aware Loss
- OHEM（Online Hard Example Mining）
- Auxiliary loss head

**最小验证**：
- 统计不同 loss 下各类别的 gradient norm 分布
- 在 hard example 上单独计算 loss 值
- 添加辅助 loss 看浅层 gradient norm 是否改善

---

## 9. Domain / Distribution Shift

**表现**：训练集和验证集来自不同区域/传感器时 mIoU 大幅下降。
同一模型在不同城市或不同时相的图像上表现差异大。

**相关变量**：
- 直接：源域和目标域的数据分布差异（颜色、纹理、视角、分辨率）
- 衍生：feature space 中的 domain gap、BN 统计量偏移

**可查找模块**：
- Domain adaptation（CORAL, DAN, MCD）
- Image-level augmentation（color jitter, grayscale, Gaussian blur）
- Style transfer / normalization
- Multi-source training strategy

**最小验证**：
- 统计源域和目标域在 feature space 的 distribution distance（MMD, CORAL distance）
- 对比图像级 augmentation 后的 mIoU 变化
- 分别评估模型在不同传感器来源数据上的 IoU

---

## 10. Large Region Consistency Failure

**表现**：大面积均匀区域（road 中央、building 屋顶、水体）出现预测孔洞或斑块噪声。
mIoU 中 homogeneous 区域的 IoU 低于预期。

**相关变量**：
- 直接：dilation 大小、ERF 覆盖范围、上采样策略
- 衍生：区域内像素的一致性正则强度、上下文建模范围

**可查找模块**：
- Non-local / Self-Attention
- Criss-cross attention
- Large kernel convolution
- CRF（条件随机场）后处理
- Consistency regularization

**最小验证**：
- 在 homogeneous 区域上单独计算 IoU 和 precision
- 可视化 homogeneous 区域的 prediction 波动图
- 增大 dilation 或加入 non-local 后 homogeneous 区域是否改善
