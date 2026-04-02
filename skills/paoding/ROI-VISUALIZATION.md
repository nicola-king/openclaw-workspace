# 庖丁 ROI 可视化优化方案

> 太一 v4.0 | 借鉴 Bot Dashboard 思路优化 ROI 展示

---

## 🎯 优化目标

**当前状态**：
- 庖丁 ROI 计算器：`skills/paoding/ROI-CALCULATOR.md`
- 输出格式：Markdown 表格 + 文本
- 缺失：实时图表/趋势可视化/交互式 Dashboard

**优化方向**（借鉴 Bot Dashboard）：
1. Web UI 可视化（替代纯文本）
2. 实时趋势图表（Token 消耗/响应时间/成本）
3. 交互式筛选（按任务/Bot/时间范围）
4. 自动刷新（5 秒/10 秒/30 秒）

---

## 📊 可视化方案

### 方案 A：轻量级 Web Dashboard（推荐）

**技术栈**：
- 前端：HTML + Chart.js（单文件，无构建）
- 后端：Python FastAPI（轻量级）
- 数据源：`memory/2026-04-02.md` + `reports/*.md`

**功能模块**：
| 模块 | 功能 | 图表类型 |
|------|------|----------|
| **今日概览** | 总任务数/总成本/平均 ROI | 指标卡片 |
| **成本趋势** | 每小时 Token 消耗 | 折线图 |
| **任务分布** | 按 Bot 职责域分类 | 饼图 |
| **ROI 排行** | 任务 ROI Top 10 | 条形图 |
| **效率对比** | 估计工时 vs 实际工时 | 柱状图 |

**文件结构**：
```
skills/paoding/roi-dashboard/
├── index.html          # 单文件 Dashboard
├── chart.min.js        # Chart.js 库（CDN 或本地）
├── server.py           # FastAPI 后端
├── data_loader.py      # 数据加载器
└── README.md           # 使用说明
```

**启动命令**：
```bash
cd skills/paoding/roi-dashboard
python server.py
# 访问 http://localhost:8080
```

---

### 方案 B：终端可视化（快速实现）

**技术栈**：
- Python + Rich 库（终端图表）
- 无 Web 依赖，纯终端展示

**功能**：
- 实时表格（Rich Table）
- 进度条（Rich Progress）
- 简单图表（Rich Graph）

**启动命令**：
```bash
python skills/paoding/roi_terminal.py
```

---

### 方案 C：集成 Bot Dashboard（最小改动）

**方式**：
- 在 Bot Dashboard 添加"ROI 统计"页面
- 复用现有数据源和 UI 框架

**路由**：
- `/roi-stats` - ROI 统计页面
- `/api/roi-data` - ROI 数据 API

**优点**：
- 复用现有 UI（像素办公室/侧边栏）
- 统一访问入口（一个 Dashboard 看所有）

**缺点**：
- 需修改 Bot Dashboard 源码
- 依赖 Next.js 构建流程

---

## 🚀 推荐执行计划

### Phase 1：终端可视化（今日，30 分钟）
**目标**：快速验证可视化效果
**产出**：`skills/paoding/roi_terminal.py`
**功能**：
- Rich 表格展示今日任务
- 成本趋势图（ASCII 艺术）
- Top 5 ROI 任务排行

### Phase 2：Web Dashboard（明日，2 小时）
**目标**：完整 Web UI 可视化
**产出**：`skills/paoding/roi-dashboard/`
**功能**：
- Chart.js 图表（折线/柱状/饼图）
- 实时刷新（10 秒）
- 时间范围筛选

### Phase 3：集成 Bot Dashboard（可选，1 小时）
**目标**：统一入口
**产出**：Bot Dashboard `/roi-stats` 页面
**功能**：
- 复用现有 UI
- 统一认证/配置

---

## 📊 数据源设计

### 数据格式（JSON）
```json
{
  "date": "2026-04-02",
  "tasks": [
    {
      "id": "TASK-050",
      "name": "知几首笔下注",
      "bot": "知几",
      "estimated_minutes": 30,
      "actual_minutes": 5,
      "efficiency": "6x",
      "token_cost": 5000,
      "cost_yuan": 0.35,
      "roi": "high"
    }
  ],
  "summary": {
    "total_tasks": 11,
    "total_cost_yuan": 2.5,
    "avg_efficiency": "11x",
    "total_tokens": 150000
  }
}
```

### 数据提取
**来源**：
- `memory/2026-04-02.md` - 任务执行记录
- `reports/*.md` - 执行报告
- `skills/paoding/ROI-CALCULATOR.md` - ROI 计算逻辑

**提取脚本**：
```python
def extract_roi_data(date):
    # 解析 memory/YYYY-MM-DD.md
    # 提取任务列表 + 成本数据
    # 返回 JSON 格式
    pass
```

---

## 🎨 UI 设计参考（Bot Dashboard）

### 配色方案
| 用途 | 颜色 | 示例 |
|------|------|------|
| 主色调 | 龙虾红 🦞 | `#FF6B6B` |
| 成功 | 绿色 | `#4CAF50` |
| 警告 | 黄色 | `#FFC107` |
| 危险 | 红色 | `#F44336` |
| 背景 | 深色模式 | `#1a1a2e` |

### 图表样式
- 折线图：平滑曲线 + 渐变填充
- 柱状图：圆角 + 悬停提示
- 饼图：3D 效果 + 图例

---

## ⚠️ 注意事项

1. **数据隐私**：ROI 数据包含成本信息，不公开分享
2. **性能**：大数据量时启用分页/懒加载
3. **实时性**：自动刷新频率不宜过高（建议 10-30 秒）
4. **兼容性**：Web Dashboard 支持主流浏览器

---

## 🔗 相关链接

- 庖丁 ROI 计算器：`skills/paoding/ROI-CALCULATOR.md`
- Bot Dashboard：http://localhost:3000
- Chart.js：https://www.chartjs.org/
- Rich 库：https://github.com/Textualize/rich

---

*创建时间：2026-04-02 21:37 | 太一 AGI v4.0 | 庖丁 ROI 可视化优化方案*
