# weclaw 微信集成配置指南

> 最后更新：2026-03-27 18:54

---

## ✅ weclaw 状态

**编译安装**: ✅ /usr/local/bin/weclaw

**运行状态**: ✅ 运行中

**登录状态**: ⏳ 等待微信扫码

---

## 📱 扫码登录

### 方式 1: 直接访问二维码 URL

```
https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=5e686030af1257b57bb8d6b4c84fd6af&bot_type=3
```

**操作步骤**:
1. 复制上面 URL
2. 在手机浏览器打开
3. 或截图二维码，用微信扫描
4. 确认登录

### 方式 2: 命令行查看

```bash
weclaw login
# 会显示二维码或 URL
```

---

## 🔧 配置多 Bot

**配置文件**: `~/.weclaw/config.yaml`

```yaml
agents:
  - name: taiyi
    endpoint: http://127.0.0.1:18789/taiyi
  - name: zhiji
    endpoint: http://127.0.0.1:18789/zhiji
  - name: shanmu
    endpoint: http://127.0.0.1:18789/shanmu
  - name: suwen
    endpoint: http://127.0.0.1:18789/suwen
  - name: wangliang
    endpoint: http://127.0.0.1:18789/wangliang
  - name: paoding
    endpoint: http://127.0.0.1:18789/paoding

switch_command: /
default_agent: taiyi
```

---

## ✅ 登录成功后

**测试命令**:
```bash
weclaw status
weclaw --version
```

**预期输出**:
```
weclaw is running
weclaw version: dev
```

---

## 📋 使用方式

**微信聊天**:
```
发送消息给 weclaw 机器人

切换 Bot:
/taiyi → 切换到太一
/zhiji → 切换到知几
/shanmu → 切换到山木
...

自然语言:
"今天有什么交易信号？"
"帮我写一篇文章"
...
```

---

*创建时间：2026-03-27 18:54*
