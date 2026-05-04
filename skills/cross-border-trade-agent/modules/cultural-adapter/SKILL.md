# cultural-adapter Skill

## 描述
跨文化本地化引擎：文化适配·多语言内容·本地化策略·山木内容蒸馏

## 蒸馏来源
- 山木内容系统：小红书/微信公众号/YouTube/Facebook 内容生成
- 太一系统：多语言客服 + 社交媒体矩阵
- GEO 推广：本地化权威构建
- 流量优先策略：本地化引流

## 独立运行
```bash
python core.py --task localize --content "产品介绍" --target_language "en" --market "Australia"
```

## 依赖
- cross-border-core: ^10.0.0
- geo-outbound: ^10.0.0

## 核心能力

### 1. 文化适配
- 目标市场文化特征分析
- 禁忌/偏好识别
- 颜色/符号/数字文化含义
- 商务礼仪差异

### 2. 多语言内容
- 自动翻译 + 文化适配
- 本地化文案生成
- 多语言 SEO 优化
- 多语言社媒内容

### 3. 本地化策略
- 市场进入文化策略
- 品牌本地化定位
- 营销渠道本地化
- 客服本地化

### 4. 内容矩阵
- LinkedIn 专业内容
- Facebook 社群内容
- YouTube 视频脚本
- 微信公众号内容（反向）

## API

### 输入
```json
{
  "task": "localize",
  "content": "折叠房屋产品介绍",
  "target_language": "en",
  "market": "Australia",
  "platform": "linkedin"
}
```

### 输出
```json
{
  "status": "success",
  "localized_content": "...",
  "cultural_notes": {...},
  "platform_optimized": true,
  "seo_keywords": [...],
  "engagement_score": 85
}
```

## 配置
```json
{
  "localization": {
    "enabled": true,
    "auto_translate": true,
    "cultural_check": true
  },
  "platforms": {
    "linkedin": {"tone": "professional", "length": "medium"},
    "facebook": {"tone": "friendly", "length": "short"},
    "youtube": {"tone": "engaging", "length": "long"},
    "wechat": {"tone": "informative", "length": "medium"}
  }
}
```

## 使用示例
```python
from core import CulturalAdapter

adapter = CulturalAdapter(config_path="config.json")

# 内容本地化
result = adapter.localize(
    content="折叠房屋产品介绍",
    target_language="en",
    market="Australia",
    platform="linkedin"
)

# 文化分析
culture = adapter.analyze_culture(
    market="Australia",
    industry="construction"
)

# 多语言内容生成
contents = adapter.generate_multilingual(
    content="产品发布",
    languages=["en", "de", "fr", "ja"]
)
```
