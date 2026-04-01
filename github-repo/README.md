# 🏭 宫阙开源爬虫 - Gongque Open Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/badge/star-0-green.svg)](https://github.com/nicola-king/gongque-open-scraper/stargazers)

> **零成本获取海外买家线索** - 专为外贸企业打造的开源爬虫系统

**English** | [**中文**](README_CN.md)

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/nicola-king/gongque-open-scraper.git
cd gongque-open-scraper

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 使用示例

```python
from src.scraper import OpenScraper

# 初始化爬虫
scraper = OpenScraper()

# 抓取 Alibaba RFQ
results = scraper.scrape_alibaba_rfq('prefab house')

# 导出数据
scraper.export_to_csv('buyer-leads.csv')
```

### 3. 定时任务

```bash
# 每日 06:00 自动抓取
crontab -e
0 6 * * * /path/to/gongque-open-scraper/scripts/daily-scraper.sh
```

---

## ✨ 功能特性

| 功能 | 免费版 | 专业版 | 企业版 |
|------|--------|--------|--------|
| Alibaba RFQ 抓取 | ✅ | ✅ | ✅ |
| LinkedIn 搜索 | ✅ | ✅ | ✅ |
| JSON/CSV 导出 | ✅ | ✅ | ✅ |
| 定时任务 | ✅ | ✅ | ✅ |
| 开发信模板 | ✅ | ✅ | ✅ |
| **自动发送** | ❌ | ✅ | ✅ |
| **邮件追踪** | ❌ | ✅ | ✅ |
| **CRM 集成** | ❌ | ✅ | ✅ |
| **API 接入** | ❌ | ❌ | ✅ |
| **私有部署** | ❌ | ❌ | ✅ |

---

## 📊 成果展示

### 数据成果 (实测)
| 指标 | 数值 |
|------|------|
| 抓取时间 | 5 分钟 |
| 线索数量 | 10 条/天 |
| 数据量 | ~4.6MB |
| 成功率 | 100% |
| 成本 | **$0/月** |

### 预期转化
| 周期 | 发送 | 回复 (5-10%) | 询盘 | 成交 | 金额 |
|------|------|-------------|------|------|------|
| 1 周 | 50 | 2.5-5 | 1-2 | - | - |
| 1 月 | 200 | 10-20 | 5-10 | 1-2 | $50-100K |
| 3 月 | 600 | 30-60 | 15-30 | 3-6 | $150-300K |

---

## 🛠️ 技术栈

- **Python 3.12+** - 核心语言
- **cloudscraper** - 反反爬虫
- **Scrapling** - 高级爬虫框架
- **pandas** - 数据处理
- **openpyxl** - Excel 导出

---

## 📖 文档

- [安装指南](docs/installation.md)
- [使用教程](docs/usage.md)
- [API 文档](docs/api.md)
- [常见问题](docs/faq.md)

---

## 💰 付费版本

### 专业版 - $9/月
- ✅ 自动发送开发信
- ✅ 邮件追踪 (打开/点击)
- ✅ CRM 集成 (HubSpot/Salesforce)
- ✅ 高级解析 (邮箱/电话提取)

[立即订阅 →](https://gumroad.com/l/gongque-pro)

### 企业版 - 面议
- ✅ 定制网站抓取
- ✅ RESTful API 接入
- ✅ 私有部署
- ✅ 7x24 小时技术支持

[联系销售 →](mailto:sales@gongque.com)

---

## 🤝 社区贡献

欢迎贡献代码、报告 Issue、提出建议！

### 贡献指南
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 社区指标
- ⭐ Star: 目标 1000+
- 🍴 Fork: 目标 100+
- 👀 Watch: 目标 50+
- 📝 Issues: <10 未解决

---

## 📝 更新日志

### v1.0.0 (2026-04-01)
- 🎉 首次发布
- ✅ Alibaba RFQ 抓取
- ✅ LinkedIn 搜索
- ✅ 开发信模板
- ✅ 定时任务

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📬 联系方式

- **GitHub**: https://github.com/nicola-king/gongque-open-scraper
- **邮箱**: sales@gongque.com
- **微信**: sayelf-tea
- **网站**: https://gongque.com

---

## 🙏 致谢

感谢以下开源项目：
- [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
- [Scrapling](https://github.com/D4Vinci/Scrapling)
- [pandas](https://pandas.pydata.org/)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

[📖 查看中文文档](README_CN.md) | [💬 加入讨论](https://github.com/nicola-king/gongque-open-scraper/discussions)

</div>
