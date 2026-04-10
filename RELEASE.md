# 太一 AGI 发布规范 · Release Guidelines

> **创建时间**: 2026-04-10  
> **灵感**: OpenClaw v2026.4.9 iOS Version Pinning  
> **版本格式**: CalVer vYYYY.MM.DD[-iteration]

---

## 📋 版本格式

### CalVer (Calendar Versioning)

```
vYYYY.MM.DD[-iteration]
```

**示例**:
| 版本 | 日期 | 说明 |
|------|------|------|
| `v2026.4.10` | 2026-04-10 | 首次发布 |
| `v2026.4.10-1` | 2026-04-10 | 同日第二次发布 |
| `v2026.4.11` | 2026-04-11 | 次日发布 |
| `v2026.4.15-3` | 2026-04-15 | 同日第三次发布 |

---

## 🚀 发布流程

### 标准发布 (每日首次)

```bash
# 1. 完成功能开发
# 2. 运行测试
# 3. 更新 HEARTBEAT.md
# 4. 执行版本脚本
./scripts/git-version.sh

# 5. 生成发布说明 (自动)
# 6. 推送标签 (自动)
```

### 同日多次发布

```bash
# 脚本自动检测并添加 iteration
./scripts/git-version.sh
# 输出：创建版本标签：v2026.4.10-1
```

---

## 📝 发布说明模板

```markdown
# 太一 AGI 发布 · vYYYY.MM.DD[-iteration]

> **发布日期**: YYYY-MM-DD  
> **类型**: [功能发布/修复/安全更新]

## 🎯 核心更新

### 新增功能
- 

### 功能增强
- 

### Bug 修复
- 

### 文档更新
- 

## 📊 统计

| 指标 | 数值 |
|------|------|
| Git 提交 | X 次 |
| 新增文件 | X 个 |
| 代码变更 | X 行 |
| 能力涌现 | X 个 |

## 🙏 致谢

- 灵感来源：OpenClaw v2026.4.9

---

*太一 AGI · 自动发布系统*
```

---

## 🔧 版本管理脚本

### git-version.sh

```bash
#!/bin/bash
# 自动创建 CalVer 版本标签

VERSION="v$(date +%Y.%m.%d)"
ITERATION=1

# 检查今日是否已有标签
while git rev-parse "${VERSION}-${ITERATION}" >/dev/null 2>&1; do
    ITERATION=$((ITERATION + 1))
done

if [ $ITERATION -gt 1 ]; then
    FULL_VERSION="${VERSION}-${ITERATION}"
else
    FULL_VERSION="${VERSION}"
fi

echo "🏷️ 创建版本标签：$FULL_VERSION"
git tag -a "$FULL_VERSION" -m "太一 AGI 发布 $FULL_VERSION"
git push origin "$FULL_VERSION"
echo "✅ 版本发布完成"
```

---

## 📊 版本历史

### 2026-04

| 版本 | 日期 | 类型 | 核心更新 |
|------|------|------|---------|
| v2026.4.10 | 2026-04-10 | 功能 | OpenClaw 4.9 融合 (P0/P1/P2) |

---

## 🎯 版本策略

### 主版本 (Major)
- 年度大版本：`v2026.1.1`
- 架构变更
- 重大功能发布

### 日版本 (Daily)
- 每日功能发布：`v2026.4.10`
- 常规更新
- 功能累积

### 迭代版本 (Iteration)
- 同日多次发布：`v2026.4.10-1`
- 紧急修复
- 快速迭代

---

## 🔍 版本查询

### 查看当前版本

```bash
# 最新标签
git describe --tags --abbrev=0

# 所有版本
git tag -l "v2026.*" | sort -V
```

### 版本对比

```bash
# 两个版本差异
git diff v2026.4.10 v2026.4.10-1

# 版本变更统计
git diff --stat v2026.4.10 v2026.4.10-1
```

---

## 📌 最佳实践

### ✅ 推荐

- 每日最多 1 次主版本发布
- 紧急修复使用 iteration
- 发布前运行完整测试
- 更新 HEARTBEAT.md
- 生成发布说明

### ❌ 避免

- 频繁发布 (每日>3 次)
- 无测试发布
- 无发布说明
- 跳过版本号

---

## 🎨 发布美学

**发布即艺术**:
- 清晰的版本历史
- 规范的发布说明
- 一致的提交信息
- 完整的测试覆盖

---

*文档：太一 AGI · 发布规范*  
*灵感：OpenClaw v2026.4.9 iOS Version Pinning*  
*创建时间：2026-04-10 13:45*
