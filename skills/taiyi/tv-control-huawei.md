# 太一电视控制 - 华为电视专用配置

> 版本：v1.0 | 创建：2026-03-28 13:57
> 电视品牌：华为 (Huawei)
> 控制方式：HDMI-CEC (工控机直连)

---

## 📺 华为电视信息

| 项目 | 配置 |
|------|------|
| **品牌** | 华为 (Huawei) |
| **协议** | HiLink / Android TV |
| **CEC 端口** | 自动检测 |
| **Token** | ❌ 不需要 |
| **控制方式** | HDMI-CEC |

---

## 🚀 快速启动 (华为电视)

### Step 1: 开启电视 CEC 功能

**遥控器操作**:
```
1. 按"设置"键
2. 输入源 → HDMI 控制 → 开启
   或
   通用 → CEC 控制 → 开启
3. 确认开启
```

**华为 CEC 功能名称**:
- 可能是 "Huawei Link"
- 或 "HDMI CEC 控制"
- 或 "设备联动"

---

### Step 2: 安装依赖 (工控机)

```bash
# 更新软件源
sudo apt-get update

# 安装 CEC 工具
sudo apt-get install -y cec-utils

# 安装音频工具
sudo apt-get install -y alsa-utils

# 安装 Python 依赖
pip install flask
```

---

### Step 3: 测试 CEC 连接

```bash
# 运行测试脚本
cd ~/.openclaw/workspace/skills/taiyi
bash test-huawei-tv.sh
```

**或手动测试**:
```bash
# 扫描设备
echo "scan" | cec-client -s

# 应该看到：
# device 0: TV (Huawei)
```

---

### Step 4: 测试控制

```bash
# 开机
echo "on" | cec-client -s

# 关机
echo "standby" | cec-client -s

# 音量+
echo "volup" | cec-client -s

# 音量-
echo "voldown" | cec-client -s

# 静音
echo "mute" | cec-client -s
```

---

### Step 5: 启动太一电视控制

```bash
# 后台运行
cd ~/.openclaw/workspace/skills/taiyi
nohup python3 tv-control-ipc.py &

# 查看日志
tail -f ~/.openclaw/workspace/logs/tv-control.log
```

---

## 📱 Telegram 指令

**Bot**: @taiyi_bot

| 指令 | 功能 | 示例 |
|------|------|------|
| `/tv on` | 开机 | `/tv on` |
| `/tv off` | 关机 | `/tv off` |
| `/tv vol+` | 音量+ | `/tv vol+` |
| `/tv vol-` | 音量- | `/tv vol-` |
| `/tv mute` | 静音 | `/tv mute` |
| `/tv status` | 查询状态 | `/tv status` |

---

## 🔍 故障排除

### 问题 1: CEC 扫描不到电视

**解决**:
```
1. 确认电视已通电 (即使关机)
2. 确认 HDMI 线连接正常
3. 在电视设置中开启 CEC 功能
4. 重启电视和工控机
```

### 问题 2: 控制指令无响应

**解决**:
```bash
# 重启 CEC 服务
sudo systemctl restart cec-client

# 重新扫描
echo "scan" | cec-client -s

# 检查电视 CEC 是否关闭
# 在电视设置中重新开启
```

### 问题 3: 音量控制无效

**解决**:
```bash
# 检查音频设备
amixer scontrols

# 测试音频控制
amixer set Master 50%

# 如无效，可能是电视音频由遥控器控制
# 改用 CEC 音量控制
echo "volup" | cec-client -s
```

---

## 📊 性能测试

```bash
# 测试响应时间
time echo "on" | cec-client -s
# 应该 <10ms

# 测试稳定性 (连续 10 次)
for i in {1..10}; do
    echo "volup" | cec-client -s
    sleep 0.5
done
```

---

## 🎯 使用示例

### 示例 1: 远程开机

```
你 (Telegram): /tv on
太一 → 工控机：echo "on" | cec-client -s
工控机 → 华为电视 (HDMI): 开机信号
华为电视 → 开机
太一 → 你：✅ 电视已打开
```

### 示例 2: 观影模式

```
你：/tv movie
太一：
  1. echo "on" | cec-client -s (开机)
  2. amixer set Master 30% (音量 30%)
  3. 切换到 HDMI1 (如支持)
太一：🎬 观影模式已启动
```

### 示例 3: 定时关电视

```
23:00 → 太一自动提醒
太一：该休息了，需要关电视吗？
你：/tv off
太一 → 工控机：echo "standby" | cec-client -s
电视 → 待机
太一：✅ 电视已关闭
```

---

## 📋 依赖检查清单

- [ ] cec-utils 已安装
- [ ] alsa-utils 已安装
- [ ] flask 已安装
- [ ] 电视 CEC 功能已开启
- [ ] HDMI 线连接正常
- [ ] 工控机和电视在同一电源回路

---

*版本：v1.0 | 创建时间：2026-03-28 13:57*
*状态：✅ 华为电视专用配置*
