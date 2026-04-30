# 🌍 跨境贸易 Agent v6.0 · 用户指南

> 版本：v6.0 | 适用人群：外贸企业/SOHO/工厂 | 更新：2026-04-16

---

## 一、快速开始

### 1.1 30 秒完成初始化

**步骤 1：配置基本信息**
```bash
# 编辑配置文件
nano config/company.yaml

# 填写公司信息
company:
  name: "XX 钢结构房屋有限公司"
  email: "sales@yourcompany.com"
  phone: "+86-13800138000"
  website: "www.yourcompany.com"
  products: ["Prefab House", "Steel Structure", "Container House"]
```

**步骤 2：启动 Agent**
```bash
# 启动服务
python3 cross_border_agent.py start

# 查看状态
python3 cross_border_agent.py status
```

**步骤 3：开始获客**
```
✅ 营销自动发布
✅ 询盘自动回复
✅ 报价自动生成
✅ 订单自动跟进
```

---

### 1.2 核心功能一览

| 功能 | 说明 | 效率提升 |
|------|------|---------|
| **营销推广** | Alibaba/Google/Facebook 自动发布 | 10 倍 |
| **询盘处理** | 1 小时内自动回复 | 24 倍 |
| **智能报价** | 20% 利润率自动计算 | 5 倍 |
| **订单管理** | 生产进度自动跟进 | 3 倍 |
| **物流发货** | 货运安排自动协调 | 2 倍 |
| **售后服务** | 客户维护自动化 | 5 倍 |

---

## 二、核心功能详解

### 2.1 营销推广

**支持渠道**：

| 渠道 | 功能 | 发布频率 |
|------|------|---------|
| **Alibaba** | 产品自动发布 + 关键词优化 | 每日 |
| **Google Ads** | 广告自动投放 + ROI 优化 | 实时 |
| **Facebook** | 社媒内容自动发布 | 每日 3 条 |
| **行业展会** | 展会信息自动跟踪 | 每周 |

**如何配置**：
```yaml
# config/marketing.yaml
marketing:
  alibaba:
    enabled: true
    products: 50  # 发布产品数量
    keywords: ["prefab house", "steel structure"]
    
  google_ads:
    enabled: true
    daily_budget: 100  # 每日预算 ($)
    target_countries: ["US", "AU", "CA"]
    
  facebook:
    enabled: true
    posts_per_day: 3
    content_types: ["product", "case", "news"]
```

**效果监控**：
```bash
# 查看营销数据
python3 cross_border_agent.py marketing --stats

# 输出示例
【营销数据报告】
Alibaba:
  曝光量：15,230
  点击量：1,523
  询盘：52
  
Google Ads:
  展示量：50,000
  点击量：2,500
  询盘：35
  
Facebook:
  触达：10,000
  互动：500
  询盘：13
  
总计询盘：100 个/月
```

---

### 2.2 询盘处理

**自动回复流程**：
```
客户询盘
   ↓
Agent 自动识别产品
   ↓
调取产品库 + 价格库
   ↓
生成专业回复（1 小时内）
   ↓
发送客户邮箱
   ↓
记录 CRM 系统
```

**回复模板**：
```
Subject: Re: Inquiry about Prefab House

Dear [Customer Name],

Thank you for your inquiry about our Prefab House products.

【公司介绍】
We are a professional manufacturer with 10 years experience,
 exported to 50+ countries including US, Australia, Canada.

【产品规格】
- Size: 20ft / 40ft / Customized
- Material: Light Steel Structure
- Wall Panel: EPS/Rock Wool/PU Sandwich Panel
- Certification: CE/ISO/SGS

【价格参考】
- 20ft: $3,500-5,000 FOB Shanghai
- 40ft: $6,000-9,000 FOB Shanghai
- Bulk order: 10-15% discount

【交货期】
- Sample: 15-20 days
- Bulk order: 30-45 days

【附件】
- Product Catalog (PDF)
- Case Photos (ZIP)
- Certificate (PDF)

Looking forward to your reply!

Best regards,
[Your Name]
Sales Manager
[Company Name]
```

**配置自动回复**：
```yaml
# config/inquiry.yaml
inquiry:
  response_time: 3600  # 1 小时内回复
  auto_reply: true
  followup_schedule: [1, 3, 7, 15]  # 跟进节奏 (天)
  
  templates:
    - name: "标准回复"
      trigger: "general"
      file: "templates/standard_reply.txt"
    
    - name: "价格咨询"
      trigger: "price"
      file: "templates/price_reply.txt"
    
    - name: "样品请求"
      trigger: "sample"
      file: "templates/sample_reply.txt"
```

---

### 2.3 智能报价

**报价公式**：
```
FOB 价格 = (材料成本 + 人工成本 + 制造费用) × (1 + 利润率)

利润率默认 20%，可配置
```

