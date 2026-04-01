# TV Control Skill - 太一电视控制

> 版本：v1.0 | 创建：2026-03-28 13:59
> 功能：通过 HDMI-CEC 和系统命令控制电视
> 支持：华为/小米/海信/TCL/索尼/三星/LG 等品牌
> 通讯：Telegram Bot + HTTP API (5001 端口)

---

## 🎯 功能特性

| 功能 | 说明 | 状态 |
|------|------|------|
| **开关机** | HDMI-CEC 远程开关 | ✅ |
| **音量控制** | 音量+/音量-/静音 | ✅ |
| **频道切换** | 频道+/频道- | ✅ |
| **信号源切换** | HDMI1/HDMI2/AV 等 | ⏳ |
| **应用启动** | 打开指定应用 | ⏳ |
| **状态查询** | 电源/音量/信号源 | ✅ |
| **定时任务** | 定时开关电视 | ⏳ |
| **场景模式** | 观影/游戏/音乐模式 | ⏳ |

---

## 📺 支持品牌

| 品牌 | 协议 | 端口 | CEC 支持 | 状态 |
|------|------|------|---------|------|
| **华为** | HiLink | 8899 | ✅ | ✅ |
| **小米** | MIOT | 5555 | ✅ | ✅ |
| **海信** | Hisense | 8080 | ✅ | ✅ |
| **TCL** | TV+ | 8002 | ✅ | ✅ |
| **索尼** | BRAVIA | 10000 | ✅ | ✅ |
| **三星** | SmartTV | 8001 | ✅ | ✅ |
| **LG** | webOS | 3000 | ✅ | ✅ |
| **创维** | Skyworth | 8080 | ✅ | ✅ |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# HDMI-CEC 工具
sudo apt-get install cec-utils

# 音频工具
sudo apt-get install alsa-utils

# Python 依赖
pip install flask python-miio samsungtvws pylgtv
```

### 2. 配置电视

编辑 `config.yaml`:
```yaml
tv:
  brand: huawei          # 电视品牌
  ip: 192.168.1.100      # IP 地址 (网络控制需要)
  port: 8899             # 端口 (自动)
  token: ""              # Token (部分品牌需要)
  control_method: cec    # 控制方式：cec/xset/network

api:
  port: 5001             # HTTP API 端口
  token: your_secret     # API 认证 token

telegram:
  bot_token: "xxx"       # Telegram Bot Token
  chat_id: "xxx"         # 聊天 ID
```

### 3. 测试连接

```bash
# 运行测试脚本
bash scripts/test-tv.sh

# 或手动测试
echo "scan" | cec-client -s
echo "on" | cec-client -s
```

### 4. 启动服务

```bash
# 开发模式
python3 main.py

# 生产模式 (后台)
nohup python3 main.py &

# 或 systemd 服务
sudo systemctl enable taiyi-tv-control
sudo systemctl start taiyi-tv-control
```

---

## 📱 使用方法

### Telegram Bot 指令

**Bot**: @taiyi_bot

| 指令 | 功能 | 示例 |
|------|------|------|
| `/tv on` | 开机 | `/tv on` |
| `/tv off` | 关机 | `/tv off` |
| `/tv vol+` | 音量+ | `/tv vol+` |
| `/tv vol-` | 音量- | `/tv vol-` |
| `/tv mute` | 静音 | `/tv mute` |
| `/tv ch+` | 频道+ | `/tv ch+` |
| `/tv ch-` | 频道- | `/tv ch-` |
| `/tv status` | 查询状态 | `/tv status` |
| `/tv source HDMI1` | 切换信号源 | `/tv source HDMI1` |
| `/tv app YouTube` | 打开应用 | `/tv app YouTube` |

### HTTP API

**端点**: `http://192.168.1.X:5001/tv/control`

**请求示例**:
```bash
curl -X POST http://localhost:5001/tv/control \
  -H "Content-Type: application/json" \
  -d '{"command": "power", "token": "your_secret"}'
```

**响应示例**:
```json
{
  "status": "success",
  "command": "power",
  "tv_state": "on"
}
```

---

## 🔧 工具模块

### tools/cec.py - HDMI-CEC 控制

```python
from tools.cec import CECController

cec = CECController()
cec.power_on()      # 开机
cec.power_off()     # 关机
cec.volume_up()     # 音量+
cec.volume_down()   # 音量-
cec.mute()          # 静音
```

