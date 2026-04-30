import { Activity, GitCommit, Settings } from 'lucide-react'

export default function Header() {
  return (
    <header className="h-16 bg-card-bg border-b border-border-color flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold text-taiyi-blue">太一 Dashboard 2.0</h1>
        <nav className="flex gap-4">
          <a href="/" className="text-sm text-gray-400 hover:text-white">仪表盘</a>
          <a href="/agents" className="text-sm text-gray-400 hover:text-white">Agent</a>
          <a href="/skills" className="text-sm text-gray-400 hover:text-white">Skill</a>
        </nav>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm text-success-green">
          <Activity size={16} />
          <span>系统正常</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <GitCommit size={16} />
          <span>v2.0.0</span>
        </div>
        <Settings size={20} className="text-gray-400 cursor-pointer hover:text-white" />
      </div>
    </header>
  )
}
