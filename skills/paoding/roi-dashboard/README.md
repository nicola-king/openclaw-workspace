# 庖丁 ROI Dashboard

> 太一 AGI v4.0 | 三阶段可视化方案

---

## 🎯 概述

庖丁 ROI Dashboard 提供实时成本追踪与效率分析，三阶段逐步增强：

| 阶段 | 形式 | 技术栈 | 访问方式 |
|------|------|--------|----------|
| **Phase 1** | 终端可视化 | Python + Rich | `python roi_terminal.py` |
| **Phase 2** | 独立 Web | HTML + Chart.js | `http://localhost:8080` |
| **Phase 3** | 集成 Dashboard | Next.js | `http://localhost:3000/roi-stats` |

---

## 🚀 快速启动

### Phase 1：终端可视化

```bash
cd /home/nicola/.openclaw/workspace/skills/paoding
python roi_terminal.py
```

**依赖**：
```bash
pip install rich
```

**功能**：
- ✅ 汇总面板（任务数/成本/效率/Token）
- ✅ 任务表格（ID/名称/效率/成本/ROI）
- ✅ ASCII 趋势图
- ✅ 深色终端主题

---

### Phase 2：独立 Web Dashboard

```bash
cd /home/nicola/.openclaw/workspace/skills/paoding/roi-dashboard
python server.py
```

**依赖**：
```bash
pip install fastapi uvicorn
```

**访问**：http://localhost:8080

**功能**：
- ✅ 汇总卡片（4 项核心指标）
- ✅ 成本趋势图（Chart.js 折线图）
- ✅ 效率分布图（Chart.js 柱状图）
- ✅ 任务详情表格
- ✅ 10 秒自动刷新
- ✅ 深色模式 UI

---

### Phase 3：集成 Bot Dashboard

**前提**：已安装 Bot Dashboard（`/tmp/OpenClaw-bot-review`）

**步骤**：
```bash
cd /tmp/OpenClaw-bot-review

# 1. 创建 API 路由
mkdir -p app/api/roi-data
# 复制 route.ts（参考 PHASE3-INTEGRATION.md）

# 2. 创建页面
mkdir -p app/roi-stats
# 复制 page.tsx（参考 PHASE3-INTEGRATION.md）

# 3. 修改侧边栏
# 编辑 app/sidebar.tsx，添加 ROI 统计菜单

# 4. 重新构建
npm run build
npm start
```

**访问**：http://localhost:3000/roi-stats

---

## 📊 数据源

**来源**：`memory/YYYY-MM-DD.md`

**格式**：
```markdown
| TASK-050 | 知几首笔下注 | ✅ **完成** | 17:10 | 5 USDC |
```

**解析逻辑**：
- 提取包含 `TASK-` 和 `✅` 的行
- 解析任务 ID、名称、状态、效率、成本
- 汇总计算总任务数、总成本、平均效率

---

## 🎨 UI 设计

**配色方案**：
| 用途 | 颜色 | 示例 |
|------|------|------|
| 主色调 | 龙虾红 🦞 | `#FF6B6B` |
| 成功 | 绿色 | `#4CAF50` |
| 警告 | 黄色 | `#FFC107` |
| 背景 | 深色 | `#1a1a2e` |

**视觉元素**：
- 🦞 龙虾图标（太一 IP）
- 渐变背景
- 圆角卡片
- 悬停动画

---

## 📈 核心指标

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| 总任务数 | 今日完成任务总数 | 计数 |
| 总成本 | 今日总 Token 成本（¥） | Σ 任务成本 |
| 平均效率 | 平均效率提升倍数 | 估计工时/实际工时 |
| 总 Token | 今日总 Token 消耗 | Σ 任务 Token |

---

## ⚠️ 注意事项

1. **数据隐私**：ROI 数据包含成本信息，不公开分享
2. **刷新频率**：建议 10-30 秒，避免频繁读取文件
3. **文件权限**：确保有读取 `memory/*.md` 的权限
4. **依赖安装**：Phase 2 需要 FastAPI，Phase 3 需要 Node.js

---

## 🔗 相关文件

- ROI 计算器：`../ROI-CALCULATOR.md`
- ROI 可视化方案：`../ROI-VISUALIZATION.md`
- Bot Dashboard：`/tmp/OpenClaw-bot-review`
- 集成方案：`PHASE3-INTEGRATION.md`

---

*创建时间：2026-04-02 21:47 | 太一 AGI v4.0 | 庖丁 ROI Dashboard v1.0*
