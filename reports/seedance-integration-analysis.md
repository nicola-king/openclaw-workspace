# 🎬 Seedance 2.0 集成分析报告

> **分析时间**: 2026-04-10 15:40  
> **分析者**: 太一 AGI  
> **主题**: Seedance SKII 本地部署可行性

---

## 📋 核心结论

| 问题 | 答案 | 说明 |
|------|------|------|
| **能否本地部署？** | ❌ **不能** | Seedance 2.0 是云端 API 服务 |
| **能否本地调用？** | ✅ **可以** | 通过官方 Python SDK 调用 API |
| **需要 GPU 吗？** | ❌ **不需要** | 计算在 ByteDance 云端 |
| **需要 API Key 吗？** | ✅ **需要** | Volcengine 火山引擎账号 |

---

## 🔍 Seedance 2.0 技术架构

### 官方定位

```
Seedance 2.0 = ByteDance 云端 AI 视频生成服务
             ≠ 本地可部署模型
```

**部署模式**:
```
┌─────────────────┐      HTTPS API      ┌──────────────────┐
│   本地客户端    │ ←─────────────────→ │   ByteDance 云端  │
│   (Python SDK)  │                     │   (GPU 集群)      │
└─────────────────┘                     └──────────────────┘
       ↓                                        ↓
   发送提示词                                视频生成
   接收视频 URL                              返回结果
```

---

## 📦 安装方式

### 方式 1: Python SDK (推荐)

```bash
# 安装官方 SDK
pip install seedance

# 或从 GitHub 安装
pip install git+https://github.com/seedance-2/seedance-2.0.git
```

### 方式 2: 命令行工具

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/.../seedance)"

# Windows
# 下载 seedance_x64.7z 运行安装程序
```

### 方式 3: Docker (可选)

```bash
docker pull seedance/seedance-2.0:latest
docker run -e API_KEY=your_key seedance/seedance-2.0
```

---

## 🔑 API 配置

### 获取 API Key

1. **注册 Volcengine 火山引擎**
   - 网址：https://www.volcengine.com/
   - 需要实名认证

2. **开通 Seedance 服务**
   - 控制台 → AI 实验室 → Seedance 2.0
   - 订阅付费计划

3. **获取 API Key**
   - 控制台 → API 管理 → 创建密钥
   - 保存 `SEEDANCE_API_KEY`

### 价格参考 (2026)

| 计划 | 价格 | 额度 |
|------|------|------|
| **免费** | ¥0 | 10 次/月 (水印) |
| **专业** | ¥299/月 | 500 次 (无水印) |
| **企业** | ¥2999/月 | 5000 次 + 优先队列 |

---

## 💻 太一集成方案

### 方案 A: API 调用 (推荐) ✅

**创建 Skill**: `skills/seedance-video/SKILL.md`

```python
#!/usr/bin/env python3
"""
Seedance 2.0 视频生成 Skill

功能:
1. 文本生成视频 (Text-to-Video)
2. 图片生成视频 (Image-to-Video)
3. 多模态参考 (最多 12 个文件)
4. 原生音频生成

依赖:
- pip install seedance
- 环境变量：SEEDANCE_API_KEY
"""

import os
from seedance import SeedanceClient

class SeedanceVideoSkill:
    def __init__(self):
        self.api_key = os.getenv("SEEDANCE_API_KEY")
        if not self.api_key:
            raise ValueError("缺少 SEEDANCE_API_KEY 环境变量")
        
        self.client = SeedanceClient(api_key=self.api_key)
    
    async def generate_video(self, prompt, **kwargs):
        """生成视频"""
        
        config = {
            "prompt": prompt,
            "model": "seedance-v2-turbo",
            "duration": kwargs.get("duration", 5),  # 5/10/15 秒
            "resolution": kwargs.get("resolution", "1080p"),
            "fps": kwargs.get("fps", 60),
            "with_audio": kwargs.get("with_audio", True),
            "creativity_scale": kwargs.get("creativity_scale", 0.7),
        }
        
        # 提交任务
        task = await self.client.submit_task(**config)
        
        # 轮询结果
        result = await self.client.poll_until_complete(task.id)
        
        return {
            "video_url": result.video_url,
            "thumbnail_url": result.thumbnail_url,
            "duration": result.duration,
            "resolution": result.resolution
        }
```

**优点**:
- ✅ 无需本地 GPU
- ✅ 生成速度快 (1-5 分钟)
- ✅ 2K 60fps 高质量
- ✅ 原生音频生成
- ✅ 多模态参考支持

**缺点**:
- ❌ 需要付费 (按次计费)
- ❌ 依赖网络
- ❌ 视频上传到云端

---

### 方案 B: 本地替代方案 (开源模型)

如果用户坚持要**本地部署**,可考虑以下开源替代方案:

| 模型 | 本地部署 | GPU 需求 | 质量 |
|------|---------|---------|------|
| **Stable Video Diffusion** | ✅ 可部署 | RTX 3090+ (24GB) | ⭐⭐⭐ |
| **ModelScope** | ✅ 可部署 | RTX 4090+ (24GB) | ⭐⭐⭐⭐ |
| **AnimateDiff** | ✅ 可部署 | RTX 3080+ (12GB) | ⭐⭐⭐ |
| **Zeroscope** | ✅ 可部署 | RTX 3060+ (8GB) | ⭐⭐ |

**推荐**: Stable Video Diffusion (SVD)

```bash
# 安装 SVD
pip install stable-video-diffusion

