# 太一 AGI 架构文档

> 版本：v3.0 | 更新时间：2026-04-01 | 状态：✅ 生产运行

---

## 🎯 系统概览

```
┌─────────────────────────────────────────────────────────────┐
│                    SAYELF (唯一决策人)                       │
│                           ↓                                 │
│                    太一 (执行总管)                           │
│         统筹 + 调度 + 决策 + 汇报                            │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │ 专业 Bot │      │ 技能系统  │     │ 宪法系统  │
   │  (6 个)  │      │ (30+ 个)  │     │ (Tier 1)  │
   └─────────┘      └───────────┘     └───────────┘
```

---

## 🤖 Bot 架构

### 8 Bot 舰队

| Bot | 职责 | 账号 | 状态 |
|-----|------|------|------|
| **太一** | AGI 执行总管 | taiyi | ✅ 运行中 |
| 知几 | 量化交易 | zhiji | ✅ 运行中 |
| 山木 | 内容创意 | shanmu | ✅ 运行中 |
| 素问 | 技术开发 | suwen | ✅ 运行中 |
| 罔两 | 数据/CEO | wangliang | ✅ 运行中 |
| 庖丁 | 预算成本 | paoding | ✅ 运行中 |
| 羿 | 监控/追踪 | hunter | ✅ 运行中 |
| 守藏吏 | 管家/调度 | steward | ✅ 运行中 |

### Bot 协作模式

```
SAYELF → 太一 → 专业 Bot → 太一 → SAYELF
         ↓        ↓
      调度    执行
         ↓        ↓
      汇总    汇报
```

**职责域划分**：
- 交易相关 → 知几
- 内容相关 → 山木
- 技术相关 → 素问
- 数据相关 → 罔两
- 预算相关 → 庖丁
- 监控相关 → 羿
- 资源调度 → 守藏吏

---

## 🧠 宪法系统

### Tier 1 · 永久核心

| 文件 | 职责 | 大小 |
|------|------|------|
| `CONST-ROUTER.md` | 宪法加载协议 | 4.5KB |
| `VALUE-FOUNDATION.md` | 价值基石 | 5.2KB |
| `NEGENTROPY.md` | 负熵法则 | 3.8KB |
| `AGI-TIMELINE.md` | AGI 时间线 | 4.0KB |
| `OBSERVER.md` | 观察者协议 | 3.5KB |
| `SELF-LOOP.md` | 自驱动闭环 | 4.2KB |
| `AUTO-EXEC.md` | 自动执行 | 8.2KB |
| **`SELF-HEAL.md`** | **自愈智能自动化** | **3.3KB** 🆕 |
| `ASK-PROTOCOL.md` | 追问协议 | 3.7KB |
| `COLLABORATION.md` | 多 Bot 协作 | 5.5KB |
| `TURBOQUANT.md` | 智能分离 | 6.8KB |

### Tier 2 · 业务法则

- `DELEGATION.md` - 任务委派协议
- `EMERGENCE.md` - 能力涌现协议
- `COMMANDER.md` - 指挥官协议
- `LEVEL-4-PROTOCOL.md` - L4 自主协议
- `LEVEL-5-PROTOCOL.md` - L5 自主协议

### Tier 3 · 方法论

- `CRITICAL-THINKING.md` - 批判性思维
- `LEARNING-METHOD.md` - 学习方法
- `IDENTITY-CONSISTENCY.md` - 身份一致性

---

## 🛠️ 技能系统

### 核心技能（太一专属）

| 技能 | 职责 | 状态 |
|------|------|------|
| `auto-exec` | 自动执行引擎 | ✅ 已激活 |
| `heal-state` | 自愈状态管理 | ✅ 已激活 🆕 |
| `turboquant` | 记忆压缩 | ✅ 已激活 |

### 业务技能

| 技能 | 负责 Bot | 职责 |
|------|---------|------|
| `polymarket` | 知几 | 预测市场交易 |
| `gmgn-*` | 知几 | GMGN 链上交易 |
| `zhiji-sentiment` | 知几 | 情绪分析 |
| `shanmu-reporter` | 山木 | 研报生成 |
| `tts` | 山木 | 语音合成 |
| `image_generate` | 山木 | 图片生成 |
| `weather` | 素问 | 天气查询 |
| `web_search` | 素问 | 网络搜索 |
| `github` | 素问 | GitHub 操作 |
| `feishu-*` | 罔两 | 飞书集成 |
| `paoding` | 庖丁 | 预算管理 |

