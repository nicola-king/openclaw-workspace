# Agent 通信协议

## 黑板系统 (Blackboard Pattern)
所有跨 Agent 通信通过以下文件进行：

### blackboard/tasks.md — 任务队列
格式：
```
## [TASK-001] 任务标题
- 发起者：taiyi
- 执行者：zhiji
- 状态：pending | running | done | failed
- 创建：2026-03-24 09:00
- 描述：具体任务内容
```

### blackboard/events.md — 事件日志
格式：
```
[2026-03-24 09:00] taiyi → zhiji: 请求市场分析
[2026-03-24 09:05] zhiji → blackboard: 分析完成，见 agents/zhiji/memory/2026-03-24.md
```

### blackboard/alerts.md — 紧急告警
格式：
```
## [ALERT] 标题
- 级别：info | warn | critical
- 来源：agent名称
- 时间：时间戳
- 内容：告警详情
```

## 记忆隔离原则
- 每个 Agent 只操作 agents/{id}/memory/ 下的文件
- 禁止直接读写其他 Agent 的 memory 目录
- 需要共享的结论写入 blackboard/，由目标 Agent 主动读取

## 模型路由原则
- 简单查询 / heartbeat：qwen3.5-plus（默认）
- 复杂推理 / 代码：qwen3-coder-plus
- 长上下文 / 分析：qwen3-max
- 最终备用：gemini-2.5-pro
