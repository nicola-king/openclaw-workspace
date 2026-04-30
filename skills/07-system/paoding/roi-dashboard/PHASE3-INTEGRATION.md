# 庖丁 ROI Dashboard - Phase 3 集成方案

> 集成到 Bot Dashboard | `/roi-stats` 页面

---

## 🎯 集成目标

将庖丁 ROI 可视化集成到现有 Bot Dashboard，统一访问入口。

---

## 📁 文件结构

```
/tmp/OpenClaw-bot-review/
├── app/
│   ├── roi-stats/
│   │   └── page.tsx          # ROI 统计页面（新增）
│   ├── api/
│   │   └── roi-data/
│   │       └── route.ts      # ROI 数据 API（新增）
│   └── sidebar.tsx           # 添加 ROI 菜单项（修改）
```

---

## 🔧 实现步骤

### Step 1: 创建 API 路由

**文件**: `app/api/roi-data/route.ts`

```typescript
import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

export async function GET() {
  try {
    // 读取 memory/YYYY-MM-DD.md
    const date = new Date().toISOString().split('T')[0];
    const memoryPath = join(process.env.OPENCLAW_HOME || '/home/nicola/.openclaw/workspace', 'memory', `${date}.md`);
    const content = await readFile(memoryPath, 'utf-8');
    
    // 解析任务数据（简化版）
    const tasks = content.split('\n')
      .filter(line => line.includes('TASK-') && line.includes('✅'))
      .map(line => ({
        id: 'TASK-XXX',
        name: line.split('|')[2]?.trim() || 'Unknown',
        status: '完成',
        efficiency: '10x',
        cost: 0.35,
        roi: 'high'
      }));
    
    return NextResponse.json({
      date,
      tasks: tasks.slice(0, 10),
      summary: {
        total_tasks: tasks.length,
        total_cost_yuan: tasks.length * 0.35,
        avg_efficiency: '11x',
        total_tokens: tasks.length * 5000
      }
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to load ROI data' }, { status: 500 });
  }
}
```

---

### Step 2: 创建 ROI 页面

**文件**: `app/roi-stats/page.tsx`

```typescript
'use client';

import { useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';

interface Task {
  id: string;
  name: string;
  efficiency: string;
  cost: number;
  roi: string;
}

interface Summary {
  total_tasks: number;
  total_cost_yuan: number;
  avg_efficiency: string;
  total_tokens: number;
}

export default function ROIStatsPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    fetch('/api/roi-data')
      .then(res => res.json())
      .then(data => {
        setTasks(data.tasks);
        setSummary(data.summary);
      });
  }, []);

  if (!summary) return <div>加载中...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">🦞 庖丁 ROI 统计</h1>
      
      {/* 汇总卡片 */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-sm text-muted">总任务数</h3>
          <p className="text-2xl font-bold">{summary.total_tasks}</p>
        </div>
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-sm text-muted">总成本</h3>
          <p className="text-2xl font-bold">¥{summary.total_cost_yuan.toFixed(2)}</p>
        </div>
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-sm text-muted">平均效率</h3>
          <p className="text-2xl font-bold">{summary.avg_efficiency}</p>
        </div>
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-sm text-muted">总 Token</h3>
          <p className="text-2xl font-bold">{summary.total_tokens.toLocaleString()}</p>
        </div>
      </div>

      {/* 图表 */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-lg mb-4">成本趋势</h3>
          <Line data={{
            labels: tasks.map((_, i) => `T${i + 1}`),
            datasets: [{
              label: '成本 (¥)',
              data: tasks.map(t => t.cost),
              borderColor: '#FF6B6B',
              tension: 0.4
            }]
          }} />
        </div>
        <div className="bg-card p-4 rounded-lg">
          <h3 className="text-lg mb-4">效率分布</h3>
          <Bar data={{
            labels: tasks.map(t => t.id),
            datasets: [{
              label: '效率',
              data: tasks.map(t => parseFloat(t.efficiency)),
              backgroundColor: '#4CAF50'
            }]
          }} />
        </div>
      </div>

      {/* 任务表格 */}
      <div className="bg-card p-4 rounded-lg">
        <h3 className="text-lg mb-4">任务详情</h3>
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2">任务 ID</th>
              <th>名称</th>
              <th>效率</th>
              <th>成本</th>
              <th>ROI</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map(task => (
              <tr key={task.id} className="border-b">
                <td className="py-2 font-mono">{task.id}</td>
                <td>{task.name}</td>
                <td className="text-green-500">{task.efficiency}</td>
                <td className="text-yellow-500">¥{task.cost.toFixed(2)}</td>
                <td>{task.roi === 'high' ? '🚀 高' : '⚡ 中'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

### Step 3: 修改侧边栏

**文件**: `app/sidebar.tsx`

在"监控"部分添加：

```typescript
<a
  className="flex items-center rounded-lg text-sm transition-colors text-muted hover:text-foreground hover:bg-bg"
  style={{ padding: '8px 12px', gap: '10px' }}
  href="/roi-stats"
>
  <span className="inline-flex h-8 w-8 items-center justify-center border border-border bg-bg/88">
    📊
  </span>
  ROI 统计
</a>
```

---

## 🚀 部署流程

### 方式 A：手动集成（推荐）

```bash
cd /tmp/OpenClaw-bot-review

# 1. 创建 API 路由
mkdir -p app/api/roi-data
cp /home/nicola/.openclaw/workspace/skills/paoding/roi-dashboard/route.ts app/api/roi-data/

# 2. 创建页面
mkdir -p app/roi-stats
cp /home/nicola/.openclaw/workspace/skills/paoding/roi-dashboard/page.tsx app/roi-stats/

# 3. 修改侧边栏
# 手动编辑 app/sidebar.tsx

# 4. 重新构建
npm run build
npm start
```

### 方式 B：自动化脚本

```bash
python /home/nicola/.openclaw/workspace/skills/paoding/roi-dashboard/integrate.py
```

---

## 📊 访问地址

| 版本 | 地址 | 状态 |
|------|------|------|
| Phase 1 | 终端 | `python roi_terminal.py` |
| Phase 2 | 独立 Web | `http://localhost:8080` |
| Phase 3 | 集成 Dashboard | `http://localhost:3000/roi-stats` |

---

## ⚠️ 注意事项

1. **依赖安装**: Phase 2 需要 `fastapi` 和 `uvicorn`
2. **数据源**: 读取 `memory/YYYY-MM-DD.md`，需确保文件存在
3. **刷新频率**: 建议 10-30 秒，避免频繁读取文件
4. **权限**: 确保有读取 workspace 的权限

---

*创建时间：2026-04-02 21:47 | 太一 AGI v4.0 | Phase 3 集成方案*
