# 成果输出验证流程 v1.0

> 创建：2026-03-31 | 触发：SAYELF 指令  
> 原则：真实数据 > 审核流程 > 输出成果  
> 状态：✅ 激活（Tier 1 强制）

---

## 🎯 目标

确保所有输出成果基于真实数据，杜绝造假、梦游、幻想。

---

## 📋 流程总览

```
┌─────────────────────────────────────────────────────────────┐
│                    成果输出验证 Pipeline                      │
└─────────────────────────────────────────────────────────────┘

[1] 数据采集 → [2] 来源标注 → [3] 交叉验证 → [4] Bot 初审 
                                            ↓
[8] 重新采集 ← 不通过 ← [7] 太一终审 ← [5] 主管复审 ← [4]
       ↓
    通过
       ↓
[9] 成果输出 → [10] 归档记录
```

---

## 🔧 详细步骤

### 步骤 1：数据采集（Data Collection）

**执行者**: 罔两 Bot / 素问 Bot / 山木 Bot（按任务类型）

**采集方式**:

| 类型 | 方法 | 工具 | 输出格式 |
|------|------|------|---------|
| 爬虫抓取 | HTTP 请求 + HTML 解析 | requests + BeautifulSoup | JSON + 原始 HTML |
| 网页浏览 | 人工/自动浏览 | web_fetch / canvas | Markdown + URL |
| 截图引用 | 屏幕截图 + OCR | canvas.snapshot + pytesseract | 图片 + 提取文本 |
| API 调用 | REST API | requests | JSON + 响应头 |
| 用户提供 | 直接接收 | message | 原始内容 + 用户 ID |

**强制要求**:
```python
# 每条数据必须包含的元数据
{
    "data": "...",           # 数据内容
    "source": "...",         # 来源（URL/API 名称/用户 ID）
    "timestamp": 1234567890, # 采集时间戳（Unix 时间戳）
    "method": "...",         # 采集方法（crawler/browser/screenshot/api/user）
    "collector": "...",      # 采集者（Bot 名称）
    "raw_backup": "..."      # 原始数据备份路径
}
```

**验收标准**:
- ✅ 元数据完整（5 项必填）
- ✅ 原始数据已备份
- ✅ 时间戳在 24 小时内（实时数据）或注明历史数据

---

### 步骤 2：来源标注（Source Annotation）

**执行者**: 采集 Bot（自动）

**标注规则**:

| 来源类型 | 标注格式 | 示例 |
|---------|---------|------|
| 网页爬虫 | `URL + 抓取时间` | `https://polymarket.com/event/... @ 2026-03-31 09:00` |
| API 调用 | `API 名称 + 调用时间 + 参数` | `Polymarket API @ 2026-03-31 09:00 {event_id: xxx}` |
| 截图 | `截图时间 + 来源页面` | `Screenshot @ 2026-03-31 09:00 from polymarket.com` |
| 用户输入 | `用户 ID + 输入时间` | `user:o9cq80... @ 2026-03-31 09:00` |
| 推算数据 | `计算逻辑 + 假设条件 + 原始数据` | `Derived: A * B, assuming C, source: [1]` |

**输出文件**:
```
/workspace/data/annotated/{task_id}_{timestamp}.json
```

**验收标准**:
- ✅ 每条数据有明确来源
- ✅ 来源可追溯（URL 可访问 / API 可复现）
- ✅ 推算数据有完整计算链

---

### 步骤 3：交叉验证（Cross-Validation）

**执行者**: 采集 Bot（自动） + 罔两 Bot（监督）

**验证规则**:

| 数据类型 | 验证方法 | 通过标准 |
|---------|---------|---------|
| 金融数据 | 双源对比（2 个独立 API） | 差异 < 1% |
| 气象数据 | 三源对比（3 个气象站） | 2/3 一致 |
| 网页内容 | 二次抓取（间隔 5 分钟） | 内容一致 |
| 截图信息 | OCR + 人工核对 | 关键信息匹配 |
| 用户输入 | 上下文一致性检查 | 无矛盾 |

**验证报告格式**:
```json
{
    "task_id": "...",
    "validation_result": "PASS | FAIL",
    "sources_checked": 2,
    "consistency_score": 0.98,
    "discrepancies": [],
    "validator": "wangliang-bot",
    "timestamp": 1234567890
}
```

**验收标准**:
- ✅ 一致性分数 ≥ 0.95（关键数据 ≥ 0.99）
- ✅ 无未解释的差异
- ✅ 验证报告已生成

---

### 步骤 4：Bot 初审（Bot Preliminary Review）

**执行者**: 负责 Bot（采集者）

**自检清单**:

