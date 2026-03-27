# 微信集成 (weclaw) 配置指南

> weclaw 是 Go 项目，不是 Node.js 项目

---

## 🔧 编译安装

### 步骤 1: 检查 Go 环境

```bash
go version
```

### 步骤 2: 编译 weclaw

```bash
cd /tmp/weclaw
go build -o weclaw ./cmd/
```

### 步骤 3: 安装到系统

```bash
sudo cp weclaw /usr/local/bin/
sudo chmod +x /usr/local/bin/weclaw
```

### 步骤 4: 测试运行

```bash
weclaw --help
weclaw login
weclaw start
```

---

## 📋 使用流程

### 1. 登录微信

```bash
weclaw login
# 会显示二维码
# 用微信扫码登录
```

### 2. 启动服务

```bash
weclaw start
```

### 3. 配置多 Bot

编辑配置文件:
```yaml
# ~/.weclaw/config.yaml
agents:
  - name: taiyi
    endpoint: http://127.0.0.1:18789/taiyi
  - name: zhiji
    endpoint: http://127.0.0.1:18789/zhiji
  - name: shanmu
    endpoint: http://127.0.0.1:18789/shanmu

switch_command: /
default_agent: taiyi
```

---

## ⚠️ 注意事项

1. **Go 环境要求**: Go 1.21+
2. **微信版本**: 需要最新版微信电脑版
3. **网络要求**: 需要稳定网络连接
4. **账号安全**: 官方接口，无封号风险

---

*创建时间：2026-03-27*
