# 三设备协同一键部署指南

> 免费开源 · 零月度费用 · 完全自动化

---

## 📋 快速开始

### 步骤 1: 太一工控机 (自动执行)

```bash
# 下载并执行脚本
cd ~/.openclaw/workspace
sudo bash scripts/taiyi-auto-setup.sh
```

**执行后**:
- ✅ Tailscale 安装并启动
- ✅ Syncthing 安装并启动
- ✅ 同步目录创建
- ✅ 监控服务部署
- ✅ 防火墙配置

**下一步**:
```bash
# 登录 Tailscale
sudo tailscale up
# 复制链接到浏览器登录
```

---

### 步骤 2: 工作站 (数据存储中心)

```bash
# 下载脚本
wget https://github.com/nicola-king/openclaw-workspace/raw/main/scripts/workstation-auto-setup.sh
# 或手动复制到工作站

# 执行脚本
sudo bash workstation-auto-setup.sh
```

**执行后**:
- ✅ Tailscale 安装并启动
- ✅ Syncthing 安装并启动
- ✅ D 盘目录结构创建
- ✅ SMB 共享配置
- ✅ 任务监控服务部署
- ✅ 防火墙配置

**下一步**:
```bash
# 登录 Tailscale
sudo tailscale up

# 设置 Samba 密码
sudo smbpasswd -a 你的用户名
```

---

### 步骤 3: 笔记本 (移动办公)

```bash
# 下载脚本
wget https://github.com/nicola-king/openclaw-workspace/raw/main/scripts/laptop-auto-setup.sh

# 执行脚本
bash laptop-auto-setup.sh
```

**执行后**:
- ✅ Tailscale 安装并启动
- ✅ Syncthing 安装并启动
- ✅ 同步目录创建
- ✅ SMB 客户端配置
- ✅ 访问脚本创建

**下一步**:
```bash
# 登录 Tailscale
sudo tailscale up

# 访问工作站共享
./access-workstation.sh

# 调取数据
./request-from-workstation.sh
```

---

## 📁 目录结构

### 太一工控机

```
~/.openclaw/workspace/
├── sync-to-workstation/       # 发送到工作站
│   ├── backup/                # 备份数据
│   ├── commands/              # 命令文件
│   └── results/               # 接收结果
├── sync-from-workstation/     # 从工作站接收
│   ├── results/               # 任务结果
│   ├── data/                  # 数据文件
│   └── requests/              # 工作站请求
└── logs/                      # 日志
```

### 工作站 (D 盘)

```
/mnt/d/syncthing-hub/
├── from-taiyi/               # 从太一接收
│   ├── backup/               # 太一备份
│   └── commands/             # 太一命令
├── to-taiyi/                 # 发送给太一
│   ├── results/              # 任务结果
│   └── data/                 # 数据文件
├── from-laptop/              # 从笔记本接收
│   ├── data/
│   └── requests/
├── to-laptop/all-data/       # 笔记本可访问所有数据
├── shared/                   # SMB 共享
│   ├── public/
│   ├── projects/
│   └── archives/
└── scripts/
    └── command-monitor.py    # 任务监控
```

### 笔记本

```
~/laptop-sync/
├── sync-to-workstation/
│   ├── data/
│   └── requests/
├── sync-from-workstation/
│   ├── results/
│   └── data/
└── local/                    # 本地不同步
```

---

## 🔧 Syncthing 配置

### 太一 → 工作站 (单向)

**太一端**:
- 文件夹 ID: `taiyi-backup`
- 路径：`~/.openclaw/workspace/sync-to-workstation`
- 共享给：工作站设备 ID
- 权限：发送接收

**工作站端**:
- 文件夹 ID: `from-taiyi`
- 路径：`/mnt/d/syncthing-hub/from-taiyi`
- 共享给：太一设备 ID
- 权限：**仅接收 (只读)** ⚠️

---

### 工作站 → 太一 (单向)

**工作站端**:
- 文件夹 ID: `workstation-results`
- 路径：`/mnt/d/syncthing-hub/to-taiyi`
- 共享给：太一设备 ID
- 权限：发送接收

**太一端**:
- 文件夹 ID: `from-workstation`
- 路径：`~/.openclaw/workspace/sync-from-workstation`
- 共享给：工作站设备 ID
- 权限：**仅接收 (只读)** ⚠️

---

### 笔记本 → 工作站 (单向)

**笔记本端**:
- 文件夹 ID: `laptop-data`
- 路径：`~/laptop-sync/sync-to-workstation`
- 共享给：工作站设备 ID
- 权限：发送接收

