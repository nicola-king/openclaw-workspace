# 🔐 GitHub 账户配置

> **主账户**: shanyejingling@gmail.com  
> **GitHub 用户名**: nicola-king  
> **配置时间**: 2026-04-12 18:25  
> **状态**: ✅ 已保存

---

## 📊 账户信息

| 项目 | 配置 |
|------|------|
| **GitHub 用户名** | nicola-king |
| **登录邮箱** | shanyejingling@gmail.com |
| **认证方式** | SSH + Token |
| **Git 协议** | SSH |
| **Token 权限** | repo, workflow, admin |
| **Token 过期** | 2026-04-23 |

---

## 🔑 认证配置

**SSH Key**:
```
✅ 已配置：~/.ssh/id_rsa.pub
✅ 已添加到 GitHub: https://github.com/settings/keys
✅ 认证成功：Hi nicola-king! You've successfully authenticated
```

**GitHub CLI**:
```
✅ 已登录：gh auth login
✅ 主机：github.com
✅ 用户：nicola-king (shanyejingling@gmail.com)
```

**Personal Access Token**:
```
✅ Token 1: 太一 AGI CLI 自动化 (read:org, repo)
   - 过期：2026-04-23
   - 最后使用：2 周内

✅ Token 2: 太一 AGI 自动化 (repo, workflow)
   - 过期：2026-04-23
   - 状态：未使用

✅ Token 3: 太一 (admin 权限)
   - 过期：2026-04-15
   - 状态：未使用
```

---

## 🗑️ 已删除/清理的账户

**无其他 GitHub 账户配置**

当前系统仅配置了单一账户：
- ✅ nicola-king (shanyejingling@gmail.com)

---

## 📁 配置文件位置

| 文件 | 路径 |
|------|------|
| GitHub CLI 配置 | `~/.config/gh/hosts.yml` |
| SSH 私钥 | `~/.ssh/id_rsa` |
| SSH 公钥 | `~/.ssh/id_rsa.pub` |
| Git 全局配置 | `~/.gitconfig` |

---

## 🔧 Git 全局配置

```bash
# 查看当前配置
git config --global user.name
git config --global user.email

# 应显示:
# nicola-king
# shanyejingling@gmail.com
```

---

## ✅ 验证命令

**检查 GitHub CLI 认证**:
```bash
gh auth status
```

**检查 SSH 连接**:
```bash
ssh -T git@github.com
# 应显示：Hi nicola-king! You've successfully authenticated
```

**检查 Git 配置**:
```bash
git config --global user.name
git config --global user.email
```

**查看已登录用户**:
```bash
gh api user
```

---

## 🚀 已上线仓库 (9 个)

所有仓库均已推送到 `nicola-king` 账户:

1. ✅ polymarket-trading-agent
2. ✅ gmgn-trading-agent
3. ✅ binance-trading-agent
4. ✅ cross-border-trade-agent
5. ✅ taiyi-voice-agent
6. ✅ taiyi-memory-system-v3
7. ✅ taiyi-education-agent
8. ✅ taiyi-office-agent
9. ✅ taiyi-diagram-agent

**查看**: https://github.com/nicola-king?tab=repositories

---

## 🔐 安全提示

**Token 管理**:
- ✅ Token 存储在安全位置
- ✅ 定期轮换 (每 90 天)
- ✅ 最小权限原则
- ⚠️ Token 3 即将过期 (2026-04-15)

**SSH Key 管理**:
- ✅ 私钥权限：600
- ✅ 已设置密码短语 (可选)
- ✅ 已添加到 GitHub

---

**🔐 GitHub 账户配置已保存：shanyejingling@gmail.com**

**太一 AGI · 2026-04-12**
