import { Cpu, BookOpen, CheckCircle, Activity, TrendingUp, Clock } from 'lucide-react'
import AgentCard from '../components/Dashboard/AgentCard'
import RealtimeChart from '../components/Visualization/RealtimeChart'
import Timeline from '../components/Visualization/Timeline'
import EvolutionProgress from '../components/Visualization/EvolutionProgress'

const agents = [
  { name: '太一', status: 'running', tasks: 12, health: 98 },
  { name: '知几', status: 'running', tasks: 8, health: 95 },
  { name: '山木', status: 'running', tasks: 5, health: 97 },
  { name: '素问', status: 'running', tasks: 3, health: 99 },
  { name: '罔两', status: 'idle', tasks: 0, health: 100 },
  { name: '庖丁', status: 'running', tasks: 7, health: 96 },
]

const recentEvents = [
  { time: '23:05', event: 'Dashboard 2.0 设计完成', type: 'success' },
  { time: '22:52', event: '任务成果汇报完成', type: 'success' },
  { time: '22:44', event: '进度汇报完成', type: 'info' },
  { time: '22:38', event: 'Mission Control 学习完成', type: 'success' },
  { time: '22:35', event: 'NASA OpenMCT 学习完成', type: 'success' },
  { time: '22:29', event: 'OpenClaw 升级到 4.14', type: 'success' },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Agent 数量</p>
              <p className="text-3xl font-bold text-white mt-2">9</p>
            </div>
            <Cpu className="text-taiyi-blue" size={40} />
          </div>
        </div>

        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Skill 数量</p>
              <p className="text-3xl font-bold text-white mt-2">471</p>
            </div>
            <BookOpen className="text-taiyi-blue" size={40} />
          </div>
        </div>

        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">今日任务</p>
              <p className="text-3xl font-bold text-white mt-2">342</p>
            </div>
            <CheckCircle className="text-success-green" size={40} />
          </div>
        </div>

        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">系统健康度</p>
              <p className="text-3xl font-bold text-white mt-2">98%</p>
            </div>
            <Activity className="text-success-green" size={40} />
          </div>
        </div>
      </div>

      {/* Agent 状态和自进化进度 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Cpu size={20} />
            Agent 状态
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent) => (
              <AgentCard key={agent.name} {...agent} />
            ))}
          </div>
        </div>

        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrendingUp size={20} />
            自进化程度
          </h2>
          <EvolutionProgress level={3} progress={92} nextLevel={95} />
          
          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-taiyi-blue">+50</p>
              <p className="text-sm text-gray-400">本周技能</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-taiyi-blue">+23</p>
              <p className="text-sm text-gray-400">优化技能</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-taiyi-blue">+15</p>
              <p className="text-sm text-gray-400">新增洞察</p>
            </div>
          </div>
        </div>
      </div>

      {/* 实时数据流和时间线 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity size={20} />
            实时任务流
          </h2>
          <RealtimeChart />
        </div>

        <div className="bg-card-bg rounded-lg p-6 border border-border-color">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Clock size={20} />
            事件时间线
          </h2>
          <Timeline events={recentEvents} />
        </div>
      </div>
    </div>
  )
}
