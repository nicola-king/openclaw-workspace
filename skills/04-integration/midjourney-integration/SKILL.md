---
name: midjourney-integration
version: 1.0.0
description: Midjourney 集成 - AI 绘画/图像生成/Gemini 分析
category: content
tags: ['midjourney', 'ai-art', 'image-generation', 'gemini-analysis', 'content-creation']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P1
---

# 🎨 Midjourney Integration - MJ 集成 v1.0

> **状态**: ✅ 新创建 | **版本**: 1.0.0 | **创建时间**: 2026-04-08  
> **核心功能**: AI 绘画/图像生成/Gemini 分析/自动保存

---

## 🎯 核心功能

### 1. 图像生成 ✅

- 文生图 (Text-to-Image)
- 图生图 (Image-to-Image)
- 变体生成 (Variations)
- 放大 (Upscale)
- 参数定制

### 2. Discord 集成 ✅

- 自动发送提示词
- 监听生成完成
- 多频道轮询
- 自动下载图片

### 3. Gemini 分析 ✅

- 图像内容分析
- 质量评估
- 标签生成
- 优化建议

### 4. 自动保存 ✅

- 本地存储
- 元数据记录
- 分类管理
- 快速检索

---

## 📦 文件结构

```
midjourney-integration/
├── SKILL.md (本文档)
├── mj_bot.py (MJ 机器人核心)
├── mj_generator.py (图像生成器)
├── config/
│   └── mj_config.json (配置文件)
├── services/
│   ├── discord_service.py (Discord 服务)
│   ├── mj_api.py (MJ API)
│   └── gemini_analyzer.py (Gemini 分析)
├── storage/
│   ├── local_storage.py (本地存储)
│   └── metadata_db.py (元数据数据库)
└── tests/
    └── test_mj.py (测试)
```

---

## 🔐 配置说明

### 现有配置

**文件位置**: `/home/nicola/.openclaw/workspace-taiyi/config/mj-integration.json`

**已配置内容**:
```json
{
  "userId": "785428c1-08d4-400b-b75b-8f92eec169a4",
  "discordServerId": "1490580943210020996",
  "discordChannelId": "1100294922176827403",
  "botToken": "已配置",
  "defaultModel": "midjourney-6",
  "defaultAspectRatio": "16:9"
}
```

### 环境变量

```bash
# Discord Bot Token
export DISCORD_BOT_TOKEN="your_token"

# Midjourney User ID
export MJ_USER_ID="your_user_id"

# Gemini API Key
export GEMINI_API_KEY="your_api_key"
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.midjourney_integration.mj_bot import MJBot

# 初始化
mj = MJBot()

# 生成图像
result = mj.generate(
    prompt="一只可爱的猫咪，赛博朋克风格",
    aspect_ratio="16:9",
    quality="high"
)

# 获取结果
print(f"图像 URL: {result.image_url}")
print(f"保存路径：{result.local_path}")

# Gemini 分析
analysis = mj.analyze_with_gemini(result.local_path)
print(f"分析结果：{analysis}")
```

### 命令行用法

```bash
# 生成图像
python3 mj_bot.py --prompt "未来城市，霓虹灯，赛博朋克"

# 批量生成
python3 mj_bot.py --batch prompts.txt --count 10

# 分析图像
python3 mj_bot.py --analyze image.png
```

---

## 📊 生成配置

### 默认参数

```yaml
模型：midjourney-6
比例：16:9
质量：high
自动放大：true
自动保存：true
频道策略：round-robin
```

### 支持参数

```yaml
比例选项:
  - 1:1 (正方形)
  - 16:9 (宽屏)
  - 9:16 (竖屏)
  - 4:3 (标准)
  - 3:4 (肖像)

质量选项:
  - low (快速)
  - medium (平衡)
  - high (高质量)

风格选项:
  - raw (原始)
  - artistic (艺术)
  - realistic (写实)
  - anime (动漫)
```

---

## 🎨 提示词模板

### 基础模板

```
[主体描述]，[风格]，[光照]，[构图]，[参数]

示例:
一只可爱的猫咪，赛博朋克风格，霓虹灯光，中心构图，--ar 16:9 --v 6
```

### 高级模板

```
/imagine prompt: [主体] + [细节] + [环境] + [风格] + [技术] --ar [比例] --v [版本]

示例:
/imagine prompt: 未来城市夜景，高楼大厦，飞行汽车，霓虹灯，赛博朋克风格，数字艺术，细节丰富 --ar 16:9 --v 6 --q 2
```

---

## 📁 存储管理

### 本地存储路径

```
~/.openclaw/workspace-taiyi/media/midjourney/
├── 2026-04/
│   ├── 20260408_001.png
│   ├── 20260408_001.json (元数据)
│   ├── 20260408_002.png
│   └── 20260408_002.json
├── 2026-05/
└── index.json (索引)
```

### 元数据格式

```json
{
  "id": "20260408_001",
  "prompt": "一只可爱的猫咪，赛博朋克风格",
  "model": "midjourney-6",
  "aspect_ratio": "16:9",
  "quality": "high",
  "created_at": "2026-04-08T16:15:00+08:00",
  "image_url": "https://cdn.midjourney.com/xxx.png",
  "local_path": "~/.openclaw/workspace-taiyi/media/midjourney/2026-04/20260408_001.png",
  "gemini_analysis": {
    "tags": ["猫咪", "赛博朋克", "霓虹灯"],
    "quality_score": 0.95,
    "description": "一张高质量的赛博朋克风格猫咪图像..."
  }
}
```

---

## 🔧 故障排查

### Q: 无法连接 Discord？

**检查**:
1. Bot Token 是否正确
2. 服务器 ID 是否正确
3. 机器人是否已邀请到服务器

### Q: 生成失败？

**检查**:
1. 提示词是否违规
2. 频道是否有权限
3. 速率限制是否触发

### Q: Gemini 分析失败？

**检查**:
1. Gemini API Key 是否有效
2. 图像文件是否存在
3. 网络连接是否正常

---

## ⚠️ 注意事项

### 1. 速率限制

```yaml
Midjourney 限制:
  - 免费账户：约 200 张/月
  - 标准账户：约 1000 张/月
  - 专业账户：无限生成
  
建议:
  - 监控使用量
  - 批量生成前检查额度
  - 失败自动重试 (最多 3 次)
```

### 2. 内容规范

```yaml
禁止内容:
  - 暴力/血腥
  - 成人内容
  - 侵权内容
  - 政治敏感
  
建议:
  - 使用安全提示词
  - 自动过滤敏感词
  - 违规自动跳过
```

### 3. 版权说明

```yaml
版权归属:
  - 付费账户：用户拥有版权
  - 免费账户：CC BY-NC 4.0
  
建议:
  - 商业用途使用付费账户
  - 保留生成记录
  - 注明 AI 生成
```

---

## 📚 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `SKILL.md` | 本文档 | `skills/midjourney-integration/` |
| `mj_bot.py` | 机器人核心 | `skills/midjourney-integration/` |
| `mj-integration.json` | 配置文件 | `workspace-taiyi/config/` |

---

## 🎯 下一步

- [ ] 创建 `mj_bot.py` 核心实现
- [ ] 创建 `mj_generator.py` 生成器
- [ ] 创建 Discord 服务模块
- [ ] 创建 Gemini 分析模块
- [ ] 创建本地存储模块
- [ ] 测试图像生成流程
- [ ] 集成到太一 AGI 系统

---

*版本：1.0.0 | 创建时间：2026-04-08 | 状态：✅ 已创建*
