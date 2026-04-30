import { Activity, Server, Clock } from 'lucide-react'

export default function Footer() {
  const now = new Date().toLocaleString('zh-CN')

  return (
    <footer className="h-10 bg-card-bg border-t border-border-color flex items-center justify-between px-6 text-sm text-gray-400">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Activity size={14} />
          <span>Gateway: 运行中</span>
        </div>
        <div className="flex items-center gap-2">
          <Server size={14} />
          <span>OpenClaw 2026.4.14</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Clock size={14} />
        <span>{now}</span>
      </div>
    </footer>
  )
}
