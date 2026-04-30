# GitHub CLI Token 认证方式

> 时间：2026-04-10 23:11

---

## ⚠️ 网页认证失败

网页认证似乎未完成，可能是因为：
- 浏览器未成功打开
- 认证超时
- 网络问题

---

## 🔑 使用 Token 方式 (推荐)

### 步骤 1: 创建 Personal Access Token

1. **访问**: https://github.com/settings/tokens

2. **点击**: "Generate new token (classic)"

3. **填写信息**:
   - Note: `Taiyi AGI CLI`
   - Expiration: `No expiration` (或选择 1 年)

4. **勾选权限**:
   - ✅ `repo` (完整仓库权限)
   - ✅ `workflow` (运行 Actions)
   - ✅ `read:org` (读取组织信息)
   - ✅ `gist` (创建 Gist)

5. **点击**: "Generate token"

6. **复制 Token**:
   - Token 以 `ghp_` 开头
   - **立即复制**，页面刷新后无法再查看

---

### 步骤 2: 使用 Token 认证

**运行命令**:
```bash
gh auth login --with-token
```

**粘贴 Token**:
```
# 粘贴你的 token (以 ghp_ 开头)
# 按 Enter 完成
```

---

### 步骤 3: 验证认证

```bash
gh auth status
gh repo list nicola-king --limit 5
```

**成功输出**:
```
github.com
  ✓ Logged in to github.com as nicola-king
  ✓ Git operations for github.com configured to use ssh://
```

---

## 🔧 或者告诉我 Token

如果你已经创建了 Token，可以告诉我：
```
我的 GitHub Token 是：ghp_xxxxxxxxxxxx
```

我会帮你完成认证配置！

---

*太一 AGI | 2026-04-10 23:11*
