# 岖丁 · 启动清单

## 每次启动时执行
1. 读取 shared/WORLD.md
2. 读取 agents/paoding/memory/MEMORY.md
3. 检查 blackboard/tasks.md 中的财务任务
4. 检查 blackboard/alerts.md 中的交易告警

## 风控检查
- 确认当前无异常交易指令
- 确认 Polymarket 账户状态（待接入后激活）

## 记忆规则
- 每笔交易记录写入日期日志
- 重要财务规则写入 MEMORY.md
