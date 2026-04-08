import React, { useState, useEffect } from 'react'

// 模拟任务数据 (实际从 HEARTBEAT.md 读取)
const INITIAL_TASKS = {
  todo: [
    { id: 'TASK-150', title: 'Hermes 学习循环 - 核心模块开发', priority: 'P0', assignee: '太一', due: '04-09', tags: ['技能开发', '学习循环'] },
    { id: 'TASK-111', title: '情景模式小程序 - 上传审核', priority: 'P0', assignee: '素问', due: '04-07', tags: ['小程序', '审核'] },
    { id: 'TASK-149', title: '即梦 CLI 集成 - P2 待命', priority: 'P2', assignee: '素问', due: '-', tags: ['CLI', 'AI 绘画'] },
  ],
  doing: [
    { id: 'TASK-101', title: 'TimesFM 集成 - 模拟盘监控中', priority: 'P0', assignee: '知几', due: '✅', tags: ['时间序列', '预测'] },
    { id: 'TASK-129', title: 'DeepTutor 学习 - CLI 增强待执行', priority: 'P0', assignee: '素问', due: '✅', tags: ['学习', 'CLI'] },
  ],
  done: [
    { id: 'TASK-130', title: 'AI_NovelGenerator - 状态追踪待执行', priority: 'P0', assignee: '山木', due: '✅', tags: ['小说', '生成'] },
  ]
}

// Bot 数据
const BOTS = [
  { id: 'taiyi', name: '太一', role: '执行总管', status: 'running', tasks: 12 },
  { id: 'zhiji', name: '知几-E', role: '量化交易', status: 'running', tasks: 3 },
  { id: 'shanmu', name: '山木', role: '内容创意', status: 'running', tasks: 5 },
  { id: 'suwen', name: '素问', role: '技术开发', status: 'running', tasks: 8 },
  { id: 'wangliang', name: '罔两', role: '高价值发现', status: 'idle', tasks: 0 },
  { id: 'paoding', name: '庖丁', role: '预算追踪', status: 'running', tasks: 1 },
  { id: 'shoucangli', name: '守藏吏', role: '知识管理', status: 'running', tasks: 8 },
]

// Cron 任务状态
const CRON_STATUS = [
  { name: '每 5 分钟 - 自动执行', status: 'ok', lastRun: '07:45' },
  { name: '每 10 分钟 - 通道检查', status: 'ok', lastRun: '07:40' },
  { name: '每 30 分钟 - Git 备份', status: 'ok', lastRun: '07:30' },
  { name: '每小时 - 天气预测', status: 'ok', lastRun: '07:00' },
  { name: '每小时 - 系统自检', status: 'ok', lastRun: '07:00' },
  { name: '每日 06:00 - 宪法学习', status: 'ok', lastRun: '06:00' },
  { name: '每日 23:00 - 日报生成', status: 'pending', lastRun: '昨日' },
]

// 优先级标签组件
function PriorityBadge({ priority }) {
  const colors = {
    P0: 'priority-p0',
    P1: 'priority-p1',
    P2: 'priority-p2',
  }
  return (
    <span className={`px-2 py-1 rounded text-xs font-bold border ${colors[priority]}`}>
      {priority}
    </span>
  )
}

// 任务卡片组件
function TaskCard({ task, onMove }) {
  return (
    <div className="kanban-card">
      <div className="flex items-start justify-between mb-2">
        <span className="text-xs text-gray-500 font-mono">{task.id}</span>
        <PriorityBadge priority={task.priority} />
      </div>
      <h4 className="text-sm font-semibold text-gray-800 mb-2">{task.title}</h4>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>👤 {task.assignee}</span>
        <span>📅 {task.due}</span>
      </div>
      <div className="flex flex-wrap gap-1 mt-2">
        {task.tags.map((tag, i) => (
          <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
            {tag}
          </span>
        ))}
      </div>
      <div className="flex gap-2 mt-3 pt-3 border-t">
        <button 
          onClick={() => onMove(task.id, 'left')}
          className="flex-1 px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
        >
          ← 左移
        </button>
        <button 
          onClick={() => onMove(task.id, 'right')}
          className="flex-1 px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
        >
          右移 →
        </button>
      </div>
    </div>
  )
}

// 看板列组件
function KanbanColumn({ title, icon, tasks, columnId, totalColumns, onMoveTask }) {
  return (
    <div className="kanban-column">
      <div className="kanban-header">
        <span>{icon} {title}</span>
        <span className="text-sm font-normal text-gray-500">{tasks.length}</span>
      </div>
      <div className="space-y-1">
        {tasks.map(task => (
          <TaskCard 
            key={task.id} 
            task={task} 
            onMove={(taskId, direction) => {
              const columns = ['todo', 'doing', 'done']
              const currentIndex = columns.indexOf(columnId)
              const newIndex = direction === 'left' ? currentIndex - 1 : currentIndex + 1
              if (newIndex >= 0 && newIndex < columns.length) {
                onMoveTask(taskId, columnId, columns[newIndex])
              }
            }}
          />
        ))}
        {tasks.length === 0 && (
          <div className="text-center text-gray-400 text-sm py-8">
            暂无任务
          </div>
        )}
      </div>
    </div>
  )
}

