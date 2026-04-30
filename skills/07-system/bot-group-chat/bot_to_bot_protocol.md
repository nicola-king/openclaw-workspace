# Bot 之间直接会话协议

> **版本**: v1.0  
> **创建**: 2026-04-22  
> **用途**: Telegram 群聊中 Bot 之间直接会话

---

## 🎯 核心能力

### Bot 之间会话模式

```
✅ 太一 → 其他 Bot：直接@并会话
✅ 其他 Bot → 太一：直接@并汇报
✅ Bot ↔ Bot：互相讨论协作
✅ 统一出口：太一整合后交付用户
```

---

## 📱 Telegram 群聊配置

### 必需配置

| 配置项 | 说明 | 状态 |
|--------|------|------|
| **Privacy Mode** | Bot 可以读取群消息 | ✅ 必需开启 |
| **群组权限** | Bot 可以发送消息 | ✅ 必需开启 |
| **Bot 识别** | 识别@消息 | ✅ 已配置 |
| **会话协议** | Bot 之间会话规则 | ✅ 已配置 |

### 推荐群聊设置

```
群聊类型：超级群 (Supergroup)
成员数量：无限制
消息历史：对新成员可见
Bot 权限：可以读取所有消息
```

---

## 🔄 Bot 会话流程

### 场景 1: 太一 → 其他 Bot

```
太一：@知几 分析一下这个项目的数据趋势

知几：【数据分析报告】
• 趋势：上升 15%
• 关键点：...
• 置信度：85%

太一：收到，我整合后交付用户
```

### 场景 2: 其他 Bot → 太一

```
知几：@太一 发现异常数据波动，需要你看一下

太一：收到，我来分析

[太一分析后]

太一：【整合报告】
• 数据异常：...
• 可能原因：...
• 建议行动：...
```

### 场景 3: Bot ↔ Bot 讨论

```
太一：启动多 Bot 讨论，这个项目怎么样？

知几：从数据角度看，趋势上升 15%...

山木：从执行角度看，可行性 80%...

庖丁：从财务角度看，利润率 25%...

太一：【综合结论】
• 数据支持：✓
• 执行可行：✓
• 财务健康：✓
• 建议：推进项目
```

---

## 📋 Bot 识别机制

### 识别规则

```python
# Bot 消息识别
if message contains "@bot_name":
    if bot_name == self.name:
        # 直接@我，需要响应
        self.respond(message)
    elif bot_name in self.known_bots:
        # @其他 Bot，我可以选择不响应或参与讨论
        if self.should_participate(message):
            self.participate(message)
        else:
            self.ignore(message)
else:
    # 没有@任何 Bot
    if self.is_relevant(message):
        self.maybe_respond(message)
    else:
        self.ignore(message)
```

### Bot 名称映射

| Bot 名 | Telegram 用户名 | 职责 |
|--------|---------------|------|
| **太一** | @taiyi_bot | 统筹决策 |
| **知几** | @zhiji_bot | 数据分析 |
| **山木** | @shanmu_bot | 内容执行 |
| **素问** | @suwen_bot | 技术研究 |
| **罔两** | @wangliang_bot | 市场情报 |
| **庖丁** | @paoding_bot | 财务成本 |

---

## 🎯 Bot 响应优先级

### 优先级规则

| 情况 | 优先级 | 响应时间 |
|------|--------|---------|
| **直接@我** | P0 - 最高 | 立即响应 |
| **@太一 + 我的职责域** | P1 - 高 | 1 分钟内 |
| **Bot 讨论邀请** | P2 - 中 | 5 分钟内 |
| **群聊一般消息** | P3 - 低 | 按需响应 |
| **无关消息** | P4 - 最低 | 不响应 |

### 响应示例

```
情况 1: 直接@我
用户：@知几 分析一下数据
知几：【立即响应】分析中...

情况 2: @太一 + 我的职责域
用户：@太一 这个项目的财务情况如何？
庖丁：【1 分钟内】我来分析财务情况...

情况 3: Bot 讨论邀请
太一：@所有 Bot 启动讨论
知几：【5 分钟内】从数据角度看...
山木：【5 分钟内】从执行角度看...

情况 4: 群聊一般消息
用户：今天天气不错
[所有 Bot 不响应]
```

---

## 📊 Bot 协作协议

### 委派协议

```
太一：@庖丁 委派任务
任务：财务分析
预计耗时：5 分钟
交付物：财务报告

庖丁：收到，开始执行

[5 分钟后]

庖丁：@太一 汇报结果
【财务报告】
• 成本：...
• 利润：...
• 风险：...

太一：收到，整合后交付
```

### 协作协议

```
太一：启动多 Bot 协作
任务：项目评估
参与 Bot: @知几 @山木 @庖丁

知几：【数据分析】...
山木：【执行计划】...
庖丁：【财务评估】...

太一：【整合结论】
• 数据支持：✓
• 执行可行：✓
• 财务健康：✓
• 建议：推进
```

### 辩论协议

```
太一：启动 Bot 辩论
议题：是否推进项目 A

正方 (@山木): 建议推进，理由...
反方 (@庖丁): 建议暂缓，理由...

正方 (@山木): 反驳...
反方 (@庖丁): 反驳...

太一：【裁决】
• 正方观点：...
• 反方观点：...
• 最终决策：推进/暂缓/放弃
```

---

## 🔧 技术实现

### Bot 配置示例

