# 太一电视控制配置

> 版本：v1.0 | 创建：2026-03-28 13:54
> ⚠️ 请根据实际情况填写以下配置

---

## 📺 电视信息

**请填写你的电视信息**:

| 项目 | 填写内容 |
|------|---------|
| **品牌** | `xiaomi` / `hisense` / `tcl` / `sony` / `samsung` / `lg` / `huawei` / `skyworth` |
| **型号** | _______________ |
| **IP 地址** | `192.168.1.___` |
| **端口** | (自动，见下方品牌端口表) |
| **Token** | (部分品牌需要，见下方获取方法) |

---

## 🔌 品牌端口对照表

| 品牌 | 默认端口 | Token 需求 |
|------|---------|-----------|
| **小米** | 5555 | ✅ 需要 |
| **海信** | 8080 | ❌ 不需要 |
| **TCL** | 8002 | ❌ 不需要 |
| **索尼** | 10000 | ❌ 不需要 |
| **三星** | 8001 | ❌ 不需要 |
| **LG** | 3000 | ❌ 不需要 |
| **华为** | 8899 | ❌ 不需要 |
| **创维** | 8080 | ❌ 不需要 |

---

## 🔑 Token 获取方法

### 小米电视 Token 获取

**方法 1: Mi Home APP**
```
1. 安装 Mi Home APP
2. 登录小米账号
3. 绑定电视
4. 访问：https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor
5. 按照说明获取 Token
```

**方法 2: 抓包**
```
1. 手机连接同一 WiFi
2. 安装抓包工具 (如 HttpCanary)
3. 打开 Mi Home APP 控制电视
4. 抓取包含 token 的请求
```

### 其他品牌

大多数品牌无需 Token，首次连接时电视会弹出确认对话框，点击"允许"即可。

---

## 📝 配置步骤

### Step 1: 编辑配置文件

```bash
nano ~/.openclaw/workspace/skills/taiyi/tv-control-config.yaml
```

### Step 2: 填写配置

```yaml
# 电视配置
tv_brand: "xiaomi"          # 你的电视品牌
tv_ip: "192.168.1.100"      # 你的电视 IP
tv_port: 5555               # 端口 (可自动)
tv_token: "YOUR_TOKEN_HERE" # Token (如需要)

# API 配置
api_port: 5001              # HTTP API 端口
api_token: "your_secret_token"  # API 认证 token

# Telegram 配置
telegram_bot_token: "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
telegram_chat_id: "7073481596"
```

### Step 3: 测试连接

```bash
# 测试开机
python3 skills/taiyi/tv-control.py --test power

# 测试音量
python3 skills/taiyi/tv-control.py --test volume_up
```

### Step 4: 启动服务

```bash
# 后台运行
cd ~/.openclaw/workspace/skills/taiyi
nohup python3 tv-control.py &

# 或者 systemd 服务
sudo systemctl enable taiyi-tv-control
sudo systemctl start taiyi-tv-control
```

---

## 🎮 Telegram 指令

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
| `/tv app YouTube` | 打开应用 | `/tv app YouTube` |
| `/tv source HDMI1` | 切换信号源 | `/tv source HDMI1` |

---

## 🌐 HTTP API

**端点**: `http://192.168.1.X:5001/tv/control`

**请求示例**:
```bash
curl -X POST http://192.168.1.100:5001/tv/control \
  -H "Content-Type: application/json" \
  -d '{"command": "power", "token": "your_secret_token"}'
```

**响应示例**:
```json
{
  "status": "success",
  "command": "power",
  "message": "TV turned on"
}
```

---

## 🔐 安全配置

### Token 认证

```yaml
api_token: "your_very_secret_token_here"
```

### IP 白名单 (可选)

```yaml
allowed_ips:
  - "192.168.1.1"
  - "192.168.1.100"
  - "192.168.1.101"
```

---

## 📊 依赖安装

```bash
# 小米电视
pip install python-miio

# 三星电视
pip install samsungtvws

# LG 电视
pip install pylgtv

# HTTP API
pip install flask

# 全部安装
pip install python-miio samsungtvws pylgtv flask
```

---

## 🚨 故障排除

### 问题 1: 电视无响应

**检查**:
- [ ] 电视和太一在同一 WiFi 网络
- [ ] 电视 IP 地址正确
- [ ] 电视已开启网络控制功能
- [ ] 防火墙未阻止端口

### 问题 2: Token 错误 (小米)

**解决**:
```
1. 重新获取 Token
2. 确认 Token 格式正确 (32 位十六进制)
3. 重启电视
```

### 问题 3: 首次连接被拒绝

**解决**:
```
三星/LG 电视首次连接时会在电视上弹出确认对话框
请在电视上点击"允许"或"Accept"
```

---

*版本：v1.0 | 创建时间：2026-03-28 13:54*
*状态：⏳ 待配置电视信息*
