# 太一 AGI 架构全景图

**版本：** v2.0  
**更新：** 2026-03-24 23:54  
**授权：** SAYELF  
**状态：** ✅ 生产环境

---

## 🗺️ 目录结构总览

```
太一 AGI 系统
├── 📁 ~/.openclaw/workspace/          # 工作空间（核心）
├── 📁 ~/.taiyi/                       # 敏感配置（凭证/密钥）
├── 📁 ~/.openclaw/                    # OpenClaw 系统
└── 📁 /opt/openclaw/                  # OpenClaw 安装目录
```

---

## 📁 1. 工作空间 (~/.openclaw/workspace/)

### 1.1 核心文件
| 文件 | 用途 | 状态 |
|------|------|------|
| `SOUL.md` | 身份锚点 | ✅ 只读 |
| `AGENTS.md` | 工作台说明 | ✅ 只读 |
| `USER.md` | 用户信息 | ✅ 可编辑 |
| `TOOLS.md` | 工具配置 | ✅ 可编辑 |
| `HEARTBEAT.md` | 待办事项 | ✅ 实时更新 |
| `MEMORY.md` | 长期记忆 | ✅ 每日更新 |
| `CONFIG.md` | 配置汇总 | ✅ 可编辑 |
| `IDENTITY.md` | 身份说明 | ✅ 只读 |
| `README.md` | 项目说明 | ✅ 可编辑 |

### 1.2 宪法目录 (`constitution/`)
```
constitution/
├── ARCHITECTURE.md          # 架构白皮书
├── CONST-ROUTER.md          # 宪法加载协议
├── CONST-ARCHITECTURE.md    # 架构宪法
├── CONST-LAYERS.md          # 分层宪法
├── CONST-REVISION.md        # 修订宪法
├── COLLABORATION.md         # 多 Bot 协作
├── axiom/                   # 公理层
│   ├── VALUE-FOUNDATION.md  # 价值基石
│   └── MEMORY-PHILOSOPHY.md # 记忆哲学
├── directives/              # 指令层
│   ├── NEGENTROPY.md        # 负熵法则
│   ├── OBSERVER.md          # 观察者协议
│   ├── SELF-LOOP.md         # 自驱动闭环
│   ├── AUTONOMY.md          # 太一独立协议
│   ├── ASK-PROTOCOL.md      # 追问协议
│   └── LEARNING-METHOD.md   # 学习方法
├── skills/                  # 技能层
│   ├── MODEL-ROUTING.md     # 模型调度
│   ├── MULTI-BOT.md         # 多 Bot 协作
│   ├── SKILL-MARKET.md      # 技能市场
│   └── REVIEW-PROCESS.md    # 审查流程
├── quality-gates/           # 质量门禁
│   ├── NEW-SKILL-PRINCIPLES.md  # 新技能八大原则 ⭐
│   ├── ORIGINALITY.md       # 原创性验证
│   └── DISTILLATION.md      # 蒸馏协议
├── modules/                 # 模块层
│   ├── AGI-FLYWHEEL-PLAN.md # AGI 飞轮计划
│   └── ...
├── extensions/              # 扩展层
│   └── DELEGATION.md        # 任务委派协议
└── principles/              # 原则层
    └── ...
```

### 1.3 技能目录 (`skills/`)
```
skills/
├── taiyi/                   # 太一核心技能
│   ├── daily-routine.sh
│   ├── daily-memory-consolidate.sh
│   ├── self-check.sh
│   ├── shutdown.sh
│   ├── agent-diary.md
│   ├── skill-market-plan.md
│   ├── skill-pricing-model.md
│   ├── email_sender.py
│   ├── habit_learning.py
│   ├── skill-evaluation-checklist.md  ⭐
│   └── model-router/        # 模型路由
├── zhiji/                   # 知几（量化交易）
│   ├── strategy_v21.py
│   ├── polymarket_client.py
│   ├── x-auto-poster.py
│   ├── x-polymarket-poster.py
│   ├── x-poster.py
│   ├── x-quick-post.py
│   ├── telegram-notifier.py
│   ├── telegram-notifier-v2.py
│   ├── monitor.py
│   ├── whale_tracker.py
│   ├── autoresearch.py
│   ├── auto-publish-plan.md
│   └── terminal-*.md
├── shanmu/                  # 山木（内容创意）
│   └── ...
├── suwen/                   # 素问（技术开发）
│   ├── service-catalog.md
│   └── ...
├── wangliang/               # 罔两（数据/CEO）
│   └── ...
├── feishu/                  # 飞书集成
├── polymarket/              # Polymarket 工具
├── weather/                 # 天气技能
├── web/                     # Web 工具
├── wechat/                  # 微信集成
└── ssh/                     # SSH 工具
```