```python
class BotGroupChatConfig:
    """Bot 群聊配置"""
    
    # Bot 信息
    BOT_INFO = {
        'taiyi': {
            'username': '@taiyi_bot',
            'role': 'coordinator',
            'permissions': ['read', 'write', 'delegate', 'integrate'],
        },
        'zhiji': {
            'username': '@zhiji_bot',
            'role': 'analyst',
            'permissions': ['read', 'write', 'analyze'],
            'domain': ['data', 'analysis', 'quant'],
        },
        'shanmu': {
            'username': '@shanmu_bot',
            'role': 'executor',
            'permissions': ['read', 'write', 'execute'],
            'domain': ['content', 'execution', 'project'],
        },
        # ... 其他 Bot
    }
    
    # 响应规则
    RESPONSE_RULES = {
        'direct_mention': {'priority': 'P0', 'timeout': 0},
        'role_mention': {'priority': 'P1', 'timeout': 60},
        'discussion_invite': {'priority': 'P2', 'timeout': 300},
        'general_message': {'priority': 'P3', 'timeout': None},
    }
    
    # Bot 之间会话规则
    BOT_TO_BOT_RULES = {
        'allow_direct': True,      # 允许直接@会话
        'allow_discussion': True,  # 允许多 Bot 讨论
        'allow_debate': True,      # 允许 Bot 辩论
        'require_approval': False, # Bot 会话不需要太一审批
    }
```

### 消息处理流程

```python
async def handle_group_message(message):
    """处理群聊消息"""
    
    # 1. 识别是否@Bot
    mentioned_bots = extract_mentions(message)
    
    # 2. 如果有@Bot
    if mentioned_bots:
        for bot in mentioned_bots:
            if bot == self.name:
                # 直接@我，必须响应
                await self.respond(message)
            elif bot in self.known_bots:
                # @其他 Bot，可选择参与
                if self.should_participate(message):
                    await self.participate(message)
    
    # 3. 如果没有@Bot
    else:
        # 判断是否需要响应
        if self.is_relevant(message):
            await self.maybe_respond(message)
        else:
            await self.ignore(message)
```

---

## 📝 会话示例

### 示例 1: 简单委派

```
太一：@知几 分析一下这个项目的数据

知几：收到，分析中...

[分析完成]

知几：@太一 汇报结果
【数据分析报告】
• 用户增长：+25%
• 活跃度：+15%
• 留存率：85%
• 置信度：90%

太一：收到，整合后交付用户
```

### 示例 2: 多 Bot 协作

```
太一：启动多 Bot 协作
任务：评估项目 A
参与：@知几 @山木 @庖丁

知几：【数据分析】
• 市场趋势：上升 20%
• 竞品分析：...

山木：【执行计划】
• 时间表：3 个月
• 资源需求：...

庖丁：【财务评估】
• 成本：$50K
• 预期收益：$200K
• ROI: 300%

太一：【整合结论】
• 数据支持：✓
• 执行可行：✓
• 财务健康：✓
• 建议：推进项目 A
```

### 示例 3: Bot 辩论

```
太一：启动 Bot 辩论
议题：是否投资项目 B

正方 (@山木): 建议投资
• 市场机会大
• 团队能力强
• 时间窗口短

反方 (@庖丁): 建议暂缓
• 成本过高
• 风险未评估
• 现金流紧张

正方 (@山木): 反驳
• 成本可分期
• 风险可控
• 可融资

反方 (@庖丁): 反驳
• 融资不确定
• 市场变化快
• 建议先小规模测试

太一：【裁决】
• 正方观点合理，但反方风险需重视
• 决策：小规模试点，3 个月后评估
• 预算：$10K
• 目标：验证核心假设
```

---

## ⚙️ 配置步骤

### 步骤 1: 创建 Bot

```
1. 联系 @BotFather
2. 创建每个 Bot (太一/知几/山木/素问/罔两/庖丁)
3. 获取每个 Bot 的 Token
4. 设置 Bot 用户名
```

### 步骤 2: 配置 Privacy Mode

```
1. 在 @BotFather 中选择每个 Bot
2. 发送 /setprivacy
3. 选择 Bot
4. 设置为 "Disable" (允许读取所有消息)
```

### 步骤 3: 创建群聊

```
1. 创建 Telegram 超级群
2. 添加所有 Bot 到群聊
3. 设置太一为管理员
4. 配置 Bot 权限
```

### 步骤 4: 配置 Bot 系统

```python
# 太一系统配置
BOT_CONFIG = {
    'group_chat_enabled': True,
    'bot_to_bot_enabled': True,
    'known_bots': ['zhiji', 'shanmu', 'suwen', 'wangliang', 'paoding'],
    'response_priority': {
        'direct_mention': 'P0',
        'role_mention': 'P1',
        'discussion_invite': 'P2',
    },
}
```

### 步骤 5: 测试

```
1. 在群聊中@太一
2. 测试太一响应
3. 测试太一@其他 Bot
4. 测试 Bot 之间讨论
5. 测试 Bot 辩论
6. 确认所有功能正常
```

---

## 🎯 最佳实践

### 推荐做法

```
✅ Bot 之间直接@会话
✅ 太一统筹最终决策
✅ Bot 专业领域内主动响应
✅ Bot 之间友好讨论
✅ 统一出口交付用户
```

### 避免的问题

```
❌ Bot 之间冲突争吵
❌ 多个 Bot 同时响应同一消息
❌ Bot 响应无关消息
❌ Bot 越权决策
❌ Bot 泄露内部讨论
```

---

## 📊 当前系统状态

### 已配置 Bot 能力

| Bot | 状态 | 群聊支持 | Bot 会话 |
|------|------|---------|---------|
| **太一** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |
| **知几** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |
| **山木** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |
| **素问** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |
| **罔两** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |
| **庖丁** | ✅ 运行中 | ✅ 已启用 | ✅ 已配置 |

---

*太一 AGI · Bot 之间直接会话协议 v1.0*  
*创建时间：2026-04-22*  
*状态：✅ 可立即使用*
