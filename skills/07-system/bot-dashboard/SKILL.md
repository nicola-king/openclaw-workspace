---
skill: bot-dashboard
version: 1.0.0
author: 太一 AGI
created: 2026-04-06
status: active
tags: ['Dashboard', 'Bot 监控，系统状态，产出统计，Web UI']
category: monitoring
---



# Bot Dashboard Skill

> 8 Bot 舰队监控与管理系统

---

## 📊 功能概述

提供 8 Bot 可视化监控:
- Bot 状态实时显示
- 任务队列管理
- 产出统计
- 系统健康监控
- 配置管理

---

## 🛠️ 技术栈

| 组件 | 用途 | 状态 |
|------|------|------|
| React 19 | 前端框架 | 🟡 待安装 |
| Tailwind CSS | 样式 | 🟡 待安装 |
| Recharts | 图表 | 🟡 待安装 |
| Zustand | 状态管理 | 🟡 待安装 |
| TanStack Query | HTTP | 🟡 待安装 |

---

## 🎨 界面设计

### 布局结构
```
┌─────────────────────────────────────────────────┐
│  顶部导航栏                                     │
│  [太一 AGI] [系统状态] [宪法] [记忆] [技能]      │
├─────────────────────────────────────────────────┤
│                                                 │
│  左侧边栏          │  主内容区                   │
│  ├─ Bot 列表       │  ┌─────────────────────┐   │
│  │  ├─ 知几       │  │  Bot 详情/工作台     │   │
│  │  ├─ 山木       │  │                     │   │
│  │  ├─ 素问       │  │  - 状态卡片         │   │
│  │  ├─ 罔两       │  │  - 任务列表         │   │
│  │  ├─ 庖丁       │  │  - 产出统计         │   │
│  │  ├─ 羿         │  │  - 配置选项         │   │
│  │  ├─ 守藏吏     │  │                     │   │
│  │  └─ 太一       │  └─────────────────────┘   │
│  │                │                            │
│  ├─ 任务队列      │  右侧边栏                   │
│  ├─ 系统日志      │  ├─ 系统状态               │
│  └─ 设置          │  ├─ Git 状态               │
│                   │  ├─ 内存使用               │
│                   │  └─ 宪法完整               │
└─────────────────────────────────────────────────┘
```

---

## 🔧 核心组件

### 1. 状态卡片
```jsx
<StatusCard
  title="知几-E"
  status="running"
  balance="$10,000"
  todayPnL="+5.38%"
  winRate="54%"
  tasks={3}
/>
```

### 2. 任务列表
```jsx
<TaskList
  tasks={[
    { id: 1, name: "模拟盘监控", status: "running" },
    { id: 2, name: "策略分析", status: "pending" },
    { id: 3, name: "报告生成", status: "completed" }
  ]}
/>
```

### 3. 产出统计
```jsx
<OutputStats
  today={{ files: 20, code: "35KB", commits: 8 }}
  week={{ files: 150, code: "200KB", commits: 50 }}
  month={{ files: 500, code: "800KB", commits: 200 }}
/>
```

---

## 📋 使用示例

### 场景 1: 查看 Bot 状态
```javascript
// 访问 Dashboard
GET http://localhost:3000

// 查看知几-E 详情
GET http://localhost:3000/bots/zhiji-e
```

### 场景 2: 任务管理
```javascript
// 暂停任务
POST /api/tasks/123/pause

// 重启任务
POST /api/tasks/123/resume

// 查看任务日志
GET /api/tasks/123/logs
```

### 场景 3: 系统监控
```javascript
// 查看系统状态
GET /api/system/status

// 查看 Git 状态
GET /api/system/git

// 查看内存使用
GET /api/system/memory
```

---

## 🎯 守藏吏 Bot 集成

```python
# 守藏吏 - Dashboard 数据提供
async def shoucangli_dashboard_data():
    # 收集 8 Bot 状态
    bots_status = await collect_all_bots_status()
    
    # 收集系统指标
    system_metrics = await collect_system_metrics()
    
    # 返回 Dashboard 数据
    return {
        "bots": bots_status,
        "system": system_metrics,
        "updated_at": datetime.now().isoformat()
    }
```

---

## 🔗 集成文档

- 原型设计：`integrations/bot-dashboard/prototype.md`
- DESIGN.md: `design-systems/taiyi/DESIGN.md`

---

## 📝 待办事项

- [ ] React 项目创建
- [ ] 核心组件实现
- [ ] API 对接
- [ ] 部署测试

---

*创建时间：2026-04-06 01:00 | 太一 AGI*
