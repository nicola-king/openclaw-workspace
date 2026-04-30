# 🦀 Claw Code API 密钥配置指南

> **配置时间**: 2026-04-16 22:50  
> **状态**: ⏳ 需要配置 API 密钥

---

## ⚠️ 当前状态

```bash
$ claw prompt "say hello"
error: missing Anthropic credentials; export ANTHROPIC_AUTH_TOKEN or ANTHROPIC_API_KEY
```

**需要配置**: Anthropic API 密钥

---

## 🔑 获取 API 密钥

### 方式 1: Anthropic API (推荐)

1. 访问 https://console.anthropic.com/
2. 登录/注册账号
3. 进入 API Keys 页面
4. 创建新的 API 密钥
5. 复制密钥 (格式：`sk-ant-...`)

---

### 方式 2: OpenAI API (备用)

1. 访问 https://platform.openai.com/api-keys
2. 登录/注册账号
3. 创建新的 API 密钥
4. 复制密钥 (格式：`sk-...`)

---

### 方式 3: Google Gemini API (备用)

1. 访问 https://makersuite.google.com/app/apikey
2. 登录/注册账号
3. 创建新的 API 密钥
4. 复制密钥

---

## ⚙️ 配置方式

### 方式 1: 环境变量 (推荐)

编辑 `~/.bashrc`:

```bash
# 添加到 ~/.bashrc 末尾
cat >> ~/.bashrc << 'EOF'

# ===== Claw Code API 密钥配置 =====
# Anthropic API (Claude)
export ANTHROPIC_API_KEY="sk-ant-你的密钥"

# 或者使用 OpenAI API
# export OPENAI_API_KEY="sk-你的密钥"

# 或者使用 Google Gemini API
# export GEMINI_API_KEY="你的密钥"
EOF

# 刷新配置
source ~/.bashrc
```

---

### 方式 2: 临时配置

```bash
# 单次使用
export ANTHROPIC_API_KEY="sk-ant-你的密钥"
claw prompt "say hello"
```

---

### 方式 3: 配置文件

创建 `~/.claw/config.json`:

```bash
mkdir -p ~/.claw
cat > ~/.claw/config.json << 'EOF'
{
  "api_key": "sk-ant-你的密钥",
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096
}
EOF
```

---

## ✅ 验证配置

```bash
# 检查环境变量
echo $ANTHROPIC_API_KEY

# 诊断配置
claw doctor

# 测试使用
claw prompt "say hello"
```

---

## 📋 预期输出

### 配置前

```bash
$ claw prompt "say hello"
error: missing Anthropic credentials; export ANTHROPIC_AUTH_TOKEN or ANTHROPIC_API_KEY
```

---

### 配置后

```bash
$ claw prompt "say hello"
🦀 使用 Claw Code 执行任务...
==================================
Hello! How can I help you today?
```

---

## 🔐 安全提示

### 密钥安全

```
✅ 不要将密钥提交到 Git
✅ 不要将密钥分享给他人
✅ 定期轮换密钥
✅ 使用环境变量而非硬编码
```

---

### Git 忽略

确保 `~/.bashrc` 和 `~/.claw/config.json` 不被提交:

```bash
# 添加到 .gitignore
echo "~/.bashrc" >> .gitignore
echo "~/.claw/" >> .gitignore
```

---

## 🎯 支持的平台

| 平台 | 环境变量 | 密钥格式 |
|------|----------|----------|
| **Anthropic** | `ANTHROPIC_API_KEY` | `sk-ant-...` |
| **OpenAI** | `OPENAI_API_KEY` | `sk-...` |
| **Google** | `GEMINI_API_KEY` | `...` |
| **Ollama** | `OLLAMA_HOST` | `http://localhost:11434` |

---

## 🚀 完整配置示例

```bash
# 1. 获取 API 密钥
# 访问 https://console.anthropic.com/

# 2. 添加到 ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# ===== Claw Code API 密钥配置 =====
export ANTHROPIC_API_KEY="sk-ant-你的密钥"

# 可选：配置默认模型
export CLAW_MODEL="claude-sonnet-4-20250514"

# 可选：配置最大 token 数
export CLAW_MAX_TOKENS="4096"
EOF

# 3. 刷新配置
source ~/.bashrc

# 4. 验证配置
echo $ANTHROPIC_API_KEY  # 应该显示密钥 (部分)

# 5. 诊断配置
claw doctor

# 6. 测试使用
claw prompt "say hello"
```

---

## 📊 诊断输出

### 配置前

```bash
$ claw doctor
Doctor
  Summary
    OK               3
    Warnings         3  ← API 密钥警告
    Failures         0

  Auth
    Status           fail  ← 认证失败
    Summary          no supported auth env vars were found
```

---

### 配置后

```bash
$ claw doctor
Doctor
  Summary
    OK               5
    Warnings         1  ← 仅沙盒警告
    Failures         0

  Auth
    Status           ok  ← 认证成功
    Summary          API key configured
```

---

## 🎊 下一步

配置完成后:

```
1. ✅ 验证配置 (claw doctor)
2. ✅ 测试使用 (claw prompt "say hello")
3. ✅ 集成到 OpenClaw (code-dev-tool.sh)
4. ✅ 开始日常使用
```

---

*太一 AGI · Claw Code API 密钥配置指南 v1.0 · 2026-04-16 22:50*

**🦀 请配置 API 密钥后即可使用 Claw Code！**
