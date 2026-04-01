# 情景模式系统架构设计

> 创建：2026-03-31 10:11  
> 核心：384 体验单元内容架构  
> 状态：✅ 系统架构文档

---

## 🎯 架构目标

```
支持 384 体验单元内容生产、存储、匹配、输出的完整系统
```

**核心需求**:
- ✅ 内容创作：支持 384 个体验单元的高效生产
- ✅ 结构化存储：每个体验单元 5 维数据结构化
- ✅ 快速匹配：用户测试→匹配体验单元（<100ms）
- ✅ 动态输出：根据匹配结果生成个性化报告

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     情景模式系统架构                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                          │
│  │  用户层      │                                          │
│  │  (小程序)    │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │  应用层      │                                          │
│  │  - 情景测试  │                                          │
│  │  - 报告生成  │                                          │
│  │  - 用户追踪  │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │  服务层      │      │  算法层      │                    │
│  │  - 匹配服务  │◄────►│  - 匹配算法  │                    │
│  │  - 内容服务  │      │  - 推荐算法  │                    │
│  │  - 用户服务  │      │              │                    │
│  └──────┬───────┘      └──────────────┘                    │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │  数据层      │      │  内容层      │                    │
│  │  - PostgreSQL│      │  - 384 体验单元                   │
│  │  - Redis     │      │  - 64 状态详情                   │
│  │  - 用户数据  │      │  - 测试题库    │                    │
│  └──────────────┘      └──────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 数据架构

### 1. 体验单元数据模型

```json
{
  "experience_unit": {
    "id": "A01-03",
    "state_id": "A01",
    "state_name": "积累未显期",
    "step": 3,
    "step_name": "开始怀疑路径",
    "type": "调整型",
    
    "experience": {
      "surface": "你很努力，但结果一直不理想...",
      "deep": "你在证明自己的价值，避免被看作失败..."
    },
    
    "emotion": {
      "primary": ["焦虑", "自我怀疑"],
      "intensity": 7,
      "source": "努力与回报不匹配"
    },
    
    "cognition": {
      "core_belief": "努力就应该有回报",
      "thinking_pattern": "非黑即白",
      "cognitive_distortion": ["读心术", "过度概括"]
    },
    
    "behavior": {
      "typical": "更加努力地重复旧方法",
      "frequency": "每天工作 12 小时+",
      "consequence": "短期缓解焦虑，长期可能路径错配"
    },
    
    "body": {
      "signals": ["肩膀紧绷", "胃部不适"],
      "state": ["睡眠质量下降", "容易疲劳"]
    },
    
    "report": {
      "insight": "路径 × 资源 × 时机 未对齐",
      "psychology": {
        "adler": "你的价值感驱动着持续努力",
        "jung": "潜意识里在重复某种模式",
        "freud": "防御机制让你难以放手"
      },
      "steps": {
        "current": 3,
        "progress": [
          {"step": 1, "name": "刚开始不对劲", "status": "completed"},
          {"step": 2, "name": "逐渐察觉问题", "status": "completed"},
          {"step": 3, "name": "开始怀疑路径", "status": "current"},
          {"step": 4, "name": "尝试调整方式", "status": "next"},
          {"step": 5, "name": "逐步适应", "status": "pending"},
          {"step": 6, "name": "进入新状态", "status": "pending"}
        ]
      },
      "actions": {
        "stop": ["停止过度努力", "停止与他人比较"],
        "look": ["看清路径是否真正匹配", "看清环境时机是否成熟"],
        "change": ["换一种努力方式", "换一种评估标准"]
      },
      "today": [
        "写下 3 件今天做得好的事",
        "和一个信任的人聊聊你的困惑",
        "给自己放个小假",
        "问自己：如果放下'必须成功'，我会怎么做？"
      ],
      "encouragement": "你现在经历的不是失败，而是积累未显..."
    },
    
    "metadata": {
      "created_at": "2026-03-31T10:00:00+08:00",
      "updated_at": "2026-03-31T10:00:00+08:00",
      "version": "1.0",
      "quality_score": 48,
      "status": "published"
    }
  }
}
```

### 2. 数据库表设计

