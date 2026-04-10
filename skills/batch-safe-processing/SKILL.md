# 批量安全处理系统

> **版本**: 1.0.0  
> **创建时间**: 2026-04-10 20:46  
> **灵感**: GEO Content Writer Batch-safe  
> **应用**: 批量内容生成/安全处理

---

## 🎯 核心功能

**批量安全**:
- ✅ backlog 100 prompts
- ✅ per-article QC loop
- ✅ 防止 raw markdown leaks
- ✅ 自动重试机制

---

## 📊 处理流程

```
1. Build fanout backlog (100 prompts)
   ↓
2. Select top rows (优先级排序)
   ↓
3. Generate payload (批量生成)
   ↓
4. Draft article (草稿生成)
   ↓
5. Quality check loop (质量检查)
   ↓
6. Publish (安全发布)
```

---

## 🔒 安全机制

### 1. Batch-safe

```python
class BatchSafeProcessor:
    """批量安全处理器"""
    
    def __init__(self, max_batch_size=100):
        self.backlog = []
        self.max_batch_size = max_batch_size
    
    def add_to_backlog(self, prompt):
        """添加到 backlog"""
        if len(self.backlog) >= self.max_batch_size:
            self._process_batch()
        
        self.backlog.append(prompt)
    
    def _process_batch(self):
        """处理批量"""
        # 批量处理
        results = []
        for prompt in self.backlog:
            result = self._safe_process(prompt)
            results.append(result)
        
        # 清空 backlog
        self.backlog = []
        
        return results
```

### 2. Quality Gate

```python
def quality_check(article):
    """质量检查"""
    
    checks = {
        "citations": len(article.citations) >= 5,
        "not_ideal": article.not_ideal_count >= 3,
        "word_count": article.word_count >= 1200,
        "no_raw_markdown": not article.has_raw_markdown(),
        "decision_sections": article.has_decision_sections()
    }
    
    passed = all(checks.values())
    
    return {
        "passed": passed,
        "checks": checks,
        "recommendation": "发布" if passed else "需要修改"
    }
```

### 3. Safe Publishing

```python
def safe_publish(article):
    """安全发布"""
    
    # 防止 raw markdown leaks
    content = article.content
    content = content.replace("```", "<code>")
    content = sanitize_html(content)
    
    # 发布到 WordPress
    try:
        result = wordpress.publish(content)
        return {"success": True, "url": result.url}
    except Exception as e:
        # 自动重试
        if should_retry(e):
            return retry_publish(article)
        else:
            return {"success": False, "error": str(e)}
```

### 4. Freshness Check

```python
def check_freshness(topic):
    """检查新鲜度 (避免重复)"""
    
    # 查询历史文章
    existing = search_existing_articles(topic)
    
    if existing:
        # 主题已存在
        return {
            "fresh": False,
            "existing_url": existing[0].url,
            "recommendation": "跳过或更新现有文章"
        }
    else:
        return {
            "fresh": True,
            "recommendation": "可以发布"
        }
```

---

## 🎯 太一实现

### 批量内容生成

```python
class TaiyiBatchProcessor:
    """太一批量处理器"""
    
    def __init__(self):
        self.backlog = []
        self.qc_loop = QualityCheckLoop()
    
    def generate_content(self, topics):
        """批量生成内容"""
        
        # 1. Build backlog
        for topic in topics:
            self.backlog.append({
                "topic": topic,
                "priority": self._calculate_priority(topic)
            })
        
        # 2. Select top rows
        self.backlog.sort(key=lambda x: x["priority"], reverse=True)
        top_topics = self.backlog[:10]
        
        # 3. Generate payload
        articles = []
        for topic in top_topics:
            article = self._generate_article(topic)
            articles.append(article)
        
        # 4. Quality check loop
        for article in articles:
            qc_result = self.qc_loop.check(article)
            if not qc_result["passed"]:
                self._revise_article(article, qc_result)
        
        # 5. Safe publish
        for article in articles:
            result = self._safe_publish(article)
            if result["success"]:
                print(f"✅ 发布成功：{result['url']}")
            else:
                print(f"❌ 发布失败：{result['error']}")
```

---

## 📋 集成状态

| 功能 | 状态 | 说明 |
|------|------|------|
| Backlog 管理 | ⏳ 待执行 | 100 prompts |
| 质量检查循环 | ⏳ 待执行 | per-article QC |
| 安全发布 | ⏳ 待执行 | 防止 markdown leaks |
| 新鲜度检查 | ⏳ 待执行 | 避免重复 |
| 太一集成 | ⏳ 待执行 | 批量内容生成 |

---

## 🚀 使用方式

### 方式 1: 命令行

```bash
# 批量处理
python3 skills/batch-safe-processing/process.py \
    --topics "topic1,topic2,topic3" \
    --batch-size 10
```

### 方式 2: API 调用

```python
from batch_safe_processing import BatchProcessor

processor = BatchProcessor()

# 批量生成
results = processor.generate(
    topics=["AI", "AGI", "太一"],
    batch_size=10
)
```

### 方式 3: 太一集成

```python
@taiyi.daily_task
def batch_content_generation():
    """每日批量内容生成"""
    processor = BatchProcessor()
    topics = get_trending_topics()
    processor.generate(topics)
```

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 批量大小 | 100 prompts | 待测试 |
| QC 通过率 | >90% | 待测试 |
| 发布成功率 | >95% | 待测试 |
| 重复率 | <5% | 待测试 |

---

## 🎯 下一步

- [ ] 实现 backlog 管理
- [ ] 开发质量检查循环
- [ ] 集成安全发布
- [ ] 实现新鲜度检查
- [ ] 太一集成测试

---

*太一 AGI · 批量安全处理系统*  
*创建时间：2026-04-10 20:46*  
*应用：批量内容生成/安全处理*
