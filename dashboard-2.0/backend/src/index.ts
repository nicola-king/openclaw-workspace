import express from 'express'
import cors from 'cors'
import { WebSocketServer } from 'ws'
import { createServer } from 'http'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 8000

// 中间件
app.use(cors())
app.use(express.json())

// 健康检查
app.get('/healthz', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// API 路由
app.get('/api/v1/system/health', (req, res) => {
  res.json({
    status: 'healthy',
    gateway: 'running',
    openclaw: '2026.4.14',
    agents: 9,
    skills: 471,
  })
})

app.get('/api/v1/system/stats', (req, res) => {
  res.json({
    agents: 9,
    skills: 471,
    tasksToday: 342,
    health: 98,
    evolutionLevel: 3,
    evolutionProgress: 92,
  })
})

app.get('/api/v1/agents', (req, res) => {
  res.json([
    { id: 'taiyi', name: '太一', status: 'running', tasks: 12, health: 98 },
    { id: 'zhiji', name: '知几', status: 'running', tasks: 8, health: 95 },
    { id: 'shanmu', name: '山木', status: 'running', tasks: 5, health: 97 },
    { id: 'suwen', name: '素问', status: 'running', tasks: 3, health: 99 },
    { id: 'wangliang', name: '罔两', status: 'idle', tasks: 0, health: 100 },
    { id: 'paoding', name: '庖丁', status: 'running', tasks: 7, health: 96 },
  ])
})

// 创建 HTTP 服务器
const server = createServer(app)

// WebSocket 服务器
const wss = new WebSocketServer({ server, path: '/ws' })

wss.on('connection', (ws) => {
  console.log('Client connected')

  ws.on('message', (message) => {
    console.log('Received:', message.toString())
    // 广播消息给所有客户端
    wss.clients.forEach((client) => {
      if (client !== ws && client.readyState === client.OPEN) {
        client.send(message)
      }
    })
  })

  ws.on('close', () => {
    console.log('Client disconnected')
  })
})

// 启动服务器
server.listen(PORT, () => {
  console.log(`🚀 Dashboard 2.0 Backend running on port ${PORT}`)
  console.log(`📊 Health: http://localhost:${PORT}/healthz`)
  console.log(`🔌 WebSocket: ws://localhost:${PORT}/ws`)
})
