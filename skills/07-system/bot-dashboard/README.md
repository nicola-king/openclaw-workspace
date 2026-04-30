# OpenClaw Bot Dashboard 集成技能

> 太一 v4.0 技能 | 一键启动 Bot 监控仪表盘

---

## 🎯 功能

通过自然语言触发词启动 OpenClaw Bot Dashboard 服务：

**触发词**：
- "打开 OpenClaw-bot-review"
- "打开 Openclaw dashboard"
- "打开 bot review"
- "打开机器人大盘"
- "打开 openclaw 机器人大盘"

---

## 🚀 快速启动

### 方式 1：自然语言触发
```
用户：打开 bot dashboard
太一：✅ Dashboard 已启动，访问 http://localhost:3000
```

### 方式 2：手动启动
```bash
cd /tmp/OpenClaw-bot-review
npm run dev
```

---

## 📊 Dashboard 功能

| 模块 | 功能 |
|------|------|
| **机器人总览** | 所有 Bot 状态/模型/平台绑定 |
| **像素办公室** | 动画像素风办公室（Bot 拟人化） |
| **模型列表** | 配置模型/上下文/推理支持 |
| **会话管理** | Session 浏览/Token 消耗/连接测试 |
| **消息统计** | Token/响应时间趋势图 |
| **告警中心** | 告警规则配置/飞书通知 |
| **技能管理** | 已安装技能浏览/搜索 |

---

## 🔧 技术栈

- Next.js 16 + TypeScript
- Tailwind CSS 4
- 无数据库（直接读取 `~/.openclaw/openclaw.json`）

---

## 📁 部署位置

**源码**：`/tmp/OpenClaw-bot-review`  
**访问**：`http://localhost:3000`  
**状态**：🟡 运行中（开发模式）

---

## ⚠️ 注意事项

1. **临时目录**：源码在 `/tmp`，重启后需重新克隆
2. **开发模式**：`npm run dev` 适合测试，生产用 `npm run build && npm start`
3. **配置读取**：自动读取 `~/.openclaw/openclaw.json`
4. **端口占用**：默认 3000，冲突需修改

---

## 🔗 相关链接

- 源码：https://github.com/xmanrui/OpenClaw-bot-review
- 作者：@xmanrui
- 太一集成：`skills/bot-dashboard/SKILL.md`

---

*集成时间：2026-04-02 21:26 | 太一 AGI v4.0*