### 1.4 记忆系统 (`memory/`)
```
memory/
├── 2026-03-22.md            # 启动日记录
├── 2026-03-23.md            # 独立日记录
├── 2026-03-24.md            # 今日记录 ⭐
├── 2026-03-22-cad-project.md
├── 2026-03-22-polymarket-task.md
├── 2026-03-23-api-management.md
├── 2026-03-23-claude-api-guide.md
├── cross-border-products.md
└── ... (专题记忆)
```

### 1.5 内容目录 (`content/`)
```
content/
├── wechat_first_post.md     # 公众号首篇
├── wechat_7_scenarios.md    # 公众号 7 场景
├── xiaohongshu/             # 小红书内容
│   └── day1_wallpaper.md
├── email/                   # 邮件内容
│   └── daily_report_*.html
└── ...
```

### 1.6 日志目录 (`logs/`)
```
logs/
├── daily-report-*.md        # 日报
├── cron-*.log               # 定时任务日志
└── ...
```

---

## 🔐 2. 敏感配置 (~/.taiyi/)

**权限：** 600（仅所有者可读写）

```
.taiyi/
├── accounts/                # 账号配置
│   ├── README.md
│   ├── polymarket.json      # Polymarket 账户
│   ├── social-media.json    # 社交媒体账号
│   ├── feishu.json          # 飞书应用
│   ├── email.json           # 邮件配置
│   └── api-keys.json        # API 凭证
├── memos/                   # MemOS 记忆系统 ⭐
│   ├── memos_scheduler.py   # 核心调度器
│   ├── auto-extract.py      # 自动提炼器
│   ├── integration-plan.md  # 融合计划
│   ├── index.json           # 记忆索引
│   ├── tasks/               # 任务记忆
│   ├── skills/              # 技能记忆
│   ├── knowledge/           # 知识记忆
│   └── agents/              # Bot 共享记忆
├── x/                       # X 平台配置
│   ├── config.json
│   └── authorization.json   # 自动发布授权 ⭐
├── zhiji/                   # 知几配置
│   ├── config.json
│   ├── telegram.json
│   ├── telegram-config.json
│   └── metamask-config.json # MetaMask 钱包 ⭐
├── model-router/            # 模型路由
│   └── config.json
├── wechat-assistant/        # 微信助手
│   └── config.json
├── wallet/                  # 钱包配置
│   └── polygon_wallet.json
└── moltbook/                # Moltbook 配置
```

---

## ⏰ 3. 定时任务 (crontab)

### 太一定时任务
| 时间 | 任务 | 脚本 |
|------|------|------|
| **06:00** | 行动汇总 | `echo "太一行动汇总时间"` |
| **07:00** | 晨间汇报 + 气象采集 | `zhiji-cron.sh` |
| **09:00** | 晨间检查 | `echo "太一晨间检查时间"` |
| **12:00** | 午间进度 | `echo "太一午间进度时间"` |
| **17:00** | 晚间检查 | `echo "太一晚间检查时间"` |
| **23:00** | Agent 日记 + 记忆提炼 | `daily-memory-consolidate.sh` |
| **00:00** | 自主行动 | `echo "太一自主行动时间"` |

### 知几-E 定时任务
| 时间 | 任务 | 脚本 |
|------|------|------|
| **07:00** | 气象数据采集 | `zhiji-cron.sh` |
| **08:00** | X 早报发布 | `x-auto-poster.py --type morning` |
| **10:00** | X 交易信号 | `x-auto-poster.py --type signal --auto` |
| **15:00** | X 收益报告 | `x-auto-poster.py --type pnl --auto` |
| **18:00** | X 日报 + 公众号邮件 | `x-auto-poster.py --type daily --auto` |
| **22:00** | X 复盘 | `x-auto-poster.py --type review --auto` |

