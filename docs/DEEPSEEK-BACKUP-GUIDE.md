# DeepSeek 备用模型配置指南






> 更新时间：2026-04-26 14:18  
> 状态：✅ 已配置

---

## 📋 配置概览






| 项目 | 配置 |
|------|------|
| **备用模型** | DeepSeek V4 Flash (主力) / DeepSeek V4 Pro (备用) |
| **触发条件** | 百炼配额 98% 耗尽 |
| **切换顺序** | 百炼 → DeepSeek → Gemini → 本地模型 |
| **API 端点** | https://api.deepseek.com/v1 |

---

## 🔑 配置 DeepSeek API Key






### 1. 获取 API Key






1. 访问 https://platform.deepseek.com
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key

### 2. 配置环境变量






```bash

# 编辑 ~/.bashrc 或 ~/.zshrc





echo 'export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"' >> ~/.bashrc
source ~/.bashrc
```

## 3. 验证配置






```bash

# 检查环境变量





echo $DEEPSEEK_API_KEY

# 测试 API





curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

---

## 🔄 自动切换逻辑






### 切换流程






```
百炼正常 → 使用 qwen3.5-plus
    ↓ (配额 98%)
DeepSeek V3 → 使用 deepseek-v3
    ↓ (DeepSeek 限额)
Gemini 2.5 Pro → 使用 gemini-2.5-pro
    ↓ (Gemini 限额)
本地模型 → 使用 Qwen 2.5 7B
```

### 切换规则






| 条件 | 动作 |
|------|------|
| 百炼配额 98% | 自动切换到 DeepSeek V3 |
| DeepSeek 限额 | 切换到 Gemini 2.5 Pro |
| Gemini 限额 | 切换到本地模型 |
| 百炼恢复 | 强制切回百炼 |

---

## 📊 模型对比






| 模型 | 上下文 | 用途 | 成本 |
|------|--------|------|------|
| **qwen3.5-plus** | 131K | 主力模型 | ¥0.05/1K |
| **deepseek-v4-flash** | 128K | 主力备用 | ¥0.05/1K |
| **deepseek-v4-pro** | 128K | 均衡备用 | ¥0.1/1K |
| **gemini-2.5-pro** | 2M | 长文本 | 免费额度 |
| **Qwen 2.5 7B** | 8K | 本地兜底 | ¥0 |

---

## 🛠️ 相关文件






| 文件 | 用途 |
|------|------|
| `constitution/skills/MODEL-ROUTING.md` | 模型调度协议 |
| `config/provider-aliases.json` | 提供商别名配置 |
| `scripts/check-bailian-quota.py` | 百炼配额监控 |
| `scripts/check-deepseek-quota.py` | DeepSeek 配额监控 |

---

## ✅ 验收标准






- [x] DEEPSEEK_API_KEY 已配置
- [x] API 调用测试成功
- [ ] 自动切换逻辑验证
- [ ] 配额监控脚本运行

---

## 📊 可用模型






| 模型 ID | 名称 | 上下文 | 用途 |
|---------|------|--------|------|
| `deepseek-v4-flash` | DeepSeek V4 Flash | 128K | 快速/主力备用 |
| `deepseek-v4-pro` | DeepSeek V4 Pro | 128K | 均衡/备用 |

---

*太一 AGI · 2026-04-26*
