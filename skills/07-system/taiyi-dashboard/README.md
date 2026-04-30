# 太一 Dashboard - 综合总览

> 创建时间：2026-04-10  
> 版本：1.0.0  
> 状态：✅ 已运行

---

## 🎯 功能说明

太一 Dashboard 是一个综合性的系统总览页面，实时显示：

- ✅ 所有服务运行状态
- ✅ 系统资源使用 (内存/磁盘)
- ✅ Google 服务集成状态
- ✅ 快速访问链接
- ✅ 最近报告列表

---

## 🚀 访问方式

**本地访问**:
```
http://localhost:5001
```

**局域网访问**:
```
http://192.168.3.74:5001
```

---

## 📊 监控的服务

| 服务 | 端口 | 说明 |
|------|------|------|
| **Gateway** | 18789 | OpenClaw 网关 |
| **Bot Dashboard** | 3000 | Bot 状态仪表盘 |
| **ROI Dashboard** | 8080 | 收益追踪器 |
| **Skill Dashboard** | 5002 | 技能管理中心 |
| **百度网盘** | - | 云存储客户端 |

---

## 🌐 Google 服务状态

| 服务 | 状态 | 说明 |
|------|------|------|
| **Gemini** | ✅ 已配置 | API 已集成 |
| **NotebookLM** | ✅ 已配置 | 网页自动化 |
| **Google Drive** | 🟡 待凭证 | 需 Cloud 凭证 |
| **Chromium** | ✅ 已安装 | 浏览器自动化 |

---

## 📁 文件结构

```
taiyi-dashboard/
├── app.py              # Flask 后端
├── templates/
│   └── index.html      # 前端界面
├── static/             # 静态资源
└── README.md           # 本文档
```

---

## 🔧 API 接口

### 获取系统状态
```
GET /api/status
```

**响应**:
```json
{
  "system": {
    "gateway": true,
    "bot_dashboard": true,
    "roi_dashboard": true,
    "skill_dashboard": true,
    "baidu_netdisk": true
  },
  "skills_count": 206,
  "memory": {...},
  "disk": {...},
  "google_services": {...}
}
```

### 获取最近报告
```
GET /api/reports
```

---

## 🎨 界面特色

- **实时状态**: 每 10 秒自动刷新
- **资源图表**: Chart.js 可视化
- **快速访问**: 一键跳转各服务
- **响应式设计**: 适配手机/平板/桌面

---

## 📋 启动方式

**手动启动**:
```bash
cd /home/nicola/.openclaw/workspace/skills/taiyi-dashboard
python3 app.py
```

**后台启动**:
```bash
cd /home/nicola/.openclaw/workspace/skills/taiyi-dashboard
nohup python3 app.py > /tmp/taiyi-dashboard.log 2>&1 &
```

---

## 🔗 相关服务

| 服务 | 地址 | 说明 |
|------|------|------|
| 太一 Dashboard | http://localhost:5001 | 综合总览 |
| Bot Dashboard | http://localhost:3000 | Bot 状态 |
| ROI Dashboard | http://localhost:8080 | 收益追踪 |
| Skill Dashboard | http://localhost:5002 | 技能管理 |

---

*太一 AGI | 2026-04-10*
