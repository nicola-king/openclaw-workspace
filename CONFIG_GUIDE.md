# OpenClaw 分布式配置指南

## 在 openclaw.json 中为各 Agent 设置独立 workspace

在 agents.list 数组中为每个 agent 添加 workspace 字段：

```json
{
  "agents": {
    "defaults": {
      "workspace": "/home/nicola/.openclaw/workspace",
      "heartbeat": { "every": "2h" },
      "compaction": { "mode": "safeguard", "reserveTokensFloor": 32000 },
      "model": {
        "primary": "bailian/qwen3.5-plus",
        "fallbacks": [
          "bailian/qwen3-max-2026-01-23",
          "bailian/qwen3-coder-plus",
          "google/gemini-2.5-pro"
        ]
      }
    },
    "list": [
      {
        "id": "taiyi",
        "workspace": "/home/nicola/.openclaw/workspace/agents/taiyi",
        "identity": { "name": "太一", "emoji": "☘️" }
      },
      {
        "id": "zhiji",
        "workspace": "/home/nicola/.openclaw/workspace/agents/zhiji",
        "identity": { "name": "知几", "emoji": "📊" },
        "model": { "primary": "bailian/qwen3-max-2026-01-23" }
      },
      {
        "id": "shanmu",
        "workspace": "/home/nicola/.openclaw/workspace/agents/shanmu",
        "identity": { "name": "山木", "emoji": "🎨" }
      },
      {
        "id": "suwen",
        "workspace": "/home/nicola/.openclaw/workspace/agents/suwen",
        "identity": { "name": "素问", "emoji": "💻" },
        "model": { "primary": "bailian/qwen3-coder-plus" }
      },
      {
        "id": "wangliang",
        "workspace": "/home/nicola/.openclaw/workspace/agents/wangliang",
        "identity": { "name": "罔两", "emoji": "📈" }
      },
      {
        "id": "paoding",
        "workspace": "/home/nicola/.openclaw/workspace-paoding",
        "identity": { "name": "岖丁", "emoji": "💰" }
      }
    ]
  }
}
```

## 新增 Agent 流程
1. 在 workspace/agents/ 下创建新目录
2. 添加 SOUL.md、BOOT.md、MEMORY.md
3. 在 openclaw.json agents.list 中添加条目
4. 运行 openclaw gateway restart
5. 运行 openclaw doctor 验证

## 删除 Agent 流程
1. 在 openclaw.json agents.list 中移除条目
2. 运行 openclaw gateway restart
3. 保留 workspace/agents/{id}/ 目录（归档，不删除）
4. 如需彻底清理：mv workspace/agents/{id} workspace/agents/{id}.archived
