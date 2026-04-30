# 山木 AI 生图配置指南

## 🚀 快速开始

### 1. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/apikey)
2. 登录 Google 账号
3. 点击 "Create API Key"
4. 复制 API Key（格式：`AIzaSy...`）

### 2. 配置环境变量

**方式 A：临时配置（测试用）**
```bash
export GEMINI_API_KEY="你的 API Key"
```

**方式 B：永久配置（推荐）**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export GEMINI_API_KEY="你的 API Key"' >> ~/.bashrc
source ~/.bashrc
```

**方式 C：写入配置文件**
```bash
# 创建配置文件
echo "GEMINI_API_KEY=你的 API Key" > ~/.openclaw/workspace/skills/shanmu/.env
```

### 3. 测试运行

```bash
# 测试模式（生成示例图片）
cd ~/.openclaw/workspace/skills/shanmu
bash ai-image-gen.sh --test

# 自定义主题
bash ai-image-gen.sh "AI 量化交易策略海报"

# 自动模式（从公众号文章提取主题）
bash ai-image-gen.sh
```

## 📁 目录结构

```
skills/shanmu/
├── ai-image-gen.sh          # AI 生图主脚本
├── wechat-article-collect.sh # 公众号采集脚本
└── prompt-library/          # 提示词库
    ├── 赛博朋克.txt
    ├── 3D 插画.txt
    ├── 写实摄影.txt
    ├── 极简主义.txt
    ├── 国潮风.txt
    └── 水彩画.txt
```

## 🎨 输出内容

```
content/
├── ai-images/               # 生成的图片
│   ├── test_demo_20260326.png
│   └── schemes_主题_20260326.md  # 方案报告
└── prompt-library/          # 提示词库
```

## ⏰ 定时任务

每天 09:30 自动执行（公众号采集后 30 分钟）：

```cron
30 9 * * * /home/nicola/.openclaw/workspace/skills/shanmu/ai-image-gen.sh
```

## 🔧 自定义提示词

编辑 `prompt-library/风格名.txt`：

```markdown
# 风格名 风格提示词模板

## 核心提示词
- 主体：{subject}
- 风格：风格名
- 色调：{color_scheme}
- 构图：{composition}
- 光影：{lighting}

## 质量词
8k, ultra detailed, professional, masterpiece, best quality

## 负面提示词
low quality, worst quality, blurry, distorted, ugly
```

## 📊 工作流

```
公众号采集 (09:00)
    ↓
提取文章主题
    ↓
AI 生图 (09:30)
    ↓
生成 3 套方案（赛博朋克/3D 插画/写实摄影）
    ↓
输出到 content/ai-images/
    ↓
公众号文章配图完成
```

## ⚠️ 注意事项

1. **API 配额**: Gemini 免费额度有限，注意监控用量
2. **图片尺寸**: 默认 16:9，可修改脚本中的 `aspectRatio`
3. **网络要求**: 需要能访问 Google API（可能需要代理）
4. **依赖检查**: 确保已安装 `curl` 和 `jq`

## 🛠️ 故障排除

| 问题 | 解决方案 |
|------|---------|
| GEMINI_API_KEY 未配置 | 按上述方式配置环境变量 |
| 图片生成失败 | 检查网络连接和 API Key 有效性 |
| 占位图无法生成 | 安装 ImageMagick: `sudo apt install imagemagick` |
| JSON 解析错误 | 确保已安装 jq: `sudo apt install jq` |

---

*最后更新：2026-03-26 | 版本：v1.0 | 山木*
