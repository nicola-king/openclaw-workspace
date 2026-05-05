# 屏幕录制工具调研 - Linux 开源方案

> 生成时间：2026-05-05 | 系统：Ubuntu 26 (Wayland)

## 约束条件
- 必须支持 Wayland（需 PipeWire/Portal 接口）
- 开源免费优先
- 实用为第一标准（功能最适用）

## 对比结论

### ❌ 不推荐（Wayland 不可用）
- **SimpleScreenRecorder** (MaartenBaert/ssr) - 5K⭐，Qt 设计，X11 专用
- **Kap** (wulkano/Kap) - 19K⭐，Electron，Mac 专用
- **ScreenToGif** (NickeManarin) - 27K⭐，C# WPF，Windows 专用

### ✅ 推荐
1. **eSearch** (xushengfeng/eSearch) — 6.3K⭐，Electron/TS
   - 截屏+离线OCR+搜索翻译+以图搜图+录屏+屏幕翻译
   - 原生支持 Wayland (PipeWire)
   - 跨平台 Win/Mac/Linux ✅
   - AppImage 安装，零依赖
   - **🥇 首选**

2. **OBS Studio** (obsproject/obs-studio) — 63K⭐，C++/Qt
   - 行业标准，功能最全
   - 支持 Wayland（通过 PipeWire）
   - 重量级，适合专业场景
   - `sudo apt install obs-studio`

3. **Screenity** (alyssaxuu/screenity)
   - Chrome 扩展，零安装
   - 隐私友好，无限制免费
   - 需要 Chrome 浏览器

### 未找到
- **OpenScreen** (Siddharth Vaddem) — GitHub 上未找到此仓库
