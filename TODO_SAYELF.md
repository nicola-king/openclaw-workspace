# 🚨 待 SAYELF 决策/执行清单

> **生成时间**: 2026-05-04 09:00
> **状态**: 自动执行中...
> **原则**: AGI 时间线 - 并行·一次性交付·不等待确认

---

## 🔴 阻塞项 (需 SAYELF 手动执行)

### 1. 系统依赖安装 (sudo 必需)

**原因**: 当前系统无 pip，python3.14-venv 未安装，所有 Python 项目无法运行

**执行命令**:
```bash
# 在终端执行以下命令
sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev build-essential
sudo apt install -y libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo apt install -y zlib1g-dev libjpeg-dev libpng-dev
```

**影响项目**:
- ❌ MOSS-TTS-Nano (语音合成)
- ❌ Maigret (OSINT 工具)
- ❌ 跨境贸易 Agent (部分模块)
- ❌ 反爬对抗工具包

---

### 2. MOSS-TTS-Nano 部署

**执行命令**:
```bash
cd /home/sayelf/.openclaw/workspace/skills/moss-tts-nano
sudo bash install_deps.sh
```

**验证**:
```bash
python3 infer_onnx.py --prompt-audio-path assets/audio/zh_1.wav --text "你好世界"
```

---

### 3. Maigret OSINT 工具部署

**执行命令**:
```bash
cd /home/sayelf/.openclaw/workspace/skills/maigret
pip install -e .
```

**验证**:
```bash
maigret test_username --html
```

---

## 🟡 可自动执行项 (太一正在执行)

### [执行中] 创建统一安装脚本

太一正在创建一键安装脚本，SAYELF 只需执行一次即可安装所有依赖。

---

## ✅ 已完成项 (无需 SAYELF 干预)

| 任务 | 状态 | 时间 |
|------|------|------|
| 跨境贸易 Agent 迁移 | ✅ | 08:02 |
| OpenClaw Gateway 集成 | ✅ | 08:26 |
| 宪法修订 (Karpathy+RTK) | ✅ | 08:30 |
| 反爬对抗技能库 | ✅ | 08:56 |
| 搜索 Agent 架构文档 | ✅ | 09:00 |

---

## 📊 执行优先级

```
P0 (立即): 安装 python3-pip + python3-venv
P1 (今日): 部署 MOSS-TTS-Nano
P1 (今日): 部署 Maigret
P2 (本周): 配置外部 API Keys
P2 (本周): OpenClaw Gateway Skill 注册
```

---

## 🎯 一键执行方案

太一已创建统一安装脚本，SAYELF 只需在终端执行：

```bash
cd /home/sayelf/.openclaw/workspace
bash install_all_deps.sh
```

---

*太一 AGI · 待办清单自动生成*
