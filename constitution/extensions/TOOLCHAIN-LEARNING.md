# 太一 AI 工具链 v2.0 - 金尘马案例学习

> 基于@jinchenma_ai 工具栈 | 版本：v2.0 | 创建：2026-03-27

---

## 📊 工具链对比

| 用途 | 金尘马 | 太一当前 | 太一优化 |
|------|--------|---------|---------|
| **编程** | Codex GPT-5.4 | Qwen3-Coder-Plus | ✅ 保持 |
| **写作** | Claude Opus 4.6 | 山木 (Qwen3.5) | ⏳ 可增强 |
| **X 运营** | Grok | 山木 + 自动发布 | ✅ 保持 |
| **笔记** | OpenClaw+ 飞书 +Obsidian | OpenClaw+Obsidian | ✅ 一致 |
| **生图** | lovart (80 积分/天) | Gemini 2.0 | 🟡 可补充 |
| **语音** | 闪电说 + 豆包 | 无 | 🔴 待添加 |
| **问答** | 豆包 | Qwen3.5-Plus | ✅ 保持 |

---

## 🛠️ 太一工具链优化方案

### 优化 1: 写作能力增强

```
当前：山木 (Qwen3.5-Plus)
评估：✅ 足够用，成本低

可选升级:
- Claude Opus 4.6 (写作最强)
- 成本：$15/百万 tokens
- 场景：公众号长文/Gumroad 产品描述

建议：
保持 Qwen3.5-Plus 为主力
关键内容用 Claude 增强
```

### 优化 2: 生图工具补充

```
当前：Gemini 2.0 (免费额度)
评估：✅ 够用

补充方案:
- lovart: 每天 80 积分免费
- 用途：公众号配图/产品封面
- 工作流：山木生成提示词 → lovart 生图

配置:
export LOVART_API_KEY=xxx
export LOVART_DAILY_CREDITS=80
```

### 优化 3: 语音输入集成

```
当前：无
评估：🔴 待添加

推荐方案:
- 闪电说 + 豆包
- 成本：免费 20h + ¥1/h
- 用途：快速记录灵感/语音笔记

集成方式:
1. 安装闪电说 App
2. 配置豆包 API
3. 语音→文字→Obsidian 自动保存
```

### 优化 4: OpenClaw+Obsidian 工作流增强

```
当前工作流:
太一 → OpenClaw → 记忆系统 → Obsidian

金尘马工作流:
OpenClaw → skills → Obsidian 仓库

优化方案:
1. 增强 skills 写入 Obsidian 功能
2. 自动分类归档
3. 双向同步 (Obsidian 编辑→太一读取)

配置:
export OBSIDIAN_VAULT_PATH=~/.openclaw/workspace/obsidian
export AUTO_SYNC=true
```

---

## 📋 太一完整工具链 v2.0

### 核心层 (太一 AGI)

```
┌─────────────────────────────────────┐
│         太一 (总管/决策)             │
│  模型：Qwen3.5-Plus                 │
│  职责：任务分析/Bot 调度/结果整合     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│        专业 Bot 团队 (6 个)           │
├─────────────────────────────────────┤
│ 知几：量化交易 (Qwen3-Coder)        │
│ 山木：内容创意 (Qwen3.5+Gemini)     │
│ 素问：技术开发 (Qwen3-Coder)        │
│ 罔两：数据分析 (Qwen3.5)            │
│ 庖丁：预算成本 (Qwen3.5)            │
└─────────────────────────────────────┘
```

### 工具层 (集成服务)

```
【编程开发】
- Qwen3-Coder-Plus ✅
- GitHub Copilot (可选)

【内容写作】
- Qwen3.5-Plus ✅ (主力)
- Claude Opus 4.6 (关键内容增强)

【图像生成】
- Gemini 2.0 ✅ (主力)
- lovart (补充，80 积分/天免费)

【语音输入】
- 闪电说 + 豆包 🔴 (待配置)

【笔记管理】
- Obsidian ✅
- OpenClaw 记忆系统 ✅
- 飞书 (可选，团队协作)

【社交平台】
- Twitter/X API ✅
- Telegram Bot ✅
- 微信公众号 ✅
- 小红书 (待配置)
```

### 数据层 (存储同步)

```
【本地存储】
- /home/nicola/.openclaw/workspace/
  ├── memory/ (核心记忆)
  ├── constitution/ (宪法)
  ├── skills/ (技能)
  └── obsidian/ (笔记仓库) ✅

【云端同步】
- Syncthing ✅ (工作站备份)
- GitHub ✅ (代码版本)
- 飞书 (可选，文档协作)
```

---

## 🚀 立即执行优化

### 任务 1: lovart 生图集成

```bash
# 1. 注册 lovart 账号
访问：https://lovart.ai

# 2. 获取 API Key
设置 → API → 创建 Key

# 3. 配置环境变量
cat >> ~/.openclaw/.env << EOF
LOVART_API_KEY=你的 Key
LOVART_DAILY_CREDITS=80
EOF

# 4. 测试生图
python3 /home/nicola/.openclaw/workspace/scripts/test-lovart.py
```

### 任务 2: Obsidian 工作流增强

```bash
# 1. 创建 Obsidian 自动同步脚本
cat > /home/nicola/.openclaw/scripts/sync-obsidian.sh << 'EOF'
#!/bin/bash
# Obsidian 自动同步

OBSIDIAN_VAULT="$HOME/.openclaw/workspace/obsidian"
TAIYI_MEMORY="$HOME/.openclaw/workspace/memory"

# 同步记忆文件
cp -r "$TAIYI_MEMORY"/*.md "$OBSIDIAN_VAULT/memory/"

# 同步技能文档
cp -r "$HOME/.openclaw/workspace/skills"/*.md "$OBSIDIAN_VAULT/skills/"

echo "✅ Obsidian 同步完成"
EOF

chmod +x /home/nicola/.openclaw/scripts/sync-obsidian.sh

# 2. 配置定时任务 (每小时同步)
crontab -l | echo "0 * * * * /home/nicola/.openclaw/scripts/sync-obsidian.sh" | crontab -
```

### 任务 3: 语音输入配置 (可选)

```bash
# 1. 下载闪电说 App
# 访问：https://shuodian.ai (示例)

# 2. 配置豆包 API
export DOUBAO_API_KEY=你的 Key

# 3. 测试语音输入
# 打开闪电说 App → 说话 → 自动转文字 → 发送到 Obsidian
```

---

## 💡 核心洞察

```
金尘马工具栈的启示:

1. 工具在精不在多
   ✅ 太一已有核心工具链
   ✅ 按需补充，不盲目追求

2. 免费额度最大化
   ✅ lovart 80 积分/天
   ✅ Gemini 免费额度
   ✅ 豆包新用户 20h

3. 工作流自动化
   ✅ OpenClaw+Obsidian 自动同步
   ✅ 语音→文字→笔记自动保存

4. 效率优先
   ✅ 简单问题用豆包 (快)
   ✅ 复杂问题用 Claude (强)
   ✅ 代码用 Codex/Qwen(专)

太一的优势:
✅ 已有多 Bot 协作架构
✅ 已有 OpenClaw+Obsidian
✅ 已有自动化工作流
✅ 成本更低 (免费优先)
```

---

*版本：v2.0 | 创建时间：2026-03-27 | 太一 AGI*

*「工具为用，效率为王」*
