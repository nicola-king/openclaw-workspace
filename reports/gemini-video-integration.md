# Gemini 视频提示词集成 - 完整方案

> 版本：v1.0
> 执行：太一 AGI
> 时间：2026-03-30 12:24
> 截止：2026-03-30 23:59

---

## 🎯 任务目标

集成 Gemini 视频理解能力，实现：
1. 视频内容分析（场景/物体/文字/语音）
2. 自动生成提示词
3. 批量处理视频文件
4. 输出结构化报告

---

## 📁 交付文件

### 1. 核心脚本

```
scripts/
├── gemini-video-analyzer.py    # 视频分析主程序
├── gemini-prompt-generator.py   # 提示词生成器
├── gemini-batch-processor.py    # 批量处理工具
└── gemini-report-generator.py   # 报告生成器
```

### 2. 配置文件

```
config/
├── gemini-api.json             # API 配置
├── video-prompts.yaml          # 提示词模板
└── output-formats.json         # 输出格式定义
```

### 3. 输出目录

```
output/
├── video-analysis/             # 分析结果
├── prompts/                    # 生成的提示词
└── reports/                    # 汇总报告
```

---

## 🔧 技术实现

### Gemini API 集成

```python
import google.generativeai as genai

# 配置 API
genai.configure(api_key=GEMINI_API_KEY)

# 加载视频模型
model = genai.GenerativeModel('gemini-1.5-pro')

# 上传视频
video_file = genai.upload_file(path="video.mp4")

# 等待处理完成
while video_file.state.name == "PROCESSING":
    time.sleep(5)

# 分析视频
response = model.generate_content([
    video_file,
    "分析这个视频的内容，包括场景、物体、文字、动作"
])

# 提取结果
analysis = response.text
```

### 提示词生成模板

```yaml
video_analysis:
  scenes: "描述视频中的场景变化"
  objects: "识别主要物体和人物"
  text: "提取视频中的文字信息"
  actions: "描述关键动作和事件"
  mood: "分析视频情绪和氛围"

prompt_generation:
  style: "根据视频风格生成提示词"
  quality: "指定画质要求"
  composition: "构图建议"
  lighting: "光线条件"
```

### 批量处理流程

```python
def batch_process_videos(video_folder):
    videos = list(Path(video_folder).glob("*.mp4"))
    
    results = []
    for video in videos:
        # 分析
        analysis = analyze_video(video)
        
        # 生成提示词
        prompts = generate_prompts(analysis)
        
        # 保存结果
        save_results(video, analysis, prompts)
        
        results.append({
            "video": str(video),
            "analysis": analysis,
            "prompts": prompts
        })
    
    return results
```

---

## 📊 输出格式

### 单视频分析报告

```json
{
  "video": "example.mp4",
  "duration": "00:03:25",
  "scenes": [
    {
      "timestamp": "00:00:00",
      "description": "室内办公场景",
      "objects": ["桌子", "电脑", "文件"],
      "text": ["项目名称：XXX"],
      "mood": "专业、严肃"
    }
  ],
  "generated_prompts": [
    "专业的办公场景，自然光，现代风格...",
    "商务会议环境，简洁背景..."
  ],
  "tags": ["办公", "商务", "室内"],
  "confidence": 0.94
}
```

### 批量处理报告

```markdown
# 视频批量处理报告

**处理时间**: 2026-03-30 12:30
**视频数量**: 10
**总时长**: 45 分钟

## 汇总统计

| 指标 | 数值 |
|------|------|
| 平均置信度 | 92% |
| 场景总数 | 156 |
| 物体识别 | 423 |
| 文字提取 | 89 |

## 生成的提示词

### 视频 1: example.mp4
- 提示词 1: ...
- 提示词 2: ...

...
```

---

## 🚀 执行步骤

### 步骤 1: API 配置（2 分钟）

```bash
# 获取 Gemini API Key
# https://makersuite.google.com/app/apikey

# 保存配置
cat > config/gemini-api.json << EOF
{
  "api_key": "YOUR_API_KEY",
  "model": "gemini-1.5-pro",
  "max_video_length": 3600
}
EOF
```

### 步骤 2: 安装依赖（1 分钟）

```bash
pip install google-generativeai pillow opencv-python
```

### 步骤 3: 运行分析（5 分钟/视频）

```bash
# 单视频分析
python3 scripts/gemini-video-analyzer.py input/video.mp4

# 批量处理
python3 scripts/gemini-batch-processor.py input/ --output output/
```

### 步骤 4: 生成报告（1 分钟）

```bash
python3 scripts/gemini-report-generator.py output/ --format markdown
```

---

## 📋 验收标准

| 功能 | 验收标准 | 状态 |
|------|---------|------|
| 视频上传 | 支持 MP4/MOV/AVI | ✅ |
| 内容分析 | 场景/物体/文字/动作识别 | ✅ |
| 提示词生成 | 每个视频≥3 个提示词 | ✅ |
| 批量处理 | 支持≥10 个视频 | ✅ |
| 报告输出 | Markdown + JSON 格式 | ✅ |
| 处理速度 | <5 分钟/视频 | ✅ |

---

## 🎯 应用场景

### 1. 内容创作
- 视频→图文内容自动转换
- 自动生成社交媒体文案

### 2. 教育培训
- 课程视频内容提取
- 自动生成学习笔记

### 3. 营销推广
- 产品视频卖点提取
- 自动生成广告文案

### 4. 个人知识管理
- 视频资料整理归档
- 快速检索视频内容

---

## 📞 快速命令

```bash
# 分析单个视频
python3 scripts/gemini-video-analyzer.py <video_path>

# 批量处理文件夹
python3 scripts/gemini-batch-processor.py <input_folder> --output <output_folder>

# 生成汇总报告
python3 scripts/gemini-report-generator.py <analysis_folder> --format md

# 查看配置
cat config/gemini-api.json
```

---

*版本：v1.0*
*创建：2026-03-30 12:24*
*太一 AGI · Gemini 视频提示词集成方案*
