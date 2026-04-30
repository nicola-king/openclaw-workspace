# Telegram 群聊多 Bot 协作配置指南

> **版本**: v1.0  
> **创建**: 2026-04-22  
> **用途**: 太一与其他 Bot 在 Telegram 群聊中的会话配置

---

## 🏗️ 架构说明

### 太一多 Bot 协作架构

```
太一 (taiyi) ← 唯一主 Agent / 最终决策者
│
├── 核心决策层（太一直属）
│   ├── 知几 (zhiji) ← 量化交易·数据分析
│   ├── 山木 (shanmu) ← 内容创意·业务执行
│   ├── 素问 (suwen) ← 技术研究·系统开发
│   ├── 罔两 (wangliang) ← 市场情报·竞品监控
│   └── 庖丁 (paoding) ← 财务成本·预算控制
│
└── 专项能力层（按需激活）
    ├── 羿 (yi) ← 监控追踪·信号捕捉
    └── 守藏吏 (steward) ← 资源调度·任务分发
```

---

## 📱 Telegram 群聊配置

### 方案 1: 单 Bot 模式 (推荐)

**配置**:
```
• 只添加太一 Bot 到群聊
• 其他 Bot 作为太一的能力模块
• 用户与太一对话，太一内部调用其他 Bot
```

**优点**:
- ✅ 简洁，用户只需与太一交互
- ✅ 统一出口，避免混乱
- ✅ 太一统筹所有 Bot 能力

**缺点**:
- ⚠️ 其他 Bot 不直接可见

**设置步骤**:
```
1. 创建 Telegram 群聊
2. 添加太一 Bot (@sayelfbot) 到群聊
3. 设置太一为管理员 (可选)
4. 完成
```

**使用方式**:
```
用户：@sayelfbot 分析一下这个项目的财务情况

太一：【委派确认】
任务：财务分析
执行频道：庖丁
预计耗时：5 分钟
交付物：财务分析报告

开始执行 → 回复「收到」
取消委派 → 回复「取消」

[切换到庖丁频道分析]

太一：【庖丁分析报告】
• 成本结构：...
• 利润率：...
• 风险点：...
```

---

### 方案 2: 多 Bot 模式 (高级)

**配置**:
```
• 添加多个 Bot 到群聊
• 每个 Bot 独立响应
• 太一负责统筹和最终决策
```

**优点**:
- ✅ 各 Bot 可直接交互
- ✅ 用户可直接@特定 Bot
- ✅ 更灵活的协作

**缺点**:
- ⚠️ 需要更多配置
- ⚠️ 可能出现 Bot 之间冲突

**设置步骤**:
```
1. 创建 Telegram 群聊
2. 添加以下 Bot 到群聊:
   - 太一 Bot (@sayelfbot)
   - 知几 Bot (@zhiji_bot)
   - 山木 Bot (@shanmu_bot)
   - 素问 Bot (@suwen_bot)
   - 罔两 Bot (@wangliang_bot)
   - 庖丁 Bot (@paoding_bot)
3. 设置太一为管理员
4. 配置 Bot 权限
5. 完成
```

**使用方式**:
```
方式 1: 直接@特定 Bot
用户：@zhiji_bot 分析一下这个数据
知几：[分析结果]

方式 2: 通过太一派委
用户：@sayelfbot 委派知几分析数据
太一：【委派确认】...
[知几执行后]
太一：【整合结果】...

方式 3: Bot 之间讨论
用户：这个项目怎么样？
太一：【启动多 Bot 讨论】
知几：从数据角度看...
山木：从执行角度看...
庖丁：从财务角度看...
太一：【综合结论】...
```

---

## 🔧 Bot 配置要求

### 每个 Bot 需要

| 配置项 | 说明 | 状态 |
|--------|------|------|
| **Telegram Bot Token** | 从 BotFather 获取 | 每个 Bot 独立 |
| **Webhook URL** | 接收消息的 URL | 每个 Bot 独立 |
| **群聊权限** | 发送消息/读取消息 | 群管理员设置 |
| **Bot 人格** | 角色定义/职责域 | 已配置 |
| **协作协议** | 多 Bot 协作规则 | 已配置 |

