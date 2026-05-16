# Changelog

## v1.3.0 (2026-05-17)

- 新增 Output Mode Rule（Compact/Full/Diagnosis/Innovation 四模式）
- 新增 Variable Interaction Cards（7 组变量交换关系）
- 新增 `CONTRIBUTING.md`（案例贡献规范）
- 新增 `check_response_against_checkpoints.py`（测试自动评分脚本）
- 扩展工程样例：ThreadLocal remove、Redis 随机 TTL、延迟双删一致性
- 修复 `.claude/skills/thinking-essence-extraction/SKILL.md` 副本缺失
- 验证脚本增加 .idea 文件检查和 Output Mode Rule 验证

- 新增 Problem Type Router（5 类问题路由）
- 新增 Evidence Level Rule（事实/推断/假设分层）
- 新增 Variable Table Rule（四类变量组织）
- 新增 Failure Diagnosis Template（实验失效诊断模板）
- 新增 Innovation Review Rule（5 维创新评价）
- 新增 `anti_patterns.md`（5 组错误→修正对照）
- 新增 `test_prompts.md`（9 个可执行测试）
- 新增 `variable_cards.md`（14 张变量卡片）
- 修正 ASPP 示例类别描述不一致
- 修正 Failure Diagnosis 示例中的时间硬编码
- 规范 Forbidden Phrases 措辞

## v1.1 (2026-05-16)

- 删除 `model.prompt` 嵌套，规则移至 Markdown 正文
- description 改为触发型描述
- 压缩 6 个子模型为"内部检查器"，禁止机械列出
- 反模式从表格改为自查清单
- 新增 `remote_sensing_segmentation_examples.md`

## v1.0 (2026-05-16)

- 初始 SKILL.md 创建
- 核心规则：变量表、机制链、代价交换、可验证实验
- 6 个子模型（First Principles, TOC, Scientific Method, Inversion, Pre-mortem, Red Team）
- 5 步分析流程
- 7 种反模式
