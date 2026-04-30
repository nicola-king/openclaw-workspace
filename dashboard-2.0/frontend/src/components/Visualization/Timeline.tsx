import { Clock } from 'lucide-react'

interface Event {
  time: string
  event: string
  type: 'success' | 'info' | 'warning' | 'error'
}

interface TimelineProps {
  events: Event[]
}

export default function Timeline({ events }: TimelineProps) {
  const typeConfig = {
    success: 'text-success-green',
    info: 'text-taiyi-blue',
    warning: 'text-warning-yellow',
    error: 'text-error-red',
  }

  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <div key={index} className="flex gap-3">
          <div className="flex flex-col items-center">
            <div className={`w-3 h-3 rounded-full ${typeConfig[event.type]} mt-1`} />
            {index < events.length - 1 && (
              <div className="w-px h-full bg-border-color my-2" />
            )}
          </div>
          <div className="flex-1 pb-4">
            <div className="flex items-center gap-2">
              <Clock size={14} className="text-gray-400" />
              <span className="text-sm text-gray-400">{event.time}</span>
            </div>
            <p className={`text-sm mt-1 ${typeConfig[event.type]}`}>{event.event}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