### 系统维护任务
| 时间 | 任务 | 频率 |
|------|------|------|
| **每 5 分钟** | 同步今日数据 | `sync-today.sh` |
| **每 10 分钟** | 自动自愈通讯 | `auto-heal-comms.sh` |
| **每日 03:00** | 微信清理 | `weixin-cleanup.sh` |

---

## 🧠 4. 双记忆系统

### 4.1 传统记忆 (`~/.openclaw/workspace/memory/`)
- **用途：** 人类可读的 Markdown 记录
- **格式：** `YYYY-MM-DD.md`
- **更新：** 每日 23:00 自动归档
- **检索：** 关键词匹配
- **优点：** 易读、易编辑、易分享

### 4.2 MemOS 记忆 (`~/.taiyi/memos/`) ⭐
- **用途：** 机器可读的结构化记忆
- **格式：** JSON（索引 + 分类存储）
- **更新：** 对话中自动提炼
- **检索：** 毫秒级语义检索
- **优点：** 快速、精准、可注入

### 记忆流向
```
对话 → 自动提炼 → MemOS (结构化)
  ↓
每日 23:00 归档
  ↓
memory/YYYY-MM-DD.md (人类可读)
  ↓
每月回顾 → MEMORY.md (长期记忆)
```

---

## 🤖 5. 多 Bot 架构

| Bot | 职责 | 配置位置 | 技能目录 |
|------|------|---------|---------|
| **太一** | 统筹/决策 | `~/.taiyi/` | `skills/taiyi/` |
| **知几** | 量化交易 | `~/.taiyi/zhiji/` | `skills/zhiji/` |
| **山木** | 内容创意 | `~/.taiyi/shanmu/` | `skills/shanmu/` |
| **素问** | 技术开发 | `~/.taiyi/suwen/` | `skills/suwen/` |
| **罔两** | 数据/CEO | `~/.taiyi/wangliang/` | `skills/wangliang/` |
| **庖丁** | 预算成本 | `~/.taiyi/paoding/` | `skills/paoding/` |

---

## 🔗 6. 外部集成

### 6.1 社交媒体
| 平台 | 账号 | 配置 | 状态 |
|------|------|------|------|
| **Telegram** | @sayelf_bot (太一) | `~/.taiyi/accounts/social-media.json` | ✅ |
| **Telegram** | @sayelf_bot (知几) | `~/.taiyi/zhiji/telegram.json` | ✅ |
| **X (Twitter)** | @SayelfTea | `~/.taiyi/x/authorization.json` | ✅ 自动 |
| **微信个人号** | sayelf-tea | `~/.taiyi/wechat-assistant/` | ✅ |
| **微信公众号** | SAYELF 山野精灵 | `~/.md2wechat/config.json` | ✅ |
| **小红书** | AI 缪斯｜龙虾研究所 | `~/.taiyi/accounts/social-media.json` | 🟡 |
| **小红书** | SAYELF 山野精灵 | `~/.taiyi/accounts/social-media.json` | 🟡 |
| **视频号** | SAYELF 山野精灵 | `~/.taiyi/accounts/social-media.json` | 🟡 |

### 6.2 交易/金融
| 平台 | 配置 | 状态 |
|------|------|------|
| **Polymarket** | `~/.taiyi/accounts/polymarket.json` | ✅ |
| **MetaMask** | `~/.taiyi/zhiji/metamask-config.json` | ✅ |
| **钱包地址** | `0x2b45165959433831d9009716A15367421D6c97C9` | ✅ |

### 6.3 开发/部署
| 工具 | 配置 | 状态 |
|------|------|------|
| **GitHub** | `~/.ssh/` | ✅ |
| **飞书** | `~/.taiyi/accounts/feishu.json` | ✅ |
| **CAD 工具** | LibreCAD + FreeCAD | ✅ |

---

## 📋 7. 文档存储规范

