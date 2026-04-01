# 技能模板库

> 版本：v1.0 | 创建：2026-03-28 13:35 | 太一技能模板
> 使用说明：复制模板 → 修改配置 → 快速创建新技能

---

## 📋 模板列表

| 模板 | 功能 | 预计创建时间 | 状态 |
|------|------|-------------|------|
| Todoist 集成 | 自动同步任务 | 30 分钟 | ✅ 就绪 |
| Notion 集成 | 自动写入数据库 | 30 分钟 | ✅ 就绪 |
| Gmail 集成 | 自动分类邮件 | 30 分钟 | ✅ 就绪 |
| Calendar 集成 | 自动添加事件 | 30 分钟 | ✅ 就绪 |
| 天气提醒 | 每日天气推送 | 15 分钟 | ✅ 就绪 |
| 新闻摘要 | 每日新闻简报 | 30 分钟 | ✅ 就绪 |
| RSS 订阅 | 自动抓取更新 | 30 分钟 | ✅ 就绪 |
| GitHub 监控 | Issue/PR 提醒 | 30 分钟 | ✅ 就绪 |
| 价格监控 | 加密货币/股票 | 30 分钟 | ✅ 就绪 |
| 定时提醒 | 自定义提醒 | 15 分钟 | ✅ 就绪 |

---

## 🔧 模板 1: Todoist 集成

**文件**: `skills/templates/todoist-sync.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todoist 自动同步技能
功能：将太一任务同步到 Todoist
"""

import os
import requests
from datetime import datetime

# 配置
TODOIST_API_KEY = os.getenv('TODOIST_API_KEY', '')
PROJECT_NAME = "太一任务"

def create_task(content, due_string="today", priority=1):
    """创建 Todoist 任务"""
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "content": content,
        "due_string": due_string,
        "priority": priority,
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def sync_from_taiyi():
    """从太一同步任务"""
    # TODO: 读取太一任务列表
    tasks = [
        {"content": "Polymarket 数据更新", "due": "today", "priority": 1},
        {"content": "每日简报发送", "due": "tomorrow", "priority": 2},
    ]
    
    for task in tasks:
        create_task(task['content'], task['due'], task['priority'])

if __name__ == '__main__':
    sync_from_taiyi()
```

**快速启动**:
```bash
export TODOIST_API_KEY="your_api_key"
python3 skills/templates/todoist-sync.py
```

---

## 🔧 模板 2: Notion 集成

**文件**: `skills/templates/notion-database.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 数据库写入技能
功能：将太一数据写入 Notion 数据库
"""

import os
import requests
from datetime import datetime

# 配置
NOTION_API_KEY = os.getenv('NOTION_API_KEY', '')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID', '')

def add_to_database(properties):
    """添加记录到 Notion 数据库"""
    url = f"https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties,
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def log_trade(trade_data):
    """记录交易数据"""
    properties = {
        "Name": {"title": [{"text": {"content": trade_data['market']}}]},
        "Date": {"date": {"start": trade_data['date']}},
        "PnL": {"number": trade_data['pnl']},
        "Status": {"select": {"name": trade_data['status']}},
    }
    
    add_to_database(properties)

if __name__ == '__main__':
    # 测试
    trade_data = {
        'market': '2026 hottest year',
        'date': '2026-03-28',
        'pnl': 5.9,
        'status': 'Open',
    }
    log_trade(trade_data)
```

**快速启动**:
```bash
export NOTION_API_KEY="your_api_key"
export NOTION_DATABASE_ID="your_database_id"
python3 skills/templates/notion-database.py
```

---

## 🔧 模板 3: Gmail 集成

