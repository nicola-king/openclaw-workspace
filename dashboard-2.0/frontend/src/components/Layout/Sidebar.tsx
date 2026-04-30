import { LayoutDashboard, Cpu, BookOpen, CheckSquare, ClipboardList, Users, Settings } from 'lucide-react'
import { useLocation } from 'react-router-dom'

const menuItems = [
  { icon: LayoutDashboard, label: '仪表盘', path: '/' },
  { icon: Cpu, label: 'Agent', path: '/agents' },
  { icon: BookOpen, label: 'Skill', path: '/skills' },
  { icon: CheckSquare, label: '任务', path: '/tasks' },
  { icon: ClipboardList, label: '审批', path: '/approvals' },
  { icon: Users, label: '审计', path: '/audit' },
  { icon: Settings, label: '设置', path: '/settings' },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="w-64 bg-card-bg border-r border-border-color flex flex-col">
      <nav className="flex-1 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <a
              key={item.path}
              href={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-colors ${
                isActive
                  ? 'bg-taiyi-blue text-white'
                  : 'text-gray-400 hover:bg-border-color hover:text-white'
              }`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </a>
          )
        })}
      </nav>
    </aside>
  )
}
