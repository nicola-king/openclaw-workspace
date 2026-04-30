# 通讯智能自动化配置

> 创建：2026-03-28 22:37
> 状态：需要配置环境变量

---

## 🔑 配置项

### 飞书 (Feishu)

```bash
export FEISHU_APP_ID="cli_a9086d6b5779dcc1"
export FEISHU_APP_SECRET="tXHOop03ZHQynCRuEPkambASNori3KhZ"
```

**状态**: ✅ 已有配置 (MEMORY.md)

---

### 微信 (WeChat)

```bash
export WECHAT_APP_ID="wx720a4c489fec9df3"
export WECHAT_APP_SECRET="94066275ad79af78b29b3c5f1ef7660c"
```

**状态**: ✅ 已配置 (2026-04-01 14:10 确认)

**AppSecret**: `94066275ad79af78b29b3c5f1ef7660c`

**待完成**:
- 🔴 IP 白名单配置（需 SAYELF 扫码）
  - 添加 IP: `106.92.155.1` (当前出口)
  - 添加 IP: `103.172.182.26` (服务器公网)

**详细指南**: `WECHAT-SETUP.md`

---

### Telegram

```bash
export TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
```

**状态**: ✅ 已有配置 (太一 Bot)

---

## 📋 配置步骤

### Step 1: 添加到 ~/.bashrc

```bash
cat >> ~/.bashrc << 'EOF'

# 通讯智能自动化配置 (太一 AGI)
export FEISHU_APP_ID="cli_a9086d6b5779dcc1"
export FEISHU_APP_SECRET="tXHOop03ZHQynCRuEPkambASNori3KhZ"
export WECHAT_APP_ID="wx720a4c489fec9df3"
export WECHAT_APP_SECRET="待获取"
export TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
EOF
```

---

### Step 2: 应用配置

```bash
source ~/.bashrc
```

---

### Step 3: 验证配置

```bash
env | grep -E "FEISHU|WECHAT|TELEGRAM"
```

**预期输出**:
```
FEISHU_APP_ID=cli_a9086d6b5779dcc1
FEISHU_APP_SECRET=tXHOop03ZHQynCRuEPkambASNori3KhZ
WECHAT_APP_ID=wx720a4c489fec9df3
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
```

---

### Step 4: 测试通讯路由器

```bash
python3 ~/.openclaw/workspace/skills/taiyi/smart-communication/smart_communication.py
```

---

## 📊 配置状态追踪

| 渠道 | App ID | App Secret | 环境变量 | 测试状态 |
|------|--------|-----------|---------|---------|
| 飞书 | ✅ | ✅ | 🟡 待配置 | 🟡 待测试 |
| 微信 | ✅ | ❌ 待获取 | 🟡 待配置 | 🔴 不可用 |
| Telegram | ✅ | - | 🟡 待配置 | 🟡 待测试 |

---

*创建时间：2026-03-28 22:37*
*太一 AGI · 通讯智能自动化*
