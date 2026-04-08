# 山木公众号助手 - 快速配置指南

> 5 分钟配置，从此写文章发邮件就能发布

---

## 第 1 步：获取 QQ 邮箱授权码

1. 登录 QQ 邮箱：https://mail.qq.com
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务**
4. 开启 **IMAP/SMTP 服务**
5. 点击 **生成授权码**
6. 按提示发送短信验证
7. **复制授权码**（不是 QQ 密码！）

---

## 第 2 步：创建配置文件

```bash
mkdir -p ~/.taiyi/wechat-assistant
cat > ~/.taiyi/wechat-assistant/config.json << 'EOF'
{
  "sender_email": "你的 QQ 邮箱@qq.com",
  "smtp_password": "刚才获取的授权码",
  "recipient_email": "285915125@qq.com"
}
EOF
```

---

## 第 3 步：测试发送

```bash
cd ~/.openclaw/workspace/skills/shanmu/wechat-assistant
python3 wechat_sender.py --topic "AI 管家"
```

**收到邮件 = 配置成功！** ✅

---

## 第 4 步：日常使用

### 方式 1：命令行

```bash
taiyi wechat-assistant write --topic "文章主题"
```

### 方式 2：自动执行（推荐）

```bash
# 每日 18:00 自动撰写明日文章
0 18 * * * cd ~/.openclaw/workspace/skills/shanmu/wechat-assistant && python3 wechat_sender.py --topic "明日主题"
```

---

## 收到邮件后

1. **打开邮件**
2. **复制标题**（3 选 1）
3. **登录公众号后台**
4. **新建图文** → 粘贴标题
5. **复制正文** → 粘贴
6. **上传封面图**
7. **填写摘要**
8. **预览** → **发布**

**全程 5 分钟！**

---

## 常见问题

### Q：授权码和 QQ 密码不一样？
A：是的，授权码是专门给第三方应用用的，更安全。

### Q：邮件发送失败？
A：检查：
- sender_email 是否填写正确（包括@qq.com）
- smtp_password 是否是授权码（不是 QQ 密码）
- 是否开启了 SMTP 服务

### Q：可以发给其他人吗？
A：可以，修改 recipient_email 即可。

---

## 技术支持

- 公众号：SAYELF 山野精灵
- 微信：sayelf-tea

---

*山木 · 2026 年 3 月*
