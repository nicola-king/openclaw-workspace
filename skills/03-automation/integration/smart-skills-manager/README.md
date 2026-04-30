# Smart Skills Manager - 使用指南

> 版本：v1.0 | 创建：2026-04-03 22:17 | 更新：2026-04-03 22:51

---

## 🎯 快速开始

### 安装新技能

```bash
# 从 ClawHub 安装
cd /home/nicola/.openclaw/workspace/skills/smart-skills-manager
./scripts/install-skill.sh clawhub <skill-name>

# 从 GitHub 安装
./scripts/install-skill.sh github https://github.com/user/openclaw-skill-x

# 从本地安装
./scripts/install-skill.sh local /path/to/skill
```

### 更新技能

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

---

## 📁 模块说明

| 模块 | 职责 | 负责 Bot |
|------|------|---------|
| **discovery** | 技能发现 (ClawHub/GitHub) | 守藏吏 |
| **security** | 安全扫描 + 兼容性检查 | 素问 |
| **creator** | 技能模板生成 + 质量门禁 | 太一/素问 |
| **self-improve** | 性能监控 + 优化建议 | 太一/素问 |
| **workflows** | 工作流注册 + 执行追踪 | 太一/守藏吏 |

---

## 🔧 脚本说明

| 脚本 | 用途 | 状态 |
|------|------|------|
| `scripts/install-skill.sh` | 技能安装 (支持 ClawHub/GitHub/本地) | ✅ 已完成 |
| `scripts/update-skill.sh` | 技能更新 (单个/全部) | ✅ 已完成 |
| `scripts/health-check.sh` | 技能健康检查 + 报告生成 | ✅ 已完成 |

---

## 📊 整合的 5 个社区 Skills

| 原 Skill | 自建模块 | 状态 |
|---------|---------|------|
| self-improving-agent | `modules/self-improve/` | ✅ 已实现 |
| skill-creator | `modules/creator/` | ✅ 已实现 (增强版) |
| find-vetter | `modules/discovery/` | ✅ 已实现 |
| skills-vetter | `modules/security/` | ✅ 已实现 |
| automation-workflows | `modules/workflows/` | ✅ 已实现 |

**整合优势**:
1. ✅ 统一架构 - 5 个模块统一管理
2. ✅ 深度集成 - 与现有 8 Bot 协作
3. ✅ 自主可控 - 不依赖外部维护
4. ✅ 持续进化 - 自我优化机制

---

## 📈 技能健康统计

**首次检查** (2026-04-03 22:50):

| 指标 | 数值 |
|------|------|
| 总技能数 | 70 |
| 健康 | 53 ✅ |
| 警告 | 2 🟡 |
| 严重 | 14 🔴 |
| 健康率 | 75.7% |

**已修复**:
- ✅ flowsint-integration (缺少 SKILL.md)
- ✅ gmgn (缺少 SKILL.md)
- ✅ gumroad (缺少 SKILL.md)
- ✅ marketplace (缺少 SKILL.md)

**待修复**: 10 个技能 (主要是系统自带技能，不影响使用)

---

## 📝 使用案例

### 案例 1: 发现并安装新技能

```bash
# 1. 搜索 ClawHub
python3 modules/discovery/clawhub-search.py weather

# 2. 发现感兴趣的技能后，安全扫描
python3 modules/security/security-scan.py /tmp/skill-candidate

# 3. 安装技能
./scripts/install-skill.sh clawhub weather-plus

# 4. 质量门禁
python3 modules/creator/quality-gate.py skills/weather-plus

# 5. 测试运行
cd skills/weather-plus && python3 collector.py

# 6. 性能监控 (一周后)
python3 modules/self-improve/optimization-suggest.py weather-plus
```

### 案例 2: 创建自定义技能

```bash
# 1. 使用模板生成器
python3 modules/creator/template-generator.py --type collector --name crypto-price

# 2. 编辑 SKILL.md 和 collector.py
cd skills/crypto-price
# 编辑文件...

# 3. 质量门禁检查
python3 modules/creator/quality-gate.py skills/crypto-price

# 4. 提交 Git
git add skills/crypto-price
git commit -m "feat: 创建 crypto-price 技能"
git push
```

### 案例 3: 批量更新技能

```bash
# 1. 更新所有技能
./scripts/update-skill.sh --all

# 2. 查看更新报告
cat logs/skill-update.log

# 3. 健康检查验证
./scripts/health-check.sh --all
```

---

## 🔗 相关文档

| 文档 | 说明 |
|------|------|
| `SKILL.md` | 主入口文档 |
| `modules/*/SKILL.md` | 各模块详细说明 |
| `constitution/guarantees/SELF-HEAL.md` | 自愈系统 |
| `constitution/workflows/README.md` | 工作流模板库 |

---

## 📜 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 22:17 | 初始创建 (5 模块 +1 脚本) |
| v1.1 | 2026-04-03 22:51 | 新增 update-skill.sh + health-check.sh |

---

*创建：2026-04-03 22:17 | 更新：2026-04-03 22:51 | 太一 AGI · 智能技能管理系统*