### ✅ 正确位置
| 文档类型 | 存储位置 | 示例 |
|---------|---------|------|
| **身份/宪法** | `~/.openclaw/workspace/` | `SOUL.md`, `AGENTS.md` |
| **技能代码** | `~/.openclaw/workspace/skills/` | `skills/zhiji/strategy_v21.py` |
| **记忆记录** | `~/.openclaw/workspace/memory/` | `memory/2026-03-24.md` |
| **敏感凭证** | `~/.taiyi/` (权限 600) | `~/.taiyi/accounts/polymarket.json` |
| **MemOS 记忆** | `~/.taiyi/memos/` | `~/.taiyi/memos/tasks/` |
| **内容草稿** | `~/.openclaw/workspace/content/` | `content/wechat_first_post.md` |
| **日志文件** | `~/.openclaw/workspace/logs/` | `logs/daily-report-*.md` |

### ❌ 错误位置（避免）
| 错误做法 | 正确做法 |
|---------|---------|
| 凭证明文写在代码里 | → 存 `~/.taiyi/` + 环境变量 |
| 记忆写在对话里不归档 | → 每日 23:00 写入 `memory/` |
| 配置文件散落在各处 | → 集中到 `~/.taiyi/` |
| 技能代码放在根目录 | → 放到 `skills/{bot}/` |
| 日志直接输出到屏幕 | → 写入 `logs/` 目录 |

---

## 🛡️ 8. 安全规范

### 文件权限
| 文件类型 | 权限 | 说明 |
|---------|------|------|
| **敏感凭证** | 600 | `~/.taiyi/accounts/*.json` |
| **API Keys** | 600 | `~/.taiyi/zhiji/config.json` |
| **钱包配置** | 600 | `~/.taiyi/zhiji/metamask-config.json` |
| **技能代码** | 755 | `*.sh`, `*.py` (可执行) |
| **文档配置** | 644 | `*.md`, `*.json` (只读) |

### 备份策略
| 内容 | 备份频率 | 备份位置 |
|------|---------|---------|
| **工作空间** | 每日 | Git 提交 + 本地备份 |
| **敏感凭证** | 手动 | 加密 U 盘 |
| **记忆文件** | 实时 | Git + 飞书文档 |
| **配置文件** | 每周 | Git 提交 |

---

## 📊 9. 性能指标

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| **上下文大小** | <50K tokens | ~100K | 🟡 |
| **MemOS 检索** | <100ms | <50ms | ✅ |
| **记忆复用率** | >50% | ~10% | 🟡 |
| **Bot 共享** | 6 Bot | 0 Bot | 🔴 |
| **Token 节省** | >50% | ~20% | 🟡 |
| **定时任务** | 100% 执行 | 98% | ✅ |

---

## 🎯 10. 关键决策点

### 新增 Skills/Agent/软件
**必须通过八大原则审查：**
1. P1: 蒸馏来源
2. P2: 查看本地
3. P3: 比对差异
4. P4: 取其精华
5. P5: 验证实名
6. P6: 安全评估
7. P7: 系统保护
8. P8: 融合进化

**审查流程：**
- L1 快速（P1-P4）：太一自主
- L2 标准（P1-P6）：告知 SAYELF
- L3 深度（P1-P8）：SAYELF 批准

### 记忆存储决策
| 内容类型 | 存储位置 | 归档频率 |
|---------|---------|---------|
| **对话记录** | MemOS → memory/ | 实时 → 每日 |
| **关键决策** | MEMORY.md | 即时 |
| **技能代码** | skills/ | 版本控制 |
| **配置文件** | ~/.taiyi/ | 变更时 |
| **日志文件** | logs/ | 每日归档 |

---

## 📝 11. 维护清单

### 每日维护
- [ ] 23:00 记忆归档
- [ ] 检查定时任务日志
- [ ] 验证 Bot 状态
- [ ] 检查磁盘空间

### 每周维护
- [ ] 备份敏感凭证
- [ ] 清理临时文件
- [ ] 更新依赖包
- [ ] 审查安全日志

### 每月维护
- [ ] 系统更新
- [ ] 技能审查
- [ ] 记忆整理
- [ ] 性能优化

---

## 🔗 12. 相关文档

- `SOUL.md` - 身份锚点
- `AGENTS.md` - 工作台说明
- `constitution/ARCHITECTURE.md` - 架构白皮书
- `constitution/quality-gates/NEW-SKILL-PRINCIPLES.md` - 新技能八大原则
- `~/.taiyi/memos/integration-plan.md` - MemOS 融合计划

---

*创建时间：2026-03-24 23:54 | 版本：v2.0 | 下次审查：2026-04-24*

*「架构是活的，随系统进化而更新」*
