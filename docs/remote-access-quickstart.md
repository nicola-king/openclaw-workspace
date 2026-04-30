# 太一看板远程访问 - 快速配置指南

**当前状态**: ✅ 运行中 (http://localhost:5001)  
**局域网访问**: http://192.168.3.74:5001  
**远程访问**: 待配置

---

## 🎯 推荐方案：Tailscale (安全+ 免费)

### 为什么选择 Tailscale？
- ✅ 端到端加密
- ✅ 固定 IP 地址
- ✅ 完全免费
- ✅ 支持多人共享
- ✅ 手机/电脑都能用

### 安装步骤 (需输入密码)

**步骤 1: 添加仓库**
```bash
curl -fsSL https://tailscale.com/gpgkeys/tailscale.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/tailscale.gpg

echo "deb [signed-by=/usr/share/keyrings/tailscale.gpg] \
  https://pkgs.tailscale.com/stable/ubuntu noble main" | \
  sudo tee /etc/apt/sources.list.d/tailscale.list
```

**步骤 2: 安装**
```bash
sudo apt-get update
sudo apt-get install tailscale
```

**步骤 3: 启动**
```bash
sudo tailscale up
```

**步骤 4: 获取 IP**
```bash
tailscale ip
# 输出：100.x.y.z
```

**步骤 5: 手机访问**
1. 手机下载 Tailscale App
2. 登录同一账号
3. 访问：`http://[100.x.y.z]:5001`

---

## 🚀 免 root 方案：Cloudflare Tunnel

### 优势
- ✅ 无需 sudo 权限
- ✅ 固定域名
- ✅ HTTPS 加密
- ✅ 完全免费

### 安装步骤

**步骤 1: 下载 cloudflared**
```bash
mkdir -p ~/bin
curl -Lo ~/bin/cloudflared \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x ~/bin/cloudflared
export PATH="$HOME/bin:$PATH"
```

**步骤 2: 创建 Tunnel**
1. 访问 https://dash.teams.cloudflare.com/
2. 注册免费账号
3. Zero Trust → Access → Tunnels
4. Create a tunnel

**步骤 3: 运行 Connector**
```bash
~/bin/cloudflared tunnel --url http://localhost:5001
```

**步骤 4: 获取 URL**
- 输出会显示 `https://xxx.trycloudflare.com`

**步骤 5: 手机访问**
- 访问：`https://xxx.trycloudflare.com`

---

## 📱 本地网络方案 (无需配置)

### 如果手机和电脑在同一 WiFi

**直接访问**:
```
http://192.168.3.74:5001
```

**如果打不开**:
1. 检查防火墙：`sudo ufw allow 5001/tcp`
2. 确认同一网络
3. 重启 API 服务

---

## 🎯 我的建议

| 使用场景 | 推荐方案 |
|---------|---------|
| **在家使用** | 局域网访问 (无需配置) |
| **外出查看** | Tailscale (安全+ 稳定) |
| **临时分享** | Cloudflare Tunnel (快速) |
| **长期使用** | Tailscale + 云服务器 |

---

## 🔧 快速测试

**检查服务状态**:
```bash
curl http://localhost:5001/api/stats
```

**查看监听端口**:
```bash
ss -tlnp | grep 5001
```

**查看本机 IP**:
```bash
hostname -I
```

---

## 📝 下一步

**SAYELF，请选择**:

1. **手动配置 Tailscale** - 复制上方命令执行
2. **使用 Cloudflare Tunnel** - 免 root 快速方案
3. **保持现状** - 仅局域网使用
4. **其他需求** - 告诉我具体场景

---

*文档创建：太一 AGI | 2026-04-09 08:45*
