# Content Creator 内容创作引擎

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P0

---

## 📋 概述

内容创作引擎提供完整的内容生产工作流：排期 → 优化 → 发布 → 生成一体化。支持小红书、微信公众号、Twitter 等多平台。

---

## 🏗️ 架构

```
content-creator/
├── __init__.py              # 主入口，ContentCreator 类
├── SKILL.md                 # 技能定义
├── scheduler/               # 排期模块
│   └── scheduler.py         # 内容排期管理
├── optimizer/               # 优化模块
│   └── optimizer.py         # 爆款标题/文案生成
├── publisher/               # 发布模块
│   └── publisher.py         # 多平台发布
└── generator/               # 生成模块
    └── generator.py         # AI 内容生成
```

---

## 🚀 快速开始

### 初始化

```python
from skills.content_creator import ContentCreator

cc = ContentCreator()
```

### 内容排期

```python
# 添加发布任务
cc.scheduler.add_task(
    platform='xiaohongshu',
    content_type='note',
    publish_time='2026-04-07 21:00',
    content={
        'title': 'AI 工具推荐',
        'body': '内容正文...'
    }
)

# 查看排期
schedule = cc.scheduler.get_schedule('2026-04-07')

# 取消任务
cc.scheduler.cancel_task(task_id)
```

### 内容优化

```python
# 生成爆款标题
titles = cc.optimizer.generate_viral_titles(
    topic='AI 工具',
    platform='xiaohongshu',
    count=10
)

# 优化文案
optimized = cc.optimizer.optimize_content(
    original_text='原始文案...',
    style='emoji',  # emoji | formal | casual
    platform='xiaohongshu'
)

# 生成标签
tags = cc.optimizer.generate_tags('AI 工具 效率 办公')
```

### 内容发布

```python
# 发布到微信
result = cc.publisher.publish(
    platform='wechat',
    title='文章标题',
    content='文章内容',
    cover_image='path/to/cover.jpg'
)

# 发布到小红书
result = cc.publisher.publish(
    platform='xiaohongshu',
    title='笔记标题',
    content='笔记内容',
    images=['img1.jpg', 'img2.jpg']
)

# 发布到 Twitter
result = cc.publisher.publish(
    platform='twitter',
    content='推文内容',
    thread=True  # 是否线程
)
```

### AI 内容生成

```python
# 根据主题生成完整内容
content = cc.generator.generate(
    topic='AI 工具推荐',
    platform='xiaohongshu',
    tone='friendly',  # friendly | professional | humorous
    length='medium'  # short | medium | long
)

# 根据大纲生成
content = cc.generator.generate_from_outline(
    outline=['引言', '主体 1', '主体 2', '总结'],
    topic='AI 工具'
)
```

---

## 📱 支持平台

| 平台 | 状态 | 功能 |
|------|------|------|
| **小红书** | ✅ | 笔记/图文/视频 |
| **微信公众号** | ✅ | 文章/图文 |
| **Twitter/X** | ✅ | 推文/线程 |
| **Discord** | ✅ | 消息/嵌入 |
| **WhatsApp** | ✅ | 消息/广播 |

---

## 🎨 内容风格

### 小红书风格

- ✅ Emoji 丰富
- ✅ 分段清晰
- ✅ 标签优化
- ✅ 爆款标题

### 公众号风格

- ✅ 深度内容
- ✅ 结构化
- ✅ 专业术语
- ✅ 配图建议

### Twitter 风格

- ✅ 简洁有力
- ✅ 线程支持
- ✅ Hashtag 优化
- ✅ 互动引导

---

## ⚠️ 注意事项

### 发布前检查

- ✅ 敏感词检测
- ✅ 内容审核
- ✅ 图片版权
- ✅ 链接有效性

### 速率限制

| 平台 | 限制 | 建议 |
|------|------|------|
| 小红书 | 5 条/小时 | 间隔 12 分钟 |
| 公众号 | 1 条/天 | 固定时间 |
| Twitter | 10 条/小时 | 间隔 6 分钟 |

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/content_creator/tests/ -v

# 测试标题生成
python3 -m pytest skills/content_creator/tests/test_optimizer.py -v

# 测试发布（模拟）
python3 -m pytest skills/content_creator/tests/test_publisher.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [内容创作指南](../constitution/content/CONTENT-GUIDE.md)

---

*维护：太一 AGI | Content Creator v2.0*
