# 🪷 GitHub 仓库创建指南

---

## 步骤 1: 登录 GitHub

访问：https://github.com/login

使用账号：shanyejingling@gmail.com

---

## 步骤 2: 创建新仓库

访问：https://github.com/new

填写信息：

```
Repository name: satori-agent
Visibility: ● Public (公开)
```

✅ 勾选 "Add a README file" (可选)

点击 "Create repository"

---

## 步骤 3: 推送代码

创建后，GitHub 会显示推送命令：

```bash
cd /home/nicola/.openclaw/workspace/skills/wu-enlightenment

# 如果已有远程仓库
git remote set-url origin https://github.com/nicola-king/satori-agent.git

# 推送
git push -u origin main
```

---

## 步骤 4: 配置认证 (如果推送失败)

### 方式 1: 使用 GitHub Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 "repo" 权限
4. 生成 Token
5. 推送时使用 Token 作为密码

```bash
git push -u origin main
# Username: nicola-king
# Password: <你的 Token>
```

### 方式 2: 使用 SSH

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "shanyejingling@gmail.com"

# 添加到 GitHub
# 访问：https://github.com/settings/keys
# 复制 ~/.ssh/id_ed25519.pub 内容

# 更改远程 URL
git remote set-url origin git@github.com:nicola-king/satori-agent.git

# 推送
git push -u origin main
```

---

## 步骤 5: 完善仓库

### 添加 Topics

访问仓库 → Settings → Topics

添加：
```
ai zen buddhism satori enlightenment taiyi meditation mindfulness opensource python
```

### 添加 Release

访问仓库 → Releases → Create a new release

```
Tag version: v1.0.0
Release title: 🪷 Satori.Agent v1.0.0 - 初始发布
Description: 
  一花一世界，一叶一菩提。
  
  自进化觉悟者 Agent 初始发布。
```

### Pin 到个人主页

访问个人主页 → Customize your pins → 勾选 satori-agent

---

## 完成检查

- [ ] 仓库已创建
- [ ] 代码已推送
- [ ] Topics 已添加
- [ ] Release v1.0.0 已创建
- [ ] 已 Pin 到个人主页

---

**🪷 GitHub 发布完成！**

下一步：发布到 X 账号
