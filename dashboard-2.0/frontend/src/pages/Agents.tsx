import { useState } from 'react'
import { Search, Plus, Edit, Trash2, MoreVertical } from 'lucide-react'

const mockAgents = [
  { id: 'taiyi', name: '太一', status: 'running', tasks: 12, health: 98, lastActive: '刚刚' },
  { id: 'zhiji', name: '知几', status: 'running', tasks: 8, health: 95, lastActive: '1 分钟前' },
  { id: 'shanmu', name: '山木', status: 'running', tasks: 5, health: 97, lastActive: '2 分钟前' },
  { id: 'suwen', name: '素问', status: 'running', tasks: 3, health: 99, lastActive: '3 分钟前' },
  { id: 'wangliang', name: '罔两', status: 'idle', tasks: 0, health: 100, lastActive: '5 分钟前' },
  { id: 'paoding', name: '庖丁', status: 'running', tasks: 7, health: 96, lastActive: '刚刚' },
]

export default function Agents() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filter, setFilter] = useState<'all' | 'running' | 'idle'>('all')

  const filteredAgents = mockAgents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filter === 'all' || agent.status === filter
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Agent 管理</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-taiyi-blue text-white rounded-lg hover:bg-tech-blue transition-colors">
          <Plus size={20} />
          <span>新建 Agent</span>
        </button>
      </div>

      {/* 搜索和筛选 */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="搜索 Agent..."
            className="w-full pl-10 pr-4 py-2 bg-card-bg border border-border-color rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-taiyi-blue"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select
          className="px-4 py-2 bg-card-bg border border-border-color rounded-lg text-white focus:outline-none focus:border-taiyi-blue"
          value={filter}
          onChange={(e) => setFilter(e.target.value as 'all' | 'running' | 'idle')}
        >
          <option value="all">全部</option>
          <option value="running">运行中</option>
          <option value="idle">空闲</option>
        </select>
      </div>

      {/* Agent 列表 */}
      <div className="bg-card-bg rounded-lg border border-border-color overflow-hidden">
        <table className="w-full">
          <thead className="bg-border-color">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">名称</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">状态</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">任务</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">健康度</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">最后活跃</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-color">
            {filteredAgents.map((agent) => (
              <tr key={agent.id} className="hover:bg-border-color/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="w-10 h-10 rounded-full bg-taiyi-blue flex items-center justify-center text-white font-bold">
                      {agent.name[0]}
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-white">{agent.name}</div>
                      <div className="text-sm text-gray-400">{agent.id}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    agent.status === 'running'
                      ? 'bg-success-green/20 text-success-green'
                      : 'bg-warning-yellow/20 text-warning-yellow'
                  }`}>
                    {agent.status === 'running' ? '运行中' : '空闲'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                  {agent.tasks} 进行中
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="w-full bg-border-color rounded-full h-2 mr-2">
                      <div
                        className={`h-2 rounded-full ${
                          agent.health >= 95 ? 'bg-success-green' : 'bg-warning-yellow'
                        }`}
                        style={{ width: `${agent.health}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-400">{agent.health}%</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                  {agent.lastActive}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-taiyi-blue hover:text-white mr-3">
                    <Edit size={16} />
                  </button>
                  <button className="text-error-red hover:text-white mr-3">
                    <Trash2 size={16} />
                  </button>
                  <button className="text-gray-400 hover:text-white">
                    <MoreVertical size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 统计信息 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">总 Agent 数</div>
          <div className="text-2xl font-bold text-white mt-1">{mockAgents.length}</div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">运行中</div>
          <div className="text-2xl font-bold text-success-green mt-1">
            {mockAgents.filter(a => a.status === 'running').length}
          </div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">平均健康度</div>
          <div className="text-2xl font-bold text-taiyi-blue mt-1">
            {Math.round(mockAgents.reduce((sum, a) => sum + a.health, 0) / mockAgents.length)}%
          </div>
        </div>
      </div>
    </div>
  )
}
