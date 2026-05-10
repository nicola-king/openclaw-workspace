# dispatch-viz Skill

## 描述
调度拓扑可视化引擎 — 轻量方案。

每次太一执行 Agent 调度后，自动生成 Mermaid 拓扑图：
- 采集本次调度的 Agent 拓扑结构
- 生成 Mermaid flowchart 代码
- 支持写入飞书画板（lark-whiteboard）或本地文件

## 支持的域
- `travel`  — 旅游探路者调度拓扑
- `trade`   — 跨境贸易调度拓扑

## API

### generate_topology(domain, active_bots, task_description, metadata)
生成单次调度的 Mermaid 拓扑图。

### generate_landscape()
生成全系统 Agent 全景拓扑图。

## CLI 示例
```bash
# 旅游调度拓扑（激活山木+庖丁）
python3 core.py --domain travel --bots 山木 庖丁 --desc "三亚家族旅行10天"

# 跨境贸易拓扑（全部 Bot）
python3 core.py --domain trade --task topology

# 全系统全景图
python3 core.py --task landscape

# 输出到文件
python3 core.py --domain travel --bots 知几 山木 --desc "东京攻略" -o topo.mmd
```
