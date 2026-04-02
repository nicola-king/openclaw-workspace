# opencli 命令完整列表

> 来源：用户分享截图 | 整理时间：2026-04-02  
> 平台覆盖：15+ | 状态：✅ 已整合到 OpenClaw fetch 规范

---

## 📋 命令分类

### 信息获取类（公开 API，无需浏览器登录）

| 平台 | 命令 | 说明 |
|------|------|------|
| **Hacker News** | `opencli hackernews top --limit 5` | 热帖 Top5 |
| **GitHub** | `opencli hf top` | Trending 项目 |
| **StackOverflow** | `opencli stackoverflow hot --limit 5` | 热门问题 |
| **arXiv** | `opencli arxiv search "关键词"` | 论文搜索 |
| **BBC** | `opencli bbc news` | 新闻资讯 |
| **Wikipedia** | `opencli wikipedia random` | 随机词条 |

---

### 国内平台（需要 Chrome 已登录）

| 平台 | 命令 | 说明 |
|------|------|------|
| **B 站** | `opencli bilibili hot --limit 10` | 热榜 Top10 |
| **知乎** | `opencli zhihu hot -f json` | 热搜（JSON 格式） |
| **小红书** | `opencli xiaohongshu search "AI 工具"` | 关键词搜索 |
| **微博** | `opencli weibo hot` | 热搜榜 |
| **豆瓣** | `opencli douban top250` | 电影 Top250 |
| **Boss 直聘** | `opencli boss search "前端开发"` | 职位搜索 |
| **V2EX** | `opencli v2ex latest --limit 5` | 最新帖子 |
| **即刻** | `opencli jike feed` | 动态流 |

---

### 海外平台

| 平台 | 命令 | 说明 |
|------|------|------|
| **Twitter** | `opencli twitter trending` | 趋势话题 |
| **Product Hunt** | `opencli producthunt top` | 今日热门 |
| **Reddit** | `opencli reddit hot --subreddit all` | 热门帖子 |

---

## 🎯 使用场景

### 每日晨报

```bash
#!/bin/bash
# 每日晨报信息收集
opencli hackernews top --limit 5 > /tmp/hn.txt
opencli github trending > /tmp/gh.txt
opencli zhihu hot -f json > /tmp/zhihu.json
# 发送给 AI 总结
```

### 市场调研

```bash
#!/bin/bash
# 竞品监控
opencli xiaohongshu search "AI 工具" > /tmp/xhs.txt
opencli twitter trending > /tmp/tw.txt
# 分析趋势
```

### 技术学习

```bash
#!/bin/bash
# 技术动态
opencli arxiv search "large language model" > /tmp/papers.txt
opencli stackoverflow hot --limit 5 > /tmp/so.txt
# 学习最新技术
```

---

## 📊 效率对比

| 任务 | 手动 | opencli | 提升 |
|------|------|---------|------|
| 收集 5 平台热榜 | 15 分钟 | 30 秒 | 30x |
| 搜索小红书内容 | 5 分钟 | 3 秒 | 100x |
| 监控 Twitter 趋势 | 2 分钟 | 2 秒 | 60x |

---

## 🔗 OpenClaw 整合

已整合到 `openclaw fetch` 命令：

```bash
openclaw fetch hackernews top --limit 5
openclaw fetch github trending
openclaw fetch zhihu hot --format json
openclaw fetch xiaohongshu search "AI 工具"
openclaw fetch twitter trending
```

**设计参考**：opencli 的 15+ 平台命令结构

---

## 📝 备注

1. **国内平台**：需要 Chrome 已登录状态（Cookie 共享）
2. **海外平台**：部分需要代理
3. **JSON 输出**：支持 `-f json` 或 `--format json`
4. **Limit 参数**：默认 5-10 条，可自定义

---

*整理时间：2026-04-02 | 来源：用户分享 | 整合状态：✅ 完成*