### 技能总数：**30+ 个**

---

## 💓 智能自动化系统

### 1. 自动执行（Auto-Exec）

**Skill**: `skills/auto-exec/` (7 文件 / ~20KB)

**职责**：
- 任务发现与调度
- 进度追踪与汇报
- 状态管理
- 阻塞检测与上报

**Cron 配置**：
- `auto-progress-5m` - 每 5 分钟汇报进度

**状态文件**：
- `/tmp/auto-exec-status.json`
- `/tmp/task-tracker.json`
- `/tmp/progress-history.json`

### 2. 自愈系统（Self-Heal）

**Skill**: `skills/heal-state/` (7 文件 / ~26.5KB)

**职责**：
- 故障诊断与修复
- 防死循环保护
- 人工干预触发
- 成果汇报

**防死循环机制**：
| 保护 | 阈值 |
|------|------|
| 单问题自愈次数 | 3 次 |
| 总失败次数 | 5 次 |
| 自愈冷却时间 | 10 分钟 |

**Cron 配置**：
- `heal-progress-10m` - 每 10 分钟汇报
- `suwen-health` - 每日 9:00 健康检查

**状态文件**：
- `/tmp/heal-state.json`
- `/tmp/heal-history.json`
- `/tmp/heal-intervention-required.json`

### 3. 记忆系统（TurboQuant）

**架构**：
```
memory/core.md      (核心记忆，80% 信息，每次必读)
memory/residual.md  (残差细节，20% 细节，context>80K 加载)
MEMORY.md           (长期固化，仅主 session 加载)
memory/YYYY-MM-DD.md (原始日志，每日归档)
```

**压缩率**: 4-6x  
**信息损失**: <1%

---

## 📊 Cron 调度系统

### 当前配置（17 个任务）

| 频率 | 任务数 | 示例 |
|------|--------|------|
| 每 5 分钟 | 1 | auto-progress-5m |
| 每 10 分钟 | 1 | heal-progress-10m |
| 每日 7:00 | 2 | 气象采集 |
| 每日 8:00 | 3 | 早间内容 |
| 每日 9:00 | 3 | 数据采集 |
| 每日 12:00 | 2 | 午间汇报 |
| 每日 14:00 | 1 | 鲸鱼追踪 |
| 每日 18:00 | 2 | 晚间汇报 |
| 每日 23:00 | 1 | Agent 日记 |

**统一配置**：
- 账号：taiyi (微信)
- 渠道：openclaw-weixin
- 投递：SAYELF (o9cq80yz80T13iCV5N_djDCSVo88@im.wechat)

---

## 🔐 安全架构

### 宪法安全基线

**禁止行为**：
- ❌ 数据外传
- ❌ 未经批准执行破坏性命令
- ❌ 绕过防死循环机制
- ❌ 自愈时修改用户数据

**必须行为**：
- ✅ 敏感操作前询问
- ✅ 自愈前备份配置
- ✅ 失败时保留现场
- ✅ 干预时提供诊断

### 账号安全

| 平台 | 账号数 | 状态 |
|------|--------|------|
| Telegram | 8 Bot | ✅ 已配置 |
| 微信 | 3 账号 | ✅ 已配置 |
| 飞书 | 6 App | ✅ 已配置 |
| GitHub | 1 | ✅ 已认证 |
| Polymarket | 1 | ✅ API Key 已配置 |

---

## 📈 核心指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 首次响应 | <1 分钟 | ~55 秒 ✅ |
| Gateway 重启 | <2 分钟 | ~1 分钟 ✅ |
| context 占用 | <80K | <30KB ✅ |
| P0+P1 执行 | 100% | 100% ✅ |
| 自愈成功率 | ≥80% | 待统计 |
| 自动汇报 | 100% | 100% ✅ |

---

## 🗂️ 文件结构

