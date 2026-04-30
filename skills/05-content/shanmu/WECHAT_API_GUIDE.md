# 📱 微信公众号 API 集成指南

> **版本**: 1.0  
> **创建时间**: 2026-04-11  
> **状态**: 中期方案 (需服务号认证)

---

## 🎯 API 能力

**已实现**:
- ✅ 访问令牌获取
- ✅ 草稿箱创建
- ✅ 定时发布
- ✅ 数据统计

**待实现**:
- ⏳ 封面图上传
- ⏳ 多账号管理
- ⏳ 评论管理
- ⏳ 用户管理

---

## 🔐 获取 API 权限

### 步骤 1: 服务号认证

1. 登录微信公众平台：https://mp.weixin.qq.com/
2. 设置 → 公众号设置 → 认证
3. 选择"微信认证"
4. 支付 300 元认证费
5. 等待审核 (1-3 个工作日)

### 步骤 2: 获取 AppID 和 AppSecret

1. 设置 → 基本配置
2. 复制 **AppID** (开发者 ID)
3. 复制 **AppSecret** (开发者密码)

**当前配置**:
```json
{
  "official_account": {
    "app_id": "wx720a4c489fec9df3",
    "app_secret": "94066275ad79af78b29b3c5f1ef7660c"
  }
}
```

### 步骤 3: 配置 IP 白名单

1. 设置 → 基本配置 → IP 白名单
2. 添加服务器 IP：`103.172.182.26`

---

## 📋 API 调用示例

### 1. 获取访问令牌

```python
import requests

def get_access_token(app_id, app_secret):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data['access_token']  # 有效期 7200 秒
```

### 2. 创建草稿

```python
def create_draft(access_token, article):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    payload = {
        "articles": [{
            "title": article['title'],
            "content": article['content'],
            "thumb_media_id": article['cover_id'],
            "author": "SAYELF",
            "show_cover_pic": 1
        }]
    }
    
    response = requests.post(url, json=payload)
    return response.json()['media_id']
```

### 3. 定时发布

```python
def schedule_publish(access_token, media_id, publish_time):
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    
    payload = {
        "media_id": media_id,
        "preview": False,
        "send_time": publish_time  # "2026-04-11 20:00:00"
    }
    
    response = requests.post(url, json=payload)
    return response.json()
```

### 4. 获取数据

```python
def get_metrics(access_token, begin_date, end_date):
    url = "https://api.weixin.qq.com/datacube/getarticlesummary"
    params = {
        "access_token": access_token,
        "begin_date": begin_date,  # "20260411"
        "end_date": end_date
    }
    
    response = requests.get(url, params=params)
    return response.json()['list']
```

---

## 📊 数据指标

**核心指标**:
| 指标 | 说明 | API 字段 |
|------|------|---------|
| 阅读量 | 文章阅读次数 | int_page_read_count |
| 分享量 | 文章分享次数 | share_count |
| 点赞量 | 文章点赞次数 | user_like_count |
| 收藏量 | 文章收藏次数 | collect_count |
| 转化率 | 分享/阅读比例 | share_count/int_page_read_count |

**ROI 计算**:
```
ROI = (收益 - 成本) / 成本 * 100%

收益 = 付费转化数 * 客单价
成本 = 内容成本 + 推广成本
```

---

## 🔧 使用脚本

### 短期方案 (邮件发送)

```bash
# 生成文章并发送邮件草稿
python3 wechat-auto-publish.py --topic "AI 管家" --mode email

# 查看邮件 → 复制粘贴 → 手动发布
```

### 中期方案 (API 发布)

```bash
# 生成文章并推送到草稿箱
python3 wechat-auto-publish.py --topic "AI 管家" --mode api

# 定时发布
python3 wechat-auto-publish.py --topic "AI 管家" --mode api --publish-time "2026-04-11 20:00"

# 获取文章数据
python3 wechat-auto-publish.py --metrics

# 查看数据 Dashboard
python3 wechat-metrics-dashboard.py
```

### 定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务
0 8 * * * /usr/bin/python3 /home/nicola/.openclaw/workspace/skills/shanmu/wechat-auto-publish.py --topic "AI 管家" --mode email
0 9 * * * /usr/bin/python3 /home/nicola/.openclaw/workspace/skills/shanmu/wechat-metrics-dashboard.py
```

---

## 📈 数据 Dashboard

**查看数据**:
```bash
python3 wechat-metrics-dashboard.py
```

**输出示例**:
```
============================================================
📊 微信公众号数据 Dashboard
============================================================

统计周期：20260404 ~ 20260411
文章数量：7 篇

总阅读量：1,234
总分享量：56
总点赞量：89

平均阅读：176
转化率：4.54%

生成时间：2026-04-11T17:18:17
============================================================
```

---

## ⚠️ 注意事项

**API 限制**:
- 访问令牌有效期：7200 秒 (2 小时)
- 每日调用次数：根据认证等级
- IP 白名单：必须配置

**内容规范**:
- 遵守微信公众号运营规范
- 不发布违规内容
- 注意版权问题

**数据安全**:
- AppSecret 妥善保管
- 不要提交到 Git
- 定期更新密码

---

**📱 微信公众号 API 集成指南已创建！**

**太一 AGI · 2026-04-11** ✨