### 太一统筹配置

```python
# 太一系统内部配置
BOT_CONFIG = {
    'taiyi': {
        'token': 'YOUR_TAIYI_TOKEN',
        'role': 'coordinator',
        'permissions': ['read', 'write', 'delegate'],
    },
    'zhiji': {
        'token': 'YOUR_ZHIJI_TOKEN',
        'role': 'analyst',
        'permissions': ['read', 'write'],
        'domain': ['data', 'analysis', 'quant'],
    },
    'shanmu': {
        'token': 'YOUR_SHANMU_TOKEN',
        'role': 'executor',
        'permissions': ['read', 'write'],
        'domain': ['content', 'execution', 'project'],
    },
    # ... 其他 Bot
}
```

---

## 📋 委派命令格式

### 标准委派命令

```
/委派 [Bot 名] [任务描述]
```

### 示例

```
/委派知几 分析一下这个项目的数据趋势
/委派素问 研究一下这个技术的原理
/委派庖丁 计算一下这个项目的成本利润
/委派山木 执行这个项目的推广计划
/委派罔两 监控一下竞争对手的动态
```

### 委派确认格式

```
【委派确认】
任务：[任务描述]
执行频道：[Bot 名]
预计耗时：[时间]
交付物：[格式]

开始执行 → 回复「收到」
取消委派 → 回复「取消」
```

---

## 🎯 Bot 职责域

| Bot | 职责域 | 触发关键词 |
|------|--------|-----------|
| **太一** | 统筹/决策 | 所有任务 |
| **知几** | 数据/分析/量化 | 数据/分析/图表/趋势/统计/量化 |
| **山木** | 内容/执行/项目 | 内容/执行/项目/计划/任务/落地 |
| **素问** | 技术/研究/开发 | 技术/研究/开发/原理/机制/代码 |
| **罔两** | 市场/情报/竞品 | 市场/竞品/价格/动态/情报/舆情 |
| **庖丁** | 财务/成本/预算 | 财务/成本/利润/账目/预算/风险 |

---

## 🔄 协作流程

### 单 Bot 任务
```
1. 用户 → 太一：提出任务
2. 太一 → 判断职责域
3. 太一 → 对应 Bot：委派任务
4. Bot → 太一：汇报结果
5. 太一 → 用户：交付结果
```

### 多 Bot 协作任务
```
1. 用户 → 太一：提出跨域任务
2. 太一 → 拆解为子任务
3. 太一 → 各 Bot：分别委派
4. 各 Bot → 太一：汇报结果
5. 太一 → 整合所有结果
6. 太一 → 用户：交付整合结果
```

### Bot 之间讨论
```
1. 用户 → 太一：提出问题
2. 太一 → 激活多 Bot 讨论
3. 各 Bot → 从专业角度分析
4. 太一 → 汇总讨论结果
5. 太一 → 用户：交付综合结论
```

---

## ⚙️ 技术实现

### 方案 1: 单 Bot Token (推荐)

```python
# 太一系统内部处理所有 Bot 能力
class TaiyiBot:
    def __init__(self):
        self.token = "YOUR_TAIYI_TOKEN"
        self.modules = {
            'zhiji': ZhijiModule(),
            'shanmu': ShanmuModule(),
            'suwen': SuwenModule(),
            # ...
        }
    
    def handle_message(self, message):
        # 判断是否需要委派
        if self.needs_delegation(message):
            bot_name = self.identify_bot(message)
            return self.modules[bot_name].process(message)
        else:
            return self.process(message)
```

**优点**:
- ✅ 只需 1 个 Bot Token
- ✅ 统一管理
- ✅ 用户感知简洁

**缺点**:
- ⚠️ 其他 Bot 不独立可见

---

### 方案 2: 多 Bot Token

