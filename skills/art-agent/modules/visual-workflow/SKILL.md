# visual-workflow Skill v2.0.0

## 描述
太一可视化工作流引擎 — 重量方案。

基于 React Flow 兼容的 JSON Schema，构建可交互的 Agent 调度面板。

## 功能
- 调度拓扑 JSON（React Flow 原生格式）
- 执行历史追蹤 → 时间线可视化
- 节点状态追踪（idle / running / success / error）
- 自动 DFS 布局引擎
- 兼容 dispatch-viz Mermaid 导出

## API

### build_dispatch_workflow(workflow_id, domain, task_description, active_bots, ...)
构建单次调度的 React Flow 兼容工作流 JSON。

### build_full_system_workflow()
构建全系统 Agent 全景拓扑。

### export_mermaid(workflow_id)
工作流 → Mermaid flowchart。

### export_json(workflow_id)
导出 React Flow 原生 JSON。

### add_timestamp(workflow_id, node_id, status, message)
更新节点状态（时间线部件）。

## CLI 示例
```bash
# 构建调度工作流 JSON
python3 core.py --task dispatch --domain travel --bots 知几 山木 --desc "东京攻略"

# 全系统拓扑
python3 core.py --task system -o /tmp/system.json

# 导出 Mermaid
python3 core.py --task mermaid --domain trade --bots 知几 罔两 --desc "竞品监控" -o /tmp/wf.mmd
```
