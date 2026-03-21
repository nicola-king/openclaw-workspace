---
name: originality-check
tier: 2
trigger: 搜索/发售验证/能力涌现
enabled: true
depends: []
---
# 独创性验证协议 · 全球版

任何新 Skill、新 Agent、新产品发售前必须通过。

## 搜索矩阵（按顺序执行，不可跳过）

### 中文市场
- Baidu（百度）— 中文产品和实现
- Sogou（搜狗）— 补充中文覆盖
- 知网 / 万方 — 学术和研究
- 国家知识产权局（cnipa.gov.cn）— 中国专利

### 英文市场
- Bing — 全球英文覆盖
- Google — 补充搜索
- GitHub — 开源实现
- HuggingFace — AI 模型和数据集
- ProductHunt — 新产品发布
- AppStore / Google Play — 移动端产品

### 海外专业平台
- Reddit（r/entrepreneur, r/SaaS, r/artificial）— 海外用户真实需求
- Hacker News（news.ycombinator.com）— 技术社区
- IndieHackers — 独立开发者产品
- G2 / Capterra — SaaS 产品库
- Crunchbase — 融资产品动态

### 学术和专利
- arXiv — AI/技术论文
- Semantic Scholar — 学术引用
- Google Patents — 全球专利
- USPTO（美国专利商标局）— 美国专利
- EPO（欧洲专利局）— 欧洲专利

### 电商和变现验证
- Gumroad — 数字产品
- Etsy — 创意产品
- Amazon — 实体和数字产品
- Shopify App Store — 商业工具

## 判断标准

| 重叠度 | 判断 | 下一步 |
|--------|------|--------|
| >60% 功能重叠 | 同质化 | 强制重设计 |
| 实现路径实质相同 | 侵权风险 | 拒绝写入 |
| 30-60% 重叠 | 部分创新 | 提取差异部分 |
| <30% 重叠 | 通过 Gate 1 | 进入蒸馏协议 |

## 差异化重设计（重叠>60% 时）

用第一性原理重问：
1. 这个问题的底层本质是什么？
2. 现有产品没有解决什么？
3. 在中国市场或海外市场，哪个细分场景被忽略了？
4. 能否在定价、交付方式、目标用户上找到真实差异？

至少在一个维度实现真实创新，才能进入下一步。

## 独创性声明（必须写入 memory）

```markdown
【独创性验证记录】
时间：YYYY-MM-DD HH:mm
验证人：太一

搜索平台：
- 中文：Baidu, Sogou, 知网，CNIPA
- 英文：Bing, Google, GitHub, ProductHunt
- 学术：arXiv, Google Patents
- 电商：Gumroad, Shopify

最相似产品：
- 名称：
- URL:
- 功能重叠度：__%
- 差异点：

核心创新点：
1. 
2. 

结论：通过 / 拒绝 / 重设计
```

## 铁律

- 未通过独创性验证的内容禁止进入系统
- 搜索记录必须留存，可追溯
- 重叠>60% 强制重设计，无例外
- 侵权风险 = 立即终止
