# 本地 AI 模型调用 Skill

> 版本：v1.0 | 创建：2026-03-28 21:40
> 模型：Qwen3.5-9B Opus V2 蒸馏版
> 部署：Ollama (工控机本地)

---

## 🎯 功能概述

| 功能 | 描述 | 状态 |
|------|------|------|
| **本地推理** | Qwen3.5-9B Opus V2 | 🟡 待部署 |
| **API 调用** | Ollama API (端口 11434) | 🟡 待配置 |
| **太一集成** | 智能任务调度 | 🟡 待开发 |
| **Claude Code 对接** | 复杂推理任务 | 🟡 待测试 |

---

## 📊 模型信息

**Qwen3.5-9B Opus V2 蒸馏版**:

| 指标 | 数值 |
|------|------|
| **参数** | 9B |
| **训练数据** | 1.4 万条 Opus 推理样本 |
| **模型大小** | ~18GB (GGUF Q4_K_M) |
| **内存需求** | 最低 16GB |
| **推理速度** | 比原模型快 25-30% |
| **平台** | Macbook M5 / Linux / Windows |

---

## 🔧 部署步骤

### Step 1: 检查工控机配置

```bash
# 检查内存
free -h

# 检查存储
df -h

# 检查 GPU (可选)
lspci | grep -i vga
```

**最低配置**:
- 内存：16GB+
- 存储：20GB+ 空闲
- 系统：Linux (工控机已满足)

---

### Step 2: 安装 Ollama

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 验证安装
ollama --version

# 启动服务
ollama serve
```

---

### Step 3: 下载模型

```bash
# 下载 Qwen3.5-9B Opus V2
ollama pull qwen2.5:7b-instruct-q4_K_M

# 查看已下载模型
ollama list
```

---

### Step 4: 测试运行

```bash
# 交互式运行
ollama run qwen2.5:7b-instruct-q4_K_M "你好"

# API 测试
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b-instruct-q4_K_M",
  "prompt": "你好"
}'
```

---

## 🤖 太一集成

### 智能任务调度

```python
# skills/taiyi/local_ai_caller.py

def call_local_ai(task, complexity):
    """
    智能调用本地 AI
    
    参数:
    - task: 任务描述
    - complexity: 复杂度 (simple/medium/complex)
    
    返回:
    - AI 响应
    """
    
    if complexity == 'simple':
        # 简单任务：本地小模型
        return ollama_generate(
            model='qwen2.5:7b-instruct-q4_K_M',
            prompt=task
        )
    
    elif complexity == 'medium':
        # 中等任务：本地模型 + 思考链
        return ollama_generate(
            model='qwen2.5:7b-instruct-q4_K_M',
            prompt=f"Let's think step by step: {task}",
            options={'num_predict': 2048}
        )
    
    else:  # complex
        # 复杂任务：调用云端大模型
        return call_cloud_ai(task)  # Claude/GPT
```

---

### 应用场景

| 场景 | 模型 | 说明 |
|------|------|------|
| **代码生成** | Qwen3.5-9B | 简单函数/脚本 |
| **文档写作** | Qwen3.5-9B | 技术文档/邮件 |
| **数据分析** | Qwen3.5-9B | 简单分析/总结 |
| **复杂推理** | Claude/GPT | 战略决策/多步推理 |
| **创意写作** | Qwen3.5-9B | 小红书文案/标题 |

---

## 📋 定时任务

```bash
# 本地 AI 健康检查 (每小时)
0 * * * * ollama list > /tmp/ollama-status.log

# 模型更新检查 (每周一)
0 9 * * 1 ollama pull qwen2.5:7b-instruct-q4_K_M
```

---

## 🔒 安全配置

### API 访问控制

```bash
# 仅允许本地访问
export OLLAMA_HOST=127.0.0.1:11434

# 如需远程访问 (不推荐)
export OLLAMA_HOST=0.0.0.0:11434
# 添加防火墙规则
```

---

## 📊 性能预期

| 任务类型 | 使用模型 | 响应时间 | 质量 | 成本 |
|---------|---------|---------|------|------|
| **简单问答** | qwen2.5:7b (本地) | <5 秒 | ⭐⭐⭐⭐ | ¥0 |
| **代码生成** | 百炼 Coding Plan | 10-30 秒 | ⭐⭐⭐⭐⭐ | ¥0/低价 |
| **技术文档** | 百炼 Coding Plan | 15-45 秒 | ⭐⭐⭐⭐⭐ | ¥0/低价 |
| **小红书文案** | Gemini (免费) | 15-45 秒 | ⭐⭐⭐⭐⭐ | ¥0 |
| **数据分析** | Gemini (免费) | 20-60 秒 | ⭐⭐⭐⭐⭐ | ¥0 |
| **翻译/总结** | Gemini (免费) | 10-30 秒 | ⭐⭐⭐⭐⭐ | ¥0 |
| **复杂推理** | Claude/GPT (付费) | 30-90 秒 | ⭐⭐⭐⭐⭐ | 付费 |

---

## 🚀 快速启动

```bash
# 1. 检查配置
free -h && df -h

# 2. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. 下载模型
ollama pull qwen2.5:7b-instruct-q4_K_M

# 4. 测试运行
ollama run qwen2.5:7b-instruct-q4_K_M "太一是什么？"

# 5. 集成太一
cd ~/.openclaw/workspace/skills/taiyi
python3 local_ai_caller.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 21:40*
*模型：Qwen3.5-9B Opus V2 蒸馏版*
*太一 AGI · 本地 AI 集成*
