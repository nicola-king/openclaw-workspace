import React, { useState, useEffect } from 'react'

// 初始任务数据 (实际从 API 读取)
const INITIAL_TASKS = {
  todo: [
    { id: 'TASK-150', title: 'Hermes 学习循环 - 核心模块开发', priority: 'P0', assignee: '太一', due: '04-09', tags: ['技能开发', '学习循环'], status: '🟢 新创建', nextStep: '核心模块开发' },
    { id: 'TASK-111', title: '情景模式小程序 - 上传审核', priority: 'P0', assignee: '素问', due: '04-07', tags: ['小程序', '审核'], status: '🟡 MVP 完成', nextStep: '上传审核' },
    { id: 'TASK-149', title: '即梦 CLI 集成 - P2 待命', priority: 'P2', assignee: '素问', due: '-', tags: ['CLI', 'AI 绘画'], status: '🟡 P2 待命', nextStep: '按需激活' },
  ],
  doing: [
    { id: 'TASK-101', title: 'TimesFM 集成 - 模拟盘监控中', priority: 'P0', assignee: '知几', due: '✅', tags: ['时间序列', '预测'], status: '✅ 完成', nextStep: '模拟盘监控中' },
    { id: 'TASK-129', title: 'DeepTutor 学习 - CLI 增强待执行', priority: 'P0', assignee: '素问', due: '✅', tags: ['学习', 'CLI'], status: '✅ 完成', nextStep: 'CLI 增强待执行' },
  ],
  done: [
    { id: 'TASK-130', title: 'AI_NovelGenerator - 状态追踪待执行', priority: 'P0', assignee: '山木', due: '✅', tags: ['小说', '生成'], status: '✅ 完成', nextStep: '状态追踪待执行' },
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
    P0: 'bg-red-100 text-red-700 border-red-300',
    P1: 'bg-yellow-100 text-yellow-700 border-yellow-300',
    P2: 'bg-green-100 text-green-700 border-green-300',
  }
  return (
    <span className={`px-2 py-1 rounded text-xs font-bold border ${colors[priority] || colors.P2}`}>
      {priority}
    </span>
  )
}

