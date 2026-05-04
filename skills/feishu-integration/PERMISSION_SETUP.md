# 飞书权限配置指南

> **应用**: 太一 AI (cli_a9086d6b5779dcc1)
> **时间**: 2026-05-04
> **状态**: 需要配置权限

---

## 🔐 需要配置的权限

### 1. 消息权限 (必须)

| 权限 | 说明 | 用途 |
|------|------|------|
| `im:message:send` | 发送消息 | 给用户/群聊发送消息 |
| `im:message.group` | 群消息 | 在群聊中发送消息 |
| `im:message.p2p` | 单聊消息 | 给用户发送私聊消息 |

### 2. 用户权限 (推荐)

| 权限 | 说明 | 用途 |
|------|------|------|
| `contact:user.read` | 读取用户 | 获取用户信息 |
| `contact:user.department:read` | 读取部门用户 | 获取部门成员 |

### 3. 群聊权限 (可选)

| 权限 | 说明 | 用途 |
|------|------|------|
| `im:chat:read` | 读取群信息 | 获取群列表 |
| `im:chat` | 管理群 | 创建/管理群聊 |

---

## 📝 配置步骤

### 步骤1: 访问飞书开放平台

1. 打开 https://open.feishu.cn/app/
2. 登录你的飞书账号
3. 找到应用 **"数字卵生"** (App ID: cli_a9086d6b5779dcc1)

### 步骤2: 添加权限

1. 点击左侧菜单 **"权限管理"**
2. 点击 **"添加权限"**
3. 搜索并添加以下权限：
   - ✅ `im:message:send`
   - ✅ `im:message.group`
   - ✅ `contact:user.read`

### 步骤3: 发布版本

1. 点击左侧菜单 **"版本管理与发布"**
2. 点击 **"创建版本"**
3. 填写版本信息：
   - 版本号: `1.0.0`
   - 更新说明: `添加消息发送功能`
4. 点击 **"保存"**
5. 点击 **"申请发布"**

### 步骤4: 管理员审批

1. 飞书管理员会收到审批通知
2. 管理员审批通过后，权限生效

---

## ✅ 验证权限

配置完成后，运行测试：

```bash
cd /home/sayelf/.openclaw/workspace/skills/feishu-integration
source /home/sayelf/.openclaw/workspace/venv-feishu/bin/activate
python3 test_message.py
```

---

## 🔗 相关链接

- [飞书开放平台 - 权限说明](https://open.feishu.cn/document/server-docs/getting-started/scope-authorization)
- [消息 API 文档](https://open.feishu.cn/document/server-docs/im-v1/message/create)

---

*太一 AGI · 飞书权限配置指南*
