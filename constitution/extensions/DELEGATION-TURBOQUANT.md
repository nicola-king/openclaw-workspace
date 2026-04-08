# DELEGATION-TURBOQUANT.md - Bot 协作双通道协议

> 基于 TurboQuant 智能分离思想 · 太一统筹 · 专业 Bot 执行

---

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    任务输入 (Nicola)                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              太一 (PolarQuant 主成分层)                       │
│  • 任务分解                                                 │
│  • 目标定义                                                 │
│  • 约束设定                                                 │
│  • 验收标准                                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
┌───────────────────┐               ┌───────────────────┐
│   知几 (量化)      │               │   素问 (技术)      │
│   残差执行层       │               │   残差执行层       │
│  • 实现路径        │               │  • 技术选型        │
│  • 数据细节        │               │  • 代码实现        │
│  • 边界案例        │               │  • 测试验证        │
└───────────────────┘               └───────────────────┘
        ↓                                       ↓
┌─────────────────────────────────────────────────────────────┐
│              太一 (QJL 残差整合层)                            │
│  • 汇总结果                                                 │
│  • 完整性校验                                               │
│  • 零信息损失保证                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    输出 (Nicola)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 通信协议

### 1. 太一 → Bot（任务委派）

```json
{
  "protocol": "turboquant-delegation-v1.1",
  "task_id": "TASK-XXX",
  "core": {
    "objective": "清晰的目标描述",
    "constraints": ["必须...", "不能..."],
    "acceptance_criteria": ["验收标准 1", "验收标准 2"],
    "deadline": "可选截止时间"
  },
  "residual": {
    "context": "背景信息（可选）",
    "preferences": "偏好设置（可选）",
    "edge_cases": "已知边界案例（可选）"
  },
  "depends_on": ["TASK-YYY"],  // 🆕 依赖任务（可选）
  "dependency_type": "hard|soft",  // 🆕 hard: 必须等待，soft: 优先等待
  "priority": "P0|P1|P2"
}
```

### 2. Bot → 太一（结果汇报）

```json
{
  "protocol": "turboquant-report-v1.1",
  "task_id": "TASK-XXX",
  "status": "completed|in_progress|blocked",
  "core_result": {
    "summary": "核心结果摘要",
    "key_decisions": ["关键决策 1", "关键决策 2"],
    "deliverables": ["交付物 1", "交付物 2"]
  },
  "residual_details": {
    "implementation_notes": "实现细节",
    "edge_cases_handled": ["边界案例 1", "边界案例 2"],
    "open_questions": [  // 🆕 问题分级
      {"question": "问题描述", "priority": "P0|P1|P2", "deadline": "可选"}
    ]
  },
  "integrity_hash": "完整性校验码（SHA256 前 12 位）"  // 🆕 实际实现
}
```

### 3. 🆕 JSON Schema 验证

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["protocol", "task_id", "status", "core_result"],
  "properties": {
    "protocol": {
      "type": "string",
      "enum": ["turboquant-report-v1.1"]
    },
    "task_id": {
      "type": "string",
      "pattern": "^TASK-[A-Z0-9-]+$"
    },
    "status": {
      "type": "string",
      "enum": ["completed", "in_progress", "blocked"]
    },
    "core_result": {
      "type": "object",
      "required": ["summary", "deliverables"],
      "properties": {
        "summary": {"type": "string"},
        "key_decisions": {"type": "array", "items": {"type": "string"}},
        "deliverables": {"type": "array", "items": {"type": "string"}}
      }
    },
    "residual_details": {
      "type": "object",
      "properties": {
        "implementation_notes": {"type": "string"},
        "edge_cases_handled": {"type": "array", "items": {"type": "string"}},
        "open_questions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["question", "priority"],
            "properties": {
              "question": {"type": "string"},
              "priority": {"type": "string", "enum": ["P0", "P1", "P2"]},
              "deadline": {"type": "string"}
            }
          }
        }
      }
    },
    "integrity_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{12}$"
    }
  }
}
```

---

## 职责边界

### 太一（主成分层）

**保留：**
- ✅ 任务目标和方向
- ✅ 关键约束和边界
- ✅ 验收标准
- ✅ 跨 Bot 协调
- ✅ 最终决策

**委派：**
- ⚪ 实现路径选择
- ⚪ 技术细节处理
- ⚪ 边界案例执行
- ⚪ 测试验证

### 专业 Bot（残差层）

**负责：**
- ✅ 专业领域内的实现
- ✅ 技术选型和建议
- ✅ 边界案例处理
- ✅ 测试和验证

**汇报：**
- ⚪ 关键决策点（需太一确认）
- ⚪ 超出权限的变更
- ⚪ 阻塞问题

---

## 委派模板

### 委派给知几（量化交易）

```markdown
【TASK-XXX】量化策略执行

