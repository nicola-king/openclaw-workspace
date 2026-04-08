# Agent Reach - AI 互联网感知扩展

> 状态：🟡 框架创建中  
> 优先级：P0  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 需要搜索 Twitter/Reddit/小红书等平台内容
- 需要提取 YouTube/B 站视频内容
- 需要监控 GitHub Issue/PR 动态
- 需要 RSS 订阅更新提醒
- AI 需要"联网"获取实时信息

---

## 能力

- ✅ YouTube 视频 + 字幕提取
- ✅ Twitter 搜索（无需 API）
- ✅ Reddit 帖子/评论抓取
- ✅ 小红书笔记（绕过登录）
- ✅ B 站视频/弹幕
- ✅ GitHub Issue/PR
- ✅ RSS 监控
- ✅ 抖音/LinkedIn/微信公众号/微博

---

## 配置

```bash
AGENT_REACH_MODE=cli  # cli 或 api
AGENT_REACH_RATE_LIMIT=10  # 每秒请求数
AGENT_REACH_CACHE_DIR=./cache/agent-reach/
```

---

## 使用方法

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/install.sh | bash

# YouTube
agent-reach youtube "URL"

# Twitter
agent-reach twitter "query" --limit 20

# Reddit
agent-reach reddit "subreddit" --query "keyword"

# 小红书
agent-reach xiaohongshu "URL"

# B 站
agent-reach bilibili "URL"

# GitHub
agent-reach github "URL"

# RSS
agent-reach rss "feed.xml" --notify
```

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ 安装测试
- [ ] ⏳ 平台功能验证
- [ ] ⏳ 与太一集成

---

*最后更新：2026-04-08 22:30*