### tools/audio.py - 音频控制

```python
from tools.audio import AudioController

audio = AudioController()
audio.volume_up()       # 音量+
audio.volume_down()     # 音量-
audio.mute()            # 静音
audio.get_volume()      # 获取音量
```

### tools/display.py - 显示器控制

```python
from tools.display import DisplayController

display = DisplayController()
display.turn_on()       # 开启显示器
display.turn_off()      # 关闭显示器
display.get_status()    # 获取状态
```

---

## 📊 配置选项

### 完整配置示例

```yaml
# config.yaml

# 电视配置
tv:
  brand: huawei
  ip: 192.168.1.100
  port: 8899
  token: ""
  control_method: cec  # cec / xset / network
  
  # CEC 配置
  cec:
    enabled: true
    adapter: 0
    timeout: 5
  
  # 网络控制配置
  network:
    enabled: false
    protocol: hilink  # hilink / miot / smarttv / webos
  
  # 功能开关
  features:
    power_control: true
    volume_control: true
    channel_control: false
    source_control: false
    app_control: false

# API 配置
api:
  enabled: true
  host: "0.0.0.0"
  port: 5001
  token: "your_very_secret_token"
  cors_enabled: false
  allowed_ips:
    - "127.0.0.1"
    - "192.168.1.0/24"

# Telegram 配置
telegram:
  enabled: true
  bot_token: "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
  chat_id: "7073481596"
  commands:
    - "on"
    - "off"
    - "vol+"
    - "vol-"
    - "mute"
    - "status"

# 日志配置
logging:
  level: INFO
  file: logs/tv-control.log
  max_size: 10MB
  backup_count: 5

# 定时任务
scheduler:
  enabled: false
  timezone: "Asia/Shanghai"
  tasks:
    - name: "auto_off"
      cron: "0 23 * * *"
      action: "off"
      message: "该休息了，需要关电视吗？"
```

---

## 🧪 测试

### 单元测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_cec.py
pytest tests/test_audio.py
```

### 集成测试

```bash
# 测试 CEC 连接
python3 tests/test_cec_connection.py

# 测试网络控制
python3 tests/test_network_control.py

# 测试 Telegram Bot
python3 tests/test_telegram_bot.py
```

---

## 📁 目录结构

```
skills/tv-control/
├── SKILL.md                 # Skill 说明文档
├── main.py                  # 主程序入口
├── config.yaml              # 配置文件
├── requirements.txt         # Python 依赖
├── tools/
│   ├── __init__.py
│   ├── cec.py              # HDMI-CEC 控制
│   ├── audio.py            # 音频控制
│   ├── display.py          # 显示器控制
│   └── network.py          # 网络控制
├── handlers/
│   ├── __init__.py
│   ├── telegram.py         # Telegram Bot 处理器
│   └── http.py             # HTTP API 处理器
├── scripts/
│   ├── test-tv.sh          # 测试脚本
│   └── install-deps.sh     # 依赖安装脚本
├── tests/
│   ├── __init__.py
│   ├── test_cec.py
│   ├── test_audio.py
│   └── test_api.py
└── logs/
    └── tv-control.log
```

---

## 🚨 故障排除

### 常见问题

**Q1: CEC 扫描不到电视**
```
A: 检查以下几点:
   1. 电视已通电 (即使关机)
   2. HDMI 线连接正常
   3. 电视 CEC 功能已开启
   4. 重启电视和工控机
```

**Q2: 音量控制无效**
```
A: 尝试以下方法:
   1. 检查音频设备：amixer scontrols
   2. 测试音频控制：amixer set Master 50%
   3. 改用 CEC 音量控制：echo "volup" | cec-client -s
```

**Q3: Telegram Bot 无响应**
```
A: 检查:
   1. Bot Token 是否正确
   2. Chat ID 是否正确
   3. 网络连接是否正常
   4. 查看日志：tail -f logs/tv-control.log
```

---

## 📝 更新日志

### v1.0 (2026-03-28)
- ✅ HDMI-CEC 控制
- ✅ 音频控制
- ✅ 显示器控制
- ✅ Telegram Bot 集成
- ✅ HTTP API
- ✅ 华为/小米/三星/LG 支持

---

## 📄 许可证

MIT License

---

*版本：v1.0 | 创建时间：2026-03-28 13:59*
*作者：太一 AGI 团队*
