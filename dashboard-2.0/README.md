# 🎨 太一 Dashboard 2.0

> **版本**: v2.0.0  
> **创建时间**: 2026-04-14 23:05  
> **状态**: 🟢 开发中

---

## 📋 项目简介

太一 Dashboard 2.0 是一个统一运营界面，提供多 Agent 状态监控、自进化进度可视化、实时数据流展示、时间线组件、审计日志等功能。

**核心功能**:
- ✅ 多 Agent 状态实时监控
- ✅ 自进化进度可视化
- ✅ 实时数据流展示
- ✅ 时间线组件
- ✅ 审计日志
- ✅ 审批流程管理
- ✅ 网关状态监控

**技术栈**:
- 前端：React 18 + TypeScript + Tailwind CSS
- 后端：Node.js + Express + WebSocket
- 部署：Docker Compose + Nginx

---

## 🚀 快速开始

### 前置要求
```
- Node.js 22+
- npm 10+
- Docker 20+
- Docker Compose v2
```

### 开发模式
```bash
# 安装依赖
cd dashboard-2.0
npm install

# 启动开发服务器
npm run dev

# 访问
# 前端：http://localhost:3000
# 后端：http://localhost:8000
```

### Docker 部署
```bash
# 构建并启动
docker-compose up -d --build

# 访问
# http://localhost:3000
```

---

## 📁 目录结构

```
dashboard-2.0/
├── frontend/          # 前端代码
├── backend/           # 后端代码
├── docker/            # Docker 配置
├── docker-compose.yml # Docker Compose 配置
└── README.md          # 本文件
```

---

## 📊 功能模块

### 1. 仪表盘模块
- Agent 状态卡片
- Skill 统计图表
- 任务进度条
- 系统健康度

### 2. 可视化模块
- 实时数据流图表
- 时间线组件
- 自进化进度图
- 网络拓扑图

### 3. 管理模块
- Agent 管理面板
- Skill 管理面板
- 审批队列
- 网关管理

### 4. 审计模块
- 操作日志
- 决策追踪
- 事件时间线

---

## 🔌 API 文档

详见 [API.md](./API.md)

---

## 🧪 测试

```bash
# 单元测试
npm test

# E2E 测试
npm run test:e2e

# 测试覆盖率
npm run test:coverage
```

---

## 📝 开发计划

- [x] 详细设计完成
- [ ] 阶段 1: 基础架构 (Week 1)
- [ ] 阶段 2: 可视化模块 (Week 2)
- [ ] 阶段 3: 管理模块 (Week 3)
- [ ] 阶段 4: 审计模块 (Week 4)

---

## 📄 许可证

MIT License

---

*太一 Dashboard 2.0 · 太一 AGI · 2026-04-14*
