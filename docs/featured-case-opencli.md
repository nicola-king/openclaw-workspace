# OpenClaw CLI 工具集 · 精选案例

> 来自社区的优质 CLI 工作流案例

---

## 🏆 opencli · 15+ 平台信息获取命令

**作者**：@opencli-team  
**来源**：GitHub/GitCode  
**提交时间**：2026-04-02  
**状态**：🏆 精选案例

### 项目介绍

opencli 是一个命令行信息获取工具，支持 15+ 国内外平台：

**国内平台**：
- 哔哩哔哩（`bilibili`）
- 微博（`weibo`）
- 知乎（`zhihu`）
- 豆瓣（`douban`）
- 小红书（`xiaohongshu`）
- 抖音（`douyin`）
- 快手（`kuaishou`）
- 百度贴吧（`tieba`）

**国外平台**：
- YouTube（`youtube`）
- Twitter（`twitter`）
- Instagram（`instagram`）
- TikTok（`tiktok`）
- Reddit（`reddit`）
- GitHub（`github`）
- HackerNews（`hackernews`）
- ProductHunt（`producthunt`）

### 命令格式

```bash
opencli <平台> <动作> [参数]
```

### 精选命令

#### 热门榜单
```bash
# 知乎热榜
opencli zhihu hot

# 微博热搜
opencli weibo trending

# B 站热门
opencli bilibili hot

# HackerNews Top
opencli hackernews top --limit 10

# GitHub Trending
opencli github trending
```

#### 搜索功能
```bash
# 小红书搜索
opencli xiaohongshu search "AI 工具" --limit 20

# B 站搜索
opencli bilibili search "教程" --order view

# YouTube 搜索
opencli youtube search "OpenClaw" --duration short
```

#### 用户信息
```bash
# B 站 UP 主信息
opencli bilili user <uid>

# 微博用户信息
opencli weibo user <uid>

# GitHub 用户信息
opencli github user <username>
```

### 输出格式

支持多种输出格式：

```bash
# 表格格式（默认）
opencli zhihu hot --format table

# JSON 格式
opencli zhihu hot --format json

# CSV 格式
opencli zhihu hot --format csv
```

### 对 OpenClaw 的启发

opencli 的命令设计为 OpenClaw CLI 提供了宝贵参考：

**借鉴设计**：
```bash
# OpenClaw 规划中的信息获取命令
openclaw fetch hackernews top --limit 5
openclaw fetch github trending
openclaw fetch zhihu hot --format json
openclaw fetch twitter trending
```

**核心优势**：
1. **语义清晰**：平台 + 动作 + 参数
2. **格式统一**：所有平台命令格式一致
3. **易于扩展**：新增平台只需添加新命令
4. **输出灵活**：支持多种格式

### 效率提升

| 任务 | 手动 | opencli | 提升 |
|------|------|---------|------|
| 查看知乎热榜 | 打开 App+ 加载 (30 秒) | 1 命令 (2 秒) | **15x** |
| 搜索小红书 | 打开 App+ 输入 (60 秒) | 1 命令 (3 秒) | **20x** |
| 查看 GitHub Trending | 打开网页 + 加载 (15 秒) | 1 命令 (1 秒) | **15x** |

**年化收益**：每天节省 20 分钟 = 每年 122 小时 = 5 天

---

## 🎯 案例征集

我们正在收集更多优质 CLI 工作流案例！

### 入选奖励

1. **GitHub 署名**：你的名字出现在官方 README
2. **公众号专题**：SAYELF 山野精灵专题报道
3. **小红书曝光**：AI 缪斯｜龙虾研究所推荐

### 提交方式

- **GitHub Issue**：https://github.com/nicola-king/openclaw-workspace/issues
- **截止**：2026-04-10
- **目标**：3-5 个案例

### 案例模板

```markdown
## 工作流名称
## 解决的问题
## CLI 命令/脚本
## 效率提升（量化）
## 截图/录屏（可选）
```

---

## 📚 相关资源

- [OpenClaw CLI 速查表](./openclaw-cli-cheatsheet.md)
- [最佳实践指南](./openclaw-cli-best-practices.md)
- [工作流案例集](./automation-workflow-examples.md)

---

*最后更新：2026-04-02 | OpenClaw CLI 工具集 v1.0*
