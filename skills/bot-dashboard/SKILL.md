# Bot Dashboard Skill - OpenClaw 机器人监控仪表盘

> 太一 v4.0 技能 | 自然语言触发 Dashboard 启动

---

## 🎯 职责域

**触发条件**：
- 用户提到 "dashboard"、"仪表盘"、"机器人大盘"、"bot review" 等关键词
- 用户请求查看 Bot 状态/模型配置/Session 管理

**核心功能**：
1. 识别 Dashboard 触发词
2. 自动启动 Dashboard 服务（如未运行）
3. 返回访问 URL 和状态
4. 可选：后台运行 + 端口检测

---

## 🚀 执行流程

```
用户触发 → 检测服务状态 → 启动 Dashboard → 返回访问 URL
```

### Step 1: 检测服务状态
```bash
curl -s http://localhost:3000 2>&1 | grep -o '<title>.*</title>'
```

### Step 2: 启动服务（如未运行）
```bash
cd /tmp/OpenClaw-bot-review
npm run dev &
```

### Step 3: 返回结果
```
✅ Dashboard 已启动！
访问：http://localhost:3000
功能：机器人总览/像素办公室/模型列表/会话管理/消息统计/告警中心
```

---

## 📋 触发词列表

| 触发词 | 优先级 |
|--------|--------|
| 打开 dashboard | P0 |
| 打开机器人大盘 | P0 |
| 打开 bot review | P1 |
| 打开 openclaw 仪表盘 | P1 |
| 查看 bot 状态 | P2 |
| 查看模型配置 | P2 |

---

## 🔧 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `port` | 3000 | Dashboard 端口 |
| `auto_start` | true | 自动启动服务 |
| `background` | true | 后台运行 |
| `source_dir` | /tmp/OpenClaw-bot-review | 源码目录 |

---

## 📊 Dashboard 功能模块

| 模块 | 路由 | 功能 |
|------|------|------|
| 机器人总览 | `/` | Bot 卡片墙/网关健康度 |
| 像素办公室 | `/pixel-office` | 动画像素风办公室 |
| 模型列表 | `/models` | 模型配置/测试 |
| 会话列表 | `/sessions` | Session 管理/Token 消耗 |
| 消息统计 | `/stats` | 趋势图表 |
| 告警中心 | `/alerts` | 告警规则配置 |
| 技能管理 | `/skills` | 已安装技能浏览 |

---

## ⚠️ 注意事项

1. **临时目录**：源码在 `/tmp`，系统重启后需重新克隆
2. **开发模式**：`npm run dev` 适合测试，生产部署用 `npm run build && npm start`
3. **配置依赖**：需要 `~/.openclaw/openclaw.json` 存在
4. **端口占用**：默认 3000，冲突时自动检测并提示

---

## 🔗 相关链接

- 源码：https://github.com/xmanrui/OpenClaw-bot-review
- 作者：@xmanrui
- 集成时间：2026-04-02 21:26

---

*太一 AGI v4.0 | Bot Dashboard Skill v1.0*