```python
# 每个 Bot 独立
class BotGroup:
    def __init__(self):
        self.bots = {
            'taiyi': TaiyiBot("TOKEN_TAIYI"),
            'zhiji': ZhijiBot("TOKEN_ZHIJI"),
            'shanmu': ShanmuBot("TOKEN_SHANMU"),
            # ...
        }
    
    def handle_group_message(self, message):
        # 判断哪个 Bot 响应
        target_bot = self.identify_target(message)
        return self.bots[target_bot].process(message)
```

**优点**:
- ✅ 各 Bot 独立可见
- ✅ 用户可直接@特定 Bot
- ✅ 更灵活

**缺点**:
- ⚠️ 需要多个 Bot Token
- ⚠️ 配置复杂
- ⚠️ 需要协调 Bot 之间响应

---

## 📝 创建 Telegram Bot

### 步骤 1: 联系 BotFather

```
1. 在 Telegram 搜索 @BotFather
2. 发送 /newbot
3. 按提示设置 Bot 名称和用户名
4. 获取 Bot Token
```

### 步骤 2: 配置 Bot

```
1. 设置 Bot 头像
2. 设置 Bot 描述
3. 设置 Bot 命令列表 (/help, /start 等)
4. 配置 Privacy Mode (允许读取群消息)
```

### 步骤 3: 添加到群聊

```
1. 创建 Telegram 群聊
2. 点击"添加成员"
3. 搜索 Bot 用户名
4. 添加 Bot 到群聊
5. 设置 Bot 为管理员 (可选)
```

---

## 🔒 权限配置

### Bot 群聊权限

| 权限 | 说明 | 推荐设置 |
|------|------|---------|
| **发送消息** | Bot 可以发送消息 | ✅ 开启 |
| **读取消息** | Bot 可以读取群消息 | ✅ 开启 |
| **删除消息** | Bot 可以删除消息 | ⚠️ 按需 |
| **禁言成员** | Bot 可以禁言 | ❌ 关闭 |
| **邀请成员** | Bot 可以邀请 | ❌ 关闭 |
| **管理员** | Bot 是管理员 | ⚠️ 按需 |

---

## 💡 最佳实践

### 推荐配置

```
✅ 单 Bot 模式 (太一统筹)
✅ 内部调用其他 Bot 能力
✅ 统一出口交付用户
✅ 用户只需与太一交互
```

### 避免的问题

```
❌ 多个 Bot 同时响应同一消息
❌ Bot 之间互相冲突
❌ 用户不知道@哪个 Bot
❌ Bot 权限过高
```

---

## 📊 当前系统状态

### 已配置 Bot

| Bot | 状态 | 职责 |
|------|------|------|
| **太一** | ✅ 运行中 | 统筹决策 |
| **知几** | ✅ 运行中 | 数据分析 |
| **山木** | ✅ 运行中 | 内容执行 |
| **素问** | ✅ 运行中 | 技术研究 |
| **罔两** | ✅ 运行中 | 市场情报 |
| **庖丁** | ✅ 运行中 | 财务成本 |

### Telegram 配置

| 项目 | 状态 |
|------|------|
| **太一 Bot** | ✅ @sayelfbot |
| **群聊支持** | ✅ 已启用 |
| **委派协议** | ✅ 已配置 |
| **多 Bot 协作** | ✅ 已配置 |

---

## 🎯 快速开始

### 最简单的配置 (推荐)

```
1. 创建 Telegram 群聊
2. 添加太一 Bot (@sayelfbot)
3. 完成

使用:
• 直接在群聊中与太一对话
• 使用 /委派 命令调用其他 Bot 能力
• 太一内部处理多 Bot 协作
```

### 高级配置 (多 Bot)

```
1. 创建 6 个 Telegram Bot (联系 BotFather)
2. 获取所有 Bot Token
3. 配置太一系统 (多 Bot 模式)
4. 添加所有 Bot 到群聊
5. 配置 Bot 权限
6. 完成

使用:
• 可直接@特定 Bot
• 可通过太一派委
• Bot 之间可讨论
```

---

*太一 AGI · Telegram 群聊多 Bot 配置指南 v1.0*  
*创建时间：2026-04-22*  
*状态：✅ 可立即使用*
