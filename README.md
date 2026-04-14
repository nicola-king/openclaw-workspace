# 🧬 OpenClaw-Hermes-Core

> **四层记忆架构 (Four-Layer Memory Architecture)**  
> **版本**: 2.0  
> **创建时间**: 2026-04-14  
> **灵感**: Hermes Agent + 太一 AGI 实践  
> **状态**: ✅ 生产就绪

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-4.11-green.svg)](https://github.com/openclaw/openclaw)

---

## 📊 四层记忆架构

```
┌─────────────────────────────────────────────────────────┐
│  第一层：核心记忆 (Core Memory)                          │
│  - 持久化记忆                                            │
│  - 价值观和原则                                          │
│  - 身份认同                                              │
│  - 加载策略：每次 session 必读                            │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第二层：情境记忆 (Context Memory)                       │
│  - 当前会话上下文                                        │
│  - 短期记忆                                              │
│  - 注意力焦点                                            │
│  - 加载策略：按需加载                                     │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第三层：演化记忆 (Evolution Memory)                     │
│  - 学习历史                                              │
│  - 技能演进                                              │
│  - 能力涌现记录                                          │
│  - 加载策略：恢复上下文时加载                              │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  第四层：残差记忆 (Residual Memory)                      │
│  - 细节信息                                              │
│  - 临时数据                                              │
│  - 按需加载                                              │
│  - 加载策略：context>80K 时加载                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 特性

- ✅ **四层记忆架构** - 参考 Hermes Agent 优化实现
- ✅ **自动化更新** - 每日 23:00 自动更新记忆
- ✅ **记忆流动机制** - 从日志到核心记忆的自动提炼
- ✅ **OpenClaw 集成** - 完美集成到 OpenClaw 生态系统
- ✅ **Telegram 推送** - 自动发送报告到 Telegram
- ✅ **定时任务** - 38 个 crontab 任务支持

---

## 📁 文件结构

```
openclaw-hermes-core/
├── constitution/axiom/
│   └── MEMORY-FOUR-LAYERS.md    # 四层记忆架构文档
├── memory/
│   ├── core.md                  # 核心记忆 (第一层)
│   ├── context.md               # 情境记忆 (第二层)
│   ├── evolution.md             # 演化记忆 (第三层)
│   ├── residual.md              # 残差记忆 (第四层)
│   └── MEMORY.md                # 长期固化记忆
├── scripts/
│   └── memory-four-layers-update.py  # 记忆更新脚本
├── README.md                    # 本文件
└── LICENSE                      # MIT License
```

---

## 🚀 快速开始

### 1. 安装 OpenClaw

```bash
# 安装 OpenClaw
npm install -g openclaw

# 初始化 workspace
openclaw init
```

### 2. 克隆本仓库

```bash
cd ~/.openclaw/workspace
git clone https://github.com/nicola-king/openclaw-hermes-core.git
cd openclaw-hermes-core
```

### 3. 复制文件到 workspace

```bash
# 复制记忆文件
cp memory/*.md ~/.openclaw/workspace/memory/

# 复制架构文档
cp constitution/axiom/MEMORY-FOUR-LAYERS.md ~/.openclaw/workspace/constitution/axiom/

# 复制更新脚本
cp scripts/memory-four-layers-update.py ~/.openclaw/workspace/scripts/
```

### 4. 设置定时任务

```bash
# 添加每日更新任务
(crontab -l 2>/dev/null; echo "0 23 * * * python3 ~/.openclaw/workspace/scripts/memory-four-layers-update.py daily") | crontab -
```

---

## 📋 使用说明

### 手动更新记忆

```bash
# 每日更新
python3 scripts/memory-four-layers-update.py daily

# 每周汇总
python3 scripts/memory-four-layers-update.py weekly

# 每月提炼
python3 scripts/memory-four-layers-update.py monthly
```

### 查看记忆状态

```bash
# 查看核心记忆
cat memory/core.md

# 查看情境记忆
cat memory/context.md

# 查看演化记忆
cat memory/evolution.md
```

---

## 🧠 记忆流动机制

```
每日日志 (YYYY-MM-DD.md)
         ↓
    提炼 → 情境记忆 (context.md)
         ↓
    汇总 → 核心记忆 (core.md)
         ↓
    演进 → 演化记忆 (evolution.md)
         ↓
    细节 → 残差记忆 (residual.md)
```

**更新频率**:
- 每日 (23:00): 情境记忆更新
- 每周 (周日 3:00): 演化记忆汇总
- 每月 (1 日): MEMORY.md 提炼

---

## 📊 与 Hermes Agent 对比

| 维度 | Hermes Agent | OpenClaw-Hermes-Core |
|------|--------------|---------------------|
| **核心记忆** | ✅ | ✅ 相同 |
| **情境记忆** | ✅ | ✅ 相同 + 会话归档 |
| **演化记忆** | ✅ | ✅ 相同 + 周汇总 |
| **残差记忆** | ✅ | ✅ 相同 + 按需加载 |
| **流动机制** | 基础 | ✅ 增强 (每日 + 每周 + 每月) |
| **自动化** | 手动 | ✅ 自动 (crontab) |
| **OpenClaw 集成** | ❌ | ✅ 完整集成 |
| **Telegram 推送** | ❌ | ✅ 完整支持 |

---

## 🛠️ 开发

### 运行测试

```bash
# 测试记忆更新脚本
python3 scripts/memory-four-layers-update.py daily --test
```

### 贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - 四层记忆架构灵感来源
- [OpenClaw](https://github.com/openclaw/openclaw) - AI 代理生态系统
- [太一 AGI](https://github.com/nicola-king) - 实现和优化

---

## 📱 联系方式

- **作者**: nicola king (SAYELF)
- **GitHub**: [@nicola-king](https://github.com/nicola-king)
- **Telegram**: @nicola_king

---

**🌟 如果这个项目对你有帮助，请给一个 Star！**
