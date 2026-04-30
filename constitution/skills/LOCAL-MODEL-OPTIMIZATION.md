# 太一本地模型优化配置 v1.0

**创建时间**: 2026-04-18  
**执行**: 太一  
**硬件**: Intel N150 (4 核), 32GB RAM, 无独显

---

## 📊 已安装组件

| 组件 | 版本 | 状态 | 路径 |
|------|------|------|------|
| **Ollama** | v0.21.0 | ✅ 运行中 | `/usr/local/bin/ollama` |
| **llama.cpp** | v0.9.11 | ✅ 已编译 | `/workspace/llama.cpp/build/bin/` |
| **TurboQuant** | v0.2.0 | ⚠️ 已安装 (需 GPU) | 可选，GGUF 已内置量化 |

---

## 🤖 模型部署状态

### 已部署模型

| 模型 | 格式 | 大小 | 量化 | 状态 |
|------|------|------|------|------|
| **Gemma 2 9B** | GGUF (Ollama) | 5.8GB | Q4_K_M | 🔄 下载中 |

---

## ⚙️ 优化配置

### 1. Ollama 配置

**环境变量** (`/etc/systemd/system/ollama.service`):
```ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
```

**适用场景**:
- 简单问答
- 快速翻译
- 文本润色
- 日常对话

**调用示例**:
```bash
ollama run gemma2:9b-instruct-q4_K_M "你好，请介绍一下自己"
```

---

### 2. llama.cpp 配置

**Intel N150 优化参数**:
```bash
./llama-cli \
  -m /path/to/gemma-2-9b-it-Q4_K_M.gguf \
  -n 512 \
  --n_threads 4 \
  --n_ctx 4096 \
  --batch_size 512 \
  --ubatch_size 512 \
  --no-mmap \
  -p "你好"
```

**参数说明**:
| 参数 | 值 | 说明 |
|------|-----|------|
| `--n_threads` | 4 | CPU 核心数 |
| `--n_ctx` | 4096 | 上下文长度 (减少内存占用) |
| `--batch_size` | 512 | 批处理大小 |
| `--no-mmap` | - | 禁用内存映射 (避免 swap) |

**预期性能**:
- 推理速度：~3-5 tokens/s
- 内存占用：~10GB
- 延迟：~200-500ms/token

---

### 3. GGUF 内置量化 (推荐)

**GGUF 量化等级说明**:

| 量化 | 大小 | 精度 | 推荐度 |
|------|------|------|--------|
| **Q4_K_M** | ~5.5GB | <2% 损失 | ⭐⭐⭐⭐⭐ 最佳平衡 |
| **Q5_K_M** | ~6.5GB | <1% 损失 | ⭐⭐⭐⭐ 高质量 |
| **Q6_K** | ~7.5GB | <0.5% 损失 | ⭐⭐⭐ 极高质 |
| **Q8_0** | ~10GB | ~0% 损失 | ⭐⭐ 接近原版 |

**优势**:
- ✅ 无需额外依赖
- ✅ CPU 友好 (无需 GPU)
- ✅ 量化损失极小
- ✅ Ollama/llama.cpp 原生支持

**注意**: TurboQuant 已安装但需要 NVIDIA GPU，当前配置使用 GGUF 内置量化即可。

---

## 📈 性能基准 (预期)

### Intel N150 + 32GB RAM (GGUF Q4_K_M)

| 模型 | 量化 | 上下文 | 速度 | 内存 | 用途 |
|------|------|--------|------|------|------|
| Gemma 2 9B | Q4_K_M | 4K | 3-5 t/s | ~10GB | 日常对话/英语 |
| Gemma 2 9B | Q4_K_M | 8K | 2-4 t/s | ~14GB | 中等上下文 |
| Qwen2.5 7B | Q4_K_M | 4K | 4-6 t/s | ~8GB | 中文对话 |
| Qwen2.5 14B | Q4_K_M | 4K | 2-3 t/s | ~12GB | 复杂任务 |

**GGUF Q4_K_M 量化效率**:
- 压缩率：~3-4x (vs FP16)
- 精度损失：<2%
- 速度提升：2-3x (vs FP16)

---

## 🔧 模型路由策略

### 自动路由规则

| 任务类型 | 路由目标 | 理由 |
|---------|---------|------|
| **简单问答** | Ollama (Gemma 2 9B) | 低延迟，本地免费 |
| **中文对话** | qwen3.5-plus (云端) | 中文能力更强 |
| **代码生成** | qwen3-coder-plus | 专业代码模型 |
| **长文档** | gemini-2.5-pro | 1M 上下文窗口 |
| **复杂推理** | qwen3.5-plus | 70B+ 参数 |
| **数学计算** | qwen3.5-plus | 数学能力强 |

---

## 📝 使用示例

### 1. 日常对话 (Ollama)
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma2:9b-instruct-q4_K_M",
  "prompt": "你好，请介绍一下太一系统",
  "stream": false
}'
```

### 2. 批量推理 (llama.cpp)
```bash
./llama-cli \
  -m models/gemma-2-9b-it-Q4_K_M.gguf \
  -f input.txt \
  -o output.txt \
  -n 1024 \
  --n_threads 4
```

### 3. TurboQuant 压缩测试
```bash
source /workspace/turboquant-env/bin/activate
python3 /workspace/scripts/turboquant-test.py
```

---

## 🚨 故障排除

### Ollama 下载慢
```bash
# 检查网络连接
curl -I https://ollama.com

# 重启 Ollama 服务
sudo systemctl restart ollama

# 查看下载日志
tail -f /tmp/ollama-pull.log
```

### llama.cpp 内存不足
```bash
# 减少上下文长度
--n_ctx 2048

# 减少批处理大小
--batch_size 256

# 启用 swap (最后手段)
sudo swapon -a
```

### TurboQuant 导入错误
```bash
# 激活虚拟环境
source /workspace/turboquant-env/bin/activate

# 重新安装
pip install --upgrade turboquant
```

---

## 📅 后续优化计划

### P0 (本周)
- [x] Ollama 安装
- [x] llama.cpp 编译
- [x] TurboQuant 安装
- [ ] Gemma 2 9B 部署完成
- [ ] 性能基准测试

### P1 (本月)
- [ ] Qwen2.5 7B 部署 (中文优化)
- [ ] llama.cpp + TurboQuant 集成
- [ ] 模型路由自动化
- [ ] 监控 Dashboard

### P2 (季度)
- [ ] GPU 升级评估 (3060 12GB) - 可选，用于 TurboQuant
- [ ] vLLM 生产部署
- [ ] 多模型负载均衡

**注**: 当前 GGUF 内置量化已满足需求，GPU 升级为非必需。

---

*太一 AGI · 本地模型优化 v1.0 · 2026-04-18*
