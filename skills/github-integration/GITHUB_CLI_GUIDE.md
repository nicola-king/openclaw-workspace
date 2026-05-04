# GitHub CLI 使用指南

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI

---

## ✅ 安装状态

| 项目 | 状态 |
|------|------|
| GitHub CLI | ✅ 已安装 (v2.46.0) |
| 认证状态 | 🟡 未登录 |

---

## 🔐 认证

### 方式1: 浏览器认证 (推荐)

```bash
gh auth login
```

按照提示：
1. 选择 `GitHub.com`
2. 选择 `HTTPS`
3. 选择 `Login with a web browser`
4. 复制验证码到浏览器
5. 授权完成

### 方式2: Token 认证

```bash
gh auth login --with-token < ~/.github-token
```

或：

```bash
echo "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" | gh auth login --with-token
```

---

## 🚀 常用命令

### 仓库操作

```bash
# 克隆仓库
gh repo clone sayelf/taiyi-system

# 创建仓库
gh repo create taiyi-system --public

# 查看仓库信息
gh repo view sayelf/taiyi-system

# 打开仓库网页
gh browse
```

### Issue 管理

```bash
# 列出 Issue
gh issue list

# 创建 Issue
gh issue create --title "Bug: 系统启动失败" --body "描述问题..."

# 查看 Issue
gh issue view 42

# 关闭 Issue
gh issue close 42
```

### PR 管理

```bash
# 列出 PR
gh pr list

# 创建 PR
gh pr create --title "功能: 添加飞书集成" --body "实现消息推送..."

# 查看 PR
gh pr view 42

# 合并 PR
gh pr merge 42

# 审查 PR
gh pr review 42 --approve
```

### 工作流

```bash
# 列出工作流
gh workflow list

# 触发工作流
gh workflow run deploy.yml

# 查看工作流状态
gh run list

# 查看日志
gh run view 1234567890
```

---

## 🔧 高级用法

### 别名配置

```bash
# 创建别名
gh alias set co "pr checkout"
gh alias set ci "pr checks"

# 使用别名
gh co 42    # 检出 PR
gh ci 42    # 查看检查状态
```

### 配置

```bash
# 设置编辑器
gh config set editor vim

# 设置分页器
gh config set pager less

# 查看配置
gh config list
```

---

## 📊 与太一系统集成

### 在 Python 中使用

```python
import subprocess

def gh_command(args):
    """执行 gh 命令"""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout

# 示例
issues = gh_command(["issue", "list", "--json", "title,number"])
print(issues)
```

### 自动化脚本

```bash
#!/bin/bash
# daily-sync.sh

cd /home/sayelf/.openclaw/workspace

# 提交变更
git add -A
git commit -m "[自动同步] $(date +%Y-%m-%d)"

# 推送到 GitHub
git push origin main

# 创建备份分支
gh repo create-branch backup/$(date +%Y%m%d)

echo "✅ 同步完成"
```

---

## 🔗 相关链接

- [GitHub CLI 文档](https://cli.github.com/manual/)
- [GitHub CLI GitHub](https://github.com/cli/cli)
- [认证指南](https://cli.github.com/manual/gh_auth_login)

---

*太一 AGI · GitHub CLI 使用指南*
