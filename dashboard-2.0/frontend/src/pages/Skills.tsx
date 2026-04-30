import { useState } from 'react'
import { Search, Plus, Edit, Trash2, Filter } from 'lucide-react'

const mockSkills = [
  { id: 'trading', name: '交易 Agent', category: '交易', count: 3, status: 'active' },
  { id: 'analysis', name: '分析 Agent', category: '分析', count: 5, status: 'active' },
  { id: 'content', name: '内容 Agent', category: '内容', count: 4, status: 'active' },
  { id: 'voice', name: '语音 Agent', category: '交互', count: 2, status: 'active' },
  { id: 'memory', name: '记忆 Agent', category: '系统', count: 3, status: 'active' },
]

export default function Skills() {
  const [searchTerm, setSearchTerm] = useState('')
  const [category, setCategory] = useState('all')

  const categories = ['all', '交易', '分析', '内容', '交互', '系统']

  const filteredSkills = mockSkills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = category === 'all' || skill.category === category
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Skill 管理</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-taiyi-blue text-white rounded-lg hover:bg-tech-blue transition-colors">
          <Plus size={20} />
          <span>新建 Skill</span>
        </button>
      </div>

      {/* 搜索和筛选 */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="搜索 Skill..."
            className="w-full pl-10 pr-4 py-2 bg-card-bg border border-border-color rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-taiyi-blue"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={20} className="text-gray-400" />
          <select
            className="px-4 py-2 bg-card-bg border border-border-color rounded-lg text-white focus:outline-none focus:border-taiyi-blue"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="all">全部类别</option>
            {categories.filter(c => c !== 'all').map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Skill 网格 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSkills.map((skill) => (
          <div key={skill.id} className="bg-card-bg rounded-lg p-6 border border-border-color hover:border-taiyi-blue transition-colors">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-white">{skill.name}</h3>
                <p className="text-sm text-gray-400 mt-1">{skill.category}</p>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full ${
                skill.status === 'active'
                  ? 'bg-success-green/20 text-success-green'
                  : 'bg-gray-500/20 text-gray-400'
              }`}>
                {skill.status === 'active' ? '活跃' : '停用'}
              </span>
            </div>
            <div className="text-sm text-gray-400 mb-4">
              包含 {skill.count} 个子技能
            </div>
            <div className="flex items-center gap-2">
              <button className="flex-1 px-3 py-2 bg-border-color text-white rounded-lg hover:bg-taiyi-blue transition-colors text-sm">
                编辑
              </button>
              <button className="px-3 py-2 bg-border-color text-error-red rounded-lg hover:bg-error-red hover:text-white transition-colors text-sm">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* 统计信息 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">总 Skill 数</div>
          <div className="text-2xl font-bold text-white mt-1">471</div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">活跃 Skill</div>
          <div className="text-2xl font-bold text-success-green mt-1">450</div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">类别数</div>
          <div className="text-2xl font-bold text-taiyi-blue mt-1">{categories.length - 1}</div>
        </div>
        <div className="bg-card-bg rounded-lg p-4 border border-border-color">
          <div className="text-sm text-gray-400">本周新增</div>
          <div className="text-2xl font-bold text-success-green mt-1">+50</div>
        </div>
      </div>
    </div>
  )
}
