# AI API 配置

> 状态：需要配置
> 时间：2026-03-28 22:03

---

## 🔑 需要配置的 API Key

### 1. Gemini API Key

**获取方式**:
1. 访问 https://aistudio.google.com/app/apikey
2. 创建 API Key
3. 复制到环境变量

**配置命令**:
```bash
export GEMINI_API_KEY="你的 Gemini API Key"
```

**添加到 ~/.bashrc**:
```bash
echo 'export GEMINI_API_KEY="你的 Gemini API Key"' >> ~/.bashrc
source ~/.bashrc
```

---

### 2. 百炼 API Key (DashScope)

**获取方式**:
1. 访问 https://dashscope.console.aliyun.com/apiKey
2. 创建 API Key
3. 复制到环境变量

**配置命令**:
```bash
export DASHSCOPE_API_KEY="你的百炼 API Key"
```

**添加到 ~/.bashrc**:
```bash
echo 'export DASHSCOPE_API_KEY="你的百炼 API Key"' >> ~/.bashrc
source ~/.bashrc
```

---

## ✅ 验证配置

```bash
# 验证环境变量
env | grep -E "GEMINI|DASHSCOPE"

# 测试 Gemini
python3 -c "import google.generativeai as genai; print('Gemini OK')"

# 测试百炼
python3 -c "import dashscope; print('DashScope OK')"
```

---

## 📁 配置文件位置

**环境变量**: `~/.bashrc`

**太一配置**: `~/.openclaw/.env.ai` (待创建)

---

*创建时间：2026-03-28 22:03*
*状态：需要配置 API Key*