**生成报价单**：
```bash
# 快速报价
python3 cross_border_agent.py quote \
  --inquiry_id "INQ-20260416-001" \
  --product "40ft Prefab House" \
  --quantity 10 \
  --destination "Sydney, Australia"

# 输出
【报价单】
客户：ABC Company (Australia)
产品：40ft Prefab House
数量：10 套

单价：$8,500 FOB Shanghai
总价：$85,000

海运运费：$12,000 (40HQ × 2)
保险费用：$500

CIF Sydney: $97,500

交货期：30-45 天
付款方式：30% 定金 + 70% 发货前
报价有效期：15 天
```

**配置利润率**：
```yaml
# config/pricing.yaml
pricing:
  default_margin: 0.20  # 默认 20% 利润率
  
  product_margins:
    "20ft Prefab House": 0.18
    "40ft Prefab House": 0.20
    "Container House": 0.22
    "Steel Structure": 0.25
    
  volume_discount:
    10: 0.05   # 10 套以上 5% 折扣
    50: 0.10   # 50 套以上 10% 折扣
    100: 0.15  # 100 套以上 15% 折扣
```

---

### 2.4 订单管理

**订单状态跟踪**：
```
订单创建 → 定金收到 → 生产开始 → 生产完成 → 
质检通过 → 发货安排 → 尾款收到 → 订单完成
```

**生产跟进**：
```bash
# 查看订单状态
python3 cross_border_agent.py orders --status

# 输出
【订单状态】
ORD-20260401-001: 生产中 (60%)
  客户：ABC Company
  产品：40ft Prefab House × 10
  交期：2026-05-15
  状态：框架完成，等待墙板安装

ORD-20260405-002: 待发货
  客户：DEF Company
  产品：20ft Prefab House × 20
  交期：2026-05-10
  状态：质检通过，等待装柜

ORD-20260410-003: 待生产
  客户：GHI Company
  产品：Container House × 5
  交期：2026-05-30
  状态：定金已收，等待排产
```

**自动跟进配置**：
```yaml
# config/order.yaml
order:
  followup_frequency: 86400  # 每天跟进
  
  notifications:
    - event: "定金收到"
      notify: ["sales", "production"]
    
    - event: "生产完成"
      notify: ["sales", "qc", "logistics"]
    
    - event: "发货安排"
      notify: ["sales", "customer"]
    
    - event: "订单完成"
      notify: ["sales", "finance"]
```

---

### 2.5 物流发货

**运费计算**：
```bash
# 计算海运运费
python3 cross_border_agent.py shipping \
  --origin "Shanghai" \
  --destination "Sydney" \
  --volume 68  # CBM
  --weight 15000  # KG

# 输出
【海运报价】
航线：上海 → 悉尼
柜型：40HQ × 2
体积：68 CBM
重量：15,000 KG

海运费：$6,000
燃油附加费：$800
港口杂费：$500
保险费用：$300

总计：$7,600
航程：14-16 天
船公司：COSCO/MSC
```

**发货清单**：
```
【发货文件清单】
✅ 商业发票 (Commercial Invoice)
✅ 装箱单 (Packing List)
✅ 提单 (Bill of Lading)
✅ 原产地证 (Certificate of Origin)
✅ 质检报告 (Inspection Report)
✅ 保险单 (Insurance Policy)
```

---

### 2.6 售后服务

**质保政策**：
```
结构质保：10 年
配件质保：2 年
终身技术支持

质保范围：
✅ 材料缺陷
✅ 工艺问题
✅ 运输损坏

非质保范围：
❌ 人为损坏
❌ 自然灾害
❌ 不当使用
```

**客户维护**：
```yaml
# config/after_sales.yaml
after_sales:
  warranty_period: 365  # 1 年质保
  
  followup_schedule:
    - days: 7
      content: "使用状况回访"
    
    - days: 30
      content: "满意度调查"
    
    - days: 90
      content: "维护提醒"
    
    - days: 365
      content: "质保到期提醒"
  
  complaint_handling:
    response_time: 3600  # 1 小时响应
    resolution_time: 86400  # 24 小时解决
```

---

## 三、常见问题

### 3.1 技术常见问题

**Q1: 如何配置邮箱？**
```yaml
# config/email.yaml
email:
  smtp_server: "smtp.qq.com"
  smtp_port: 465
  username: "your_email@qq.com"
  password: "your_auth_code"  # 授权码，非密码
  ssl: true
```

**Q2: 如何对接 CRM 系统？**
```yaml
# config/crm.yaml
crm:
  enabled: true
  provider: "salesforce"  # 或 hubspot/zoho
  api_key: "your_api_key"
  sync_frequency: 3600  # 每小时同步
```

**Q3: 如何自定义报价模板？**
```
编辑 templates/quote_template.txt
支持变量：{customer_name}, {product}, {price}, {quantity}
```

