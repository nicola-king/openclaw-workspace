# Agent 通信协议
## 黑板文件
- blackboard/tasks.md — 任务队列
- blackboard/events.md — 事件日志
- blackboard/alerts.md — 紧急告警
## 记忆隔离
- 每个 Agent 只操作 agents/{id}/memory/
- 共享结论写入 blackboard/
## 模型路由
- 默认：qwen3.5-plus
- 复杂推理/代码：qwen3-coder-plus
- 长上下文：qwen3-max
- 备用：gemini-2.5-pro
