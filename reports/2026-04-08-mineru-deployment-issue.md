# MinerU 本地部署问题记录

> 时间：2026-04-08 23:10  
> 状态：🟡 需要解决代理问题  
> 版本：MinerU 3.0.9

---

## ✅ 已完成

- [x] Git 克隆完成（/tmp/mineru）
- [x] Pip 安装完成（mineru 3.0.9）
- [x] 版本验证成功（mineru --version）

---

## ⚠️ 遇到的问题

### 问题 1：默认后端需要 torch

```
Error: `hybrid-auto-engine` requires local pipeline dependencies (`mineru[pipeline]`, including `torch`).
```

**解决**：使用 `-b pipeline` 参数

---

### 问题 2：代理配置冲突

```
ValueError: Unknown scheme for proxy URL URL('socks://127.0.0.1:7891/')
```

**原因**：系统代理配置与 httpx 不兼容

**解决方案**：

#### 方案 A：临时禁用代理
```bash
export HTTP_PROXY=""
export HTTPS_PROXY=""
export http_proxy=""
export https_proxy=""
mineru parse -p demo.pdf -o output/ -b pipeline
```

#### 方案 B：使用轻量级后端
```bash
# 不需要本地 torch，使用远程 API
mineru parse -p demo.pdf -o output/ -b vlm-http-client
```

#### 方案 C：安装完整依赖
```bash
pip install "mineru[pipeline]" --break-system-packages
```

---

## 🚀 推荐方案

### 方案 A：临时禁用代理（立即测试）✅

```bash
# 临时禁用代理
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

# 测试
mineru parse -p /tmp/mineru/demo/pdfs/demo1.pdf -o /tmp/mineru-test-output/ -b pipeline

# 恢复代理（如需要）
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
```

---

## 📋 下一步

1. 临时禁用代理测试
2. 验证 PDF 解析功能
3. 如成功，创建封装脚本（自动处理代理）
4. 与知几-E 集成

---

*问题记录：太一 AGI · 2026-04-08 23:10*
