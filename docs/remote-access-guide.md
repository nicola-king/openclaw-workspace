# 太一看板远程访问指南

**创建时间**: 2026-04-09 08:45  
**当前状态**: 仅局域网访问 (http://192.168.3.74:5001)

---

## 📱 方案 1: Tailscale (推荐，需手动安装)

### 为什么需要手动安装？
自动安装脚本需要 sudo 密码，请按以下步骤手动安装。

### 安装步骤

**步骤 1: 添加 Tailscale 仓库**
```bash
# 下载 GPG 密钥
curl -fsSL https://tailscale.com/gpgkeys/tailscale.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/tailscale.gpg

# 添加仓库
echo "deb [signed-by=/usr/share/keyrings/tailscale.gpg] \
  https://pkgs.tailscale.com/stable/ubuntu noble main" | \
  sudo tee /etc/apt/sources.list.d/tailscale.list
```

**步骤 2: 安装 Tailscale**
```bash
sudo apt-get update
sudo apt-get install tailscale
```

**步骤 3: 启动并认证**
```bash
sudo tailscale up
```

输出会显示一个 URL，在浏览器打开并登录 Google/Microsoft 账号。

**步骤 4: 查看 Tailscale IP**
```bash
tailscale ip
# 输出类似：100.x.y.z
```

**步骤 5: 手机访问**
1. 手机安装 Tailscale App (iOS/Android)
2. 登录同一账号
3. 访问：`http://[Tailscale IP]:5001`

---

## 🚀 方案 2: ngrok (免 root，快速)

### 安装步骤

**步骤 1: 下载 ngrok**
```bash
cd /tmp
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

**步骤 2: 注册账号 (免费)**
1. 访问 https://ngrok.com/signup
2. 注册免费账号
3. 获取 Authtoken

**步骤 3: 配置 Authtoken**
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**步骤 4: 启动穿透**
```bash
ngrok http 5001
```

**步骤 5: 手机访问**
- 输出会显示 `https://xxx.ngrok.io`
- 手机浏览器访问这个 URL 即可

---

## 🌐 方案 3: Cloudflare Tunnel (免 root，推荐)

### 优势
- ✅ 无需公网 IP
- ✅ 免费
- ✅ 固定域名
- ✅ HTTPS 加密

### 安装步骤

**步骤 1: 安装 cloudflared**
```bash
# 下载
curl -Lo --create-dirs /usr/local/bin/cloudflared \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x /usr/local/bin/cloudflared
```

**步骤 2: 创建 Tunnel**
1. 访问 https://dash.teams.cloudflare.com/
2. Zero Trust → Access → Tunnels
3. Create a tunnel → 选择 DNS

**步骤 3: 配置 Connector**
```bash
cloudflared service install YOUR_TOKEN
```

**步骤 4: 添加 Public Hostname**
- Subdomain: kanban
- Domain: yourdomain.com (或 ngrok-free.app)
- Service: http://localhost:5001

**步骤 5: 手机访问**
- `https://kanban.yourdomain.com`

---

## 📊 方案对比

| 方案 | 难度 | 成本 | 安全性 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|--------|
| **Tailscale** | ⭐⭐ | 免费 | 🔒 最高 | 🟢 高 | ⭐⭐⭐⭐⭐ |
| **ngrok** | ⭐ | 免费 | 🟡 中等 | 🟡 中等 | ⭐⭐⭐⭐ |
| **Cloudflare** | ⭐⭐ | 免费 | 🔒 高 | 🟢 高 | ⭐⭐⭐⭐⭐ |

---

## 🔧 当前状态

**太一看板**:
- 运行中：✅
- 监听地址：`0.0.0.0:5001`
- 局域网访问：`http://192.168.3.74:5001`
- 远程访问：❌ 待配置

---

## 📝 下一步

请选择一个方案执行：

**方案 A**: 手动安装 Tailscale (推荐)
```bash
# 复制以上命令执行
```

**方案 B**: 使用 ngrok (最快)
```bash
# 5 分钟搞定
```

**方案 C**: 保持现状 (仅局域网)
```bash
# 在家使用即可
```

---

*文档创建：太一 AGI | 2026-04-09*
