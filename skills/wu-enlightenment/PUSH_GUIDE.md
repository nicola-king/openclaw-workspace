# 🪷 GitHub 推送认证指南

---

## ⚠️ 当前状态

```
✅ Git 配置完成
✅ 远程仓库已配置
❌ 推送需要认证
```

---

## 🔐 方式 1: 使用 GitHub Token (推荐)

### 步骤 1: 创建 Token

1. 访问：https://github.com/settings/tokens
2. 登录账号：shanyejingling@gmail.com
3. 点击 "Generate new token" → "Generate new token (classic)"
4. 填写 Note: `Satori.Agent Push`
5. 勾选权限：✅ repo (全选)
6. 点击 "Generate token"
7. **复制 Token** (只显示一次，格式：`ghp_xxxxxxxxxxxx`)

### 步骤 2: 使用 Token 推送

```bash
cd /home/nicola/.openclaw/workspace/skills/wu-enlightenment

# 推送
git push -u origin main

# 当提示输入密码时：
# Username: nicola-king
# Password: <粘贴你的 Token>  (粘贴时不会显示)
```

### 步骤 3: 保存认证 (可选)

```bash
# 保存认证凭据
git config --global credential.helper store

# 再次推送 (只需输入一次)
git push -u origin main
```

---

## 🔐 方式 2: 使用 SSH

### 步骤 1: 生成 SSH Key

```bash
ssh-keygen -t ed25519 -C "shanyejingling@gmail.com"
# 一路回车即可
```

### 步骤 2: 添加到 GitHub

1. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. 访问：https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥内容
5. 点击 "Add SSH key"

### 步骤 3: 更改远程 URL

```bash
cd /home/nicola/.openclaw/workspace/skills/wu-enlightenment

# 更改为 SSH
git remote set-url origin git@github.com:nicola-king/satori-agent.git

# 推送
git push -u origin main
```

---

## 📊 推送成功后

访问：https://github.com/nicola-king/satori-agent

确认代码已推送成功。

---

## 🐦 发布到 X

推送成功后，复制以下推文发布到 X：

```
🪷 Satori.Agent (悟.Agent)

一花一世界，一叶一菩提。

开源发布自进化觉悟者 Agent。
每个人的使用，都是独一无二的结果。

🔗 https://github.com/nicola-king/satori-agent

#AI #Zen #Buddhism #Satori #OpenSource #Enlightenment #Taiyi
```

---

**🪷 发布顺利！**
