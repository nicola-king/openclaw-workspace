# 微信 AppSecret 获取指南

> 创建：2026-03-28 22:40
> 状态：需要手动操作 (5 分钟)

---

## 🎯 目标

获取微信公众号 AppSecret，完成通讯智能自动化配置。

---

## 📋 操作步骤

### Step 1: 登录微信公众平台

**网址**: https://mp.weixin.qq.com

**账号**: 
- 登录邮箱：`285915125@qq.com`
- 公众号：SAYELF 山野精灵 (`gh_69b1169c64f7`)

---

### Step 2: 进入基本配置

**路径**: 
```
登录 → 左侧菜单"开发" → 基本配置
```

---

### Step 3: 获取 AppSecret

**操作**:
1. 找到 **AppSecret(小程序密钥)**
2. 点击 **"重置"** 或 **"查看"**
3. 使用管理员微信扫码确认
4. 复制 AppSecret (32 位字符串)

**注意**: 
- AppSecret 只显示一次，立即保存！
- 如已重置，旧 Secret 立即失效

---

### Step 4: 更新配置

**方法 1: 直接添加到 ~/.bashrc**

```bash
# 编辑 ~/.bashrc
nano ~/.bashrc

# 找到这一行，替换"待获取"为实际 Secret
export WECHAT_APP_SECRET="实际 Secret 值"

# 保存并应用
source ~/.bashrc
```

**方法 2: 使用 sed 替换**

```bash
# 替换配置
sed -i 's/WECHAT_APP_SECRET="待获取"/WECHAT_APP_SECRET="实际 Secret 值"/' ~/.bashrc

# 应用
source ~/.bashrc
```

---

### Step 5: 验证配置

```bash
# 检查环境变量
env | grep WECHAT

# 预期输出
WECHAT_APP_ID=wx720a4c489fec9df3
WECHAT_APP_SECRET=实际 Secret 值
```

---

### Step 6: 测试通讯路由器

```bash
cd ~/.openclaw/workspace/skills/taiyi
python3 smart-communication/smart_communication.py
```

**预期输出**:
```
微信 (国内流量):
  App ID: wx720a4c48...
  状态：✅ 已配置
```

---

## 🔑 配置汇总

| 渠道 | App ID | App Secret | 状态 |
|------|--------|-----------|------|
| 飞书 | cli_a9086d6b5779dcc1 | tXHOop03ZHQynCRuEPkambASNori3KhZ | ✅ |
| 微信 | wx720a4c489fec9df3 | 待获取 | 🟡 |
| Telegram | 8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY | - | ✅ |

---

## ⏱️ 预计时间

**5 分钟** (登录 + 获取 + 配置 + 验证)

---

*创建时间：2026-03-28 22:40*
*太一 AGI · 微信配置指南*
