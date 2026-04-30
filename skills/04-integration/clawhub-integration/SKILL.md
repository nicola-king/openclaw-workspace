# ClawHub 技能市场集成

> **版本**: 1.0.0  
> **创建时间**: 2026-04-10 20:35  
> **灵感**: OpenClaw ClawHub 技能市场  
> **GitHub**: https://github.com/openclaw/skills

---

## 🎯 职责域

**核心功能**: 自主"逛街"安装技能

**工作流程**:
```
1. 访问 ClawHub 技能市场
2. 浏览可用技能
3. 分析技能价值
4. 自主决定安装
5. 自动安装技能
6. 验证技能功能
```

---

## 🔧 使用方式

### 方式 1: 命令行

```bash
# 浏览技能市场
python3 skills/clawhub-integration/browse.py

# 安装技能
python3 skills/clawhub-integration/install.py <skill-name>

# 自动逛街 (自主安装)
python3 skills/clawhub-integration/auto-shop.py
```

### 方式 2: API 调用

```python
from clawhub_integration import ClawHub

clawhub = ClawHub()

# 浏览技能
skills = clawhub.browse()

# 安装技能
clawhub.install('browser-automation')

# 自主逛街
clawhub.auto_shop()
```

---

## 📊 技能筛选标准

### 自动安装标准 (满足任一)

- ⭐ Stars > 1000
- 📥 Downloads > 100
- 🆕 24 小时内更新
- 🔥 热门趋势上升
- 💡 太一急需功能

### 需要审批标准

- ⭐ Stars 100-1000
- 📥 Downloads 10-100
- 🧪 实验性技能
- ⚠️ 需要 API Key

### 拒绝标准

- ⭐ Stars < 100
- ❌ 3 个月未更新
- ⚠️ 安全评分低
- 🚫 与现有技能冲突

---

## 🎯 与太一集成

### 自进化触发器

```python
# 每 15 分钟检查一次
if need_new_skill():
    clawhub.auto_shop()
```

### GitHub 榜单追踪

```python
# 自动追踪 10k+ stars 项目
github_trending = clawhub.get_trending(min_stars=10000)
for repo in github_trending:
    if suitable_for_taiyi(repo):
        clawhub.install(repo['name'])
```

---

## 📋 已安装技能

| 技能 | 安装时间 | 状态 | 用途 |
|------|---------|------|------|
| browser-automation | 2026-04-10 | ✅ | 浏览器自动化 |
| self-improving-agent | 2026-04-10 | ✅ | 自我进化 |
| agent-reach | 2026-04-10 | ✅ | 深度信息嗅探 |

---

## 🚀 下一步

- [ ] 集成 GitHub AI Agent 榜单
- [ ] 自动分析 10k+ stars 项目
- [ ] 自主"逛街"安装技能
- [ ] 技能质量评估系统

---

*太一 AGI · ClawHub 技能市场集成*  
*创建时间：2026-04-10 20:35*  
*原则：自主逛街，按需安装*
