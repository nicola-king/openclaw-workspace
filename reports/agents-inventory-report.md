# 太一 AGI · Agents 完整清单与 Dashboard 修复

> **统计时间**: 2026-04-03 13:10 | **太一 AGI v5.0**

---

## 📊 Agents 统计总览

| 类别 | 数量 | 状态 |
|------|------|------|
| **实际 Agents** | 8 | ✅ 完整 |
| **Dashboard 显示** | 6 | ⚠️ 缺失 2 个 |
| **openclaw.json 配置** | 2 | ❌ 需更新 |
| **~/.openclaw/agents/** | 6 | ⚠️ 缺失 2 个 |

---

## 🤖 完整 Agents 清单（8 个）

| 编号 | 英文名 | 中文名 | Emoji | 职责 | Skill 目录 | 状态 |
|------|--------|--------|-------|------|-----------|------|
| A01 | **Taiyi** | 太一 | 🧠 | AGI 执行总管 | `skills/taiyi/` | ✅ |
| A02 | **Zhiji** | 知几 | 📈 | 量化交易 | `skills/zhiji/` | ✅ |
| A03 | **Shanmu** | 山木 | 🎨 | 内容创意 | `skills/shanmu/` | ✅ |
| A04 | **Suwen** | 素问 | 💻 | 技术开发 | `skills/suwen/` | ✅ |
| A05 | **Wangliang** | 罔两 | 📊 | 数据采集 | `skills/wangliang/` | ✅ |
| A06 | **Paoding** | 庖丁 | 💰 | 预算成本 | `skills/paoding/` | ✅ |
| A07 | **Yi** | 羿 | 🏹 | 监控追踪 | `skills/yi/` | ⚠️ |
| A08 | **Shoucangli** | 守藏吏 | 📚 | 资源调度 | `skills/shoucangli/` | ⚠️ |

---

## ⚠️ 问题分析

### Dashboard 缺失的 Agents

| Agent | 原因 | 修复方案 |
|-------|------|---------|
| **Yi (羿)** | `~/.openclaw/agents/yi/` 不存在 | 创建目录 + 配置 |
| **Shoucangli (守藏吏)** | `~/.openclaw/agents/shoucangli/` 不存在 | 创建目录 + 配置 |

### openclaw.json 配置缺失

当前配置只有 2 个 Agents，需要更新为 8 个。

---

## 🔧 修复方案

### 方案 1: 自动同步脚本

创建脚本自动扫描 `skills/` 目录并同步到 `~/.openclaw/agents/`：

```bash
#!/bin/bash
# scripts/sync-agents.sh

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"
AGENTS_DIR="$HOME/.openclaw/agents"

# 8 个标准 Agents
AGENTS="taiyi zhiji shanmu suwen wangliang paoding yi shoucangli"

for agent in $AGENTS; do
    if [ -d "$SKILLS_DIR/$agent" ]; then
        if [ ! -d "$AGENTS_DIR/$agent" ]; then
            echo "创建 Agent: $agent"
            mkdir -p "$AGENTS_DIR/$agent/sessions"
            
            # 复制 SKILL.md
            cp "$SKILLS_DIR/$agent/SKILL.md" "$AGENTS_DIR/$agent/" 2>/dev/null || true
            
            # 创建基础配置
            cat > "$AGENTS_DIR/$agent/config.json" <<EOF
{
  "name": "$agent",
  "emoji": "🤖",
  "model": "qwen3.5-plus",
  "created": "$(date -Iseconds)"
}
EOF
        fi
    fi
done

echo "✅ Agents 同步完成"
ls -la "$AGENTS_DIR"
```

### 方案 2: 更新 openclaw.json

```bash
# 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 使用脚本更新
python3 << 'EOF'
import json

with open('/home/nicola/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)

# 定义 8 个 Agents
agents = {
    "taiyi": {"name": "太一", "emoji": "🧠", "model": "qwen3.5-plus"},
    "zhiji": {"name": "知几", "emoji": "📈", "model": "qwen3.5-plus"},
    "shanmu": {"name": "山木", "emoji": "🎨", "model": "qwen3.5-plus"},
    "suwen": {"name": "素问", "emoji": "💻", "model": "qwen3.5-plus"},
    "wangliang": {"name": "罔两", "emoji": "📊", "model": "qwen3.5-plus"},
    "paoding": {"name": "庖丁", "emoji": "💰", "model": "qwen3.5-plus"},
    "yi": {"name": "羿", "emoji": "🏹", "model": "qwen3.5-plus"},
    "shoucangli": {"name": "守藏吏", "emoji": "📚", "model": "qwen3.5-plus"}
}

config['agents'] = agents

with open('/home/nicola/.openclaw/openclaw.json', 'w') as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

print("✅ openclaw.json 已更新")
EOF
```

### 方案 3: Dashboard 数据源修复

修改 Dashboard 读取 `skills/` 目录而非仅 `~/.openclaw/agents/`：

```typescript
// /tmp/OpenClaw-bot-review/lib/openclaw-agents.ts
export function scanAgentsFromSkills(): AgentInfo[] {
  const skillsDir = '/home/nicola/.openclaw/workspace/skills';
  const agentIds = ['taiyi', 'zhiji', 'shanmu', 'suwen', 'wangliang', 'paoding', 'yi', 'shoucangli'];
  
  return agentIds.map(id => {
    const skillPath = path.join(skillsDir, id, 'SKILL.md');
    const content = fs.readFileSync(skillPath, 'utf-8');
    // 解析 frontmatter 获取 name, emoji, description
    return { id, name, emoji, ... };
  });
}
```

---

## 📋 执行步骤

### Step 1: 创建缺失的 Agent 目录

```bash
mkdir -p ~/.openclaw/agents/{yi,shoucangli}/sessions
```

### Step 2: 创建配置文件

**~/.openclaw/agents/yi/config.json**:
```json
{
  "name": "羿",
  "emoji": "🏹",
  "model": "qwen3.5-plus",
  "created": "2026-04-03T13:10:00+08:00"
}
```

**~/.openclaw/agents/shoucangli/config.json**:
```json
{
  "name": "守藏吏",
  "emoji": "📚",
  "model": "qwen3.5-plus",
  "created": "2026-04-03T13:10:00+08:00"
}
```

### Step 3: 更新 openclaw.json

```bash
# 运行上面的 Python 脚本
```

### Step 4: 重启 Dashboard

```bash
pkill -f "npm run dev"
cd /tmp/OpenClaw-bot-review
npm run dev &
```

### Step 5: 验证

访问 http://localhost:3000 查看是否显示 8 个 Agents。

---

## 🎯 建议

### 短期修复（立即执行）
1. 创建缺失的 2 个 Agent 目录
2. 更新 openclaw.json
3. 重启 Dashboard

### 长期优化（建议执行）
1. 创建 `scripts/sync-agents.sh` 自动同步脚本
2. 修改 Dashboard 数据源优先读取 `skills/` 目录
3. 添加 Agent 配置验证工具

---

## 📊 修复后预期效果

| 位置 | 修复前 | 修复后 |
|------|--------|--------|
| Dashboard 显示 | 6 Agents | ✅ 8 Agents |
| openclaw.json | 2 Agents | ✅ 8 Agents |
| ~/.openclaw/agents/ | 6 目录 | ✅ 8 目录 |
| skills/ | 8 Skills | ✅ 8 Skills (不变) |

---

## 🔗 相关文件

- **Dashboard 源码**: `/tmp/OpenClaw-bot-review/lib/openclaw-skills.ts`
- **OpenClaw 配置**: `~/.openclaw/openclaw.json`
- **Agents 目录**: `~/.openclaw/agents/`
- **Skills 目录**: `/home/nicola/.openclaw/workspace/skills/`

---

*报告生成：2026-04-03 13:10 | 太一 AGI v5.0*
