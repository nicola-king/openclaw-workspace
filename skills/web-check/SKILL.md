---
name: web-check
version: 2.1.9
description: 🕵️ All-in-one OSINT website analyzer - 33K⭐
category: osint
tags: ['osint', 'security', 'website-analysis', 'dns', 'ssl', 'ports']
author: lissy93
created: 2026-05-28
status: active
---

# Web-Check — 网站 OSINT 分析工具

> 融合 lissy93/web-check (33K⭐, MIT)
> 原仓库：https://github.com/Lissy93/web-check

## 能力清单

| 模块 | 功能 | 对跨境贸易的价值 |
|:----:|:----|:----------------|
| 🖥️ **IP 情报** | 服务器IP、地理位置、托管商 | 验证供应商网站真实性 |
| 🔐 **SSL 证书** | 证书链、签发机构、到期时间 | 确认网站 HTTPS 合规性 |
| 🌐 **DNS 记录** | A/AAAA/CNAME/MX/NS/SPF/DKIM | 邮件安全验证 (防钓鱼) |
| 🔌 **端口扫描** | 开放端口、服务识别 | 供应商 IT 安全评估 |
| 🧩 **技术栈** | Web框架/CMS/CDN/分析工具 | 竞品技术架构分析 |
| 📡 **Trackers** | 第三方追踪器、广告联盟 | 了解竞品营销渠道 |
| 🔗 **关联域名** | 同IP托管的其他网站 | 发现关联公司/影子网站 |
| 🛡️ **安全头** | CSP/HSTS/CORS/X-Frame-Options | 网站安全等级评分 |
| 🍪 **Cookies** | Cookie 审计、第三方cookie | 隐私合规评估 |
| 📍 **位置** | 服务器物理位置 | 物流/本地化分析 |
| 📸 **截图** | 网站页面截图 | 可视化竞品分析 |
| 🌱 **碳排放** | 网站碳足迹 | 环保合规 |

## 自动触发规则

| 用户意图 | 路由到 | 输出 |
|---------|--------|------|
| "分析这个网站 XX.com" | web-check | OSINT 完整报告 |
| "XX公司网站靠谱吗" | web-check + cross-border背调 | 综合可信度评估 |
| "查竞品技术栈" | web-check tech-stack | 技术栈清单 |
| "这个域名安全吗" | web-check SSL+安全头 | 安全等级评分 |
| "XX和XX网站有关联吗" | web-check 关联域名 | 关联关系图 |
| "做供应商背景调查 XXX.com" | web-check (全模块) + 公司背调 | 供应商评估报告 |

## 使用方式

### API 服务（部署后）
```bash
# 启动服务
cd repo && yarn dev

# 单次 API 调用
curl http://localhost:3001/api/ip?host=example.com
curl http://localhost:3001/api/dns?host=example.com
curl http://localhost:3001/api/ssl?host=example.com
```

### CLI 包装器
```bash
# 完整分析
bash scripts/web-check.sh example.com

# 单模块
bash scripts/web-check.sh dns example.com
bash scripts/web-check.sh ssl example.com
```

### Python API
```python
from scripts.web_check_api import WebCheck
wc = WebCheck(base_url="http://localhost:3001")
result = wc.analyze("example.com")  # 完整分析
tech = wc.tech_stack("example.com") # 仅技术栈
```

## 安装状态

| 组件 | 状态 |
|:----|:----:|
| 源码克隆 | ✅ repo/ |
| npm 依赖 | ❌ 未安装 |
| 本地服务 | ❌ 未运行 |
| CLI 包装器 | ✅ scripts/web-check.sh |
| Python API | ✅ scripts/web_check_api.py |

## 太一集成

### Agent 调度
智能代理调度系统自动识别网站分析需求 → 调用 web-check → 结果注入上下文

### 跨境背调
web-check 的 OSINT 数据直接输入到 cross-border 背景检查模块：
```
背调 "XX公司" -w "xx.com"
  → 公司评级 A/B/C/D（现有）
  + 网站安全评分（web-check）
  + 技术栈分析（web-check）
  + 关联域名（web-check）
  = 综合供应商评估报告
```

### 竞品监控
web-check 定期扫描竞品网站变更 → 触发竞品动态报告
