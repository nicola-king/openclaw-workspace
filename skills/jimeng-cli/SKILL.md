---
name: jimeng-cli
version: 1.0.0
description: jimeng-cli skill
category: cli
tags: []
author: 太一 AGI
created: 2026-04-07
---


# 即梦 CLI - Jimeng AI 集成

> 版本：v1.0 | 创建时间：2026-04-06 09:22 | 状态：🟡 待安装  
> 来源：字节跳动即梦 AI 官方 CLI (2026-04-01 发布)

---

## 📋 技能描述

**即梦 CLI** 是字节跳动即梦 AI 官方命令行工具，让 Agent 直接调用 **Seedance 2.0** 模型生成视频/图片。

**核心能力**：
- 🎬 **文生视频**: Text-to-Video (Seedance 2.0)
- 🖼️ **文生图**: Text-to-Image (4K 分辨率)
- 📸 **图生图**: Image-to-Image
- 🎥 **图生视频**: Image-to-Video
- 🔄 **多模态**: 8 大命令全覆盖

**太一集成**：
- 山木内容创作：视频脚本→自动成片
- 罔两数据采集：批量生成素材
- 社交媒体：自动化视频内容生产

---

## 🛠️ 安装步骤

### ⚠️  重要：需要 API 密钥！

**即梦 CLI 需要 API 密钥认证**，通过火山引擎平台获取。

### 1. 获取 API 密钥

**步骤**:
1. 打开即梦官网：https://jimeng.jianying.com
2. 登录账号 (抖音/头条/火山引擎账号)
3. 进入 **API 调用** 或 **控制台**
4. 创建 API Key，获取：
   - `AccessKeyID`
   - `SecretAccessKey`

**火山引擎文档**: https://www.volcengine.com/docs/85621/1817045

### 2. 一键安装 CLI
```bash
curl -s https://jimeng.jianying.com/cli | bash
```

### 3. 配置认证
```bash
# 方式 1: CLI 交互式登录
jimeng login
# 输入 AccessKeyID 和 SecretAccessKey

# 方式 2: 直接配置
jimeng config set access_key_id YOUR_ACCESS_KEY_ID
jimeng config set secret_access_key YOUR_SECRET_ACCESS_KEY
jimeng config set model seedance-2.0
```

### 4. 验证安装
```bash
jimeng --version
jimeng balance  # 查看余额/配额
```

---

## 🎯 使用命令

### 文生视频
```bash
# 基础用法
jimeng generate --type video --prompt "赛博朋克城市夜景"

# 高级参数
jimeng generate video \
  --prompt "未来科技城市，飞行汽车，霓虹灯" \
  --duration 10 \
  --resolution 1080p \
  --fps 30 \
  --model seedance-2.0
```

### 文生图
```bash
# 4K 高清图片
jimeng generate image \
  --prompt "中国风山水画，青山绿水" \
  --resolution 4k \
  --style artistic
```

### 图生视频
```bash
jimeng generate video \
  --image ./input.jpg \
  --prompt "让画面动起来，云朵飘动" \
  --duration 5
```

### 批量生成
```bash
# 从文件读取 prompts
jimeng batch generate \
  --prompts ./prompts.txt \
  --type video \
  --output ./output/
```

---

## 📦 输出格式

| 类型 | 格式 | 分辨率 | 时长 |
|------|------|--------|------|
| 视频 | MP4 | 720p/1080p/4K | 5-60 秒 |
| 图片 | PNG/JPG | 1K/2K/4K | - |

---

## 🔗 相关链接

- **官网**: https://jimeng.jianying.com
- **文档**: https://jimeng.jianying.com/docs
- **GitHub**: (待补充)
- **模型**: Seedance 2.0 (字节自研)

---

## ⚠️  注意事项

1. **需要登录**: 首次使用需登录即梦账号
2. **API 限额**: 免费用户有生成次数限制
3. **网络要求**: 需要稳定网络连接
4. **内容审核**: 生成内容需符合平台规范

---

## 🚀 太一集成场景

### 山木内容创作
```python
# 视频脚本自动生成视频
from skills.jimeng_cli.scripts.video_generator import VideoGenerator

generator = VideoGenerator()
video_path = generator.generate_from_script("scripts/video_script.md")
```

### 社交媒体自动化
```bash
# 批量生成小红书视频素材
jimeng batch generate \
  --prompts ./xiaohongshu_prompts.txt \
  --type video \
  --output ./social-media/xiaohongshu/
```

---

*创建：2026-04-06 09:22 | 太一 AGI*  
*状态：🟡 等待安装批准*