```sql
-- 64 状态表
CREATE TABLE states (
    id VARCHAR(10) PRIMARY KEY,  -- 'A01', 'B02', ...
    name VARCHAR(50) NOT NULL,    -- '积累未显期'
    type VARCHAR(20) NOT NULL,    -- '调整型'/'过渡型'/'观察型'/'决策型'
    theme VARCHAR(200),           -- '努力还没有看到结果'
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 384 体验单元表
CREATE TABLE experience_units (
    id VARCHAR(10) PRIMARY KEY,   -- 'A01-03'
    state_id VARCHAR(10) REFERENCES states(id),
    step INTEGER NOT NULL,        -- 1-6
    step_name VARCHAR(50),        -- '开始怀疑路径'
    
    -- 5 维体验数据 (JSONB)
    experience JSONB,
    emotion JSONB,
    cognition JSONB,
    behavior JSONB,
    body JSONB,
    
    -- 报告模板 (JSONB)
    report_template JSONB,
    
    -- 元数据
    quality_score INTEGER,        -- 质量评分 (0-50)
    status VARCHAR(20),           -- 'draft'/'review'/'published'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 测试题目表
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    type VARCHAR(20),             -- 'single_choice'/'rating'
    options JSONB,                -- 选项
    mapping JSONB,                -- 映射规则 (答案→状态类型)
    sort_order INTEGER
);

-- 用户测试记录表
CREATE TABLE user_tests (
    id UUID PRIMARY KEY,
    user_id VARCHAR(50),
    test_type VARCHAR(20),        -- 'quick'/'standard'/'deep'
    answers JSONB,
    matched_unit_id VARCHAR(10) REFERENCES experience_units(id),
    matched_state_id VARCHAR(10) REFERENCES states(id),
    matched_step INTEGER,
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户轨迹表
CREATE TABLE user_trajectories (
    id UUID PRIMARY KEY,
    user_id VARCHAR(50),
    test_id UUID REFERENCES user_tests(id),
    from_unit_id VARCHAR(10),
    to_unit_id VARCHAR(10),
    change_type VARCHAR(20),      -- 'state_change'/'step_progress'/'step_regress'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引优化
CREATE INDEX idx_experience_units_state ON experience_units(state_id);
CREATE INDEX idx_experience_units_type ON experience_units USING GIN((emotion->'primary'));
CREATE INDEX idx_user_tests_user ON user_tests(user_id);
CREATE INDEX idx_user_tests_matched ON user_tests(matched_unit_id);
```

---

## 🔧 服务架构

### 1. 匹配服务

```python
# services/matching_service.py

class MatchingService:
    """情景匹配服务"""
    
    def __init__(self):
        self.question_bank = self._load_questions()
        self.experience_units = self._load_experience_units()
    
    def quick_match(self, answers: List[Dict]) -> MatchResult:
        """
        快速测试匹配 (3 题)
        
        Args:
            answers: 用户答案 [{"q": 1, "a": "A"}, ...]
        
        Returns:
            MatchResult: 匹配结果
        """
        # Step 1: 计算 4 大类型得分
        type_scores = self._calculate_type_scores(answers)
        
        # Step 2: 确定主类型
        main_type = max(type_scores, key=type_scores.get)
        
        # Step 3: 确定状态（该类型下最匹配的）
        state = self._match_state(main_type, answers)
        
        # Step 4: 确定阶段（1-6）
        step = self._calculate_step(answers)
        
        # Step 5: 获取体验单元
        unit_id = f"{state['id']}-{step}"
        experience_unit = self._get_experience_unit(unit_id)
        
        # Step 6: 计算置信度
        confidence = self._calculate_confidence(answers, type_scores)
        
        return MatchResult(
            unit_id=unit_id,
            state=state,
            step=step,
            confidence=confidence,
            experience_unit=experience_unit
        )
    
    def _calculate_type_scores(self, answers: List[Dict]) -> Dict:
        """计算 4 大类型得分"""
        type_scores = {
            '调整型': 0,
            '过渡型': 0,
            '观察型': 0,
            '决策型': 0
        }
        
        for answer in answers:
            question = self.question_bank[answer['q']]
            mapping = question['mapping']
            selected_type = mapping[answer['a']]
            type_scores[selected_type] += 1
        
        return type_scores
    
    def _match_state(self, main_type: str, answers: List[Dict]) -> Dict:
        """匹配具体状态"""
        # 基于关键词匹配 + 权重计算
        # 简化版：返回该类型第一个状态
        states = self._get_states_by_type(main_type)
        return states[0]
    
    def _calculate_step(self, answers: List[Dict]) -> int:
        """计算阶段（1-6）"""
        # 基于情绪强度/问题严重性
        intensity = sum(a.get('intensity', 5) for a in answers)
        
        if intensity < 15:
            return 1
        elif intensity < 25:
            return 2
        elif intensity < 35:
            return 3
        elif intensity < 45:
            return 4
        elif intensity < 55:
            return 5
        else:
            return 6
    
    def _calculate_confidence(self, answers: List[Dict], 
                             type_scores: Dict) -> float:
        """计算置信度"""
        # 基于答案一致性 + 类型优势
        max_score = max(type_scores.values())
        total = sum(type_scores.values())
        
        if total == 0:
            return 0.5
        
        # 优势类型占比
        ratio = max_score / total
        
        # 置信度 = 基础值 (0.5) + 优势加成 (0-0.5)
        confidence = 0.5 + (ratio - 0.25) * 2
        
        return min(max(confidence, 0.5), 0.99)
```

