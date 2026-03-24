# 分布式配置指南

## 在 openclaw.json 中设置各 Agent 独立 workspace

编辑 ~/.openclaw/openclaw.json，在 agents.list 中添加 workspace 字段：
```json
"list": [
  { "id": "taiyi",    "workspace": "/home/nicola/.openclaw/workspace/agents/taiyi",    "identity": { "name": "太一", "emoji": "☘️" } },
  { "id": "zhiji",    "workspace": "/home/nicola/.openclaw/workspace/agents/zhiji",    "identity": { "name": "知几", "emoji": "📊" }, "model": { "primary": "bailian/qwen3-max-2026-01-23" } },
  { "id": "shanmu",   "workspace": "/home/nicola/.openclaw/workspace/agents/shanmu",   "identity": { "name": "山木", "emoji": "🎨" } },
  { "id": "suwen",    "workspace": "/home/nicola/.openclaw/workspace/agents/suwen",    "identity": { "name": "素问", "emoji": "💻" }, "model": { "primary": "bailian/qwen3-coder-plus" } },
  { "id": "wangliang","workspace": "/home/nicola/.openclaw/workspace/agents/wangliang","identity": { "name": "罔两", "emoji": "📈" } },
  { "id": "paoding",  "workspace": "/home/nicola/.openclaw/workspace-paoding",         "identity": { "name": "岖丁", "emoji": "💰" } }
]
```

## 新增 Agent
1. mkdir -p ~/.openclaw/workspace/agents/新名字/{memory,skills,docs}
2. 创建 SOUL.md / BOOT.md / MEMORY.md
3. 在 openclaw.json agents.list 添加条目
4. openclaw gateway restart

## 删除/停用 Agent
1. 从 openclaw.json agents.list 移除
2. openclaw gateway restart
3. 目录归档：mv agents/名字 agents/名字.archived
