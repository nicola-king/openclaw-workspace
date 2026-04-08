import React, { useState, useEffect } from 'react'

// 模拟 Bot 数据
const MOCK_BOTS = [
  { id: 'zhiji', name: '知几-E', status: 'running', balance: '$10,000', todayPnL: '+5.38%', winRate: '54%', tasks: 3 },
  { id: 'shanmu', name: '山木', status: 'running', balance: 'N/A', todayPnL: 'N/A', winRate: 'N/A', tasks: 5 },
  { id: 'suwen', name: '素问', status: 'running', balance: 'N/A', todayPnL: 'N/A', winRate: 'N/A', tasks: 2 },
  { id: 'wangliang', name: '罔两', status: 'idle', balance: 'N/A', todayPnL: 'N/A', winRate: 'N/A', tasks: 0 },
  { id: 'paoding', name: '庖丁', status: 'running', balance: '¥50,000', todayPnL: '+2.1%', winRate: 'N/A', tasks: 1 },
  { id: 'shoucangli', name: '守藏吏', status: 'running', balance: 'N/A', todayPnL: 'N/A', winRate: 'N/A', tasks: 8 },
  { id: 'taiyi', name: '太一', status: 'running', balance: 'N/A', todayPnL: 'N/A', winRate: 'N/A', tasks: 12 },
]

// 状态卡片组件
function StatusCard({ bot }) {
  const statusColors = {
    running: 'bg-green-500',
    idle: 'bg-yellow-500',
    error: 'bg-red-500',
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800">{bot.name}</h3>
        <span className={`${statusColors[bot.status]} text-white px-3 py-1 rounded-full text-sm`}>
          {bot.status === 'running' ? '🟢 运行中' : bot.status === 'idle' ? '🟡 待机' : '🔴 错误'}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-gray-500 text-sm">余额/预算</p>
          <p className="text-lg font-semibold">{bot.balance}</p>
        </div>
        <div>
          <p className="text-gray-500 text-sm">今日收益</p>
          <p className={`text-lg font-semibold ${bot.todayPnL.startsWith('+') ? 'text-green-600' : 'text-gray-600'}`}>
            {bot.todayPnL}
          </p>
        </div>
        <div>
          <p className="text-gray-500 text-sm">胜率</p>
          <p className="text-lg font-semibold">{bot.winRate}</p>
        </div>
        <div>
          <p className="text-gray-500 text-sm">任务数</p>
          <p className="text-lg font-semibold">{bot.tasks}</p>
        </div>
      </div>
    </div>
  )
}

// 系统状态组件
function SystemStatus() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">📊 系统状态</h3>
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-600">Gateway</span>
          <span className="text-green-600">✅ 运行中 (PID 131952)</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">内存使用</span>
          <span className="text-gray-800">669.6 MB</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">CPU 使用</span>
          <span className="text-gray-800">42.7s</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Git 状态</span>
          <span className="text-green-600">✅ 正常</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">宪法完整性</span>
          <span className="text-green-600">✅ 完整</span>
        </div>
      </div>
    </div>
  )
}

// 主应用
function App() {
  const [bots, setBots] = useState(MOCK_BOTS)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    // 模拟实时数据更新
    const interval = setInterval(() => {
      setLastUpdate(new Date())
    }, 30000) // 每 30 秒更新

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-800">🤖 太一 AGI · Bot Dashboard</h1>
            <div className="text-sm text-gray-500">
              最后更新：{lastUpdate.toLocaleTimeString('zh-CN')}
            </div>
          </div>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Bot 状态网格 */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">📡 Bot 舰队状态</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bots.map(bot => (
              <StatusCard key={bot.id} bot={bot} />
            ))}
          </div>
        </section>

        {/* 系统状态 */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SystemStatus />
          
          {/* 快速统计 */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">📈 今日统计</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded">
                <span className="text-gray-700">运行中 Bot</span>
                <span className="text-2xl font-bold text-blue-600">6</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded">
                <span className="text-gray-700">完成任务</span>
                <span className="text-2xl font-bold text-green-600">31</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-purple-50 rounded">
                <span className="text-gray-700">生成文件</span>
                <span className="text-2xl font-bold text-purple-600">20</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded">
                <span className="text-gray-700">Git 提交</span>
                <span className="text-2xl font-bold text-yellow-600">8</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-white border-t mt-8">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-gray-500 text-sm">
          太一 AGI Bot Dashboard v1.0 | 最后更新：{lastUpdate.toLocaleString('zh-CN')}
        </div>
      </footer>
    </div>
  )
}

export default App
