# 🆕 新技能集成 · last30days-skill

**来源**: AIGCLINK (@aigelink)  
**时间**: 2026-03-27 17:33  
**类型**: 研究型技能

---

## 📋 技能功能

### 核心能力

- ✅ 自动搜索 8 大社交平台 (Reddit/X/YouTube 等)
- ✅ 时间范围：最近 30 天
- ✅ 自动发现相关账号/子版块
- ✅ 按互动量/相关性/跨平台热度排序
- ✅ 支持 A vs B 对比研究
- ✅ 带数据来源的报告

---

## 🎯 应用场景

1. **市场调研**: 了解 AI 工具最新用法
2. **趋势发现**: 追踪热门话题
3. **内容创作**: 找灵感和素材
4. **竞品分析**: A vs B 对比研究

---

## 🔧 太一系统集成方案

### 方案 1: 直接集成 (推荐)

```bash
# 克隆技能仓库
git clone https://github.com/last30days/skill.git

# 配置 API Keys
export BSKY_API_KEY="your_key"
export BLUESKY_PASSWORD="your_password"

# 运行测试
python3 last30days_skill.py "银行承兑汇票"
```

---

### 方案 2: 本地实现 (智能分流)

**使用现有工具组合**:

```python
# 智能搜索 + 汇总
1. web_search (DuckDuckGo) × 8 平台
2. web_fetch (提取内容)
3. Qwen 2.5 7B (本地·汇总分析)
4. 生成报告
```

**优势**:
- ✅ 无需额外 API
- ✅ 本地模型处理 (免费)
- ✅ 可定制搜索源

---

## 📊 测试用例

### 测试话题

**话题**: "银行承兑汇票 2026 年最新政策"

**预期输出**:
- Reddit 讨论 (r/finance, r/banking)
- X/Twitter 热门推文
- YouTube 相关视频
- 专业论坛讨论
- 带数据来源汇总

---

## 🎯 集成到 OpenClaw

### 智能路由配置

```json
{
  "skills": {
    "last30days": {
      "enabled": true,
      "platforms": ["reddit", "x", "youtube", "feishu"],
      "time_range": 30,
      "model": "qwen2.5:7b-instruct-q4_K_M"
    }
  }
}
```

---

### Bot 协作

| Bot | 职责 |
|-----|------|
| **罔两** | 数据搜索 (8 平台) |
| **素问** | 内容提取 (web_fetch) |
| **Qwen 2.5 7B** | 汇总分析 (本地) |
| **山木** | 报告生成 |
| **太一** | 统筹调度 |

---

## 🚀 立即执行

### Step 1: 验证技能源

```bash
# 检查 GitHub 仓库
curl https://api.github.com/repos/last30days/skill
```

### Step 2: 配置 API

```bash
# Bluesky API
export BSKY_HANDLE="your_handle"
export BSKY_PASSWORD="your_app_password"
```

### Step 3: 测试运行

```bash
python3 last30days_skill.py "银行承兑汇票"
```

---

## 💡 优化建议

### 国内平台适配

| 原平台 | 国内替代 |
|--------|---------|
| Reddit | 知乎/豆瓣小组 |
| X/Twitter | 微博/公众号 |
| YouTube | B 站/抖音 |
| Hacker News | 掘金/思否 |

---

### 智能分流应用

```
简单搜索 → Qwen 2.5 7B (本地)
复杂分析 → qwen3.5-plus (云端)
长报告 → Gemini 2.5 Pro (云端)
```

---

*创建时间：2026-03-27 17:33 | 太一*

*「last30days-skill 集成分析完成。建议本地实现 + 智能分流，适配国内平台，成本最优。」**✅**