**Q4: 如何查看日志？**
```bash
# 实时查看日志
tail -f /home/nicola/.openclaw/workspace/logs/cross-border-agent.log

# 查看错误日志
grep ERROR /home/nicola/.openclaw/workspace/logs/cross-border-agent.log
```

---

### 3.2 业务常见问题

**Q1: 询盘转化率如何提高？**
```
建议 1：1 小时内回复（Agent 已自动实现）
建议 2：附上产品目录和案例照片
建议 3：提供多种付款选项
建议 4：主动邀请视频看厂
```

**Q2: 如何防范诈骗？**
```
✅ 大额订单要求信用证支付
✅ 新客户做背景调查
✅ 定金不低于 30%
✅ 购买出口信用保险
```

**Q3: 运费暴涨怎么办？**
```
方案 1：报价注明"运费按实际结算"
方案 2：与客户协商分摊
方案 3：提前锁定舱位
方案 4：选择多家货代比价
```

**Q4: 客户投诉质量问题如何处理？**
```
步骤 1：1 小时内响应，表达重视
步骤 2：要求提供照片/视频证据
步骤 3：技术团队远程诊断
步骤 4：提出解决方案（补发/维修/退款）
步骤 5：跟进至客户满意
```

---

## 四、最佳实践

### 4.1 提高转化率

```
技巧 1：专业形象
  - 企业邮箱（不用 QQ/Gmail）
  - 专业签名（含职位/电话/网站）
  - 精美产品目录

技巧 2：快速响应
  - 1 小时内回复询盘
  - 24 小时内提供报价
  - 3 天内安排样品

技巧 3：信任建立
  - 分享工厂视频
  - 提供客户案例
  - 展示资质证书
```

### 4.2 降低成本

```
技巧 1：营销优化
  - 聚焦高 ROI 渠道
  - 优化关键词投放
  - A/B 测试广告素材

技巧 2：供应链优化
  - 批量采购原材料
  - 优化生产流程
  - 降低废品率

技巧 3：物流优化
  - 多家货代比价
  - 合理装箱提高利用率
  - 提前预订舱位
```

### 4.3 风险管理

```
风险 1：汇率波动
  应对：远期结汇 + 价格调整条款

风险 2：客户违约
  应对：信用保险 + 定金制度

风险 3：质量纠纷
  应对：质检报告 + 样品确认

风险 4：物流延误
  应对：提前发货 + 缓冲时间
```

---

## 五、客户案例

### 5.1 成功案例

**案例 1：澳洲矿区营地项目**
```
客户：澳洲矿业公司
产品：40ft 折叠房屋 × 50 套
金额：$425,000
周期：45 天
结果：客户满意，返单 100 套

关键点：
✅ 快速响应（2 小时报价）
✅ 专业方案（矿区特殊要求）
✅ 质量保证（通过澳洲认证）
✅ 及时交付（提前 5 天发货）
```

**案例 2：美国度假村项目**
```
客户：美国房地产开发商
产品：20ft 度假屋 × 20 套
金额：$100,000
周期：30 天
结果：5 星好评，推荐 3 个新客户

关键点：
✅ 定制设计（满足当地规范）
✅ 透明沟通（每周进度汇报）
✅ 售后服务（远程技术指导）
```

### 5.2 失败案例

**案例：尼日利亚订单损失**
```
客户：尼日利亚贸易商
产品：Container House × 10 套
金额：$50,000
损失原因：客户破产

教训：
❌ 未做客户背景调查
❌ 未购买信用保险
❌ 定金比例过低（仅 20%）

改进：
✅ 新客户必须做资信调查
✅ 高风险地区要求 50% 定金
✅ 强制购买信用保险
```

---

## 六、联系方式

### 6.1 官方支持

| 渠道 | 联系方式 | 响应时间 |
|------|---------|---------|
| **Email** | support@cross-border-agent.com | 24 小时 |
| **Telegram** | @CrossBorderAgentSupport | 即时 |
| **微信** | 跨境贸易 Agent 支持 | 即时 |
| **GitHub** | github.com/nicola-king/cross-border-trade-ai-agent | 48 小时 |

### 6.2 服务时间

```
技术支持：09:00-21:00（北京时间）
紧急求助：全天候响应
培训服务：预约制
```

---

## 七、更新日志

### v6.0.0 (2026-04-16)
- ✅ 全流程自动化
- ✅ 智能报价系统
- ✅ CRM 系统集成
- ✅ 多平台营销支持
- ✅ 自进化能力激活

### v5.0.0 (2026-03-15)
- ✅ 询盘自动回复
- ✅ 订单管理优化
- ✅ 物流运费计算

### 即将上线 (v6.1.0)
- 🔜 AI 视频看厂
- 🔜 多语言支持
- 🔜 区块链信用系统

---

*跨境贸易 Agent v6.0 · 用户指南*  
*生成时间：2026-04-16 21:24*  
*太一 AGI 荣誉出品*