**文件**: `skills/templates/gmail-sorter.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail 自动分类技能
功能：自动分类太一相关邮件
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 配置
GMAIL_CREDENTIALS = os.getenv('GMAIL_CREDENTIALS_PATH', '~/.gmail/credentials.json')

def get_gmail_service():
    """获取 Gmail 服务"""
    creds = Credentials.from_authorized_user_file(GMAIL_CREDENTIALS)
    service = build('gmail', 'v1', credentials=creds)
    return service

def label_taiyi_emails():
    """标记太一相关邮件"""
    service = get_gmail_service()
    
    # 搜索太一相关邮件
    results = service.messages().list(
        userId='me',
        q='from:polymarket OR from:gmgn OR subject:"太一"'
    ).execute()
    
    messages = results.get('messages', [])
    
    for msg in messages:
        # 添加标签
        service.messages().modify(
            userId='me',
            id=msg['id'],
            body={'addLabelIds': ['Label_123']}  # 太一标签 ID
        ).execute()
    
    print(f"✅ 标记 {len(messages)} 封邮件")

if __name__ == '__main__':
    label_taiyi_emails()
```

**快速启动**:
```bash
export GMAIL_CREDENTIALS_PATH="~/.gmail/credentials.json"
python3 skills/templates/gmail-sorter.py
```

---

## 🔧 模板 4: Calendar 集成

**文件**: `skills/templates/calendar-events.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日历事件自动添加技能
功能：将太一任务添加到日历
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# 配置
GCALENDAR_CREDENTIALS = os.getenv('GCALENDAR_CREDENTIALS_PATH', '~/.gcalendar/credentials.json')

def create_event(summary, start_time, end_time, description=""):
    """创建日历事件"""
    creds = Credentials.from_authorized_user_file(GCALENDAR_CREDENTIALS)
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Shanghai'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Shanghai'},
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

def add_daily_tasks():
    """添加每日任务"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 每日简报
    create_event(
        summary='太一每日简报',
        start_time=f'{today}T08:00:00',
        end_time=f'{today}T08:15:00',
        description='查看太一每日简报'
    )
    
    # 邮件报告
    create_event(
        summary='太一邮件报告',
        start_time=f'{today}T20:00:00',
        end_time=f'{today}T20:15:00',
        description='查看太一日报邮件'
    )

if __name__ == '__main__':
    add_daily_tasks()
```

**快速启动**:
```bash
export GCALENDAR_CREDENTIALS_PATH="~/.gcalendar/credentials.json"
python3 skills/templates/calendar-events.py
```

---

## 🔧 模板 5: 天气提醒

**文件**: `skills/templates/weather-alert.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气提醒技能
功能：每日天气推送
"""

import requests
from datetime import datetime

# 配置
CITY = "Chongqing"
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID = "7073481596"

def get_weather():
    """获取天气"""
    url = f"http://wttr.in/{CITY}?format=%C+%t+%h+%w"
    response = requests.get(url)
    return response.text.strip()

def send_weather_alert():
    """发送天气提醒"""
    weather = get_weather()
    
    message = f"""🌤️ 重庆天气提醒

{datetime.now().strftime('%Y-%m-%d %H:%M')}

{weather}

---
太一 · 自动提醒"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, json=data)

if __name__ == '__main__':
    send_weather_alert()
```

**快速启动**:
```bash
python3 skills/templates/weather-alert.py
```

---

## 🔧 模板 6-10: 其他模板

详见 `skills/templates/` 目录：

- `news-digest.py` - 新闻摘要
- `rss-subscriber.py` - RSS 订阅
- `github-monitor.py` - GitHub 监控
- `price-monitor.py` - 价格监控
- `reminder.py` - 定时提醒

---

## 🚀 使用指南

### Step 1: 复制模板

```bash
cd ~/.openclaw/workspace/skills
cp templates/todoist-sync.py my-todoist-sync.py
```

### Step 2: 修改配置

```python
# 修改 API Keys
TODOIST_API_KEY = "your_actual_key"
```

### Step 3: 添加定时任务

```bash
crontab -e
# 添加：
0 8 * * * python3 /home/nicola/.openclaw/workspace/skills/my-todoist-sync.py
```

### Step 4: 测试运行

```bash
python3 my-todoist-sync.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 13:35*
*状态：✅ 10 个模板就绪*
