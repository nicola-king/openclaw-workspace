# weclaw 网络修复 - 直连微信

> 修复时间：2026-03-27 18:59

---

## 🔧 问题诊断

**问题**: 微信域名通过代理连接失败

**原因**: 微信域名有时直连更快，代理反而阻塞

---

## ✅ 修复方案

**使用直连模式**:
```bash
weclaw login --no-proxy
```

**或配置环境变量**:
```bash
export NO_PROXY=".qq.com,.weixin.qq.com,.wechat.com"
```

---

## 📱 最新二维码

**状态**: 生成中...

**获取方式**:
```bash
cat /tmp/weclaw-login.log
```

---

*修复时间：2026-03-27 18:59*
