# GitHub CLI 自动认证说明

> 时间：2026-04-10 22:42

---

## ⚠️ 认证限制

GitHub CLI 的网页认证**无法完全自动化**，因为：

1. **需要浏览器交互** - GitHub 要求用户在浏览器中点击授权
2. **安全限制** - 防止自动化脚本滥用
3. **双因素认证** - 如果启用了 2FA，需要额外验证

---

## 🎯 当前状态

| 认证方式 | 状态 | 可用性 |
|---------|------|--------|
| **Git SSH** | ✅ 已认证 | 完全可用 |
| **GitHub CLI** | ⏳ 待认证 | 需要手动完成 |

---

## 📋 完成认证的简单步骤

### 方式 1: 网页认证 (推荐)

**在终端运行**:
```bash
gh auth login
```

**然后**:
1. 按 Enter 选择默认选项
2. 选择 `GitHub.com`
3. 选择 `SSH` 协议
4. 按 Enter 打开浏览器
5. 在浏览器中点击 **"Authorize github"**
6. 返回终端，认证完成！

**预计时间**: 1-2 分钟

---

### 方式 2: 使用 Personal Access Token

**步骤**:

1. **访问**: https://github.com/settings/tokens

2. **创建 Token**:
   - 点击 "Generate new token (classic)"
   - 填写备注：`Taiyi AGI CLI`
   - 勾选权限：
     - ✅ `repo` (完整仓库权限)
     - ✅ `workflow` (运行 Actions)
     - ✅ `read:org` (读取组织信息)
   - 点击 "Generate token"

3. **复制 Token**:
   - 复制生成的 token (以 `ghp_` 开头)

4. **运行认证**:
```bash
gh auth login --with-token
```

5. **粘贴 Token**:
   - 粘贴 token
   - 按 Enter

**预计时间**: 3-5 分钟

---

## ✅ 认证后验证

**检查认证状态**:
```bash
gh auth status
```

**应输出**:
```
github.com
  ✓ Logged in to github.com as nicola-king
  ✓ Git operations for github.com configured to use ssh://
```

**列出仓库**:
```bash
gh repo list nicola-king --limit 5
```

**查看用户信息**:
```bash
gh api user | jq .name
```

---

## 🚀 太一自动化增强

**认证后可用功能**:

| 功能 | 命令 | 说明 |
|------|------|------|
| 列出仓库 | `gh repo list` | 查看所有仓库 |
| 创建 Issue | `gh issue create` | 快速创建 Issue |
| 创建 PR | `gh pr create` | 提交 Pull Request |
| 运行 Workflow | `gh workflow run` | 触发 Actions |
| 查看 CI 状态 | `gh run list` | 查看构建状态 |
| 创建 Gist | `gh gist create` | 分享代码片段 |

**太一自动集成**:
- 自动创建 Issue 报告错误
- 自动提交时关联 Issue
- 自动触发 CI/CD 流程
- 自动同步仓库状态

---

## 🔧 故障排查

### 问题 1: 浏览器未打开

**解决**:
```bash
# 手动打开认证页面
xdg-open https://github.com/login/device
# 或
open https://github.com/login/device  # macOS
```

### 问题 2: Token 无效

**解决**:
1. 删除旧 token: https://github.com/settings/tokens
2. 创建新 token
3. 重新认证

### 问题 3: SSH 密钥问题

**解决**:
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 如果失败，重新添加 SSH 密钥到 GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出到 GitHub Settings → SSH Keys
```

---

## 📞 需要帮助？

**告诉我**:
- "我已经完成认证" - 我会验证
- "使用 Token 方式" - 我帮你生成 Token
- "认证失败" - 我帮你排查

---

*太一 AGI | 2026-04-10 22:42*