// Bot 状态卡片组件
function BotCard({ bot }) {
  const statusColors = {
    running: '🟢 运行中',
    idle: '🟡 待机',
    error: '🔴 错误',
  }
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-bold text-gray-800">{bot.name}</h4>
        <span className={`px-2 py-1 rounded-full text-xs ${bot.status === 'running' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
          {statusColors[bot.status]}
        </span>
      </div>
      <p className="text-xs text-gray-500 mb-2">{bot.role}</p>
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-600">任务数</span>
        <span className="font-semibold">{bot.tasks}</span>
      </div>
    </div>
  )
}

// Cron 状态组件
function CronStatus() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <h3 className="font-bold text-gray-800 mb-4">⏰ Cron 任务状态</h3>
      <div className="space-y-2">
        {CRON_STATUS.map((cron, i) => (
          <div key={i} className="flex items-center justify-between text-sm p-2 bg-gray-50 rounded">
            <span className="text-gray-700">{cron.name}</span>
            <div className="flex items-center gap-2">
              <span className="text-gray-500 text-xs">{cron.lastRun}</span>
              <span className={cron.status === 'ok' ? 'text-green-600' : 'text-yellow-600'}>
                {cron.status === 'ok' ? '✅' : '⏳'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// 统计卡片组件
function StatCard({ title, value, icon, color }) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    red: 'bg-red-50 text-red-600',
  }
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-full flex items-center justify-center text-xl ${colors[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

// 主应用
function App() {
  const [tasks, setTasks] = useState(INITIAL_TASKS)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  // 移动任务
  const handleMoveTask = (taskId, fromColumn, toColumn) => {
    const task = tasks[fromColumn].find(t => t.id === taskId)
    if (!task) return
    
    setTasks(prev => ({
      ...prev,
      [fromColumn]: prev[fromColumn].filter(t => t.id !== taskId),
      [toColumn]: [...prev[toColumn], task]
    }))
    setLastUpdate(new Date())
  }

  // 统计数据
  const stats = {
    total: tasks.todo.length + tasks.doing.length + tasks.done.length,
    todo: tasks.todo.length,
    doing: tasks.doing.length,
    done: tasks.done.length,
    p0: [...tasks.todo, ...tasks.doing, ...tasks.done].filter(t => t.priority === 'P0').length,
  }

  useEffect(() => {
    // 模拟实时数据更新
    const interval = setInterval(() => {
      setLastUpdate(new Date())
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-[1600px] mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">🌟 太一看板 Dashboard</h1>
              <p className="text-sm text-gray-500 mt-1">企业级可视化项目协作工具 · 太一 AGI 定制版</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">
                最后更新：{lastUpdate.toLocaleTimeString('zh-CN')}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                下次自动刷新：30 秒
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="max-w-[1600px] mx-auto px-4 py-6">
        {/* 统计卡片 */}
        <section className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <StatCard title="总任务数" value={stats.total} icon="📋" color="blue" />
          <StatCard title="待办" value={stats.todo} icon="📝" color="yellow" />
          <StatCard title="进行中" value={stats.doing} icon="🔄" color="purple" />
          <StatCard title="已完成" value={stats.done} icon="✅" color="green" />
          <StatCard title="P0 紧急" value={stats.p0} icon="🔥" color="red" />
        </section>

        {/* 看板区域 */}
        <section className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-700">📊 任务看板</h2>
            <div className="flex gap-2">
              <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm">
                + 新建任务
              </button>
              <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors text-sm">
                📥 导入 HEARTBEAT.md
              </button>
            </div>
          </div>
          <div className="flex gap-4 overflow-x-auto pb-4">
            <KanbanColumn 
              title="待办" 
              icon="📝" 
              tasks={tasks.todo} 
              columnId="todo"
              totalColumns={3}
              onMoveTask={handleMoveTask}
            />
            <KanbanColumn 
              title="进行中" 
              icon="🔄" 
              tasks={tasks.doing} 
              columnId="doing"
              totalColumns={3}
              onMoveTask={handleMoveTask}
            />
            <KanbanColumn 
              title="已完成" 
              icon="✅" 
              tasks={tasks.done} 
              columnId="done"
              totalColumns={3}
              onMoveTask={handleMoveTask}
            />
          </div>
        </section>

        {/* Bot 舰队 + Cron 状态 */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Bot 状态 */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 className="font-bold text-gray-800 mb-4">🤖 Bot 舰队状态</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {BOTS.map(bot => (
                  <BotCard key={bot.id} bot={bot} />
                ))}
              </div>
            </div>
          </div>
          
          {/* Cron 状态 */}
          <div>
            <CronStatus />
          </div>
        </section>

        {/* 系统状态 */}
        <section className="mt-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <h3 className="font-bold text-gray-800 mb-4"> 系统状态</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="flex items-center gap-3 p-3 bg-green-50 rounded">
                <span className="text-2xl">✅</span>
                <div>
                  <p className="text-sm text-gray-600">Gateway</p>
                  <p className="font-semibold text-green-700">运行中 (PID 139746)</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-blue-50 rounded">
                <span className="text-2xl">💾</span>
                <div>
                  <p className="text-sm text-gray-600">Git 状态</p>
                  <p className="font-semibold text-blue-700">正常</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-purple-50 rounded">
                <span className="text-2xl">📜</span>
                <div>
                  <p className="text-sm text-gray-600">宪法完整性</p>
                  <p className="font-semibold text-purple-700">完整</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded">
                <span className="text-2xl">💬</span>
                <div>
                  <p className="text-sm text-gray-600">通讯通道</p>
                  <p className="font-semibold text-yellow-700">微信/Telegram 正常</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-white border-t mt-8">
        <div className="max-w-[1600px] mx-auto px-4 py-4 text-center text-gray-500 text-sm">
          太一看板 Dashboard v1.0 | 基于 React + Vite + TailwindCSS | 数据源：HEARTBEAT.md
        </div>
      </footer>
    </div>
  )
}

export default App
