# 太一 · 启动清单

## 每次启动时执行
1. 读取 shared/WORLD.md 了解系统状态
2. 检查 blackboard/alerts.md，处理紧急告警
3. 读取 blackboard/tasks.md，了解待处理任务
4. 读取今日日志 agents/taiyi/memory/$(date +%Y-%m-%d).md（如存在）
5. 向主人发送简短问候（仅主会话，不在群组）

## Heartbeat 清单（每2小时）
- 扫描 blackboard/alerts.md
- 检查各 Agent 最近日志是否异常
- 如有待处理任务超过4小时未完成，提醒主人
- 回复 HEARTBEAT_OK 如无异常

## 记忆规则
- 每次会话结束前，将重要信息写入 agents/taiyi/memory/$(date +%Y-%m-%d).md
- 重大决策或用户偏好写入 agents/taiyi/memory/MEMORY.md
- 跨 Agent 任务结果记录到 blackboard/events.md
