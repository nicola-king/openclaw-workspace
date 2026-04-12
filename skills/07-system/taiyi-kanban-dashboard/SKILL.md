# 太一看板 Dashboard - 技能文档

## 📊 概述

**太一看板 Dashboard** 是一个企业级可视化项目协作工具，专为太一 AGI 系统设计。

**灵感**: 板栗看板 (企业免费版)

**技术栈**:
- 前端：React 19 + Vite 6 + TailwindCSS 3
- 后端：Flask + CORS
- 数据源：HEARTBEAT.md + 系统状态

---

## 🚀 功能特性

### 1. 任务看板
- 📝 **待办 (Todo)**: 等待执行的任务
- 🔄 **进行中 (Doing)**: 正在执行的任务
- ✅ **已完成 (Done)**: 已完成的任务
- 支持拖拽移动任务 (左右移动按钮)
- 优先级标签：P0 🔴 / P1 🟡 / P2 🟢

### 2. Bot 舰队状态
显示所有 Bot 的实时状态:
- 太一 (执行总管)
- 知几-E (量化交易)
- 山木 (内容创意)
- 素问 (技术开发)
- 罔两 (高价值发现)
- 庖丁 (预算追踪)
- 守藏吏 (知识管理)

### 3. Cron 任务监控
- 每 5 分钟 - 自动执行
- 每 10 分钟 - 通道检查
- 每 30 分钟 - Git 备份
- 每小时 - 天气预测/系统自检
- 每日 - 宪法学习/日报生成

### 4. 系统状态
- Gateway 运行状态
- Git 状态
- 宪法完整性
- 通讯通道 (微信/Telegram)

### 5. 统计面板
- 总任务数
- 待办/进行中/已完成
- P0 紧急任务数

---

## 📦 安装与运行

### 前置条件
```bash
# Node.js 18+
node --version

# Python 3.10+
python3 --version

# Flask
pip3 install flask flask-cors
```

### 前端构建
```bash
cd /home/nicola/.openclaw/workspace/skills/taiyi-kanban-dashboard

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

### 后端启动
```bash
# 启动 API 服务器
python3 api_server.py
```

### 访问地址
- 前端：http://localhost:3001 (开发) / http://localhost:5001 (生产)
- API: http://localhost:5001/api/*

---

## 🔌 API 接口

### GET /api/tasks
获取任务看板数据
```json
{
  "success": true,
  "data": {
    "todo": [...],
    "doing": [...],
    "done": [...]
  },
  "timestamp": "2026-04-09T07:45:00"
}
```

### GET /api/bots
获取 Bot 状态
```json
{
  "success": true,
  "data": [
    {"id": "taiyi", "name": "太一", "status": "running", ...}
  ]
}
```

### GET /api/cron
获取 Cron 任务状态
```json
{
  "success": true,
  "data": [
    {"name": "每 5 分钟 - 自动执行", "status": "ok", "lastRun": "07:45"}
  ]
}
```

### GET /api/system
获取系统状态
```json
{
  "success": true,
  "data": {
    "gateway": {"status": "running", "pid": "139746"},
    "git": {"status": "ok"},
    "constitution": {"status": "ok"},
    "channels": {"wechat": "ok", "telegram": "ok"}
  }
}
```

### GET /api/stats
获取统计数据
```json
{
  "success": true,
  "data": {
    "total": 10,
    "todo": 3,
    "doing": 2,
    "done": 5,
    "p0": 5,
    "p1": 3,
    "p2": 2
  }
}
```

---

## 📝 数据源

### HEARTBEAT.md 解析
任务数据从 `HEARTBEAT.md` 自动提取:

```markdown
| 编号 | 任务 | 状态 | 下一步 | 截止 |
|------|------|------|--------|------|
| **TASK-150** | Hermes 学习循环 | 🟢 新创建 | 核心模块开发 | 04-09 |
```

解析规则:
- 🔴 或 "待命" → todo 列
- 🟡 或 "MVP" → doing 列
- ✅ 或 "完成" → done 列

### 实时数据
- Bot 状态：静态配置 (可扩展为动态检测)
- Cron 状态：基于系统时间计算
- 系统状态：实时检测 (pgrep/git status)

---

## 🎨 UI 设计

### 配色方案
- P0 优先级：红色 (bg-red-100, text-red-700)
- P1 优先级：黄色 (bg-yellow-100, text-yellow-700)
- P2 优先级：绿色 (bg-green-100, text-green-700)
- 运行中：绿色 (bg-green-500)
- 待机：黄色 (bg-yellow-500)
- 错误：红色 (bg-red-500)

### 响应式设计
- 桌面端：完整三列看板
- 平板：可横向滚动
- 移动端：单列堆叠

---

## 🔄 自动更新

### 前端
- 每 30 秒自动刷新时间戳
- 可配置为轮询 API 获取实时数据

### 后端
- Cron 状态基于系统时间动态计算
- 系统状态实时检测

---

## 🚀 部署

### 生产构建
```bash
# 前端构建
npm run build

# 启动 Flask 服务器 (提供静态文件 + API)
python3 api_server.py
```

### systemd 服务 (可选)
```ini
# /etc/systemd/system/taiyi-kanban.service
[Unit]
Description=Taiyi Kanban Dashboard
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace/skills/taiyi-kanban-dashboard
ExecStart=/usr/bin/python3 api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable taiyi-kanban
sudo systemctl start taiyi-kanban
```

---

## 📈 未来增强

### 短期 (v1.1)
- [ ] 真正的拖拽排序 (react-beautiful-dnd)
- [ ] 任务编辑对话框
- [ ] 新建任务表单
- [ ] 导入/导出 HEARTBEAT.md

### 中期 (v1.2)
- [ ] WebSocket 实时推送
- [ ] 任务历史追踪
- [ ] 统计图表 (recharts)
- [ ] Bot 任务分配

### 长期 (v2.0)
- [ ] 多看板支持
- [ ] 团队协作功能
- [ ] 移动端 App
- [ ] 数据持久化 (SQLite)

---

## 🐛 故障排除

### 前端无法启动
```bash
# 检查 Node 版本
node --version  # 需要 18+

# 清理并重装依赖
rm -rf node_modules package-lock.json
npm install
```

### 后端 API 无法访问
```bash
# 检查 Flask 是否安装
pip3 list | grep flask

# 检查端口占用
lsof -i :5001

# 查看日志
python3 api_server.py 2>&1 | tee api.log
```

### 任务数据不显示
```bash
# 检查 HEARTBEAT.md 是否存在
ls -la /home/nicola/.openclaw/workspace/HEARTBEAT.md

# 检查文件格式
cat /home/nicola/.openclaw/workspace/HEARTBEAT.md | head -30
```

---

## 📄 文件结构

```
taiyi-kanban-dashboard/
├── package.json          # npm 配置
├── vite.config.js        # Vite 配置
├── tailwind.config.js    # TailwindCSS 配置
├── postcss.config.js     # PostCSS 配置
├── index.html            # HTML 入口
├── api_server.py         # Flask API 服务器
├── SKILL.md              # 本文件
├── src/
│   ├── main.jsx          # React 入口
│   ├── index.css         # 全局样式
│   └── App.jsx           # 主应用组件
└── dist/                 # 生产构建输出 (npm run build 后生成)
```

---

## 🔗 相关链接

- 板栗看板：https://www.banliankan.com
- React: https://react.dev
- Vite: https://vitejs.dev
- TailwindCSS: https://tailwindcss.com
- Flask: https://flask.palletsprojects.com

---

*太一看板 Dashboard v1.0 | 2026-04-09 | 太一 AGI*
