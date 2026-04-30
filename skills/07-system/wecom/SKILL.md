---
name: wecom
tier: 1
trigger: 企业微信/企微/wecom/工作微信
enabled: true
depends: []
---
# 企业微信集成技能

## 核心功能

1. 企业微信消息发送
2. 接收企业微信消息
3. 多成员通知
4. 告警推送

---

## 配置位置

`/home/nicola/.openclaw/workspace-taiyi/config/wecom.json`

---

## 使用方法

### 发送消息

```bash
python3 skills/wecom/wecom_sender.py \
  --corp_id "wwxxxxxxxxxxxxx" \
  --agent_id "1000001" \
  --secret "xxxxxxxxx" \
  --user "nicola" \
  --message "测试消息"
```

### 群发消息

```bash
# 发送给多个用户 (用 | 分隔)
python3 skills/wecom/wecom_sender.py \
  --corp_id "wwxxx" \
  --agent_id "1001" \
  --secret "xxx" \
  --user "nicola|user2" \
  --message "群发消息"
```

---

## 消息类型

### 文本消息 (默认)

```json
{
  "msgtype": "text",
  "text": {
    "content": "消息内容"
  }
}
```

### Markdown 消息

```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "**重要通知**\n- 事项 1\n- 事项 2"
  }
}
```

### 卡片消息

```json
{
  "msgtype": "template_card",
  "template_card": {
    "card_type": "text_notice",
    "main_title": {
      "title": "卡片标题"
    }
  }
}
```

---

## 通知场景

| 场景 | 接收人 | 消息类型 |
|------|--------|---------|
| **系统告警** | 主号 + 副号 | 文本 |
| **日报周报** | 主号 | Markdown |
| **交易信号** | 主号 + 副号 | 卡片 |
| **任务完成** | 主号 | 文本 |

---

## 配置示例

```json
{
  "enabled": true,
  "corp_id": "ww6c5f8a3b2c1d9e8f",
  "agent_id": "1000001",
  "agent_secret": "abc123xyz",
  "users": {
    "SAYELF": {
      "userid": "nicola",
      "mobile": "138xxxx",
      "email": "shanyejingling@gmail.com"
    },
    "USER2": {
      "userid": "user2",
      "mobile": "139xxxx"
    }
  },
  "notifications": {
    "enabled": true,
    "notify_type": "text",
    "mention_users": ["SAYELF"],
    "urgent_keywords": ["紧急", "urgent", "ASAP"]
  }
}
```

---

## 企业微信管理后台

- **登录**: https://work.weixin.qq.com/
- **应用管理**: https://work.weixin.qq.com/wework_admin/frame#apps
- **通讯录**: https://work.weixin.qq.com/wework_admin/frame#contacts

---

## 故障排查

### Q: errcode 40014 (invalid token)
**A**: 检查 Secret 是否正确，重新获取

### Q: errcode 60011 (用户不存在)
**A**: 检查用户 ID 是否在可见范围

### Q: errcode 43038 (content 为空)
**A**: 消息内容不能为空

---

## 安全建议

1. **保护 Secret**: 不要泄露应用密钥
2. **限制可见范围**: 只选择必要的成员
3. **消息频率**: 避免短时间大量发送
4. **敏感信息**: 不要发送密码等敏感内容

---

*版本：1.0 | 创建时间：2026-04-08 | 状态：✅ 已创建*
