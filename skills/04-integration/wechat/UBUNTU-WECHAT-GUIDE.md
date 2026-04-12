# 📱 Ubuntu 微信双开安装指南

> **创建时间**: 2026-04-08 18:51  
> **状态**: ✅ 脚本已创建

---

## ✅ 已创建文件

| 文件 | 用途 | 状态 |
|------|------|------|
| `~/bin/wechat-main.sh` | 主号启动 | ✅ 已创建 |
| `~/bin/wechat-secondary.sh` | 副号启动 | ✅ 已创建 |
| `~/bin/wechat-start.sh` | 一键双开 | ✅ 已创建 |
| `~/.local/share/applications/wechat-main.desktop` | 桌面快捷方式 | ✅ 已创建 |
| `~/.local/share/applications/wechat-secondary.desktop` | 桌面快捷方式 | ✅ 已创建 |

---

## 🚀 立即启动

### 方法 1: 一键双开 (推荐)

```bash
/home/nicola/bin/wechat-start.sh
```

### 方法 2: 分别启动

```bash
# 主号
/home/nicola/bin/wechat-main.sh

# 副号 (新终端)
/home/nicola/bin/wechat-secondary.sh
```

### 方法 3: 后台启动

```bash
# 同时启动两个
/home/nicola/bin/wechat-main.sh &
/home/nicola/bin/wechat-secondary.sh &
```

---

## 🔧 安装 Playwright (用于 RPA 自动化)

**需要密码权限，手动执行**:

```bash
# 方式 1: 使用 pip3
sudo apt update
sudo apt install -y python3-pip
pip3 install playwright
playwright install chromium

# 方式 2: 使用系统包
sudo apt install -y python3-playwright

# 验证安装
python3 -c "from playwright.async_api import async_playwright; print('✅ Playwright 已安装')"
```

---

## 📱 首次使用步骤

1. **启动微信**:
   ```bash
   /home/nicola/bin/wechat-start.sh
   ```

2. **扫码登录**:
   - 主号窗口 → 主号微信扫码
   - 副号窗口 → 副号微信扫码

3. **Session 保存**:
   - 登录后浏览器会自动保存 Session
   - 下次启动无需重复扫码

---

## 🤖 RPA 自动化 (待安装 Playwright)

**安装后使用**:

```bash
cd /home/nicola/.openclaw/workspace

# 首次扫码登录
python3 skills/browser-automation/adapters/wechat_adapter.py --account main --login

# 自动发送消息
python3 skills/browser-automation/adapters/wechat_adapter.py \
  --account main \
  --message "测试消息"
```

---

## 📊 快捷命令

**添加到 PATH 后**:

```bash
# 刷新配置
source ~/.bashrc

# 直接运行
wechat-main
wechat-secondary
wechat-start
```

---

## 🎯 下一步

**立即执行**:
1. ✅ 运行 `/home/nicola/bin/wechat-start.sh` 启动微信
2. ✅ 扫码登录两个微信账号
3. 🟡 (可选) 安装 Playwright 启用 RPA 自动化

**太一 AGI 集成**:
- 微信 RPA 适配器已就绪
- 安装 Playwright 后即可使用
- 支持自动消息/文件发送/接收

---

**现在可以启动微信了！** 📱🚀