// 任务详情弹窗组件
function TaskDetailModal({ task, onClose, onMove }) {
  if (!task) return null
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <span className="text-xs text-gray-500 font-mono">{task.id}</span>
            <h3 className="text-lg font-bold text-gray-800 mt-1">{task.title}</h3>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-2xl">×</button>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <PriorityBadge priority={task.priority} />
            <span className="text-sm text-gray-600">{task.status}</span>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-500">负责人</p>
              <p className="font-semibold">👤 {task.assignee}</p>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-xs text-gray-500">截止</p>
              <p className="font-semibold">📅 {task.due}</p>
            </div>
          </div>
          
          <div className="bg-blue-50 p-3 rounded">
            <p className="text-xs text-blue-600 font-semibold">下一步行动</p>
            <p className="text-sm text-gray-800 mt-1">{task.nextStep}</p>
          </div>
          
          {task.tags && task.tags.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-2">标签</p>
              <div className="flex flex-wrap gap-2">
                {task.tags.map((tag, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          <div className="flex gap-3 pt-4 border-t">
            <button 
              onClick={() => { onMove(task.id, 'left'); onClose(); }}
              className="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors font-semibold"
            >
              ← 移到前一列
            </button>
            <button 
              onClick={() => { onMove(task.id, 'right'); onClose(); }}
              className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-semibold"
            >
              移到后一列 →
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// 任务卡片组件
function TaskCard({ task, onMove, onDetail }) {
  return (
    <div 
      className="kanban-card bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-3 cursor-pointer hover:shadow-md transition-all active:scale-[0.98]"
      onClick={() => onDetail(task)}
    >
      <div className="flex items-start justify-between mb-2">
        <span className="text-xs text-gray-500 font-mono">{task.id}</span>
        <PriorityBadge priority={task.priority} />
      </div>
      <h4 className="text-sm font-semibold text-gray-800 mb-2 line-clamp-2">{task.title}</h4>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>👤 {task.assignee}</span>
        <span className="font-medium">📅 {task.due}</span>
      </div>
      {task.tags && task.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {task.tags.slice(0, 2).map((tag, i) => (
            <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
              {tag}
            </span>
          ))}
          {task.tags.length > 2 && (
            <span className="px-2 py-0.5 text-gray-400 text-xs">+{task.tags.length - 2}</span>
          )}
        </div>
      )}
    </div>
  )
}

// 看板列组件
function KanbanColumn({ title, icon, tasks, columnId, onMoveTask, onDetail }) {
  return (
    <div className="kanban-column bg-gray-50 rounded-lg p-4 min-w-[280px] md:min-w-[320px] flex-1">
      <div className="kanban-header font-bold text-gray-700 mb-4 flex items-center justify-between">
        <span>{icon} {title}</span>
        <span className="text-sm font-normal text-gray-500 bg-white px-2 py-1 rounded-full">{tasks.length}</span>
      </div>
      <div className="space-y-1 min-h-[200px]">
        {tasks.map(task => (
          <TaskCard 
            key={task.id} 
            task={task} 
            onMove={onMoveTask}
            onDetail={onDetail}
          />
        ))}
        {tasks.length === 0 && (
          <div className="text-center text-gray-400 text-sm py-8 border-2 border-dashed border-gray-200 rounded-lg">
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
    running: 'bg-green-100 text-green-700',
    idle: 'bg-yellow-100 text-yellow-700',
    error: 'bg-red-100 text-red-700',
  }
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-bold text-gray-800">{bot.name}</h4>
        <span className={`px-2 py-1 rounded-full text-xs ${statusColors[bot.status]}`}>
          {bot.status === 'running' ? '🟢' : bot.status === 'idle' ? '🟡' : '🔴'}
        </span>
      </div>
      <p className="text-xs text-gray-500 mb-2">{bot.role}</p>
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-600">任务数</span>
        <span className="font-semibold bg-gray-100 px-2 py-1 rounded">{bot.tasks}</span>
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
            <span className="text-gray-700 text-xs">{cron.name}</span>
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
          <p className="text-gray-500 text-xs">{title}</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
        </div>
        <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg ${colors[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

// 主应用
function App() {
  const [tasks, setTasks] = useState(INITIAL_TASKS)
  const [selectedTask, setSelectedTask] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(new Date())
  const [loading, setLoading] = useState(false)

  // 从 API 加载数据
  const loadData = async () => {
    setLoading(true)
    try {
      const [tasksRes, statsRes] = await Promise.all([
        fetch('/api/tasks'),
        fetch('/api/stats')
      ])
      
      if (tasksRes.ok) {
        const tasksData = await tasksRes.json()
        if (tasksData.success && tasksData.data) {
          setTasks(tasksData.data)
        }
      }
      
      setLastUpdate(new Date())
    } catch (error) {
      console.error('加载数据失败:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000)
    return () => clearInterval(interval)
  }, [])

  // 移动任务
  const handleMoveTask = (taskId, fromColumn, toColumn) => {
    const task = tasks[fromColumn]?.find(t => t.id === taskId)
    if (!task) return
    
    setTasks(prev => ({
      ...prev,
      [fromColumn]: prev[fromColumn].filter(t => t.id !== taskId),
      [toColumn]: [...prev[toColumn], task]
    }))
    
    // TODO: 调用 API 保存变更
    console.log(`移动任务 ${taskId} 从 ${fromColumn} 到 ${toColumn}`)
  }

  // 处理卡片点击
  const handleCardClick = (task, columnId) => {
    setSelectedTask({ ...task, columnId })
  }

  // 处理弹窗中的移动
  const handleModalMove = (direction) => {
    if (!selectedTask) return
    const columns = ['todo', 'doing', 'done']
    const currentIndex = columns.indexOf(selectedTask.columnId)
    const newIndex = direction === 'left' ? currentIndex - 1 : currentIndex + 1
    
    if (newIndex >= 0 && newIndex < columns.length) {
      handleMoveTask(selectedTask.id, selectedTask.columnId, columns[newIndex])
      setSelectedTask(null)
    }
  }

  // 统计数据
  const stats = {
    total: tasks.todo.length + tasks.doing.length + tasks.done.length,
    todo: tasks.todo.length,
    doing: tasks.doing.length,
    done: tasks.done.length,
    p0: [...tasks.todo, ...tasks.doing, ...tasks.done].filter(t => t.priority === 'P0').length,
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-[1600px] mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-800">🌟 太一看板</h1>
              <p className="text-xs text-gray-500 mt-0.5">企业级可视化协作工具</p>
            </div>
            <div className="text-right">
              <div className="text-xs text-gray-500">
                {loading ? '🔄 加载中...' : `✅ ${lastUpdate.toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})}`}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="max-w-[1600px] mx-auto px-4 py-4">
        {/* 统计卡片 */}
        <section className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
          <StatCard title="总任务" value={stats.total} icon="📋" color="blue" />
          <StatCard title="待办" value={stats.todo} icon="📝" color="yellow" />
          <StatCard title="进行中" value={stats.doing} icon="🔄" color="purple" />
          <StatCard title="已完成" value={stats.done} icon="✅" color="green" />
          <StatCard title="P0 紧急" value={stats.p0} icon="🔥" color="red" />
        </section>

        {/* 看板区域 */}
        <section className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-gray-700">📊 任务看板</h2>
          </div>
          <div className="flex gap-3 overflow-x-auto pb-4" style={{ WebkitOverflowScrolling: 'touch' }}>
            <KanbanColumn 
              title="待办" 
              icon="📝" 
              tasks={tasks.todo} 
              columnId="todo"
              onMoveTask={(taskId, from, to) => handleMoveTask(taskId, from, to)}
              onDetail={(task) => handleCardClick(task, 'todo')}
            />
            <KanbanColumn 
              title="进行中" 
              icon="🔄" 
              tasks={tasks.doing} 
              columnId="doing"
              onMoveTask={(taskId, from, to) => handleMoveTask(taskId, from, to)}
              onDetail={(task) => handleCardClick(task, 'doing')}
            />
            <KanbanColumn 
              title="已完成" 
              icon="✅" 
              tasks={tasks.done} 
              columnId="done"
              onMoveTask={(taskId, from, to) => handleMoveTask(taskId, from, to)}
              onDetail={(task) => handleCardClick(task, 'done')}
            />
          </div>
        </section>

        {/* Bot 舰队 + Cron 状态 */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Bot 状态 */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 className="font-bold text-gray-800 mb-4">🤖 Bot 舰队</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
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
        <section className="mt-4">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <h3 className="font-bold text-gray-800 mb-3">💻 系统状态</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="flex items-center gap-2 p-2 bg-green-50 rounded">
                <span className="text-xl">✅</span>
                <div>
                  <p className="text-xs text-gray-600">Gateway</p>
                  <p className="font-semibold text-green-700 text-sm">运行中</p>
                </div>
              </div>
              <div className="flex items-center gap-2 p-2 bg-blue-50 rounded">
                <span className="text-xl">💾</span>
                <div>
                  <p className="text-xs text-gray-600">Git</p>
                  <p className="font-semibold text-blue-700 text-sm">正常</p>
                </div>
              </div>
              <div className="flex items-center gap-2 p-2 bg-purple-50 rounded">
                <span className="text-xl">📜</span>
                <div>
                  <p className="text-xs text-gray-600">宪法</p>
                  <p className="font-semibold text-purple-700 text-sm">完整</p>
                </div>
              </div>
              <div className="flex items-center gap-2 p-2 bg-yellow-50 rounded">
                <span className="text-xl">💬</span>
                <div>
                  <p className="text-xs text-gray-600">通道</p>
                  <p className="font-semibold text-yellow-700 text-sm">正常</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-white border-t mt-6">
        <div className="max-w-[1600px] mx-auto px-4 py-3 text-center text-gray-500 text-xs">
          太一看板 Dashboard v1.0 | 数据源：HEARTBEAT.md
        </div>
      </footer>

      {/* 任务详情弹窗 */}
      {selectedTask && (
        <TaskDetailModal 
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onMove={(taskId, direction) => {
            const columns = ['todo', 'doing', 'done']
            const currentIndex = columns.indexOf(selectedTask.columnId)
            const newIndex = direction === 'left' ? currentIndex - 1 : currentIndex + 1
            if (newIndex >= 0 && newIndex < columns.length) {
              handleMoveTask(taskId, selectedTask.columnId, columns[newIndex])
            }
            setSelectedTask(null)
          }}
        />
      )}
    </div>
  )
}

export default App
