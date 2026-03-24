# wechat-assistant - 公众号助手

> 自动撰写 + 排版 + 发送邮件，复制粘贴即可发布

---

## 功能

- ✅ 自动撰写公众号文章
- ✅ 微信排版格式化
- ✅ 发送到指定邮箱
- ✅ 附带发布指南

**输出：** 打开邮件 → 复制内容 → 粘贴到公众号后台 → 发布

---

## 安装

```bash
npx clawhub install shanmu-wechat-assistant
```

---

## 配置

编辑 `~/.taiyi/wechat-assistant/config.json`：

```json
{
  "recipient_email": "285915125@qq.com",
  "sender_email": "your-smtp-email@qq.com",
  "smtp_password": "your-smtp-password",
  "publish_guide": true,
  "auto_format": true
}
```

---

## 使用

### 方式 1：命令行

```bash
taiyi wechat-assistant write --topic "AI 管家" --style "科普"
```

### 方式 2：自动触发

```bash
# 每日 18:00 自动撰写明日文章
0 18 * * * taiyi wechat-assistant auto
```

---

## 邮件内容

每封邮件包含：

1. **文章标题**（3 个备选）
2. **文章正文**（微信格式）
3. **摘要**（120 字内）
4. **封面图建议**
5. **发布指南**（步骤说明）

---

## 发布流程

```
1. 收到邮件
2. 复制文章标题
3. 登录公众号后台
4. 新建图文 → 粘贴标题
5. 复制正文 → 粘贴
6. 上传封面图
7. 预览 → 发布
```

**全程 5 分钟搞定！**

---

## 输出示例

见 `content/email/wechat_article_template.html`

---

## 价格

**免费版：** 2 篇/月
**付费版：** ¥49/月（无限篇）

---

## 技术支持

- 公众号：SAYELF 山野精灵
- 微信：sayelf-tea
- GitHub: github.com/nicola-king/zhiji-e

---

*山木 · 2026 年 3 月*
