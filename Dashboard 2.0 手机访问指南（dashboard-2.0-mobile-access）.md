# 📱 Dashboard 2.0 手机访问指南

> **创建时间**: 2026-04-14 23:50  
> **状态**: ✅ 已配置外部访问

---

## ✅ 手机访问地址

### 局域网访问 (推荐)

**前提**: 手机和服务器在同一 WiFi 网络

```
📱 前端访问：http://192.168.31.99:3000
📱 后端访问：http://192.168.31.99:8000
📱 健康检查：http://192.168.31.99:8000/healthz
```

**服务器信息**:
```
主机名：nicola-taiyi
内网 IP: 192.168.31.99
前端端口：3000
后端端口：8000
```

---

## 🔧 已配置优化

### Vite 配置更新

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    port: 3000,
    host: '0.0.0.0', // ✅ 允许外部访问
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
```

### 服务状态

```
✅ 前端服务：运行中
✅ 网络访问：http://192.168.31.99:3000/
✅ 后端服务：运行中
✅ WebSocket: 可用
```

---

## 📱 手机访问步骤

### 步骤 1: 确认网络

```
1. 确保手机连接到同一 WiFi
2. 确认服务器 IP: 192.168.31.99
3. 确认端口开放：3000, 8000
```

### 步骤 2: 手机浏览器访问

```
1. 打开手机浏览器 (Chrome/Safari/Edge)
2. 输入地址：http://192.168.31.99:3000
3. 等待页面加载
4. 即可看到 Dashboard 2.0
```

### 步骤 3: 测试功能

```
✅ 仪表盘页面
✅ Agent 管理页面
✅ Skill 管理页面
✅ 审批管理页面
✅ 响应式布局
```

---

## 🔒 防火墙配置 (如需要)

### Linux 防火墙

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
sudo ufw status

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 检查端口监听

```bash
# 检查端口是否监听
netstat -tlnp | grep -E '3000|8000'

# 或使用 ss 命令
ss -tlnp | grep -E '3000|8000'
```

---

## 🌐 公网访问方案

### 方案 A: ngrok 内网穿透

```bash
# 安装 ngrok
npm install -g ngrok

# 启动穿透
ngrok http 3000

# 获得公网地址
# 例如：https://xxxx.ngrok.io
```

### 方案 B: frp 内网穿透

```ini
# frpc.ini 配置
[common]
server_addr = 你的服务器 IP
server_port = 7000

[dashboard]
type = tcp
local_ip = 127.0.0.1
local_port = 3000
remote_port = 3000
```

### 方案 C: Cloudflare Tunnel

```bash
# 安装 cloudflared
npm install -g @cloudflare/cloudflared

# 启动隧道
cloudflared tunnel --url http://localhost:3000
```

---

## 📊 响应式设计

### 支持的屏幕尺寸

```
✅ 手机竖屏：320px - 480px
✅ 手机横屏：481px - 767px
✅ 平板：768px - 1023px
✅ 桌面：1024px+
```

### 移动端优化

```
✅ 响应式布局
✅ 触摸友好的按钮
✅ 自适应导航菜单
✅ 优化的字体大小
✅ 移动端统计卡片
```

---

## ⚠️ 注意事项

### 安全提示

```
⚠️ 局域网访问仅限信任网络
⚠️ 不要暴露到公网 without 认证
⚠️ 生产环境需要添加认证系统
⚠️ 建议使用 HTTPS
```

### 性能优化

```
✅ 使用 WiFi 而非移动数据
✅ 关闭不必要的后台应用
✅ 清除浏览器缓存
✅ 使用现代浏览器
```

---

## 🔗 快速链接

**访问地址**:
```
📱 前端：http://192.168.31.99:3000
💻 本地：http://localhost:3000
🔌 后端：http://192.168.31.99:8000
```

**项目目录**:
```
/home/nicola/.openclaw/workspace/dashboard-2.0/
```

---

*Dashboard 2.0 手机访问指南 · 太一 AGI · 2026-04-14 23:50*

**✅ 手机可以访问！已配置外部访问支持！**