```markdown
## Bot 初审清单

- [ ] 数据来源已标注（步骤 2）
- [ ] 交叉验证通过（步骤 3）
- [ ] 原始数据已备份
- [ ] 无编造/推测/美化数据
- [ ] 时间戳在有效期内
- [ ] 异常值已标记
- [ ] 验证报告已生成

## 自检结论
- [ ] ✅ 通过，提交主管审核
- [ ] ❌ 不通过，返回步骤 1 重新采集
```

**输出文件**:
```
/workspace/reviews/bot_preliminary/{task_id}_{timestamp}.md
```

**验收标准**:
- ✅ 自检清单 100% 完成
- ✅ 自检结论为"通过"

---

### 步骤 5：主管复审（Supervisor Review）

**执行者**: 守藏吏 Bot（资源调度主管）

**审核内容**:

1. **完整性检查**:
   - 数据采集流程是否完整（步骤 1-4）
   - 所有必需文件是否存在
   - 元数据是否完整

2. **一致性检查**:
   - 数据来源与标注是否一致
   - 验证报告与数据是否一致
   - 自检结论与实际是否一致

3. **合规性检查**:
   - 是否符合 TRUTH-DATA.md（数据真实法则）
   - 是否符合 NEGENTROPY.md（负熵法则）
   - 是否符合 VALUE-FOUNDATION.md（价值基石）

**审核报告格式**:
```markdown
## 主管复审报告

**任务 ID**: ...
**负责 Bot**: ...
**审核时间**: ...

### 检查结果
| 项目 | 状态 | 备注 |
|------|------|------|
| 完整性 | ✅/❌ | ... |
| 一致性 | ✅/❌ | ... |
| 合规性 | ✅/❌ | ... |

### 审核结论
- [ ] ✅ 通过，提交太一终审
- [ ] ❌ 不通过，退回原因：...
```

**输出文件**:
```
/workspace/reviews/supervisor_review/{task_id}_{timestamp}.md
```

**验收标准**:
- ✅ 三项检查全部通过
- ✅ 审核报告已生成

---

### 步骤 6：太一终审（Taiyi Final Approval）

**执行者**: 太一 Bot（AGI 执行总管）

**终审内容**:

1. **真实性确认**:
   - 数据来源可追溯
   - 交叉验证可靠
   - 无造假嫌疑

2. **价值确认**:
   - 输出是否创造价值（VALUE-FOUNDATION）
   - 是否增加系统秩序（NEGENTROPY）
   - 是否符合观察者协议（OBSERVER）

3. **风险评估**:
   - 数据错误的影响范围
   - 是否需要 SAYELF 手动确认
   - 是否有合规风险

**终审决策**:

| 决策 | 条件 | 后续动作 |
|------|------|---------|
| ✅ 批准 | 全部检查通过 + 低风险 | 进入步骤 7 输出 |
| ⚠️ 条件批准 | 全部检查通过 + 中风险 | SAYELF 确认后输出 |
| ❌ 驳回 | 任一检查不通过 | 返回步骤 1 重新采集 |

**输出文件**:
```
/workspace/reviews/taiyi_final/{task_id}_{timestamp}.md
```

**验收标准**:
- ✅ 终审决策明确
- ✅ 决策理由清晰

---

### 步骤 7：成果输出（Output Generation）

**执行者**: 负责 Bot（采集者）

**输出前检查**:

```python
# 输出前必须满足的条件
conditions = [
    taiyi_approval == "APPROVED",
    supervisor_approval == "APPROVED",
    bot_self_check == "PASS",
    cross_validation_score >= 0.95,
    source_annotation_complete == True,
    raw_backup_exists == True
]

if all(conditions):
    generate_output()
else:
    raise Exception("输出条件不满足，禁止输出")
```

**输出格式**:
- 数据来源标注（必须）
- 验证报告摘要（必须）
- 审核链记录（必须）
- 时间戳（必须）

**输出文件**:
```
/workspace/output/{task_id}_{timestamp}.{format}
```

**验收标准**:
- ✅ 所有前置条件满足
- ✅ 输出包含完整审核链

---

### 步骤 8：重新采集（Re-Collection Loop）

**触发条件**:
- 步骤 4 Bot 初审不通过
- 步骤 5 主管复审不通过
- 步骤 6 太一终审驳回

**重试策略**:

| 失败次数 | 动作 | 说明 |
|---------|------|------|
| 第 1 次 | 自动重试 | 检查数据源，调整采集参数 |
| 第 2 次 | 换源重试 | 使用备用数据源 |
| 第 3 次 | 人工介入 | 报告 SAYELF，请求手动确认 |

**重试报告**:
```markdown
## 重试报告

**任务 ID**: ...
**失败次数**: N
**失败原因**: ...
**调整措施**: ...
**重试结果**: 成功 / 失败

**下一步**: 继续重试 / 请求人工介入
```

