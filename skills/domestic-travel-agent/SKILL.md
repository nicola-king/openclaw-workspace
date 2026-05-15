---
name: domestic-travel-agent
version: 2.0.0
description: 太一国内旅游探路者 - 短游/深度游/团体/商家信息验证
category: travel
tags: ['travel', 'tourism', 'domestic']
author: 太一 AGI
created: 2026-05-04
updated: 2026-05-04
status: active
---

# 太一国内旅游探路者 v2.0

## 子Skills

| Skill | 功能 |
|------|------|
| **intelligence-agent** | 综合情报引擎: 平台搜索/权重评分/性价比排序/大V博主 |

## 场景

| 场景 | 命令 | 适用 |
|------|------|------|
| 短游 | `short --city 北京 --days 3` | 1-3天极速游 |
| 深度游 | `deep --city 成都 --days 7` | 5-14天沉浸游 |
| 团体 | `group --city 三亚 --members 10` | 团建/会议/考察 |
| API | `serve --port 8765` | REST+MCP服务 |

## 输出规范（强制）

### 语言
- 所有输出文件（PDF/Word/HTML）均使用**中文**生成
- 中文字体优先使用系统可用字体（DroidSansFallbackFull/NotoSansCJK等），必须确保中文正确渲染
- 表头、正文、提示语全部使用中文
- 英文数字/符号正常使用不受限

### PDF生成规范
- 报告标题：中文
- 表格表头：中文
- 字段内容：中文
- 字体注册：优先注册系统DroidSansFallbackFull.ttf，失败则查找任意支持中文的TTF字体
- 失败回退：找不到中文字体时报错阻止生成，不输出无中文的PDF

---

## 10核心模块

1. planner 行程规划 | 2. weather_safety 天气预警
3. intelligence 情报引擎 | 4. hotels 真实酒店
5. restaurants 真实餐馆 | 6. attractions 真实景点
7. local_services 导游租车 | 8. destination_guide 风俗法律
9. transport 交通票务 | 10. savings_engine 省钱技能

## 5城市就绪

北京/上海/成都/重庆/三亚

> 所有信息附带 verification_links 验证链接
