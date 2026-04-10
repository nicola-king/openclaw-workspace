# Knowledge Extractor (知识提取器)

> **版本**: 1.0.0  
> **创建时间**: 2026-04-10  
> **灵感**: HyperExtract - Smart Knowledge Extraction CLI  
> **作者**: 太一 AGI

---

## 📋 职责域

**核心功能**: 从非结构化文档提取结构化知识

**输入**: Markdown/PDF/Word 等文档  
**输出**: Knowledge Abstracts (知识抽象)

**输出格式**:
- Entities (实体列表)
- Relationships (关系图谱)
- Timeline (时间线)
- Tags (标签集合)
- Summary (摘要)

---

## 🎯 使用场景

1. **记忆提炼**: daily notes → core.md
2. **能力涌现分析**: Skill 关系图谱
3. **项目文档**: README → 结构化知识
4. **研报解析**: 金融研报 → 投资洞察

---

## 🔧 命令接口

```bash
# 提取单个文件
python3 skills/knowledge-extractor/extractor.py memory/2026-04-10.md

# 提取目录
python3 skills/knowledge-extractor/extractor.py memory/ --recursive

# 指定输出格式
python3 skills/knowledge-extractor/extractor.py input.md --output graph
python3 skills/knowledge-extractor/extractor.py input.md --output timeline
python3 skills/knowledge-extractor/extractor.py input.md --output pydantic
```

---

## 📦 依赖

```bash
pip install pydantic networkx rich
```

---

## 🧠 知识抽象模型

```python
class KnowledgeAbstract(BaseModel):
    """知识抽象 - 结构化知识表示"""
    
    source: str                    # 来源文件
    extracted_at: datetime         # 提取时间
    
    entities: List[Entity]         # 实体列表
    relationships: List[Relation]  # 关系图谱
    timeline: List[Event]          # 时间线
    tags: Set[str]                 # 标签集合
    summary: str                   # 摘要
    
    # 元数据
    confidence: float              # 置信度 (0-1)
    model_used: str                # 使用的模型
```

---

## 🎨 美学原则

**输出即艺术**:
- 结构化美感 (清晰层次)
- 视觉友好 (Rich 终端输出)
- 苹果设计 80% (简约)
- 东方元素 15% (禅意留白)
- 中国元素 5% (点睛之笔)

---

## 📝 示例输出

### 终端输出

```
╔═══════════════════════════════════════════════════════════╗
║  🧠 知识抽象 · Knowledge Abstract                         ║
║  来源：memory/2026-04-10.md                               ║
═══════════════════════════════════════════════════════════╝

【实体】5 个
  ├─ 太一 AGI (Agent)
  ├─ OpenClaw 4.9 (System)
  ├─ Memory Backfill (Feature)
  ├─ Provider Aliases (Feature)
  └─ Plugin SDK (Feature)

【关系】8 条
  ├─ 太一 AGI → 融合 → OpenClaw 4.9
  ├─ 太一 AGI → 实现 → Memory Backfill
  ├─ 太一 AGI → 创建 → Provider Aliases
  └─ ...

【时间线】3 事件
  ├─ 13:00 开始 P0 实施
  ├─ 13:35 P1 功能完成
  └─ 13:50 P2 功能完成

【标签】
  #OpenClaw #记忆系统 #能力涌现 #P0/P1/P2

【摘要】
  2026-04-10 完成 OpenClaw 4.9 全面融合，实施 11 项
  P0/P1/P2功能，包括记忆回填、环境安全、模型对比等。
```

### JSON 输出

```json
{
  "source": "memory/2026-04-10.md",
  "extracted_at": "2026-04-10T15:45:00+08:00",
  "entities": [
    {"id": "taiyi", "name": "太一 AGI", "type": "Agent"},
    {"id": "openclaw", "name": "OpenClaw 4.9", "type": "System"}
  ],
  "relationships": [
    {"from": "taiyi", "to": "openclaw", "type": "融合"}
  ],
  "timeline": [
    {"time": "13:00", "event": "开始 P0 实施"}
  ],
  "tags": ["OpenClaw", "记忆系统", "能力涌现"],
  "summary": "完成 OpenClaw 4.9 全面融合..."
}
```

---

## 🔄 与太一系统集成

### 记忆系统

```
memory-backfill.py
    ↓
knowledge-extractor
    ↓
memory/core.md (更新)
```

### 能力涌现

```
emerged-skill-*/SKILL.md
    ↓
knowledge-extractor
    ↓
reports/skill-graph.json (关系图谱)
```

### 时间线索引

```
memory/timeline.md
    ↓
knowledge-extractor
    ↓
reports/knowledge-timeline.json
```

---

## 📊 质量指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 实体提取准确率 | >90% | - |
| 关系抽取召回率 | >85% | - |
| 时间线完整性 | >95% | - |
| 提取速度 | <10s/文件 | - |

---

## 🙏 致谢

- 灵感来源：HyperExtract (https://github.com/hyperextract)
- 核心模型：太一 AGI (qwen3.5-plus)
- 美学设计：苹果 80% + 东方 15% + 中国 5%

---

*Skill: 太一 AGI · Knowledge Extractor*  
*创建时间：2026-04-10 15:45*
