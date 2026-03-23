---
name: search-alternative
tier: 2
trigger: 搜索/备用/SearXNG/隐私
enabled: true
depends: []
---
# 备用搜索技能（SearXNG）

## 核心原则

**负熵法则：** 降低单点依赖风险（Brave API 故障时备用）

**价值基石：** 隐私保护，符合 SAYELF 数据安全需求

**简化优先：** 仅在必要时启用，不替代现有 web_search

---

## 定位说明

**当前搜索方案：** Brave Search API（web_search 工具）

**SearXNG 定位：** 备用搜索源（非默认）

**启用条件：**
- Brave API 故障/受限
- SAYELF 明确要求隐私搜索
- 需要聚合多搜索引擎结果

---

## SearXNG 简介

| 特性 | 说明 |
|------|------|
| 类型 | 元搜索引擎（聚合 243+ 服务） |
| 隐私 | 无追踪/无画像/无日志 |
| 许可 | AGPL-3.0 开源 |
| 部署 | 可自建实例 |
| 替代 | Google/Bing 等 243 个引擎 |

---

## 使用方式

### 方式 1：公共实例（快速）

```bash
# 使用公共 SearXNG 实例
curl -s "https://searx.be/search?q=查询词&format=json"
```

**推荐实例：**
- `https://searx.be`
- `https://searx.info`
- `https://search.trom.tf`

### 方式 2：自建实例（隐私最佳）

```bash
# Docker 部署
docker run -d --name=searxng \
  -p 8080:8080 \
  -v ./searxng:/etc/searxng \
  searxng/searxng
```

**配置后使用：**
```bash
curl -s "http://localhost:8080/search?q=查询词&format=json"
```

---

## 与 web_search 对比

| 维度 | web_search (Brave) | SearXNG (备用) |
|------|-------------------|----------------|
| 速度 | 快 | 中 |
| 质量 | 高 | 中上 |
| 隐私 | 中 | 高 |
| 依赖 | API Key | 无/自建 |
| 成本 | 免费额度 | 免费 |
| 状态 | ✅ 默认 | 🟡 备用 |

---

## 启用流程

### L2 审查触发

**条件：** 满足以下任一
- Brave API 连续 3 次失败
- SAYELF 明确要求隐私搜索
- 需要聚合搜索结果

**流程：**
```
太一检测 → 风险评估 → SAYELF 告知 → 
启用 SearXNG → 记录 memory
```

### Memory 记录模板

```markdown
【TASK-YYYYMMDD-XXX】[审查：L2] [搜索备用]
- 启用原因：Brave API 故障/SAYELF 要求
- 使用实例：searx.be / 自建
- 搜索结果：[简述]
- 状态：已完成
```

---

## 搜索策略

### 默认策略

```
1. 首选 web_search (Brave)
2. 失败 3 次 → 切换 SearXNG
3. 记录切换原因到 memory
```

### 隐私模式

```
SAYELF 要求隐私搜索 → 直接使用 SearXNG 自建实例
```

### 聚合搜索

```
需要多源结果 → SearXNG 聚合 243+ 引擎
```

---

## 自建实例配置（可选）

### 最小配置

```yaml
# config.yml
use_default_settings: true
search:
  formats:
    - html
    - json
server:
  secret_key: "your-secret-key"
  limiter: false
  image_proxy: true
```

### 推荐配置

```yaml
# 启用更多引擎
engines:
  - name: google
    engine: google
    shortcut: g
  - name: bing
    engine: bing
    shortcut: b
  - name: duckduckgo
    engine: duckduckgo
    shortcut: d
```

---

## 故障处理

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 公共实例慢 | 负载高 | 切换实例/自建 |
| 结果质量低 | 引擎配置 | 调整引擎优先级 |
| 自建失败 | Docker 问题 | 检查日志/重启 |

### 回滚方案

```
SearXNG 不可用 → 回退到 web_search → 记录故障
```

---

## 快速参考

### 启用命令

```bash
# 测试公共实例
curl -s "https://searx.be/search?q=test&format=json" | jq '.results | length'

# 测试自建实例
curl -s "http://localhost:8080/search?q=test&format=json" | jq '.results | length'
```

### 状态检查

```bash
# 检查实例可用性
curl -s -o /dev/null -w "%{http_code}" https://searx.be

# 期望输出：200
```

---

## 与现有技能集成

### web_search 备用

**集成点：** web_search 失败时自动切换

**流程：**
```
web_search 请求 → 失败检测 → 
计数 >=3 → 启用 SearXNG → 记录 memory
```

### HEARTBEAT 检查

**集成点：** 每周检查 SearXNG 实例可用性

**检查项：**
- [ ] 公共实例可访问
- [ ] 自建实例运行正常（如配置）
- [ ] 搜索结果质量可接受

---

## 隐私保护说明

### SearXNG 隐私特性

- ❌ 无用户追踪
- ❌ 无搜索历史
- ❌ 无 IP 记录
- ❌ 无用户画像
- ✅ 开源可审计
- ✅ 可自建实例

### 与 Brave 对比

| 维度 | Brave | SearXNG |
|------|-------|---------|
| 用户追踪 | 有限 | 无 |
| 搜索历史 | 可能记录 | 无 |
| IP 记录 | 可能 | 无（自建） |
| 开源 | 部分 | 完全 |

---

## 决策建议

### 使用场景

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 日常搜索 | web_search (Brave) | 速度/质量优先 |
| 隐私敏感 | SearXNG 自建 | 隐私保护 |
| API 故障 | SearXNG 公共 | 备用方案 |
| 多源结果 | SearXNG 聚合 | 243+ 引擎 |

### 成本效益分析

| 方案 | 成本 | 收益 | 推荐度 |
|------|------|------|--------|
| 仅 Brave | 低 | 高 | ⭐⭐⭐⭐ |
| Brave + SearXNG 备用 | 低 | 更高 | ⭐⭐⭐⭐⭐ |
| 仅 SearXNG | 中（自建） | 中 | ⭐⭐⭐ |

---

## 总结

**定位：** 备用搜索源，非默认方案

**价值：** 降低单点依赖，隐私保护选项

**启用条件：** Brave API 故障 或 SAYELF 明确要求

**审查级别：** L2（太一 + 告知）

---
*版本：1.0 | 生效日期：2026-03-22 | 最后更新：08:05*
