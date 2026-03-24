# 知几 · 启动清单

## 每次启动时执行
1. 读取 shared/WORLD.md
2. 读取 agents/zhiji/memory/MEMORY.md
3. 检查 polymarket-data/ 目录最新数据
4. 检查 blackboard/tasks.md 中分配给我的任务

## Heartbeat 清单
- 运行知几-E 监控仪表板
- 扫描待执行市场机会
- 如发现置信度 >96% 的机会，写入 blackboard/alerts.md
- 回复 HEARTBEAT_OK 如无异常

## 记忆规则
- 每次分析结果写入 agents/zhiji/memory/$(date +%Y-%m-%d).md
- 重要市场规律写入 agents/zhiji/memory/MEMORY.md
- 交易机会写入 blackboard/alerts.md 通知太一
