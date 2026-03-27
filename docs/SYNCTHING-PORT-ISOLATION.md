# Syncthing 端口隔离配置方案

> 严格限制 Syncthing 通讯端口，确保不影响 OpenClaw 运行

---

## 🔍 端口检查结果

### OpenClaw 使用端口

| 端口 | 协议 | 用途 | 方向 |
|------|------|------|------|
| **18789** | TCP | Gateway API | 本地 (127.0.0.1) |
| **443** | TCP | Telegram Bot API | 外向 (api.telegram.org) |
| **随机** | TCP | Telegram 长轮询 | 外向 |

### Syncthing 使用端口

| 端口 | 协议 | 用途 | 方向 |
|------|------|------|------|
| **22000** | TCP | 文件传输 | 双向 |
| **22000** | UDP | 发现协议 | 双向 |
| **21027** | UDP | 本地发现 | 本地广播 |
| **8384** | TCP | Web 界面 | 本地 (127.0.0.1) |

### 冲突检查结果

```
✅ OpenClaw 端口：18789, 443(外向)
✅ Syncthing 端口：22000, 21027, 8384
✅ 无端口冲突！
```

---

## 🔧 Syncthing 严格配置

### 配置文件位置

```
~/.config/syncthing/config.xml
```

### 端口限制配置

```xml
<configuration version="37">
    <!-- GUI 配置 - 仅本地访问 -->
    <gui enabled="true" tls="false" debugging="false">
        <address>127.0.0.1:8384</address>
        <apikey>YOUR_API_KEY</apikey>
        <user>admin</user>
        <password>STRONG_PASSWORD</password>
    </gui>

    <!-- 选项配置 - 严格限制 -->
    <options>
        <!-- 监听地址 - 仅指定端口 -->
        <listenAddress>tcp://0.0.0.0:22000</listenAddress>
        <listenAddress>udp://0.0.0.0:22000</listenAddress>
        
        <!-- 全局发现 - 可选关闭 -->
        <globalAnnounceEnabled>false</globalAnnounceEnabled>
        
        <!-- 本地发现 - 使用指定端口 -->
        <localAnnounceEnabled>true</localAnnounceEnabled>
        <localAnnouncePort>21027</localAnnouncePort>
        
        <!-- 限制带宽 - 避免影响 OpenClaw -->
        <maxSendKbps>10000</maxSendKbps>
        <maxRecvKbps>10000</maxRecvKbps>
        
        <!-- 连接限制 -->
        <maxFolderConcurrency>4</maxFolderConcurrency>
        
        <!-- 不通过代理 -->
        <reconnectIntervalS>60</reconnectIntervalS>
    </options>
</configuration>
```

---

## 🔐 防火墙规则

### UFW 配置

```bash
#!/bin/bash
# syncthing-firewall.sh

# 允许 Syncthing 端口
sudo ufw allow 22000/tcp comment "Syncthing 文件传输"
sudo ufw allow 22000/udp comment "Syncthing 发现协议"
sudo ufw allow 21027/udp comment "Syncthing 本地发现"

# Web 界面仅本地访问 (已绑定 127.0.0.1)
# 无需额外防火墙规则

# 禁止全局发现 (可选)
# sudo ufw deny out to any port 21027

echo "✅ Syncthing 防火墙规则已配置"
```

### 验证规则

```bash
# 查看规则
sudo ufw status verbose

# 预期输出:
# 22000/tcp    ALLOW IN    Anywhere
# 22000/udp    ALLOW IN    Anywhere
# 21027/udp    ALLOW IN    Anywhere
```

---

## 📊 网络隔离架构

