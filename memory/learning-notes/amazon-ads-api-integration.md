# 学习笔记：亚马逊广告 API 集成（第二阶段）

> 学习时间：2026-04-06 00:27  
> 来源：小红书 @早晚冰美式 o  
> 主题：n8n + OpenClaw 亚马逊广告自动化 - 第二阶段

---

## 📋 第二阶段：连接亚马逊广告 API

**目标**：让 OpenClaw/n8n 能够读取亚马逊广告数据

---

## 🔑 2.1 申请亚马逊广告 API 权限

### 申请流程

| 步骤 | 操作 | 说明 |
|------|------|------|
| **1** | 登录亚马逊广告后台 | advertising.amazon.com |
| **2** | 右上角账号名 → API Access | 进入 API 访问页面 |
| **3** | 点击申请 API 访问 | 填写表单（选择自用，不是代理商） |
| **4** | 等待审核 | 1-3 个工作日，邮件通知 |

### 审核通过后获得

```
Client ID（客户端 ID）
Client Secret（客户端密钥）
```

**⚠️ 注意**：妥善保管，后续步骤需要用到

---

## 🔐 2.2 获取 Refresh Token（访问令牌）

**为什么需要**：Refresh Token 是 n8n/OpenClaw 访问账号数据的钥匙

### 四步获取法

#### 第 1 步：打开授权链接
```
https://www.amazon.com/ap/oa?
  client_id=YOUR_CLIENT_ID&
  scope=profiles&
  response_type=code&
  redirect_uri=https://localhost:8080
```

**替换**：`YOUR_CLIENT_ID` → 申请到的 Client ID

#### 第 2 步：登录并授权
- 用卖家账号登录
- 点击【允许授权】

#### 第 3 步：获取 code
- 授权后跳转到 localhost 页面（可能显示无法访问）
- 看地址栏：`code=xxxxxxxxx`
- 复制这段 code

#### 第 4 步：用 code 换取 Refresh Token
```
POST https://api.amazon.com/auth/o2/token

client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
code=CODE_FROM_STEP_3&
grant_type=authorization_code&
redirect_uri=https://localhost:8080
```

**返回**：
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**🎯 目标**：拿到 `refresh_token`（长期有效）

---

## 🛠️ OpenClaw 原生实现方案

### Skill 框架

```python
# skills/amazon-ads/SKILL.md
import requests
import json
from datetime import datetime

class AmazonAdsAPI:
    """亚马逊广告 API 客户端"""
    
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self):
        """获取访问令牌（自动刷新）"""
        if self.access_token and datetime.now() < self.token_expiry:
            return self.access_token
        
        # 使用 refresh token 换取新的 access token
        url = "https://api.amazon.com/auth/o2/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(url, data=data)
        token_data = response.json()
        
        self.access_token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'])
        
        return self.access_token
    
    def fetch_campaigns(self, profile_id):
        """获取广告活动数据"""
        url = f"https://advertising-api.amazon.com/sd/campaigns"
        headers = {
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Amazon-Advertising-API-Scope': profile_id,
            'Authorization': f"Bearer {self.get_access_token()}"
        }
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def fetch_keywords(self, campaign_id):
        """获取关键词数据（包含 ACoS）"""
        # 实现类似逻辑
        pass
    
    def analyze_acos(self, keywords_data, threshold=30):
        """分析高 ACoS 关键词"""
        high_acos = []
        for kw in keywords_data:
            acos = kw.get('acos', 0)
            if acos > threshold:
                high_acos.append({
                    'keyword': kw['keywordText'],
                    'acos': acos,
                    'spend': kw['spend'],
                    'sales': kw['sales']
                })
        return high_acos
    
    def generate_bid_suggestions(self, high_acos_keywords):
        """生成调价建议（AI 辅助）"""
        suggestions = []
        for kw in high_acos_keywords:
            # 建议降价幅度
            if kw['acos'] > 50:
                suggestion = "建议降价 30-50%"
            elif kw['acos'] > 30:
                suggestion = "建议降价 10-30%"
            else:
                suggestion = "保持观察"
            
            suggestions.append({
                'keyword': kw['keyword'],
                'acos': kw['acos'],
                'suggestion': suggestion
            })
        return suggestions
```

### 配置示例