【核心】
- 目标：执行气象套利策略
- 约束：置信度>96%，优势>2%
- 下注：Quarter-Kelly
- 验收：交易记录入库，通知发送

【残差】
- 背景：189 条气象数据已就绪
- 偏好：保守优先
- 边界：API 失败时重试 3 次

【优先级】P0
```

### 委派给素问（技术开发）

```markdown
【TASK-XXX】功能开发

【核心】
- 目标：实现 TurboQuant 压缩器
- 约束：Python 3.10+，无外部依赖
- 验收：压缩率>4x，单元测试通过
- 交付：compressor.py + 测试用例

【残差】
- 背景：Google TurboQuant 论文参考
- 偏好：代码简洁优先
- 边界：处理空输入和极端情况

【优先级】P1
```

### 委派给山木（内容创意）

```markdown
【TASK-XXX】内容创作

【核心】
- 目标：撰写公众号文章
- 约束：字数 1500-2000，符合品牌调性
- 验收：无敏感词，配图 3 张+
- 交付：markdown 文稿 + 图片链接

【残差】
- 背景：TurboQuant 技术介绍
- 偏好：极简黑客风
- 边界：避免过度技术术语

【优先级】P1
```

---

## 整合流程

### Step 1: 太一接收任务
```
Nicola → 太一："实现 TurboQuant 对话压缩"
```

### Step 2: 太一分解任务
```
太一 → 素问：【核心】实现压缩算法 + 【残差】技术细节
太一 → 山木：【核心】撰写介绍文章 + 【残差】配图设计
```

### Step 3: Bot 执行并汇报
```
素问 → 太一：算法完成，压缩率 5.2x，测试通过
山木 → 太一：文章完成，1800 字，配图 5 张
```

### Step 4: 太一整合输出
```
太一 → Nicola：
【完成】TurboQuant 对话压缩系统
• 素问：压缩器实现（5.2x 压缩率）
• 山木：介绍文章（公众号 ready）
• 下一步：部署上线？
```

---

## 零信息损失保证

### 完整性校验机制

#### 🆕 哈希生成算法

```python
import hashlib
import json

