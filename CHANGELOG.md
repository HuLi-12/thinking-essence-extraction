# Changelog

## v1.4.0 (2026-05-17)

- 新增 Type F: Baseline Evolution 到 Problem Type Router
- 新增 Evolution Mode 到 Output Mode Rule
- 新增 Literature/Module Search Rule（按变量搜索而非抽象概念搜索）
- 新增 Baseline Evolution Workflow Template（P0/P1/P2 实验序列）
- 新增 `docs/baseline_defect_taxonomy.md`（10 类 baseline 缺陷类型）
- 新增 `docs/module_cards.md`（15 个模块卡片，标准化模板）
- 新增 `examples/baseline_evolution_examples.md`（2 个完整进化路线示例）
- 新增 Test 10-12 到 `evals/test_prompts.md` 和 `evals/checkpoints.json`
- 更新 `scripts/validate_skill_package.py`（新增 v1.4.0 文件清单和章节检查）

## v1.3.0 (2026-05-17)

- 解决 Core Output Requirements 与 Output Mode Rule 的冲突
- 新增 `version` 字段到 SKILL.md frontmatter
- 新增 `evals/checkpoints.json`（JSON 格式测试检查点）
- 新增 `scripts/sync_claude_skill.py`（根目录↔.claude 同步脚本）
- 新增 `.github/workflows/validate.yml`（CI 自动验证）
- 评分脚本支持 JSON checkpoint 解析和 `--soft` 模式
- 验证脚本增加 root↔.claude 内容一致性检查和版本号检查
- 新增 Variable Interaction Cards 2 组：Prototype Count↔Intra-class Variance, Boundary Loss↔Region Consistency
- 新增工程样例 2 个：秒杀链路、规则上下文
- 更新 README.md 和 CHANGELOG 结构描述

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
