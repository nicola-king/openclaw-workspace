# 太一 Telegram 集成 (Taiyi Telegram Integration)

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **类别**: 集成/消息推送/命令
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 太一系统与 Telegram Bot 的无缝集成

**适用场景**:
- 接收用户命令并路由到对应 Agent
- 推送系统状态通知
- 发送任务完成提醒
- 多 Bot 协作消息中转
- 实时交互式查询

---

## 🔧 核心组件

### 1. Bot 配置

| 属性 | 值 |
|------|-----|
| **Bot 名称** | 太一（AGI） |
| **Bot 用户名** | @sayelfbot |
| **Token** | `8351068758:AAFr3T3ZTfZNIXrl26o9ppgoeg_gBhTXTeI` |

### 2. 命令路由

| 命令 | 功能 | 路由目标 |
|------|------|---------|
| `/start` | 启动 Bot | 系统欢迎 |
| `/help` | 显示帮助 | 太一 |
| `/status` | 系统状态 | 太一 |
| `/search` | 全网搜索 | 共享搜索服务 |
| `/trade` | 跨境贸易 | 跨境贸易 Agent |
| `/travel` | 旅游规划 | 旅游探路者 |
| `/tts` | 语音合成 | MOSS-TTS |
| `/osint` | 数字足迹 | Maigret |

---

## 🚀 使用方式

### 启动 Bot

```bash
cd /home/sayelf/.openclaw/workspace/skills/telegram-integration
source venv-telegram/bin/activate
python3 telegram_bot.py
```

### 交互示例

```
用户: /search 智能水杯
Bot: 🔍 搜索结果: 智能水杯
     1. [亚马逊] 智能水杯 - $25
     2. [阿里] 智能水杯批发 - $18

用户: /trade 选品 智能水杯
Bot: 🎯 选品分析: 智能水杯
     评分: 92/100
     利润: 45%
```

---

## 📁 文件结构

```
skills/telegram-integration/
├── SKILL.md              # 技能说明
├── telegram_bot.py       # Bot 主程序
├── config.yaml           # 配置文件
└── command_router.py     # 命令路由器
```

---

*太一 AGI · Telegram 集成技能 v1.0*
