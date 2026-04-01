# 太一电视控制技能

> 版本：v1.0 | 创建：2026-03-28 13:54 | 太一电视接管
> 通讯端口：5001 (HTTP API) + Telegram 指令

---

## 🎯 控制方案对比

| 方案 | 类型 | 难度 | 成本 | 推荐度 |
|------|------|------|------|--------|
| **红外控制** | 硬件 IR 发射器 | ⭐⭐ | ¥50-100 | ⭐⭐⭐⭐ |
| **智能电视 API** | 网络控制 | ⭐ | ¥0 | ⭐⭐⭐⭐⭐ |
| **Home Assistant** | 中枢控制 | ⭐⭐ | ¥0 | ⭐⭐⭐⭐⭐ |
| **HDMI-CEC** | 硬件控制 | ⭐⭐⭐ | ¥100-200 | ⭐⭐⭐ |

---

## 📋 方案 1: 智能电视 API (首选)

### 支持品牌

| 品牌 | 协议 | 端口 | 状态 |
|------|------|------|------|
| **小米/Redmi** | MIOT | 5555 | ✅ 支持 |
| **海信** | Hisense | 8080 | ✅ 支持 |
| **TCL** | TV+ | 8002 | ✅ 支持 |
| **索尼** | BRAVIA | 10000 | ✅ 支持 |
| **三星** | SmartTV | 8001 | ✅ 支持 |
| **LG** | webOS | 3000 | ✅ 支持 |
| **华为** | HiLink | 8899 | ✅ 支持 |
| **创维** | Skyworth | 8080 | ✅ 支持 |

---

## 🔧 方案 2: Home Assistant (通用)

**优势**:
- ✅ 支持 100+ 电视品牌
- ✅ 统一接口
- ✅ 可联动其他设备
- ✅ 本地控制，隐私安全

**安装**:
```bash
# Docker 安装
docker run -d \
  --name homeassistant \
  --privileged \
  --network=host \
  -v /opt/homeassistant:/config \
  homeassistant/home-assistant:stable
```

**配置**:
```yaml
# configuration.yaml
media_player:
  - platform: xiaomi_miio
    host: 192.168.1.100
    token: YOUR_TV_TOKEN
  - platform: samsungtv
    host: 192.168.1.101
    port: 8001
```

---

## 🎮 控制功能

| 功能 | 指令 | 说明 |
|------|------|------|
| **开机** | `/tv on` | 打开电视 |
| **关机** | `/tv off` | 关闭电视 |
| **音量+** | `/tv vol+` | 增加音量 |
| **音量-** | `/tv vol-` | 减小音量 |
| **静音** | `/tv mute` | 静音切换 |
| **频道+** | `/tv ch+` | 上一个频道 |
| **频道-** | `/tv ch-` | 下一个频道 |
| **输入源** | `/tv source HDMI1` | 切换输入源 |
| **应用** | `/tv app Netflix` | 打开应用 |
| **状态** | `/tv status` | 查询状态 |

---

## 📱 通讯端口

### Telegram Bot 指令

**Bot**: @taiyi_bot
**指令前缀**: `/tv`

**示例**:
```
/tv on          # 开机
/tv off         # 关机
/tv vol+        # 音量+
/tv vol-        # 音量-
/tv mute        # 静音
/tv ch+         # 频道+
/tv app YouTube # 打开 YouTube
/tv status      # 查询状态
```

### HTTP API (5001 端口)

**端点**: `http://192.168.1.X:5001/tv/control`

**请求**:
```json
{
  "action": "power",
  "command": "on",
  "token": "YOUR_SECRET_TOKEN"
}
```

**响应**:
```json
{
  "status": "success",
  "message": "TV turned on",
  "tv_state": "on"
}
```

---

## 🔐 安全配置

### Token 认证

```python
# 配置
TV_CONTROL_TOKEN = "your_secret_token_here"

# 验证
def verify_token(token):
    return token == TV_CONTROL_TOKEN
```

### IP 白名单

```python
# 允许的 IP 列表
ALLOWED_IPS = [
    "192.168.1.1",    # 路由器
    "192.168.1.100",  # 手机
    "192.168.1.101",  # 电脑
]
```

---

## 🚀 快速启动

### Step 1: 确认电视型号

```
品牌：_______
型号：_______
IP 地址：192.168.1.___
```

### Step 2: 获取电视 Token (如需要)

**小米电视**:
```
1. 安装 Mi Home APP
2. 绑定电视
3. 获取 Token: https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor
```

**索尼电视**:
```
1. 设置 → 网络 → 远程控制
2. 启用远程控制
3. 无需 Token
```

### Step 3: 配置太一

```bash
# 编辑配置
nano ~/.openclaw/workspace/skills/taiyi/tv-control-config.yaml

# 填写电视信息
tv_brand: xiaomi
tv_ip: 192.168.1.100
tv_token: YOUR_TOKEN
tv_port: 5555
```

### Step 4: 测试控制

```bash
# 测试开机
python3 skills/taiyi/tv-control.py --test power_on

# 测试音量
python3 skills/taiyi/tv-control.py --test volume_up
```

---

## 📊 使用场景

### 场景 1: 语音控制电视

```
用户 → Telegram: "/tv on"
太一 → 电视 API: 开机指令
电视 → 开机
太一 → 用户: "✅ 电视已打开"
```

### 场景 2: 自动关电视 (定时)

```
23:00 → 太一检查时间
太一 → Telegram: "该休息了，需要关电视吗？"
用户 → "/tv off"
太一 → 电视：关机指令
```

### 场景 3: 观影模式

```
用户 → "/tv movie"
太一 → 电视：开机 + HDMI1 + 音量 30%
太一 → 灯光：调暗 (如支持)
太一 → 用户： "🎬 观影模式已启动"
```

---

## 📋 依赖安装

```bash
# 小米电视
pip install python-miio

# 三星电视
pip install samsungtvws

# 索尼电视
pip install bravia-tv

# LG 电视
pip install pylgtv

# Home Assistant
pip install homeassistant

# HTTP API
pip install flask
```

---

*版本：v1.0 | 创建时间：2026-03-28 13:54*
*状态：⏳ 待配置电视信息*