```python
# .env.amazon
AMAZON_CLIENT_ID=your_client_id
AMAZON_CLIENT_SECRET=your_client_secret
AMAZON_REFRESH_TOKEN=your_refresh_token
AMAZON_PROFILE_ID=your_profile_id
```

### 定时任务

```python
# scripts/amazon-ads-daily.py
from skills.amazon-ads.SKILL import AmazonAdsAPI
import os
from dotenv import load_dotenv

load_dotenv('.env.amazon')

api = AmazonAdsAPI(
    client_id=os.getenv('AMAZON_CLIENT_ID'),
    client_secret=os.getenv('AMAZON_CLIENT_SECRET'),
    refresh_token=os.getenv('AMAZON_REFRESH_TOKEN')
)

# 每日任务
keywords = api.fetch_keywords()
high_acos = api.analyze_acos(keywords, threshold=30)
suggestions = api.generate_bid_suggestions(high_acos)

# 生成报告
report = f"""
# 亚马逊广告日报

高 ACoS 关键词：{len(high_acos)} 个

Top 5:
"""
for i, kw in enumerate(high_acos[:5], 1):
    report += f"{i}. {kw['keyword']} - ACoS: {kw['acos']:.1f}%\n"

report += "\n调价建议:\n"
for s in suggestions[:5]:
    report += f"- {s['keyword']}: {s['suggestion']}\n"

print(report)
```

---

## 📊 与太一现有系统集成

### ROI 追踪器集成

```python
# 自动记录广告支出到 ROI 追踪器
tracker = ROITracker()

# 每日广告成本
daily_spend = sum(kw['spend'] for kw in keywords)
tracker.add_transaction(
    type='cost',
    category='亚马逊广告',
    amount=daily_spend,
    description=f"广告支出 - {len(keywords)} 个关键词"
)

# 广告带来的销售
daily_sales = sum(kw['sales'] for kw in keywords)
tracker.add_transaction(
    type='revenue',
    category='亚马逊销售',
    amount=daily_sales,
    description=f"广告销售 - ACoS: {average_acos:.1f}%"
)
```

### 预警系统集成

```python
# 预算预警
budget_used = daily_spend / daily_budget
if budget_used > 0.8:
    send_wechat_alert(f"⚠️ 广告预算已使用 {budget_used:.0%}")

# ACoS 预警
if average_acos > 40:
    send_wechat_alert(f"🔴 ACoS 过高：{average_acos:.1f}%")
```

---

## 🎯 开发优先级

### P0（已有，无需开发）
- ✅ ROI 追踪器
- ✅ 预警系统
- ✅ Cron 定时
- ✅ 微信推送

### P1（如需亚马逊自动化）
- [ ] 亚马逊 API Skill（2 小时）
- [ ] ACoS 分析逻辑（1 小时）
- [ ] 调价建议生成（0.5 小时）
- [ ] 日报生成（1 小时）
- [ ] **总计：4.5 小时**

### P2（可选增强）
- [ ] 自动调价执行（需 API 写权限）
- [ ] 竞品监控
- [ ] 历史数据趋势分析

---

## 💡 核心洞察

### 1. API 集成本质
**所有自动化系统** = API 数据 + 定时采集 + AI 分析 + 预警通知

**亚马逊广告**只是其中一个应用场景，太一已有 90% 的基础设施。

### 2. 复用价值
**已有能力复用**：
- ROI 追踪器 → 追踪广告 ROI
- 预警系统 → 预算/ACoS 预警
- 热点选题 → 关键词发现
- 增长实验 → A/B 测试广告文案

**新增开发**：仅需亚马逊 API 集成（4.5 小时）

### 3. 场景选择
**亚马逊卖家** → 值得开发（刚需）  
**非亚马逊卖家** → 无需开发（用现有技能）

**太一策略**：保持通用能力，按需开发垂直技能。

---

## 📝 行动清单

### 已确认需求
- [ ] 评估是否有亚马逊卖家需求
- [ ] 如有需求，开发亚马逊 API Skill

### 无需行动（已有）
- [x] ROI 追踪器
- [x] 预警系统
- [x] Cron 定时
- [x] 微信推送
- [x] AI 分析能力

---

*学习笔记生成：太一 AGI · 2026-04-06 00:28*  
*建议：如无亚马逊卖家需求，无需开发此 Skill*
