import { TrendingUp } from 'lucide-react'

interface EvolutionProgressProps {
  level: number
  progress: number
  nextLevel: number
}

export default function EvolutionProgress({ level, progress, nextLevel }: EvolutionProgressProps) {
  const percentage = ((progress - (level - 1) * 10) / 10) * 100

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TrendingUp className="text-taiyi-blue" size={20} />
          <span className="font-semibold text-white">Level {level}</span>
        </div>
        <span className="text-sm text-gray-400">{progress}%</span>
      </div>

      <div className="relative h-4 bg-border-color rounded-full overflow-hidden">
        <div
          className="absolute h-full bg-gradient-to-r from-taiyi-blue to-tech-blue transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="flex justify-between text-xs text-gray-400">
        <span>Level {level - 1}</span>
        <span>Level {level} ({progress}%)</span>
        <span>Level {level + 1} ({nextLevel}%)</span>
      </div>

      <div className="pt-4 border-t border-border-color">
        <p className="text-sm text-gray-400 mb-2">下一级：Level {level + 1}</p>
        <div className="flex items-center gap-2">
          <div className="flex-1 h-2 bg-border-color rounded-full overflow-hidden">
            <div
              className="h-full bg-success-green transition-all duration-500"
              style={{ width: `${((progress - 90) / 5) * 100}%` }}
            />
          </div>
          <span className="text-xs text-gray-400">{Math.round(((progress - 90) / 5) * 100)}%</span>
        </div>
      </div>
    </div>
  )
}