### 2. 报告生成服务

```python
# services/report_service.py

class ReportService:
    """报告生成服务"""
    
    def __init__(self):
        self.template_loader = TemplateLoader()
    
    def generate_report(self, match_result: MatchResult) -> str:
        """
        生成情景报告
        
        Args:
            match_result: 匹配结果
        
        Returns:
            报告文本
        """
        unit = match_result.experience_unit
        template = self.template_loader.load('experience_report')
        
        report = template.render(
            state_name=unit['state_name'],
            state_type=unit['type'],
            step=unit['step'],
            step_name=unit['step_name'],
            experience=unit['experience'],
            emotion=unit['emotion'],
            cognition=unit['cognition'],
            behavior=unit['behavior'],
            body=unit['body'],
            report_template=unit['report']
        )
        
        return report
    
    def generate_share_card(self, match_result: MatchResult) -> Image:
        """生成分享卡片"""
        # 使用 Canvas 或图片生成库
        pass
```

### 3. 内容服务

```python
# services/content_service.py

class ContentService:
    """内容管理服务"""
    
    def create_experience_unit(self, data: Dict) -> str:
        """创建体验单元"""
        # 验证数据结构
        self._validate_unit_data(data)
        
        # 生成 ID
        unit_id = self._generate_unit_id(data)
        
        # 保存到数据库
        self.db.insert('experience_units', {
            'id': unit_id,
            **data,
            'status': 'draft',
            'quality_score': 0
        })
        
        return unit_id
    
    def review_experience_unit(self, unit_id: str, 
                               quality_scores: Dict) -> bool:
        """审核体验单元"""
        # 计算质量评分
        total_score = self._calculate_quality_score(quality_scores)
        
        # 更新状态
        if total_score >= 45:
            status = 'published'
        elif total_score >= 35:
            status = 'review'
        else:
            status = 'draft'
        
        self.db.update('experience_units', 
                      {'id': unit_id},
                      {'quality_score': total_score, 
                       'status': status})
        
        return status == 'published'
    
    def get_experience_unit(self, unit_id: str) -> Dict:
        """获取体验单元"""
        return self.db.get('experience_units', {'id': unit_id})
    
    def list_experience_units(self, filters: Dict = None) -> List[Dict]:
        """列出体验单元（支持筛选）"""
        query = "SELECT * FROM experience_units"
        params = []
        
        if filters:
            conditions = []
            if 'type' in filters:
                conditions.append("type = %s")
                params.append(filters['type'])
            if 'status' in filters:
                conditions.append("status = %s")
                params.append(filters['status'])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        return self.db.query(query, params)
```

---

## 🎨 内容生产架构

### 1. 内容生产流程

```
┌─────────────────────────────────────────────────────────────┐
│  384 体验单元内容生产流程                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: 内容创作                                          │
│  ┌──────────────┐                                          │
│  │ - AI 生成初稿  │                                          │
│  │ - 人工审核   │                                          │
│  │ - 质量评分   │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  Step 2: 结构化录入                                        │
│  ┌──────────────┐                                          │
│  │ - 5 维数据填充  │                                          │
│  │ - 报告模板编写 │                                          │
│  │ - 元数据标记   │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  Step 3: 质量审核                                          │
│  ┌──────────────┐                                          │
│  │ - 具体性检查 │                                          │
│  │ - 共鸣性测试 │                                          │
│  │ - 可执行性验证 │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  Step 4: 发布上线                                          │
│  ┌──────────────┐                                          │
│  │ - 状态更新   │                                          │
│  │ - 缓存预热   │                                          │
│  │ - 监控配置   │                                          │
│  └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 内容创作模板

```markdown
# 体验单元创作模板

## 基础信息
- 状态 ID: A01
- 状态名称：积累未显期
- 阶段：3
- 阶段名称：开始怀疑路径
- 类型：调整型

## 5 维体验数据

### 1. 体验描述
【表层体验】
（你在做什么/看到什么/感受到什么）

【深层体验】
（你在害怕什么/渴望什么/证明什么）

