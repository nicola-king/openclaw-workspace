---
name: drawnix
description: 集成开源白板工具 Drawnix（13879⭐），提供思维导图、流程图、自由画的自动渲染能力。太一自动识别以下场景并调度：生成思维导图（市场分析/买家关系/竞争格局）、生成流程图（业务流程/外贸流程/供应链）、生成数据可视化图表。支持 markdown → 思维导图、mermaid → 流程图。
---

# Drawnix Skill — 智能可视化渲染

将开源白板工具 Drawnix（plait-board/drawnix ⭐13879）集成到太一系统，实现文本输出的自动可视化。

## 核心能力

| 能力 | 输入 | 输出 |
|------|------|------|
| **markdown → 思维导图** | 结构化 Markdown 文本 | 思维导图（可导出PNG） |
| **mermaid → 流程图** | Mermaid 语法 | 流程图/时序图/甘特图 |
| **自由画** | 绘图指令 | 手绘风格示意图 |
| **无限画布** | 多节点数据 | 可缩放浏览的大图 |

## 自动触发规则

| 场景 | 触发条件 | 渲染方式 |
|------|---------|---------|
| **市场分析** | 用户需要看行业/市场结构分析 | markdown → 思维导图 |
| **买家关系** | 用户想了解买家/客户之间的关系 | markdown → 思维导图 |
| **竞争格局** | 竞争分析/竞品对比 | mermaid → 流程图 |
| **业务流程** | 外贸流程/供应链/下单流程 | mermaid → 流程图 |
| **背调结果** | 五步背调完整结果 | markdown → 思维导图 |
| **项目规划** | 多步骤任务/路线图 | mermaid → 甘特图 |
| **数据报告** | 月度/季度报告总结 | markdown → 思维导图 |

## 手动触发命令

```
/思维导图 <内容>   → 将文本渲染为思维导图
/流程图 <mermaid>   → 将 mermaid 语法渲染为流程图
/关系图 <数据>      → 将关系数据渲染为拓扑图
```

## 部署方式

### 方式 A：官方在线版（零部署，推荐起步）
```
访问 https://drawnix.com 即可使用
将 markdown 文本贴入 → 自动转为思维导图
```

### 方式 B：Docker 自托管
```bash
docker pull pubuzhixing/drawnix:latest
docker run -d -p 3800:80 pubuzhixing/drawnix:latest
# 访问 http://localhost:3800
```

### 方式 C：源码本地运行
```bash
git clone https://github.com/plait-board/drawnix.git
cd drawnix
npm install
npm run start
# 访问 http://localhost:4200
```

## 集成架构

```
太一输出（文本/Markdown）
  → 自动判断是否需可视化
    → 是 → 发送到 Drawnix API
      → 渲染为思维导图/流程图
      → 导出 PNG → 返回给用户
    → 否 → 文本输出（默认）
```

## 与现有工具的关系

| 工具 | 定位 | 差异 |
|------|------|------|
| **html-anything** | 报告排版渲染 | 排版精美但非交互式 |
| **Drawnix** | 思维导图/流程图 | 可交互、可编辑、可导出 |
| **art-agent** | 品牌视觉设计 | 品牌风格版面设计 |

**协作方式**：先走 Drawnix 出结构图 → 走 html-anything 出报告 → 走 art-agent 出品牌视觉

## 配置

`config/settings.json` — 包含 Drawnix 服务地址、端口、渲染偏好。
