# 🔍 智能搜索 Agent 使用指南

## 🚀 快速开始

### 1. 基本搜索

```bash
# 搜索折叠房屋需求
python3 main.py --query "foldable container house buyer" --regions "Southeast Asia" "Middle East"

# 指定优先级
python3 main.py --query "steel structure house" --priority high

# 指定搜索引擎
python3 main.py --query "modular container house" --engine bing
```

### 2. 保存结果

```bash
# 保存为 JSON
python3 main.py --query "container house importer" --output results.json

# 查看结果
cat results.json | python3 -m json.tool
```

### 3. 系统状态

```bash
# 查看状态
python3 main.py --status

# 运行测试
python3 main.py --test

# 执行进化
python3 main.py --evolve
```

---

## 📊 搜索结果示例

```json
[
  {
    "company_name": "DXH Container House Co., Ltd",
    "website": "https://www.dxfanghouse.com",
    "email": "info@dxfanghouse.com",
    "phone": "+86-755-23456789",
    "address": "Shenzhen, China",
    "region": "Southeast Asia",
    "confidence": 0.85,
    "source": "bing",
    "timestamp": 1714128000.0
  }
]
```

---

## 🧬 自进化功能

系统会自动学习和优化：

1. **成功率跟踪** - 记录每次搜索的成功率
2. **策略优化** - 根据历史数据优化搜索策略
3. **知识库更新** - 保存成功和失败的经验
4. **自动进化** - 定期执行策略优化

---

## 🔧 配置说明

### 搜索引擎优先级

```json
{
  "search_engines": {
    "priority": ["bing", "google", "duckduckgo", "baidu"]
  }
}
```

### 代理配置

```json
{
  "proxy": {
    "enabled": true,
    "overseas": ["http://proxy1:8080"],
    "domestic": ["http://proxy2:8080"]
  }
}
```

### 反爬策略

```json
{
  "anti_scraping": {
    "enabled": true,
    "delay_range": [1, 3],
    "max_retries": 3
  }
}
```

---

## 📈 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 成功率 | >80% | 搜索成功比例 |
| 响应时间 | <5s | 平均响应时间 |
| 数据质量 | >90% | 信息准确度 |
| 反爬率 | <20% | 被反爬比例 |

---

## 🛠️ 故障排除

### 网络问题

```bash
# 检查网络连接
ping bing.com

# 测试搜索引擎
python3 -c "from core.search_agent import SearchAgent; a = SearchAgent(); print(a.search('test'))"
```

### 代理问题

```bash
# 检查代理配置
cat config/proxy_config.json

# 测试代理
curl -x http://proxy:port https://www.bing.com
```

### 日志查看

```bash
# 查看日志
tail -f logs/search_agent.log

# 搜索错误
grep ERROR logs/search_agent.log
```

---

## 🔄 集成到太一系统

```python
from skills.09_search_agent.core.search_agent import SearchAgent

# 创建搜索 Agent
agent = SearchAgent()

# 执行搜索
results = agent.search(
    query="foldable container house buyer",
    regions=["Southeast Asia", "Middle East"],
    priority="high"
)

# 处理结果
for result in results:
    print(f"{result.company_name}: {result.website}")

# 关闭
agent.close()
```

---

*太一智能搜索 Agent v1.0 · 2026-04-26*