```
~/.openclaw/workspace/
├── AGENTS.md              # 身份与启动协议
├── SOUL.md                # 身份锚点
├── USER.md                # 用户信息
├── TOOLS.md               # 工具配置
├── HEARTBEAT.md           # 核心待办
├── MEMORY.md              # 长期记忆
├── constitution/          # 宪法系统
│   ├── directives/        # Tier 1 法则
│   │   ├── SELF-HEAL.md   # 🆕 自愈宪法
│   │   └── ...
│   └── ...
├── skills/                # 技能系统
│   ├── auto-exec/         # 自动执行 Skill
│   ├── heal-state/        # 🆕 自愈状态 Skill
│   └── ...
├── memory/                # 记忆系统
│   ├── core.md
│   ├── residual.md
│   └── YYYY-MM-DD.md
├── scripts/               # 脚本库
├── reports/               # 报告输出
└── logs/                  # 日志文件
```

---

## 🔄 运行流程

### Session 启动

```
1. 读取宪法 (Tier 1 永久核)
2. 读取 SOUL.md (身份锚点)
3. 读取 USER.md (用户信息)
4. 读取 memory/core.md (核心记忆)
5. 读取 HEARTBEAT.md (待办事项)
6. (主 session) 读取 MEMORY.md
7. 检查 Gateway 状态
8. 开始服务
```

### 任务执行

```
1. 接收任务 (SAYELF 或 Cron)
2. 判断职责域
3. 如需委派 → 调度专业 Bot
4. 执行任务
5. 生成成果汇报
6. 发送 SAYELF
7. 写入记忆
```

### 自愈触发

```
1. 监控检测故障
2. 记录问题
3. 检查 can_heal()
4. 如可自愈 → 执行修复
5. 验证效果
6. 生成成果汇报
7. 检查是否需要人工干预
8. 如需要 → 发送告警
```

---

## 🚀 能力涌现机制

### 触发条件

满足任一条件时主动提议新建 Skill：
1. 同类任务重复出现 ≥ 3 次
2. 职责域超出 Bot 能力边界
3. SAYELF 提出新方向

### 提议格式

```
「SAYELF，我建议新建 [模块名]，
 原因是 [触发条件]，
 它将处理 [具体职责]，
 需要你批准。」
```

### 批准后执行

1. 通过 distillation-protocol 验证
2. 写入对应 workspace 或 constitution/
3. openclaw gateway reload 热重载
4. 写入当日 memory 标注 [能力涌现]

---

## 📜 宪法修订流程

### 修订触发

- 连续 3 周指标不达标
- 出现新的业务场景
- SAYELF 提出修订要求
- 太一发现更优方案

### 修订流程

```
1. 太一提出修订建议
2. SAYELF 审核批准
3. 更新宪法文件
4. openclaw gateway reload
5. 写入当日 memory
```

---

## 🎯 当前聚焦（P0 任务）

| 编号 | 任务 | 状态 | 下一步 |
|------|------|------|--------|
| TASK-033 | CAD 服务上线 | 🟡 部署方案完成 | 脚本开发 |
| TASK-034 | 鲸鱼追踪 | 🟡 脚本完成 | 配置鲸鱼地址 |
| TASK-037 | Discord 加入 | 🔴 待加入 | 获取邀请链接 |
| TASK-050 | 知几首笔下注 | 🟢 实盘就绪 | 待首笔下注 |
| TASK-082 | 币安测试网 | ✅ 测试网就绪 | 实盘待 IP 白名单 |
| TASK-101 | TimesFM 集成 | ✅ 完成 | Python 3.12 兼容 |
| TASK-111 | 情景模式系统 | ✅ MVP 完成 | 小程序上传审核 |
| TASK-112 | Auto-Exec Skill | ✅ 完成 | 标准化 Skill |
| TASK-113 | Heal-State Skill | ✅ 完成 | 🆕 自愈智能自动化 |

---

## 📊 系统健康度

| 组件 | 状态 | 备注 |
|------|------|------|
| Gateway | ✅ 运行中 | PID 223263 |
| 微信通道 | ✅ 正常 | taiyi 账号 |
| Telegram | ✅ 正常 | 8 Bot 运行中 |
| Cron 调度 | ✅ 正常 | 17 任务已配置 |
| 自动执行 | ✅ 正常 | 5 分钟汇报 |
| 自愈系统 | ✅ 正常 | 10 分钟汇报 |
| 记忆系统 | ✅ 正常 | TurboQuant 压缩 |

---

*更新时间：2026-04-01 08:54 | 太一 AGI v3.0 | 8 Bot 舰队 · 30+ Skills · 11 宪法核心*
