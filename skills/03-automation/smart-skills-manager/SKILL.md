---
name: smart-skills-manager
version: 1.0.0
description: smart-skills-manager skill
category: infrastructure
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Smart Skills Manager - 智能技能管理器

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：守藏吏 (主) / 素问 (辅) / 太一 (统筹)

---

## 🎯 核心定位

**整合 5 个社区 Skills 能力，自建智能自动化管理系统**

| 原 Skill | 自建模块 | 核心能力 |
|---------|---------|---------|
| self-improving-agent | `modules/self-improve/` | 技能性能监控 + 自动优化 |
| skill-creator | `modules/creator/` | 技能模板生成 + 质量门禁 |
| find-vetter | `modules/discovery/` | ClawHub/GitHub 技能发现 |
| skills-vetter | `modules/security/` | 安全扫描 + 兼容性检查 |
| automation-workflows | `modules/workflows/` | 工作流模板 + 执行追踪 |

---

## 📁 文件结构

```
skills/smart-skills-manager/
├── SKILL.md                  # 本文档
├── README.md                 # 使用说明
├── modules/
│   ├── discovery/            # 技能发现模块
│   │   ├── SKILL.md          # 模块说明
│   │   ├── clawhub-search.py # ClawHub 搜索
│   │   └── github-scan.py    # GitHub 扫描
│   ├── security/             # 安全验证模块
│   │   ├── SKILL.md
│   │   ├── security-scan.py  # 安全扫描
│   │   └── compatibility-check.py  # 兼容性检查
│   ├── creator/              # 技能创建模块
│   │   ├── SKILL.md
│   │   ├── template-generator.py  # 模板生成
│   │   └── quality-gate.py   # 质量门禁
│   ├── self-improve/         # 自我优化模块
│   │   ├── SKILL.md
│   │   ├── performance-monitor.py  # 性能监控
│   │   └── optimization-suggest.py # 优化建议
│   └── workflows/            # 工作流管理模块
│       ├── SKILL.md
│       ├── workflow-registry.py    # 工作流注册
│       └── execution-tracker.py    # 执行追踪
└── scripts/
    ├── install-skill.sh      # 技能安装
    ├── update-skill.sh       # 技能更新
    └── health-check.sh       # 健康检查
```

---

## 🤖 Bot 职责分配

### 守藏吏 (主责)
- 技能资源管理
- ClawHub/GitHub 发现
- 技能安装/更新/卸载
- 健康检查执行

### 素问 (辅助)
- 安全扫描 (代码审计)
- 兼容性检查 (依赖/版本)
- 性能监控 (响应时间/错误率)

### 太一 (统筹)
- 质量门禁最终决策
- 优化建议汇总
- 向 SAYELF 汇报

---

## 🔧 核心功能

### 1️⃣ 技能发现 (Discovery)