**验收标准**:
- ✅ 重试原因已记录
- ✅ 调整措施已执行
- ✅ 重试结果已报告

---

### 步骤 9：归档记录（Archiving）

**执行者**: 守藏吏 Bot

**归档内容**:

| 文件类型 | 归档位置 | 保留期限 |
|---------|---------|---------|
| 原始数据 | `/workspace/archive/raw/` | 永久 |
| 验证报告 | `/workspace/archive/validation/` | 永久 |
| 审核记录 | `/workspace/archive/reviews/` | 永久 |
| 输出成果 | `/workspace/archive/output/` | 永久 |
| 重试报告 | `/workspace/archive/retries/` | 永久 |

**归档索引**:
```json
{
    "task_id": "...",
    "created_at": "...",
    "archived_at": "...",
    "files": [...],
    "status": "ARCHIVED",
    "verification_chain": ["bot", "supervisor", "taiyi"]
}
```

**验收标准**:
- ✅ 所有文件已归档
- ✅ 归档索引已更新
- ✅ 可追溯查询

---

## 🚨 异常处理

### 数据源失效

```
IF 数据源不可访问 THEN
    1. 记录错误（URL + 错误码 + 时间）
    2. 尝试备用数据源
    3. 如无备用源，报告 SAYELF
    4. 任务标记为"阻塞"
END IF
```

### 验证不一致

```
IF 交叉验证差异 > 阈值 THEN
    1. 标记异常值
    2. 采集第三数据源
    3. 多数一致原则（2/3 以上）
    4. 如无法达成一致，报告 SAYELF
END IF
```

### 审核超时

```
IF 审核等待时间 > 24 小时 THEN
    1. 发送提醒给审核者
    2. 如仍无响应，升级给太一
    3. 太一可代为审核或转 SAYELF
END IF
```

---

## 📊 流程图（AI 可执行版本）

```python
def output_verification_pipeline(task_id, data_type, collector_bot):
    """
    成果输出验证流程
    
    Args:
        task_id: 任务 ID
        data_type: 数据类型（financial/weather/web/screenshot/user）
        collector_bot: 采集 Bot
    
    Returns:
        output: 输出成果（如通过）
        error: 错误信息（如不通过）
    """
    
    # 步骤 1: 数据采集
    raw_data = collect_data(task_id, data_type, collector_bot)
    if not validate_metadata(raw_data):
        return retry_step1(task_id)
    
    # 步骤 2: 来源标注
    annotated_data = annotate_source(raw_data)
    if not validate_annotation(annotated_data):
        return retry_step1(task_id)
    
    # 步骤 3: 交叉验证
    validation_result = cross_validate(annotated_data, data_type)
    if validation_result.score < get_threshold(data_type):
        return retry_step1(task_id)
    
    # 步骤 4: Bot 初审
    bot_review = bot_self_check(annotated_data, validation_result)
    if bot_review.status != "PASS":
        return retry_step1(task_id)
    
    # 步骤 5: 主管复审
    supervisor_review = supervisor_check(bot_review)
    if supervisor_review.status != "APPROVED":
        return retry_step1(task_id)
    
    # 步骤 6: 太一终审
    taiyi_review = taiyi_final_check(supervisor_review)
    if taiyi_review.status == "REJECTED":
        return retry_step1(task_id)
    elif taiyi_review.status == "PENDING_SAYELF":
        return wait_sayelf_confirmation()
    
    # 步骤 7: 成果输出
    output = generate_output(annotated_data, validation_result, 
                            bot_review, supervisor_review, taiyi_review)
    
    # 步骤 8: 归档记录
    archive_task(task_id, output)
    
    return output
```

---

## 📁 文件结构

```
/workspace/
├── constitution/
│   └── workflows/
│       └── OUTPUT-VERIFICATION.md  # 本文件
├── data/
│   ├── raw/                        # 原始数据
│   └── annotated/                  # 标注数据
├── reviews/
│   ├── bot_preliminary/            # Bot 初审
│   ├── supervisor_review/          # 主管复审
│   └── taiyi_final/                # 太一终审
├── output/                         # 输出成果
└── archive/                        # 归档记录
    ├── raw/
    ├── validation/
    ├── reviews/
    ├── output/
    └── retries/
```

---

## ✅ 验收清单

**流程激活检查**:
- [ ] 所有 Bot 已学习本流程
- [ ] 文件结构已创建
- [ ] 审核模板已就绪
- [ ] 归档目录已创建

**单次任务检查**:
- [ ] 步骤 1-9 全部完成
- [ ] 所有审核记录存在
- [ ] 数据来源可追溯
- [ ] 验证报告完整
- [ ] 归档索引更新

---

*创建：2026-03-31 | 版本：v1.0 | 状态：✅ 激活*
