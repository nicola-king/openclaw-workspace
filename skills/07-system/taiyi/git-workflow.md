# 太一 Git 分支管理规范

**版本：** v1.0  
**创建：** 2026-03-25 00:05  
**灵感：** Anthropic Git 工作流  
**参考：** https://github.com/nicola-king/zhiji-e

---

##  分支结构

```
main                    # 生产分支（稳定，随时可部署）
├── develop             # 开发分支（集成功能）
├── feature/            # 功能分支（短期）
│   ├── feature/x-auto-post
│   ├── feature/telegram-notify
│   └── feature/memos-integration
├── experiment/         # 实验分支（探索性）
│   ├── experiment/polymarket-arbitrage
│   ├── experiment/weather-prediction
│   └── experiment/whale-tracking
└── hotfix/             # 紧急修复
    └── hotfix/api-key-rotation
```

---

## 🏷️ 命名规范

### 功能分支
```
feature/{简短描述}-{日期}
feature/x-auto-post-0324
feature/telegram-v2-0325
```

### 实验分支
```
experiment/{策略名}-{版本}
experiment/polymarket-arb-v21
experiment/weather-v10
```

### 紧急修复
```
hotfix/{问题描述}-{日期}
hotfix/api-key-rotation-0324
hotfix/cron-fix-0325
```

### 发布分支
```
release/{版本号}
release/v2.1.0
release/v2.2.0
```

---

## 🔄 工作流

### 新功能开发
```bash
# 1. 从 develop 创建功能分支
git checkout develop
git checkout -b feature/x-auto-post-0324

# 2. 开发功能
git add .
git commit -m "feat: X 平台自动发布"

# 3. 推送到远程
git push origin feature/x-auto-post-0324

# 4. 创建 Pull Request
# 5. 代码审查
# 6. 合并到 develop

# 7. 删除功能分支
git branch -d feature/x-auto-post-0324
```

### 实验性探索
```bash
# 1. 从 develop 创建实验分支
git checkout develop
git checkout -b experiment/polymarket-arb-v21

# 2. 实验开发
# 3. 验证结果

# 成功 → 合并到 develop
git checkout develop
git merge experiment/polymarket-arb-v21

# 失败 → 标记后放弃
git checkout develop
git branch -D experiment/polymarket-arb-v21
```

### 发布流程
```bash
# 1. 创建发布分支
git checkout develop
git checkout -b release/v2.1.0

# 2. 最终测试
# 3. 更新版本号
# 4. 更新 CHANGELOG

# 5. 合并到 main
git checkout main
git merge release/v2.1.0

# 6. 打标签
git tag -a v2.1.0 -m "知几-E v2.1 气象套利"

# 7. 推送标签
git push origin v2.1.0

# 8. 合并回 develop
git checkout develop
git merge release/v2.1.0
```

---

## 📝 Commit 规范

### 格式
```
<类型>(<范围>): <简短描述>

[可选正文]
[可选脚注]
```

### 类型
| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat(x): 添加自动发布 |
| `fix` | 修复 bug | fix(cron): 修复定时任务 |
| `docs` | 文档更新 | docs(readme): 更新安装说明 |
| `style` | 代码格式 | style(python): 格式化代码 |
| `refactor` | 重构 | refact(arch): 重构架构 |
| `test` | 测试 | test(zhiji): 添加单元测试 |
| `chore` | 构建/工具 | chore(deps): 更新依赖 |

### 示例
```bash
# 功能提交
git commit -m "feat(zhiji): 添加 X 平台自动发布功能"

# Bug 修复
git commit -m "fix(cron): 修复气象采集定时任务"

# 文档更新
git commit -m "docs(readme): 添加安装和使用说明"

# 重构
git commit -m "refactor(memos): 优化记忆检索性能"
```

---

## 🎯 分支保护规则

### main 分支
- ✅ 必须通过 CI/CD
- ✅ 至少 1 人审查
- ✅ 禁止直接 push
- ✅ 必须从 release 分支合并

### develop 分支
- ✅ 必须通过 CI/CD
- 🟡 建议审查
- ✅ 从 feature 分支合并

### feature/experiment 分支
- 🟡 可选 CI/CD
- 🟡 可选审查
- ✅ 个人开发

---

## 📊 可视化追踪

### 颜色标记
| 颜色 | 状态 | 说明 |
|------|------|------|
| 🟢 绿色 | 成功 | 已合并到 main |
| 🟡 黄色 | 进行中 | 正在开发 |
| 🔴 红色 | 失败 | 实验失败，已放弃 |
| 🔵 蓝色 | 等待 | 等待审查/测试 |

### 工具推荐
```bash
# Git 图形化
git log --oneline --graph --all

# 安装 git-delta（增强显示）
cargo install git-delta

# VSCode Git Graph 插件
# 可视化分支合并历史
```

---

## 🛡️ 安全规范

### 敏感信息
- ❌ 不在代码中存储 API Key
- ❌ 不在 commit 中存储凭证
- ✅ 使用环境变量
- ✅ 使用 `.taiyi/` 目录（600 权限）

### 代码审查
- ✅ 所有合并到 main 的代码必须审查
- ✅ 检查是否有硬编码密码
- ✅ 检查依赖是否有漏洞
- ✅ 检查是否有危险操作

### 备份策略
- ✅ 每日自动 push 到 GitHub
- ✅ 每周本地备份
- ✅ 每月导出完整仓库

---

## 📋 检查清单

### 创建新分支前
- [ ] 确认分支类型（feature/experiment/hotfix）
- [ ] 从正确分支 checkout（develop/main）
- [ ] 命名符合规范
- [ ] 通知团队成员

### 合并前
- [ ] 代码审查通过
- [ ] 测试通过
- [ ] 无冲突
- [ ] 更新 CHANGELOG
- [ ] 更新版本号

### 合并后
- [ ] 删除旧分支
- [ ] 更新文档
- [ ] 通知相关人员
- [ ] 监控生产环境

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/nicola-king/zhiji-e
- **Git 教程**: https://git-scm.com/book
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Flow**: https://nvie.com/posts/a-successful-git-branching-model/

---

*创建时间：2026-03-25 00:05 | 版本：v1.0 | 下次审查：2026-04-25*

*「分支是思想的轨迹，每次合并都是知识的融合」*
