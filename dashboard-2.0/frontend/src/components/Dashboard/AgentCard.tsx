interface AgentCardProps {
  name: string
  status: 'running' | 'idle' | 'error'
  tasks: number
  health: number
}

export default function AgentCard({ name, status, tasks, health }: AgentCardProps) {
  const statusConfig = {
    running: { color: 'text-success-green', dot: 'bg-success-green', label: '运行中' },
    idle: { color: 'text-warning-yellow', dot: 'bg-warning-yellow', label: '空闲' },
    error: { color: 'text-error-red', dot: 'bg-error-red', label: '错误' },
  }

  const config = statusConfig[status]

  return (
    <div className="bg-border-color rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-white">{name}</h3>
        <div className={`flex items-center gap-2 ${config.color}`}>
          <div className={`w-2 h-2 rounded-full ${config.dot}`} />
          <span className="text-xs">{config.label}</span>
        </div>
      </div>
      <div className="space-y-2 text-sm text-gray-400">
        <div className="flex justify-between">
          <span>任务</span>
          <span className="text-white">{tasks} 进行中</span>
        </div>
        <div className="flex justify-between">
          <span>健康度</span>
          <span className={health >= 95 ? 'text-success-green' : 'text-warning-yellow'}>{health}%</span>
        </div>
      </div>
    </div>
  )
}