### 2. 情绪状态
- 主要情绪：
- 情绪强度（1-10）：
- 情绪来源：

### 3. 认知特征
- 核心信念：
- 思维模式：
- 认知偏差：

### 4. 行为模式
- 典型行为：
- 行为频率：
- 行为后果：

### 5. 身体感受
- 身体信号：
- 身体部位：
- 身体状态：

## 报告模板

### 核心洞察
（路径 × 资源 × 时机 分析）

### 心理学解读
- 阿德勒：
- 荣格：
- 弗洛伊德：

### 6 步演进
（当前在第几步，前后步骤描述）

### 行动建议（停看换）
【停】
【看】
【换】

### 今日具体行动
1.
2.
3.
4.

### 鼓励的话
```

### 3. 批量生产策略

```python
# scripts/batch_create_units.py

def batch_create_experience_units():
    """批量创建体验单元"""
    
    # 定义 64 状态
    states = define_64_states()
    
    # 定义 6 阶段通用结构
    step_structure = define_6_steps()
    
    # 生成 384 体验单元框架
    for state in states:
        for step in range(1, 7):
            unit_id = f"{state['id']}-{step}"
            
            # 使用 AI 生成初稿
            draft = ai_generate_unit(state, step)
            
            # 人工审核 + 优化
            reviewed = human_review(draft)
            
            # 结构化录入
            unit_data = structure_unit(reviewed)
            
            # 保存到数据库
            save_unit(unit_data)
    
    print(f"✅ 完成 384 体验单元创建")
```

---

## ⚡ 性能优化

### 1. 缓存策略

```python
# 使用 Redis 缓存热点数据

class CacheService:
    def __init__(self):
        self.redis = Redis()
    
    def get_experience_unit(self, unit_id: str) -> Dict:
        """获取体验单元（带缓存）"""
        # 先查缓存
        cached = self.redis.get(f"unit:{unit_id}")
        if cached:
            return json.loads(cached)
        
        # 缓存未命中，查数据库
        unit = self.db.get('experience_units', {'id': unit_id})
        
        # 写入缓存（TTL: 24 小时）
        self.redis.setex(
            f"unit:{unit_id}",
            86400,
            json.dumps(unit, ensure_ascii=False)
        )
        
        return unit
    
    def invalidate_unit_cache(self, unit_id: str):
        """缓存失效"""
        self.redis.delete(f"unit:{unit_id}")
```

### 2. 匹配性能

```python
# 预加载所有体验单元到内存

class MatchingService:
    def __init__(self):
        # 应用启动时预加载
        self.experience_units = self._load_all_units()
        self.questions = self._load_questions()
    
    def _load_all_units(self) -> Dict:
        """预加载所有体验单元到内存"""
        units = self.db.query("SELECT * FROM experience_units WHERE status='published'")
        return {unit['id']: unit for unit in units}
    
    def quick_match(self, answers: List[Dict]) -> MatchResult:
        """内存匹配（<10ms）"""
        # 所有计算在内存中完成
        ...
```

---

## 📊 监控指标

### 1. 业务指标

| 指标 | 目标 | 监控方式 |
|------|------|---------|
| 测试完成率 | >80% | 漏斗分析 |
| 匹配置信度 | >70% | 平均值监控 |
| 报告分享率 | >20% | 事件追踪 |
| 用户留存率 | >40% | 同期群分析 |

### 2. 技术指标

| 指标 | 目标 | 监控方式 |
|------|------|---------|
| 匹配延迟 | <100ms | APM 监控 |
| 缓存命中率 | >90% | Redis 监控 |
| 数据库查询 | <50ms | 慢查询日志 |
| API 可用性 | >99.9% | 健康检查 |

---

## 📁 文件结构

```
/workspace/
├── content/yijing/
│   ├── scenario-architecture.md    # 本文档
│   ├── scenario-mapping.md         # 底层逻辑映射
│   ├── 384-experience-units.md     # 体验单元定义
│   ├── scenario-app-design.md      # 设计方案
│   └── scenario-app-config.json    # 配置文件
├── scripts/
│   ├── scenario-agent-test.py      # 测试脚本
│   └── batch_create_units.py       # 批量生产脚本
├── services/
│   ├── matching_service.py         # 匹配服务
│   ├── report_service.py           # 报告服务
│   └── content_service.py          # 内容服务
└── database/
    └── schema.sql                  # 数据库表结构
```

---

*创建：2026-03-31 10:11 | 太一 AGI · 情景模式系统*
*状态：✅ 系统架构文档 | 版本：v1.0*
