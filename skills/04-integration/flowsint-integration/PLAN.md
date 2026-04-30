# Flowsint OSINT 调查平台集成计划

**创建时间**: 2026-03-30 22:55  
**来源**: GitHub - reconurge/flowsint  
**状态**: 🟢 克隆完成，分析中

---

## 📊 Flowsint 核心能力

**技术栈**: FastAPI + Neo4j + PostgreSQL + Celery  
**部署**: Docker 一键部署  
**定位**: 图数据库 OSINT 调查平台

**核心 Enricher**:
| 方向 | 功能 |
|------|------|
| 域名 | 子域名枚举、WHOIS、反向 DNS、历史记录、ASN 关联 |
| IP/网络 | 地理定位、ASN 查询、CIDR 枚举 |
| 社交媒体 | Malgret 用户名校平台搜索 |
| 邮箱 | 数据泄露查询、Gravatar 关联 |
| 加密货币 | 钱包交易记录、NFT 持仓 |
| 网站 | 爬虫、链接提取、Tracker 识别 |

---

## 🎯 太一集成方案

### 赋能 Bot
| Bot | 增强能力 |
|-----|---------|
| **罔两** | 数据采集增强 (域名/IP/邮箱关联) |
| **羿** | 信号追踪增强 (加密货币钱包追踪) |
| **太一** | 图谱可视化 (Neo4j 关系图) |

### 集成阶段
| 阶段 | 内容 | 时间 |
|------|------|------|
| **Phase 1** | Docker 部署测试 | 本周 |
| **Phase 2** | API 对接 (罔两/羿) | 下周 |
| **Phase 3** | 图谱可视化 | 本月 |

---

## 📋 立即执行清单

- [x] GitHub 克隆完成 ✅
- [ ] Docker 部署测试 (22:55-23:00)
- [ ] API 端点分析 (23:00-23:10)
- [ ] 罔两 Bot 集成方案 (23:10-23:20)
- [ ] 羿 Bot 集成方案 (23:20-23:30)

---

## 🔧 Docker 部署命令

```bash
cd /tmp/flowsint
docker-compose up -d
# 访问：http://localhost:8000
# API: http://localhost:8000/api/v1/
```

---

*创建：太一 AGI | 2026-03-30 22:55*
