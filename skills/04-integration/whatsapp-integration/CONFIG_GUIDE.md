# 📱 WhatsApp 集成配置指南 (后期配备)

> **创建时间**: 2026-04-11  
> **状态**: 后期配备  
> **预计时间**: 40 分钟

---

## 🎯 方案选择

### 方案 1: whatsapp-web.js (推荐)

**优势**:
- ✅ 免费开源
- ✅ 功能完整
- ✅ 无需官方 API
- ✅ 支持二维码登录

**劣势**:
- ⚠️ 需要 Node.js 环境
- ⚠️ 需要定期扫码登录

### 方案 2: Twilio API

**优势**:
- ✅ 官方支持
- ✅ 稳定可靠

**劣势**:
- ❌ 收费
- ❌ 需要申请

### 方案 3: WhatsApp Business API

**优势**:
- ✅ 官方企业 API
- ✅ 支持大规模发送

**劣势**:
- ❌ 需要企业验证
- ❌ 收费较高

---

## ⚙️ 配置步骤 (后期配备)

### 步骤 1: 安装 Node.js

```bash
# 检查是否已安装
node --version

# 如未安装
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 步骤 2: 安装 whatsapp-web.js

```bash
cd /home/nicola/.openclaw/workspace/skills/whatsapp-integration
npm install whatsapp-web.js qrcode-terminal
```

### 步骤 3: 创建配置文件

```bash
mkdir -p ~/.openclaw/workspace/config/whatsapp
cat > ~/.openclaw/workspace/config/whatsapp/config.json << 'EOF'
{
  "provider": "whatsapp-web.js",
  "session_path": "~/.openclaw/workspace/config/whatsapp/session",
  "phone_number": "+86xxxxxxxxx"
}
EOF
```

### 步骤 4: 二维码登录

```bash
# 运行客户端
python3 -m skills.whatsapp-integration.whatsapp_client

# 使用 WhatsApp Mobile 扫描二维码
# 打开 WhatsApp → 设置 → 已连接设备 → 连接设备
```

### 步骤 5: 测试验证

```python
from whatsapp_client import WhatsAppClient

client = WhatsAppClient()

# 发送测试消息
await client.send_message("86xxxxxxxxx@c.us", "测试消息")
```

---

## 🔧 故障排除

### 问题 1: Node.js 未安装

**错误**: `command not found: npm`

**解决**:
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 问题 2: 二维码过期

**原因**: 二维码有效期约 30 秒

**解决**:
- 刷新二维码
- 尽快扫描

### 问题 3: Session 丢失

**原因**: Session 文件损坏

**解决**:
```bash
# 删除旧 session
rm -rf ~/.openclaw/workspace/config/whatsapp/session

# 重新扫码登录
python3 -m skills.whatsapp-integration.whatsapp_client
```

---

## 📚 相关文档

- [whatsapp-web.js GitHub](https://github.com/pedroslopez/whatsapp-web.js)
- [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)

---

**📱 WhatsApp 集成配置指南 (后期配备)!**

**太一 AGI · 2026-04-11** ✨
