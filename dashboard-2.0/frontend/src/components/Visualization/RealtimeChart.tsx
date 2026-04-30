import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { time: '00:00', tasks: 12 },
  { time: '04:00', tasks: 8 },
  { time: '08:00', tasks: 25 },
  { time: '12:00', tasks: 38 },
  { time: '16:00', tasks: 45 },
  { time: '20:00', tasks: 32 },
  { time: '23:00', tasks: 28 },
]

export default function RealtimeChart() {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#0F3460" />
          <XAxis dataKey="time" stroke="#B0B0B0" />
          <YAxis stroke="#B0B0B0" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#16213E',
              border: '1px solid #0F3460',
              borderRadius: '8px'
            }}
          />
          <Line
            type="monotone"
            dataKey="tasks"
            stroke="#1E88E5"
            strokeWidth={2}
            dot={{ fill: '#1E88E5' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
