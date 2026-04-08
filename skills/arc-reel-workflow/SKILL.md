---
skill: arc-reel-workflow
version: 1.0.0
author: 太一 AGI
created: 2026-04-06
status: active
tags: ['视频，短剧，AI 生成，角色一致性，剪映']
category: general
---



# ArcReel 短剧工作流 Skill

> 小说→短视频全自动生成

---

## 📊 功能概述

将小说/剧本自动转换为短视频:
- 剧本拆分
- 角色设计 (一致性保证)
- 分镜绘制
- 视频生成
- 剪映草稿导出

---

## 🛠️ 技术栈

| 组件 | 用途 | 状态 |
|------|------|------|
| ArcReel | 视频生成框架 | ✅ 已克隆 |
| Veo 3.1 | Google 视频模型 | 🟡 API 待配置 |
| Seedance | 字节视频模型 | 🟡 待集成 |
| Grok | xAI 视频模型 | 🟡 待集成 |
| 剪映 | 后期编辑 | ✅ 草稿导出支持 |

---

## 🔧 核心功能

### 1. 剧本拆分
```python
from arc_reel import ScriptParser

parser = ScriptParser()

# 解析小说/剧本
scenes = parser.parse("novel.txt")

# 输出：场景列表
# [
#   {"scene": 1, "location": "咖啡厅", "characters": ["主角 A", "配角 B"]},
#   {"scene": 2, "location": "办公室", "characters": ["主角 A"]}
# ]
```

### 2. 角色设计 (一致性保证)
```python
from arc_reel import CharacterDesigner

designer = CharacterDesigner()

# 设计角色
character = await designer.create({
    "name": "主角 A",
    "description": "25 岁男性，黑色短发，蓝色眼睛",
    "personality": "冷静/聪明"
})

# 生成参考图
reference_images = await designer.generate_references(
    character,
    count=5
)

# 一致性检查
consistency_score = await designer.check_consistency(
    character,
    generated_images
)
# 输出：0.95 (95% 一致性)
```

### 3. 分镜绘制
```python
from arc_reel import StoryboardGenerator

generator = StoryboardGenerator()

storyboard = await generator.create(
    scene=scene_1,
    character_designs=[character_a, character_b],
    style="写实电影风"
)
```

### 4. 视频生成 (多模型切换)
```python
from arc_reel import VideoGenerator

generator = VideoGenerator()

# 选择模型
generator.set_model("veo31")  # 或 seedance/grok/sora2

# 生成视频
video = await generator.generate(
    storyboard=storyboard,
    duration=30,  # 秒
    resolution="1080p"
)
```

### 5. 剪映草稿导出
```python
from arc_reel import CapCutExporter

exporter = CapCutExporter()

# 导出剪映草稿
draft_path = await exporter.export(
    video=video,
    subtitles=subtitles,
    background_music="bgm.mp3"
)

# 在剪映中打开继续编辑
await exporter.open_in_capcut(draft_path)
```

---

## 📋 使用示例

### 场景 1: 小说转短剧
```python
from arc_reel_workflow import NovelToVideo

workflow = NovelToVideo()

# 上传小说
novel = "我的 AI 管家.txt"

# 全自动生成
result = await workflow.generate(
    novel_path=novel,
    output_dir="output/",
    model="veo31",
    episodes=10  # 生成 10 集
)

# 输出：10 个视频文件 + 剪映草稿
```

### 场景 2: 角色一致性保证
```python
from arc_reel import ConsistencyChecker

checker = ConsistencyChecker()

# 跨场景一致性检查
scores = await checker.check_across_scenes(
    character="主角 A",
    scenes=[1, 2, 3, 4, 5]
)

# 输出：{"avg_score": 0.94, "min_score": 0.91}

if scores["avg_score"] < 0.9:
    # 重新生成低一致性场景
    await regenerate_low_consistency_scenes()
```

### 场景 3: 批量生成
```python
# 批量处理多个剧本
scripts = ["script1.txt", "script2.txt", "script3.txt"]

for script in scripts:
    await workflow.generate(
        novel_path=script,
        output_dir=f"output/{script}",
        parallel=True  # 并行生成
    )
```

---

## 🎯 山木 Bot 集成

```python
# 山木 Bot 调用示例
async def shanmu_create_video(novel_content):
    # 1. 保存小说
    novel_path = save_temp(novel_content)
    
    # 2. 调用 ArcReel
    video = await arc_reel.generate(novel_path)
    
    # 3. 发布到平台
    await publish_to_platforms(video)
    
    return video
```

---

## 🔗 集成文档

- 集成方案：`integrations/arcreel/shanmu_integration.py`
- 工作计划：`skills/arc-reel-workflow/PLAN.md`
- 分析报告：`reports/github-daily-deep-analysis-20260406.md`

---

## 📝 待办事项

- [ ] ArcReel Docker 部署
- [ ] 多模型 API 配置
- [ ] 角色一致性测试
- [ ] 剪映导出测试

---

*创建时间：2026-04-06 01:00 | 太一 AGI*