**来源**:
- ClawHub 技能市场 (https://clawhub.ai)
- GitHub OpenClaw Skills (关键词搜索)
- 社区推荐 (Telegram/Discord)

**命令**:
```bash
# 搜索 ClawHub
clawhub search <keyword>

# 搜索 GitHub
gh search repos openclaw-skill --limit 10
```

**输出**:
```markdown
## 发现新技能

| 技能名 | 来源 | 评分 | 描述 |
|--------|------|------|------|
| skill-x | ClawHub | ⭐⭐⭐⭐ | 描述... |
```

---

### 2️⃣ 安全验证 (Security)

**检查项**:
- [ ] 代码无恶意命令 (rm -rf, curl | bash 等)
- [ ] 无敏感信息泄露 (API Key/密码)
- [ ] 依赖安全 (requirements.txt 审计)
- [ ] 权限合理 (工具调用范围)
- [ ] 与现有系统兼容 (版本/配置)

**工具**:
```python
# security-scan.py
- 正则匹配危险模式
- 依赖漏洞扫描 (pip-audit)
- 权限清单检查
```

**输出**:
```markdown
## 安全扫描报告

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 恶意代码 | ✅ | 未发现 |
| 敏感信息 | ✅ | 未发现 |
| 依赖安全 | 🟡 | 1 个警告 |
| 权限合理 | ✅ | 合理 |
| 兼容性 | ✅ | 兼容 |

**结论**: ✅ 安全 / 🟡 需审查 / 🔴 危险
```

---

### 3️⃣ 技能创建 (Creator)

**模板类型**:
- 数据采集型 (Cron + API)
- 内容生成型 (LLM + 模板)
- 交易执行型 (API + 确认)
- 监控告警型 (轮询 + 通知)
- 工具增强型 (封装外部服务)

**生成流程**:
```
1. 选择模板类型
2. 填写技能元数据 (名称/描述/职责)
3. 生成基础结构 (SKILL.md + 脚本)
4. 质量门禁检查
5. 测试验证
6. 提交 Git
```

**质量门禁**:
- [ ] SKILL.md 符合规范
- [ ] 脚本可执行 (chmod +x)
- [ ] 无语法错误 (python -m py_compile)
- [ ] 有使用说明
- [ ] 有错误处理
- [ ] 有日志记录

---

### 4️⃣ 自我优化 (Self-Improve)

**监控指标**:
| 指标 | 采集方式 | 阈值 |
|------|---------|------|
| 响应时间 | 每次执行记录 | >10s 告警 |
| 错误率 | 日志分析 | >5% 告警 |
| 调用频率 | Cron/触发器统计 | 突增告警 |
| 资源占用 | ps/top | 内存>500MB 告警 |

**优化建议生成**:
```
IF 响应时间 > 10s:
  → 建议：优化算法 / 增加缓存 / 异步执行

IF 错误率 > 5%:
  → 建议：增加重试机制 / 完善错误处理

IF 调用频率突增:
  → 建议：增加限流 / 批量处理
```

---

### 5️⃣ 工作流管理 (Workflows)

**工作流注册**:
```python
# workflow-registry.py
WORKFLOWS = {
    "content-creation": {
        "name": "内容创作工作流",
        "stages": ["选题", "大纲", "草稿", "审核", "发布"],
        "responsible_bot": "山木",
        "template": "constitution/workflows/CONTENT-CREATION.md"
    },
    # ... 其他工作流
}
```

**执行追踪**:
```markdown
## 工作流执行记录

| 工作流 | 阶段 | 开始时间 | 耗时 | 状态 |
|--------|------|---------|------|------|
| content-creation | 发布 | 10:00 | 15m | ✅ 完成 |
```

---

## 📋 使用命令

### 技能安装
```bash
# 从 ClawHub 安装
./scripts/install-skill.sh clawhub <skill-name>

# 从 GitHub 安装
./scripts/install-skill.sh github <repo-url>

# 本地安装
./scripts/install-skill.sh local <path>
```

### 技能更新
```bash
# 更新单个技能
./scripts/update-skill.sh <skill-name>

# 更新所有技能
./scripts/update-skill.sh --all
```

### 健康检查
```bash
# 检查单个技能
./scripts/health-check.sh <skill-name>

# 检查所有技能
./scripts/health-check.sh --all

# 生成报告
./scripts/health-check.sh --report
```

### 技能发现
```bash
# 搜索 ClawHub
python3 modules/discovery/clawhub-search.py <keyword>

# 扫描 GitHub
python3 modules/discovery/github-scan.py <keyword>
```

### 安全扫描
```bash
# 扫描单个技能
python3 modules/security/security-scan.py <skill-path>

# 扫描所有技能
python3 modules/security/security-scan.py --all
```

---

## 📊 技能清单

### 系统自带 Skills
| 技能 | 状态 | 位置 |
|------|------|------|
| weather | ✅ 已安装 | `~/.npm-global/lib/node_modules/openclaw/skills/weather/` |
| github | ✅ 已安装 | `~/.npm-global/lib/node_modules/openclaw/skills/github/` |
| coding-agent | ✅ 已安装 | `~/.npm-global/lib/node_modules/openclaw/skills/coding-agent/` |
| skill-creator | ✅ 已安装 | `~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/` |
| healthcheck | ✅ 已安装 | `~/.npm-global/lib/node_modules/openclaw/skills/healthcheck/` |

### 自定义 Skills
| 技能 | 状态 | 职责 |
|------|------|------|
| self-check | ✅ 已安装 | 系统自检 |
| smart-skills-manager | 🟡 开发中 | 技能管理 |
| gmgn-market | ✅ 已安装 | GMGN 市场数据 |
| gmgn-portfolio | ✅ 已安装 | GMGN 钱包组合 |
| gmgn-swap | ✅ 已安装 | GMGN 交易执行 |
| gmgn-token | ✅ 已安装 | GMGN 代币信息 |
| gmgn-track | ✅ 已安装 | GMGN 链上追踪 |
| qiaomu-info-card-designer | ✅ 已安装 | 信息卡片生成 |
| feishu | ✅ 已安装 | 飞书操作 |
| paoding | ✅ 已安装 | 预算管理 |
| polymarket | ✅ 已安装 | Polymarket 交易 |
| shanmu-reporter | ✅ 已安装 | 研报生成 |
| ssh-control | ✅ 已安装 | SSH 远程控制 |
| suwen | ✅ 已安装 | 技术研究 |
| tianji | ✅ 已安装 | 市场分析 |
| zhiji | ✅ 已安装 | Polymarket 策略 |
| zhiji-sentiment | ✅ 已安装 | 情绪分析 |

**总计**: 17 Skills

---

## 🚨 告警规则

立即通知 SAYELF 当:
- [!] 技能安全扫描发现 🔴 危险
- [!] 技能错误率 >10% 持续 1 小时
- [!] 技能响应时间 >30s
- [!] 技能依赖服务不可用
- [!] 技能配置文件损坏

---

## 📈 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 技能安装时间 | <5 分钟 | 待统计 |
| 安全扫描时间 | <1 分钟/skill | 待统计 |
| 健康检查覆盖率 | 100% | 待统计 |
| 技能更新成功率 | >95% | 待统计 |

---

## 🔄 持续优化

### v1.0 (当前)
- ✅ 基础架构
- ✅ 5 大模块框架
- 🟡 核心脚本开发中

### v1.1 (计划)
- [ ] ClawHub CLI 集成
- [ ] GitHub API 集成
- [ ] 自动化安装流程
- [ ] 性能监控仪表板

### v2.0 (计划)
- [ ] 机器学习优化建议
- [ ] 技能依赖图分析
- [ ] 自动回滚机制
- [ ] 技能市场贡献

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `skills/smart-skills-manager/SKILL.md` | 本文档 |
| `constitution/guarantees/SELF-HEAL.md` | 自愈系统 |
| `constitution/guarantees/CRON-GUARANTEE.md` | Cron 保障 |
| `constitution/workflows/README.md` | 工作流模板 |
| `scripts/skill-heartbeat.sh` | 技能心跳检测 |

---

## 📜 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 | 初始创建 (整合 5 Skills 能力) |

---

*创建：2026-04-03 22:17 | 太一 AGI · 守藏吏主责 · 智能技能管理系统*
