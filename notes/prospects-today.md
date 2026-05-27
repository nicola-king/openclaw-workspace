# 潜客搜寻报告 | 2026-05-27

## 概览
- **日期**: 2026-05-27 10:10
- **模块**: 跨境-潜客自动搜寻（Cron 定时任务）
- **数据库总潜客数**: 140

## 搜索详情
| 产品 | 市场 | 结果 |
|------|------|------|
| Smart Water Bottle | USA | fallback (搜索引擎被反爬拦截) |
| Smart Water Bottle | UK | fallback |
| Yoga Mat | Australia | fallback |
| LED Desk Lamp | USA | fallback |
| steel structure house | Australia | fallback |

## Buyer-Intel 验证
- **总记录**: 17
- **已验证**: 17
- **待审核**: 0

## 数据库状态
- **现存潜客**: 140 家

## ⚠️ 已知问题
1. **共享搜索 Agent 路径不匹配**: `guike-zhilu/core.py` 引用 `shared_search_service.py`，实际文件为 `core.py`
2. **搜索引擎被反爬拦截**: Google/DuckDuckGo/Bing 均返回 CAPTCHA 或空结果
3. **SSRF 保护**: cloudscraper 内部请求被 SSRF 保护拦截（127.0.0.1 redirect）

## 建议修复
1. `ln -s core.py shared_search_service.py` 在 shared-search-agent 目录
2. 配置代理白名单绕过 SSRF 保护
3. 使用 web_fetch 工具或 API 密钥方式进行搜索

---
*生成时间: 2026-05-27 10:10:06*