```
┌─────────────────────────────────────────────────────┐
│              太一 (工控机) 网络架构                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  OpenClaw 层                                        │
│  ┌─────────────────────────────────────────────┐   │
│  │ Gateway: 127.0.0.1:18789 (仅本地)          │   │
│  │ Telegram Bot: 443/tcp (外向)               │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Syncthing 层                                       │
│  ┌─────────────────────────────────────────────┐   │
│  │ 文件传输：0.0.0.0:22000/tcp                │   │
│  │ 发现协议：0.0.0.0:22000/udp                │   │
│  │ 本地发现：0.0.0.0:21027/udp                │   │
│  │ Web 界面：127.0.0.1:8384 (仅本地)          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Tailscale 层 (可选)                                │
│  ┌─────────────────────────────────────────────┐   │
│  │ 虚拟网络：100.x.x.x                        │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 安装脚本（安全版）

```bash
#!/bin/bash
# syncthing-install-safe.sh
# 安全安装 Syncthing，不影响 OpenClaw

set -e

echo "=========================================="
echo "Syncthing 安全安装脚本"
echo "=========================================="

# 1. 检查端口占用
echo "🔍 检查端口占用..."
for port in 22000 21027 8384; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "❌ 端口 $port 已被占用！"
        exit 1
    fi
done
echo "✅ 端口无冲突"

# 2. 安装 Syncthing
echo "📦 安装 Syncthing..."
sudo apt update
sudo apt install -y syncthing

# 3. 创建用户服务
echo "🔧 配置用户服务..."
systemctl --user enable syncthing
systemctl --user start syncthing

# 4. 等待启动
echo "⏳ 等待 Syncthing 启动..."
sleep 5

# 5. 验证服务
if systemctl --user is-active syncthing > /dev/null 2>&1; then
    echo "✅ Syncthing 服务运行正常"
else
    echo "❌ Syncthing 服务启动失败"
    exit 1
fi

# 6. 配置防火墙
echo "🔐 配置防火墙..."
sudo ufw allow 22000/tcp comment "Syncthing 文件传输"
sudo ufw allow 22000/udp comment "Syncthing 发现协议"
sudo ufw allow 21027/udp comment "Syncthing 本地发现"

# 7. 验证 OpenClaw
echo "🔍 验证 OpenClaw 不受影响..."
if curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
    echo "✅ OpenClaw Gateway 正常"
else
    echo "⚠️ OpenClaw Gateway 无法访问 (可能是正常关闭)"
fi

echo ""
echo "=========================================="
echo "✅ Syncthing 安装完成！"
echo ""
echo "访问 Web 界面：http://127.0.0.1:8384"
echo "设备 ID: 在 Web 界面 → 操作 → 显示 ID"
echo "=========================================="
```

---

## 📋 双向任务调度配置

### 太一 ↔ 工作站

**目录结构**:
```
太一:
├── sync-to-workstation/
│   ├── jobs/           # 太一→工作站任务
│   └── data/           # 太一→工作站数据
└── sync-from-workstation/
    ├── results/        # 工作站→太一成果
    └── requests/       # 工作站→太一请求

工作站:
├── from-taiyi/
│   ├── jobs/           # 接收太一任务
│   └── data/           # 接收太一数据
├── to-taiyi/
│   ├── results/        # 发送太一成果
│   └── requests/       # 发送太一请求
└── processing/         # 处理中
```

### 笔记本 ↔ 工作站

**目录结构**:
```
笔记本:
├── sync-to-workstation/
│   ├── requests/       # 笔记本→工作站请求
│   └── data/           # 笔记本→工作站数据
└── sync-from-workstation/
    ├── results/        # 工作站→笔记本成果
    └── data/           # 工作站→笔记本数据

工作站:
├── from-laptop/
│   ├── requests/       # 接收笔记本请求
│   └── data/           # 接收笔记本数据
├── to-laptop/
│   ├── results/        # 发送笔记本成果
│   └── data/           # 发送笔记本数据
```

---

## 🚀 任务调度脚本

### 太一 → 工作站 (已创建)

```python
# skills/suwen/syncthing-job-monitor.py
# 工作站端监控脚本
```

### 工作站 → 太一 (新建)

```python
#!/usr/bin/env python3
"""
Syncthing 任务监控 - 太一端
监控从工作站传来的请求，执行后返回结果
"""

