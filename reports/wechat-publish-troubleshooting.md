# 微信公众号自动发布配置

> **更新时间**: 2026-04-16 18:02  
> **问题**: 微信也没有收到通知  
> **状态**: ✅ 已诊断

---

## 🔍 问题诊断

### 微信发布流程

**当前流程**:
```
1. wechat_sender.py 生成文章
2. 发送邮件到 285915125@qq.com
3. 用户手动复制粘贴到微信公众号后台
```

**问题**:
```
❌ 不是真正的微信推送
❌ 只是发送邮件到 QQ 邮箱
❌ 用户需要手动检查邮箱
❌ 用户可能没注意到邮件
```

---

## 📊 当前配置

### 收件人配置

**文件**: `/home/nicola/.openclaw/workspace-taiyi/config/wechat.json`

```json
{
  "smtp": {
    "enabled": true,
    "sender_email": "285915125@qq.com",
    "recipient_email": "285915125@qq.com"
  }
}
```

**收件人**: 285915125@qq.com

---

### 定时任务配置

**文件**: `/home/nicola/.openclaw/workspace/crontab.txt`

```bash
# 太一微信公众号自动发布 - 每日 18:00 生成明日文章
0 18 * * * cd /home/nicola/.openclaw/workspace/skills/05-content/shanmu/wechat-assistant && python3 wechat_sender.py --topic "AI 管家" >> logs/wechat-auto-publish.log 2>&1
```

**执行时间**: 每日 18:00

---

## ✅ 发送成功验证

**日志**: `/home/nicola/.openclaw/workspace/logs/wechat-auto-publish.log`

```
✅ 邮件发送成功！
收件人：285915125@qq.com
主题：AI 管家
```

**结论**: 邮件已发送到 285915125@qq.com

---

## 🔍 用户没收到的原因

### 可能原因

1. **邮箱检查频率低**
   - 用户不常检查 285915125@qq.com 邮箱
   - 邮件被归类为垃圾邮件

2. **没有 Telegram 通知**
   - 邮件发送后没有 Telegram 提醒
   - 用户不知道有新邮件

3. **定时任务刚修复**
   - 之前定时任务一直失败
   - 今天 18:00 才第一次正常执行

---

## 💡 解决方案

### 方案 1: 添加 Telegram 通知 (推荐)

**修改 wechat_sender.py**:
```python
# 发送邮件后发送 Telegram 通知
def send_email(self, subject, content, recipient):
    # ... 邮件发送代码 ...
    
    # 发送 Telegram 通知
    self.send_telegram_notification(subject)

def send_telegram_notification(self, subject):
    """发送 Telegram 通知"""
    import subprocess
    script = self.workspace / "scripts" / "send-md-to-telegram.py"
    
    # 创建通知内容
    notification = f"""
📧 微信公众号文章已发送

主题：{subject}
收件人：{self.config['recipient_email']}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

请检查邮箱并及时发布到微信公众号。
"""
    
    # 保存并发送
    temp_file = self.output_dir / "wechat_notification.md"
    temp_file.write_text(notification, encoding='utf-8')
    
    subprocess.run(["python3", str(script), str(temp_file)])
```

---

### 方案 2: 更改收件人邮箱

**修改**: `/home/nicola/.openclaw/workspace-taiyi/config/wechat.json`

```json
{
  "smtp": {
    "recipient_email": "7073481596@qq.com"  // 改为用户常用邮箱
  }
}
```

---

### 方案 3: 添加邮件已读回执

**修改 wechat_sender.py**:
```python
def send_email(self, subject, content, recipient):
    msg = MIMEMultipart()
    msg['From'] = self.sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # 添加已读回执请求
    msg.add_header('Disposition-Notification-To', self.sender_email)
    msg.add_header('Return-Receipt-To', self.sender_email)
```

---

### 方案 4: 微信公众号 API 直接发布 (终极方案)

**使用微信公众号 API**:
```python
import requests

def publish_to_wechat(self, article):
    """直接发布到微信公众号"""
    # 1. 获取 access_token
    access_token = self.get_access_token()
    
    # 2. 上传图文素材
    draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 3. 提交发布
    publish_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    
    # ... 发布逻辑 ...
```

---

## 🚀 立即执行

### 1. 检查今日邮件

**操作**:
```
1. 登录 285915125@qq.com 邮箱
2. 检查今日 18:00 的邮件
3. 主题："AI 管家"
4. 发件人：太一 AGI
```

---

### 2. 添加 Telegram 通知

**修改 crontab**:
```bash
# 微信公众号自动发布 - 每日 18:00
0 18 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace/skills/05-content/shanmu/wechat-assistant && python3 wechat_sender.py --topic "AI 管家" >> logs/wechat-auto-publish.log 2>&1

# 发送 Telegram 通知 - 每日 18:05
5 18 * * * . /home/nicola/.openclaw/load-env.sh && python3 /home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py /home/nicola/.openclaw/workspace/skills/05-content/shanmu/wechat-assistant/output/latest.md >> logs/wechat-notify.log 2>&1
```

---

### 3. 更改收件人邮箱

**修改配置文件**:
```bash
# 编辑 wechat.json
cat > /home/nicola/.openclaw/workspace-taiyi/config/wechat.json <<EOF
{
  "smtp": {
    "recipient_email": "7073481596@qq.com"
  }
}
EOF
```

---

## 📝 总结

### 问题根源

```
❌ 微信发布 = 发送邮件到 285915125@qq.com
❌ 用户不常检查该邮箱
❌ 没有 Telegram 通知提醒
❌ 定时任务今天才修复
```

### 解决方案

```
✅ 检查 285915125@qq.com 邮箱今日 18:00 邮件
✅ 添加 Telegram 通知 (推荐)
✅ 更改收件人为 7073481596@qq.com
✅ 或直接使用微信公众号 API 发布
```

### 下次执行

```
时间：明日 18:00
主题：AI 管家 (或自定义)
收件人：285915125@qq.com (可更改)
通知：Telegram (添加后)
```

---

*太一 AGI · 微信发布故障排查 v1.0 · 2026-04-16 18:02*

**✅ 微信发布诊断完成！邮件已发送到 285915125@qq.com！**
