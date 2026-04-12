# 太一 Dashboard 导航指南

> 更新时间：2026-04-10 19:05  
> 版本：1.1.0 (支持导航)

---

## 🎯 新增功能

### 点击导航

现在太一 Dashboard 支持点击导航到详情页面！

| 可点击项目 | 跳转页面 | 说明 |
|-----------|---------|------|
| **Gateway 卡片** | `/service/gateway` | 查看网关详情 |
| **Bot Dashboard 卡片** | `/service/bot` | 查看 Bot 服务详情 |
| **ROI Dashboard 卡片** | `/service/roi` | 查看收益追踪详情 |
| **Skill Dashboard 卡片** | `/service/skill` | 查看技能管理详情 |
| **百度网盘卡片** | `/service/baidu` | 查看网盘详情 |
| **Google 服务区域** | `/google` | Google 服务详情页 |
| **快速访问区域** | `/skills` | 技能列表页 |

---

## 📊 页面结构

```
太一 Dashboard (首页)
├── /service/gateway      → Gateway 详情页
├── /service/bot          → Bot Dashboard 详情页
├── /service/roi          → ROI Dashboard 详情页
├── /service/skill        → Skill Dashboard 详情页
├── /service/baidu        → 百度网盘详情页
├── /google               → Google 服务集成页
├── /skills               → 技能列表页
└── /api/*                → API 接口
```

---

## 🌐 访问方式

**主页面**:
```
http://localhost:5001
```

**服务详情页**:
```
http://localhost:5001/service/gateway
http://localhost:5001/service/bot
http://localhost:5001/service/roi
http://localhost:5001/service/skill
http://localhost:5001/service/baidu
```

**功能页面**:
```
http://localhost:5001/google     → Google 服务
http://localhost:5001/skills     → 技能列表
```

---

## 🎨 界面特色

### 首页
- 5 个服务状态卡片 (可点击)
- 内存/磁盘使用图表
- Google 服务集成状态
- 快速访问链接
- 最近报告列表

### 服务详情页
- 服务基本信息
- 运行状态指示
- 端口/URL 信息
- 操作按钮 (启动/停止/打开)
- 日志查看区域

### Google 服务页
- 4 个服务卡片 (Gemini/NotebookLM/Drive/Chromium)
- 配置状态说明
- 快速访问链接
- 配置指南

### 技能列表页
- 搜索功能
- 技能卡片网格
- 状态指示器
- 跳转到 Skill Dashboard

---

## 🔧 API 接口

### 系统状态
```
GET /api/status
```

### 服务详情
```
GET /api/service/{service_id}
```

### 最近报告
```
GET /api/reports
```

### 技能列表 (代理到 Skill Dashboard)
```
GET http://localhost:5002/api/skills
```

---

## 📁 文件结构

```
taiyi-dashboard/
├── app.py                      # Flask 后端
├── templates/
│   ├── index.html              # 首页 (已更新)
│   ├── service_detail.html     # 服务详情页 (新增)
│   ├── google_services.html    # Google 服务页 (新增)
│   └── skills_list.html        # 技能列表页 (新增)
├── README.md                   # 基础文档
└── NAVIGATION-GUIDE.md         # 本文档
```

---

## 🚀 使用流程

1. **访问首页**: http://localhost:5001
2. **点击服务卡片**: 查看服务详情
3. **查看详情**: 了解服务状态、端口、日志
4. **操作服务**: 启动/停止/打开服务
5. **返回首页**: 继续浏览其他服务

---

## 💡 提示

- 所有卡片支持 hover 效果 (放大 + 阴影)
- 点击卡片会有视觉反馈
- 服务详情页显示实时日志
- 支持返回导航

---

*太一 AGI | 2026-04-10 19:05*