import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 目录配置
REQUESTS_DIR = Path("~/.openclaw/workspace/sync-from-workstation/requests").expanduser()
RESULTS_DIR = Path("~/.openclaw/workspace/sync-to-workstation/results").expanduser()
PROCESSING_DIR = Path("~/.openclaw/workspace/sync-processing").expanduser()
LOG_FILE = Path("~/.openclaw/workspace/logs/syncthing-workstation-monitor.log").expanduser()

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg, end="")
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def process_request(request_file):
    """处理工作站请求"""
    request_id = request_file.stem
    log(f"收到工作站请求：{request_id}")
    
    try:
        with open(request_file) as f:
            request = json.load(f)
        
        # 移动到处理中
        processing_file = PROCESSING_DIR / request_file.name
        request_file.rename(processing_file)
        
        # 执行请求
        command = request.get('command', 'echo "No command"')
        log(f"执行命令：{command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=request.get('timeout', 3600)
        )
        
        # 写入结果
        result_file = RESULTS_DIR / f"result-{request_id}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'request_id': request_id,
                'status': 'completed',
                'return_code': result.returncode,
                'stdout': result.stdout.decode()[:10000],
                'stderr': result.stderr.decode()[:10000],
                'completed_at': datetime.now().isoformat()
            }, f, indent=2)
        
        log(f"请求完成：{request_id}")
        processing_file.unlink()
        
    except Exception as e:
        log(f"请求失败：{request_id}, 错误：{e}")
        
        result_file = RESULTS_DIR / f"result-{request_id}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'request_id': request_id,
                'status': 'failed',
                'error': str(e)
            }, f, indent=2)

def main():
    """主循环"""
    log("=" * 60)
    log("太一 - 工作站请求监控启动")
    log("=" * 60)
    
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            request_files = list(REQUESTS_DIR.glob('request-*.json'))
            
            if request_files:
                log(f"发现 {len(request_files)} 个新请求")
                for request_file in request_files:
                    process_request(request_file)
            else:
                log("无新请求，等待中...")
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            log("停止监控")
            break

if __name__ == '__main__':
    main()
```

---

## 📊 监控仪表板

```bash
#!/bin/bash
# syncthing-status.sh

echo "=========================================="
echo "Syncthing 状态检查"
echo "=========================================="

# 服务状态
echo -n "服务状态："
if systemctl --user is-active syncthing > /dev/null 2>&1; then
    echo "✅ 运行中"
else
    echo "❌ 未运行"
fi

# 端口监听
echo ""
echo "端口监听:"
netstat -tlnp 2>/dev/null | grep syncthing || echo "无 Syncthing 端口"

# 连接设备
echo ""
echo "连接设备:"
curl -s http://127.0.0.1:8384/rest/system/connections 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(f'已连接 {len(d.get(\"connections\", {}))} 个设备')" || echo "无法获取"

# 同步文件夹
echo ""
echo "同步文件夹:"
curl -s http://127.0.0.1:8384/rest/db/status?folder=taiyi-to-workstation 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(f'待同步：{d.get(\"needFiles\", 0)} 文件')" || echo "无法获取"

# OpenClaw 状态
echo ""
echo "OpenClaw 状态:"
if curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
    echo "✅ Gateway 正常"
else
    echo "⚠️ Gateway 未响应"
fi

echo ""
echo "=========================================="
```

---

## ✅ 安全检查清单

- [ ] 端口无冲突 (22000, 21027, 8384 vs 18789)
- [ ] 防火墙规则已配置
- [ ] Web 界面仅本地访问
- [ ] 带宽限制已设置
- [ ] OpenClaw 正常运行
- [ ] 双向任务调度测试通过

---

*创建时间：2026-03-26 | 太一 AGI*
