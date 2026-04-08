📱 个人微信扫码登录

**当前状态**: Chromium 浏览器下载中...

**下载进度**: 后台运行中 (预计 2-5 分钟)

---

## 🚀 两种登录方式

### 方式 1: 等待 Playwright Chromium 下载完成 (推荐)

**查看下载进度**:
```bash
ls -lh ~/.cache/ms-playwright/
```

**下载完成后运行**:
```bash
/home/nicola/bin/wechat-login.sh
```

---

### 方式 2: 使用系统 Chromium (立即使用)

**手动打开微信网页版**:
```bash
# 主号
chromium-browser --profile-directory="wechat-main" \
  --user-data-dir=~/.config/chromium-wechat-main \
  --app=https://wx.qq.com

# 副号 (新终端)
chromium-browser --profile-directory="wechat-secondary" \
  --user-data-dir=~/.config/chromium-wechat-secondary \
  --app=https://wx.qq.com
```

**扫码登录**:
1. 浏览器窗口弹出
2. 手机微信扫码
3. 登录成功

---

## 📊 当前状态

| 组件 | 状态 |
|------|------|
| **Playwright** | ✅ 已安装 |
| **Chromium 下载** | 🟡 进行中 |
| **系统 Chromium** | ✅ 可用 (146.0.7680.164) |
| **微信脚本** | ✅ 已创建 |

---

**建议**: 先使用方式 2 (系统 Chromium) 手动扫码登录，等待 Playwright Chromium 下载完成后再使用 RPA 自动化功能。