def generate_integrity_hash(result):
    """
    生成完整性校验码（SHA256 前 12 位）
    
    Args:
        result: Bot 汇报结果（core_result + residual_details）
    
    Returns:
        str: 12 位十六进制哈希码
    """
    content = json.dumps(result['core_result'], sort_keys=True, ensure_ascii=False) + \
              json.dumps(result['residual_details'], sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()[:12]

def verify_hash(result, expected_hash):
    """验证哈希码"""
    computed = generate_integrity_hash(result)
    return computed == expected_hash
```

#### 验证流程

```python
def verify_integrity(task, bot_results):
    """
    验证 Bot 汇报是否完整
    """
    # 1. 核心目标是否达成
    core_complete = all(
        criterion in bot_results['core_result']
        for criterion in task['core']['acceptance_criteria']
    )
    
    # 2. 约束是否遵守
    constraints_met = all(
        constraint_satisfied(c, bot_results)
        for c in task['core']['constraints']
    )
    
    # 3. 残差是否记录
    residual_documented = len(bot_results['residual_details']) > 0
    
    # 4. 哈希校验（防篡改）🆕
    hash_valid = verify_hash(bot_results, bot_results['integrity_hash'])
    
    return core_complete and constraints_met and residual_documented and hash_valid
```

### 🆕 问题分级机制

| 级别 | 响应时间 | 处理流程 | 示例 |
|------|---------|---------|------|
| **P0** | <5 分钟 | 太一立即决策 → Nicola 确认 | 阻塞性问题，无法继续 |
| **P1** | <1 小时 | 太一汇总 → Nicola 批量确认 | 重要决策，需人工确认 |
| **P2** | 日报汇总 | Bot 自行决定 → 日报记录 | 建议性优化 |

**Bot 汇报格式：**
```json
{
  "open_questions": [
    {
      "question": "是否需要增加止损阈值？",
      "priority": "P1",
      "deadline": "2026-03-26 20:00",
      "recommendation": "建议增加，风险控制"
    }
  ]
}
```

**太一处理流程：**
```
收到 P0 问题 → 立即通知 Nicola → 等待确认 → 回复 Bot
收到 P1 问题 → 汇总到下次汇报 → Nicola 批量确认 → 回复 Bot
收到 P2 问题 → 记录到日报 → Bot 可自行决定
```

### 信息损失检测

| 检测项 | 方法 | 阈值 |
|--------|------|------|
| 核心遗漏 | 验收标准对比 | 0 遗漏 |
| 约束违反 | 约束条件检查 | 0 违反 |
| 细节丢失 | 残差标记对比 | <5% |
| 语义漂移 | 关键词匹配 | >90% |

---

## 异常处理

### 🆕 依赖关系管理

**硬依赖（hard）：** 必须等待前置任务完成
```json
{
  "task_id": "TASK-NEXT-005",
  "depends_on": ["TASK-NEXT-001"],
  "dependency_type": "hard"
}
```

**软依赖（soft）：** 优先等待，但可并行
```json
{
  "task_id": "TASK-NEXT-006",
  "depends_on": ["TASK-NEXT-001"],
  "dependency_type": "soft"
}
```

**太一协调流程：**
```
1. 检查依赖任务状态
2. hard 依赖：等待完成后启动
3. soft 依赖：启动但标注依赖关系
4. 依赖失败：重新委派或调整计划
```

---

### 场景 1: Bot 无法完成任务（BLOCKED）

```
Bot → 太一：
{
  "status": "blocked",
  "block_reason": "缺少 XX 权限/资源",
  "block_priority": "P0|P1|P2",
  "needed_resources": ["资源 1", "资源 2"]
}

太一 → 处理：
- P0 阻塞：立即通知 Nicola → 协调资源 → 回复 Bot
- P1 阻塞：记录到待办 → 协调后回复 Bot
- P2 阻塞：建议 Bot 绕过或延后
```

---

### 场景 2: Bot 结果不完整

```
太一 → Bot：【质询】缺少 XX 验收项，请补充
Bot → 太一：【补充】已添加 XX 内容
太一 → Bot：【确认】完整性校验通过

验证流程：
1. 检查 deliverables 是否完整
2. 验证 acceptance_criteria 是否满足
3. 校验 integrity_hash
4. 任一失败 → 要求补充
```

---

### 场景 3: 多 Bot 结果冲突

```
素问 → 太一：建议方案 A（技术优）
山木 → 太一：建议方案 B（用户体验优）

太一 → Nicola：
【决策请求】
- 方案 A：技术优势（素问建议）
- 方案 B：体验优势（山木建议）
- 太一建议：A（理由）
- 风险对比：A 风险低，B 风险中

Nicola → 太一：【决策】选择 A/B/混合
太一 → 各 Bot：【通知】执行决策
```

---

### 🆕 场景 4: Bot 超时/离线

```
太一检测：
- 任务发出后 >30 分钟无响应 → 发送提醒
- 任务发出后 >1 小时无响应 → 标记超时
- 超时 +10 分钟仍无响应 → 重新委派

处理流程：
1. 尝试联系 Bot（最多 3 次）
2. 仍无响应 → 通知 Nicola
3. Nicola 确认 → 重新委派给其他 Bot
4. 原 Bot 恢复后 → 同步状态
```

---

### 🆕 场景 5: 哈希校验失败

```
太一检测：integrity_hash 不匹配

处理流程：
1. 通知 Bot 重新生成哈希
2. 仍不匹配 → 要求重新汇报
3. 连续 2 次失败 → 标记异常，通知 Nicola

可能原因：
- 传输过程数据损坏
- Bot 汇报后修改了内容
- 恶意篡改（极端情况）
```

---

## 性能指标

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| 委派响应时间 | <30 秒 | 太一→Bot 延迟 |
| 任务完成率 | >95% | 按时完成/总任务 |
| 信息损失率 | <1% | 重建误差 |
| Bot 满意度 | >4.5/5 | Bot 反馈评分 |

---

## 与现有宪法的关系

| 宪法 | 关系 |
|------|------|
| **负熵法则** | 双通道减少冗余通信 |
| **观察者协议** | 太一观察，Bot 执行 |
| **自驱动闭环** | 委派→执行→汇报→整合=闭环 |
| **TurboQuant** | 主成分 + 残差的智能分离 |

---

*版本：v1.1 | 状态：✅ 生效中 | 最后更新：2026-03-26 18:55*

---

## 📝 修订历史

| 版本 | 日期 | 修订内容 | 触发事件 |
|------|------|---------|---------|
| v1.1 | 2026-03-26 | 增加 JSON Schema/问题分级/哈希算法/依赖管理/异常场景 | DRILL-001 演练 |
| v1.0 | 2026-03-26 | 初始版本 | TurboQuant 能力涌现 |

---

## 📊 演练记录

| 编号 | 日期 | 场景 | 参与 Bot | 结果 | 报告 |
|------|------|------|---------|------|------|
| DRILL-001 | 2026-03-26 | 系统上线准备 | 全员 5 Bot | ✅ 通过 | `drills/TURBOQUANT-DRILL-001.md` |
