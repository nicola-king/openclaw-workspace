# Screen Recorder · 录屏技能

> **版本**: v1.0  
> **创建时间**: 2026-04-21 16:11  
> **定位**: 太一系统内置录屏技能  
> **核心能力**: 录屏 + 白板 + 画中画

---

## 🎯 核心能力

| 能力 | 说明 | 状态 |
|------|------|------|
| **OBS 控制** | 启动/停止/配置 OBS | ✅ |
| **白板集成** | Excalidraw 自动打开 | ✅ |
| **画中画** | 摄像头小窗口叠加 | ✅ |
| **录制管理** | 文件管理/命名/存储 | ✅ |
| **快速启动** | 一键录制 | ✅ |

---

## 🚀 使用方式

### 方式 1: 语音指令

```
"太一，开始录屏"
"太一，停止录制"
"太一，打开白板"
```

### 方式 2: 文字指令

```
/录屏 开始
/录屏 停止
/白板 打开
```

### 方式 3: API 调用

```python
from screen_recorder import ScreenRecorder

recorder = ScreenRecorder()
recorder.start_recording()
recorder.stop_recording()
```

---

## 📐 录制配置

### 默认配置

| 参数 | 值 | 说明 |
|------|-----|------|
| **分辨率** | 1920x1080 | 全高清 |
| **帧率** | 30 FPS | 流畅录制 |
| **比特率** | 6000 Kbps | 高质量 |
| **格式** | MP4 | 通用格式 |
| **摄像头** | 150x150px | 右下角画中画 |
| **音频** | AAC 128kbps | 清晰音质 |

### 可调节参数

```yaml
recording:
  resolution: 1920x1080  # 可调整
  fps: 30                # 30/60
  bitrate: 6000          # 3000-10000
  format: mp4            # mp4/mkv/flv
  audio: true            # 是否录制音频
  camera: true           # 是否画中画
  camera_size: 150       # 摄像头窗口大小
  camera_position: bottom_right  # 位置
```

---

## 🎨 白板配置

### 默认白板：Excalidraw

| 参数 | 值 |
|------|-----|
| **URL** | https://excalidraw.com |
| **类型** | Web 白板 |
| **风格** | 手绘风格 |
| **协作** | 支持 |
| **导出** | PNG/SVG |

### 可选白板

| 白板 | URL | 特点 |
|------|-----|------|
| **Excalidraw** | excalidraw.com | 手绘风格 |
| **tldraw** | tldraw.com | 简洁 |
| **Witeboard** | witeboard.com | 实时协作 |

---

## 📁 文件管理

### 录制文件存储

```
/home/nicola/.openclaw/workspace/recordings/
├── 2026-04-21/
│   ├── recording_16-11-00.mp4
│   ├── recording_16-15-30.mp4
│   └── recording_16-20-15.mp4
├── 2026-04-22/
│   └── ...
└── manifest.json  # 录制清单
```

### 文件命名规则

```
recording_YYYY-MM-DD_HH-MM-SS.mp4
示例：recording_2026-04-21_16-11-00.mp4
```

---

## 🔧 系统集成

### 太一系统调用

```python
# 太一系统内部调用
result = taiyi.invoke_skill("screen_recorder", {
    "action": "start",
    "config": {
        "resolution": "1920x1080",
        "camera": True
    }
})
```

### 定时任务集成

```bash
# 可配置定时录制
0 9 * * 1-5 python3 screen_recorder.py --auto-start --duration 3600
```

---

## 📋 快捷指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `/录屏 开始` | 开始录制 | `/录屏 开始` |
| `/录屏 停止` | 停止录制 | `/录屏 停止` |
| `/录屏 暂停` | 暂停录制 | `/录屏 暂停` |
| `/录屏 继续` | 继续录制 | `/录屏 继续` |
| `/白板 打开` | 打开白板 | `/白板 打开` |
| `/摄像头 开` | 开启摄像头 | `/摄像头 开` |
| `/摄像头 关` | 关闭摄像头 | `/摄像头 关` |
| `/配置 查看` | 查看配置 | `/配置 查看` |

---

## 🎯 使用场景

### 场景 1: 教学录制

```
1. 打开 Excalidraw 白板
2. 开启摄像头画中画
3. 开始录制
4. 在白板上书写讲解
5. 停止录制
6. 自动保存文件
```

### 场景 2: 产品演示

```
1. 打开产品页面
2. 开启摄像头画中画
3. 开始录制
4. 演示产品功能
5. 停止录制
6. 自动保存文件
```

### 场景 3: 会议记录

```
1. 打开会议页面
2. 开启摄像头画中画
3. 开始录制
4. 记录会议内容
5. 停止录制
6. 自动保存文件
```

---

## ⚙️ 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| **OBS Studio** | 26.0+ | 30.0+ |
| **CPU** | 4 核 | 8 核 + |
| **内存** | 8GB | 16GB+ |
| **存储** | 10GB 可用 | 50GB+ |
| **摄像头** | 720p | 1080p |
| **麦克风** | 内置 | 外置 USB |

---

## 🔗 相关链接

| 项目 | 链接 |
|------|------|
| **OBS Studio** | https://obsproject.com |
| **Excalidraw** | https://excalidraw.com |
| **GitHub** | github.com/obsproject/obs-studio |
| **文档** | obsproject.com/help |

---

## 📊 调用统计

| 指标 | 数值 |
|------|------|
| **总录制次数** | 0 (新技能) |
| **总录制时长** | 0 分钟 |
| **总文件大小** | 0 MB |
| **平均质量** | N/A |

---

*太一 AGI · Screen Recorder Skill v1.0*  
*创建时间：2026-04-21 16:11*  
*核心：OBS Studio + Excalidraw*
