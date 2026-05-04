---
name: domestic-travel-agent
version: 2.0.0
description: 太一国内旅游探路者 - 短游/深度游/团体/商家信息验证
category: travel
tags: ['travel', 'tourism', 'domestic', 'hotels', 'restaurants', 'attractions', 'local-services']
author: 太一 AGI
created: 2026-05-04
updated: 2026-05-04
status: active
---

# 太一国内旅游探路者 v2.0

> 个人/团体/商家 三端通用 | 所有信息附带验证链接

## 场景

| 场景 | 命令 | 适用 |
|------|------|------|
| 短游 | `short --city 北京 --days 3` | 1-3天极速游 |
| 深度游 | `deep --city 成都 --days 7` | 5-14天沉浸游 |
| 团体 | `group --city 三亚 --members 10` | 团建/会议/考察 |
| API | `serve --port 8765` | REST+MCP服务 |

## 信息类型 (所有含 verification_links)

| 类型 | 内容 | 验证方式 |
|------|------|---------|
| hotels | 地址/电话/网址/图片 | Google Maps+官网+OTA |
| restaurants | 地址/电话/特色菜/图片 | Google Maps+点评 |
| attractions | 电话/地址/网址/票价 | 官网+Google Maps |
| services | 导游实名/租车电话 | 工商+身份验证 |

## 12个城市就绪

北京/上海/广州/深圳/成都/重庆/杭州/西安/昆明/桂林/三亚/丽江