**工作站端**:
- 文件夹 ID: `from-laptop`
- 路径：`/mnt/d/syncthing-hub/from-laptop`
- 共享给：笔记本设备 ID
- 权限：**仅接收 (只读)** ⚠️

---

### 工作站 → 笔记本 (单向)

**工作站端**:
- 文件夹 ID: `workstation-to-laptop`
- 路径：`/mnt/d/syncthing-hub/to-laptop`
- 共享给：笔记本设备 ID
- 权限：发送接收

**笔记本端**:
- 文件夹 ID: `from-workstation`
- 路径：`~/laptop-sync/sync-from-workstation`
- 共享给：工作站设备 ID
- 权限：**仅接收 (只读)** ⚠️

---

## 🌐 SMB 共享访问

### 笔记本访问工作站

**方式 1: 脚本访问 (推荐)**
```bash
cd ~
./access-workstation.sh
# 输入工作站 Tailscale IP
# 自动挂载到 ~/workstation-share/
```

**方式 2: 手动挂载**
```bash
sudo mount -t cifs //工作站 IP/shared ~/workstation-share -o user=你的用户名
```

**方式 3: 直接浏览**
```bash
# Ubuntu 文件管理器
smb://工作站 IP/shared

# Windows
\\工作站 IP\shared
```

---

## 📊 数据调取流程

### 笔记本 → 工作站 调取数据

```bash
# 运行调取脚本
cd ~
./request-from-workstation.sh

# 输入要调取的文件路径
# 例如：shared/projects/project-a/data.csv

# 请求文件创建在:
# ~/laptop-sync/sync-to-workstation/requests/req-YYYYMMDD-HHMMSS.json

# Syncthing 自动同步到工作站

# 工作站处理请求，准备文件

# 文件同步回笔记本:
# ~/laptop-sync/sync-from-workstation/results/
```

---

## 🔐 授权机制

### 太一操作工作站

**P0 紧急任务**:
```
太一 → 立即执行 → 事后 Telegram 通知
```

**P1 高优先级**:
```
太一 → Telegram 请求授权 → SAYELF 确认 → 执行
```

**P2 普通任务**:
```
太一 → 周批量授权 → 自动执行
```

**P3 低优先级**:
```
太一 → 记录想法 → 等待询问
```

---

## 📞 故障排查

### 问题 1: Tailscale 无法连接

```bash
# 检查状态
sudo tailscale status

# 重新登录
sudo tailscale logout
sudo tailscale up
```

### 问题 2: Syncthing 不同步

```bash
# 检查服务
systemctl --user status syncthing

# 重启服务
systemctl --user restart syncthing

# 查看日志
journalctl --user -u syncthing -f
```

### 问题 3: SMB 无法访问

```bash
# 检查 Samba 服务
sudo systemctl status smbd

# 重启 Samba
sudo systemctl restart smbd

# 检查防火墙
sudo ufw status
sudo ufw allow 445/tcp
```

### 问题 4: 工作站 IP 未知

```bash
# 在工作站执行
tailscale ip

# 或在 Tailscale 管理后台查看
# https://login.tailscale.com/admin/machines
```

---

## 📈 监控与维护

### 查看同步状态

```bash
# Syncthing Web 界面
http://127.0.0.1:8384

# 命令行
curl -s http://127.0.0.1:8384/rest/system/status | python3 -m json.tool
```

### 查看任务执行

```bash
# 工作站监控日志
tail -f /mnt/d/syncthing-hub/logs/command-monitor.log

# 太一监控日志
tail -f ~/.openclaw/workspace/logs/syncthing-workstation-monitor.log
```

### 查看设备状态

```bash
# Tailscale 设备列表
tailscale status

# Syncthing 连接设备
curl -s http://127.0.0.1:8384/rest/system/connections | python3 -m json.tool
```

---

## 🎯 验证清单

- [ ] Tailscale 三设备已登录
- [ ] Syncthing 三设备已连接
- [ ] 单向同步配置正确
- [ ] SMB 共享可访问
- [ ] 任务监控服务运行
- [ ] 太一可下发命令到工作站
- [ ] 笔记本可访问工作站数据
- [ ] 笔记本可调取工作站数据

---

## 📄 相关文档

- `constitution/extensions/AUTHORIZATION.md` - 授权协议
- `docs/SYNCTHING-PORT-ISOLATION.md` - 端口隔离配置
- `docs/SYNCTHING-SETUP.md` - Syncthing 详细配置

---

*创建时间：2026-03-26 | 太一 AGI | 版本：v1.0*
