import { useState } from 'react'
import { CheckCircle, XCircle, Clock, Filter } from 'lucide-react'

const mockApprovals = [
  {
    id: '1',
    type: 'Agent 创建',
    description: '创建新的交易 Skill',
    requester: '知几',
    time: '23:00',
    status: 'pending',
    priority: 'high'
  },
  {
    id: '2',
    type: '敏感操作',
    description: '删除旧配置文件',
    requester: '素问',
    time: '22:45',
    status: 'pending',
    priority: 'medium'
  },
  {
    id: '3',
    type: '配置变更',
    description: '更新 Gateway 配置',
    requester: '太一',
    time: '22:30',
    status: 'approved',
    priority: 'low'
  },
  {
    id: '4',
    type: 'Skill 部署',
    description: '部署新 Skill 到生产环境',
    requester: '山木',
    time: '22:15',
    status: 'rejected',
    priority: 'medium'
  },
]

export default function Approvals() {
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all')

  const filteredApprovals = mockApprovals.filter(approval => {
    if (filter === 'all') return true
    return approval.status === filter
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock size={16} className="text-warning-yellow" />
      case 'approved': return <CheckCircle size={16} className="text-success-green" />
      case 'rejected': return <XCircle size={16} className="text-error-red" />
      default: return null
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-error-red'
      case 'medium': return 'text-warning-yellow'
      case 'low': return 'text-gray-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">审批管理</h1>
        <div className="flex items-center gap-2">
          <Filter size={20} className="text-gray-400" />
          <select
            className="px-4 py-2 bg-card-bg border border-border-color rounded-lg text-white focus:outline-none focus:border-taiyi-blue"
            value={filter}
            onChange={(e) => setFilter(e.target.value as 'all' | 'pending' | 'approved' | 'rejected')}
          >
            <option value="all">全部</option>
            <option value="pending">待审批</option>
            <option value="approved">已通过</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">总审批数</div>
          <div className="text-2xl font-bold text-white mt-1">{mockApprovals.length}</div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">待审批</div>
          <div className="text-2xl font-bold text-warning-yellow mt-1">
            {mockApprovals.filter(a => a.status === 'pending').length}
          </div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">已通过</div>
          <div className="text-2xl font-bold text-success-green mt-1">
            {mockApprovals.filter(a => a.status === 'approved').length}
          </div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">已拒绝</div>
          <div className="text-2xl font-bold text-error-red mt-1">
            {mockApprovals.filter(a => a.status === 'rejected').length}
          </div>
        </div>
      </div>

      {/* 审批列表 */}
      <div className="bg-card-bg rounded-lg border border-border-color overflow-hidden">
        <table className="w-full">
          <thead className="bg-border-color">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">类型</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">描述</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">请求人</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">时间</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">优先级</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">状态</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-color">
            {filteredApprovals.map((approval) => (
              <tr key={approval.id} className="hover:bg-border-color/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{approval.type}</td>
                <td className="px-6 py-4 text-sm text-gray-400">{approval.description}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{approval.requester}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{approval.time}</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm ${getPriorityColor(approval.priority)}`}>
                  {approval.priority === 'high' ? '高' : approval.priority === 'medium' ? '中' : '低'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(approval.status)}
                    <span className="text-sm text-gray-400">
                      {approval.status === 'pending' ? '待审批' : approval.status === 'approved' ? '已通过' : '已拒绝'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  {approval.status === 'pending' && (
                    <>
                      <button className="text-success-green hover:text-white mr-3">批准</button>
                      <button className="text-error-red hover:text-white">拒绝</button>
                    </>
                  )}
                  {approval.status !== 'pending' && (
                    <button className="text-taiyi-blue hover:text-white">详情</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