# 最低要求:
# - GPU: RTX 3080 (12GB VRAM)
# - 内存：32GB RAM
# - 存储：50GB (模型 + 缓存)
```

---

## 🎯 太一集成建议

### 推荐方案：API 调用 + 本地备选

```
主方案：Seedance API (云端)
├── 高质量视频生成
├── 无需本地 GPU
└── 按使用付费

备选方案：SVD (本地)
├── 离线可用
├── 无 API 费用
└── 需要高性能 GPU
```

### 实施步骤

#### 步骤 1: 创建 Seedance Skill

```
skills/seedance-video/
├── SKILL.md (技能说明)
├── seedance_client.py (API 客户端)
└── config.json (配置)
```

#### 步骤 2: 配置环境变量

```bash
# ~/.openclaw/workspace/.env
SEEDANCE_API_KEY="your_api_key_here"
SEEDANCE_DEFAULT_DURATION=5
SEEDANCE_DEFAULT_RESOLUTION=1080p
```

#### 步骤 3: 集成到视频工厂

```python
# skills/video-factory/SKILL.md
# 添加 Seedance 作为视频生成后端

VIDEO_BACKENDS = {
    "seedance": "云端高质量 (推荐)",
    "svd": "本地离线",
    "jimeng": "即梦 API"
}
```

---

## 📊 硬件需求对比

| 方案 | GPU | 内存 | 存储 | 网络 |
|------|-----|------|------|------|
| **Seedance API** | 不需要 | 4GB | 1GB | 必需 |
| **SVD 本地** | RTX 3080+ | 32GB | 50GB | 可选 |
| **ModelScope** | RTX 4090+ | 64GB | 100GB | 可选 |

---

## 💰 成本分析

### Seedance API (云端)

```
使用频率：10 次/天
单次成本：¥0.5 (1080p 5 秒)
月成本：10 × 30 × 0.5 = ¥150/月
```

### SVD 本地部署

```
硬件成本:
- GPU (RTX 3080): ¥5000 (一次性)
- 内存 (32GB): ¥800 (一次性)
- 存储 (1TB SSD): ¥500 (一次性)
总计：¥6300 (一次性)

电费:
- 功耗：350W
- 每天 4 小时：1.4kWh
- 月电费：1.4 × 30 × ¥0.6 = ¥25/月
```

**回本周期**: ¥6300 ÷ ¥150 ≈ **42 个月** (3.5 年)

**结论**: 低频使用 → API 更划算  
**结论**: 高频使用 (>50 次/天) → 本地更划算

---

## 🚀 实施决策树

```
需要本地部署吗？
│
├─ 是 → 有高性能 GPU 吗？
│       │
│       ├─ 是 → 部署 SVD/ModelScope
│       │       └── 创建 skills/svd-video/
│       │
│       └─ 否 → 购买 GPU 或使用 API
│
└─ 否 → 使用 Seedance API
        └── 创建 skills/seedance-video/
```

---

## 📝 推荐方案总结

### 对于太一 AGI (推荐)

**方案**: Seedance API 调用

**理由**:
1. ✅ 太一已有视频工厂 Skill
2. ✅ 无需额外硬件投资
3. ✅ 高质量 2K 60fps 输出
4. ✅ 原生音频生成
5. ✅ 按需付费成本低

**实施**:
```bash
# 1. 注册 Volcengine 账号
# 2. 获取 API Key
# 3. 创建 skills/seedance-video/
# 4. 配置环境变量
# 5. 集成到视频工厂
```

---

## ⚠️ 注意事项

### 安全

- API Key 存储在 `.env` 文件
- 不要提交到 Git
- 定期轮换密钥

### 隐私

- 视频上传到 ByteDance 云端
- 敏感内容慎用
- 可考虑本地 SVD 替代

### 成本

- 设置月度预算上限
- 监控 API 使用量
- 免费额度优先使用

---

## 📋 下一步

### 立即实施 (如果确认)

1. ⏳ 注册 Volcengine 账号
2. ⏳ 获取 API Key
3. ⏳ 创建 `skills/seedance-video/`
4. ⏳ 测试 API 调用
5. ⏳ 集成到视频工厂

### 备选方案 (如果需要本地)

1. ⏳ 检查 GPU 硬件
2. ⏳ 安装 SVD 依赖
3. ⏳ 创建 `skills/svd-video/`
4. ⏳ 测试本地生成

---

*报告生成：太一 AGI*  
*分析时间：2026-04-10 15:40*  
*结论：Seedance 不能本地部署，但可通过 API 调用*
