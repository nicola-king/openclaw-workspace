# P8 · 对话式创建器设计方案

**版本**: v0.1  
**创建**: 2026-03-25 16:51  
**执行**: 太一 + 素问  
**优先级**: P8

---

## 🎯 目标

借鉴 Creao AI 对话式创建理念，实现太一原生的对话式智能体创建器。

---

## 📋 设计理念

### Creao AI 核心思路

```
用户对话描述需求
    ↓
AI 自动提取工作流
    ↓
生成智能体应用
    ↓
可视化 UI 界面
    ↓
持续迭代优化
```

### 太一适配方案

```
SAYELF 对话描述需求（微信/Telegram）
    ↓
太一自动分析职责域（知几/山木/素问...）
    ↓
提取任务流程
    ↓
生成技能配置文件
    ↓
Git 版本管理
    ↓
持续迭代（Self-Improving）
```

---

## 🔧 技术实现

### 组件 1: 需求分析器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/requirement-analyzer.py

import json
from pathlib import Path

class RequirementAnalyzer:
    """需求分析器"""
    
    def __init__(self):
        self.bot_domains = {
            "知几": ["交易", "数据", "分析", "趋势", "预测", "polymarket"],
            "山木": ["内容", "文案", "发布", "小红书", "公众号", "创意"],
            "素问": ["技术", "代码", "开发", "调研", "实现", "工具"],
            "罔两": ["市场", "竞品", "情报", "调研", "数据"],
            "庖丁": ["财务", "成本", "预算", "支出", "收入"]
        }
    
    def analyze(self, requirement_text):
        """分析需求，确定职责域"""
        # 关键词匹配
        bot_scores = {}
        for bot, keywords in self.bot_domains.items():
            score = sum(1 for kw in keywords if kw in requirement_text.lower())
            bot_scores[bot] = score
        
        # 选择最高分 Bot
        best_bot = max(bot_scores, key=bot_scores.get)
        
        return {
            "primary_bot": best_bot,
            "confidence": bot_scores[best_bot] / len(self.bot_domains[best_bot]),
            "secondary_bots": [b for b, s in bot_scores.items() if s > 0 and b != best_bot],
            "keywords": self._extract_keywords(requirement_text)
        }
    
    def _extract_keywords(self, text):
        """提取关键词"""
        # 简化版：提取名词
        return text.split()
```

### 组件 2: 工作流提取器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/workflow-extractor.py

import json
from pathlib import Path

class WorkflowExtractor:
    """工作流提取器"""
    
    def __init__(self):
        pass
    
    def extract(self, requirement, bot):
        """从需求中提取工作流"""
        # 识别任务步骤
        steps = self._parse_steps(requirement)
        
        # 识别输入输出
        inputs = self._parse_inputs(requirement)
        outputs = self._parse_outputs(requirement)
        
        # 识别工具/技能
        tools = self._parse_tools(requirement)
        
        return {
            "name": self._generate_name(requirement),
            "bot": bot,
            "steps": steps,
            "inputs": inputs,
            "outputs": outputs,
            "tools": tools
        }
    
    def _parse_steps(self, requirement):
        """解析任务步骤"""
        # 简化版：按序号或换行分割
        lines = [l.strip() for l in requirement.split("\n") if l.strip()]
        return lines
    
    def _parse_inputs(self, requirement):
        """解析输入"""
        # 查找"输入"/"需要"等关键词
        inputs = []
        if "输入" in requirement:
            inputs.append("用户输入")
        if "数据" in requirement:
            inputs.append("外部数据")
        return inputs
    
    def _parse_outputs(self, requirement):
        """解析输出"""
        outputs = []
        if "报告" in requirement:
            outputs.append("分析报告")
        if "发布" in requirement:
            outputs.append("发布内容")
        return outputs
    
    def _parse_tools(self, requirement):
        """解析工具需求"""
        tools = []
        if "搜索" in requirement:
            tools.append("web_search")
        if "浏览器" in requirement:
            tools.append("browser")
        return tools
    
    def _generate_name(self, requirement):
        """生成技能名称"""
        # 简化版：取前 10 个字
        return requirement[:10] + "..."
```

### 组件 3: 技能生成器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/skill-generator.py

from pathlib import Path
from datetime import datetime

class SkillGenerator:
    """技能生成器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    
    def generate(self, workflow):
        """生成技能文件"""
        bot = workflow["bot"]
        skill_name = self._sanitize_name(workflow["name"])
        
        # 创建技能目录
        skill_dir = self.skills_dir / bot / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成技能配置文件
        config_path = skill_dir / "skill.json"
        self._generate_config(config_path, workflow)
        
        # 生成技能实现文件
        impl_path = skill_dir / "main.py"
        self._generate_implementation(impl_path, workflow)
        
        # 生成 README
        readme_path = skill_dir / "README.md"
        self._generate_readme(readme_path, workflow)
        
        return skill_dir
    
    def _sanitize_name(self, name):
        """清理名称（用于文件名）"""
        return name.replace("...", "").replace(" ", "-").lower()
    
    def _generate_config(self, path, workflow):
        """生成配置文件"""
        config = {
            "name": workflow["name"],
            "bot": workflow["bot"],
            "version": "0.1",
            "created_at": datetime.now().isoformat(),
            "steps": workflow["steps"],
            "inputs": workflow["inputs"],
            "outputs": workflow["outputs"],
            "tools": workflow["tools"]
        }
        
        with open(path, "w", encoding="utf-8") as f:
            import json
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _generate_implementation(self, path, workflow):
        """生成实现文件（框架）"""
        code = f'''#!/usr/bin/env python3
"""
{workflow["name"]}

自动生成时间：{datetime.now().isoformat()}
"""

def execute(input_data):
    """执行技能"""
    # TODO: 实现具体逻辑
    
    result = {{
        "status": "success",
        "output": "TODO"
    }}
    
    return result

if __name__ == "__main__":
    # 测试
    result = execute({{"test": "data"}})
    print(result)
'''
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
    
    def _generate_readme(self, path, workflow):
        """生成 README"""
        readme = f'''# {workflow["name"]}

**Bot**: {workflow["bot"]}  
**创建时间**: {datetime.now().isoformat()}  
**版本**: 0.1

## 功能

自动生成技能框架，待完善。

## 输入

{chr(10).join("- " + i for i in workflow["inputs"])}

## 输出

{chr(10).join("- " + o for o in workflow["outputs"])}

## 使用工具

{chr(10).join("- " + t for t in workflow["tools"])}

## 任务步骤

{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(workflow["steps"]))}

## 待办

- [ ] 完善实现逻辑
- [ ] 添加测试用例
- [ ] 文档完善
'''
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(readme)
```

---

## 📊 使用流程

### Step 1: SAYELF 描述需求

```
SAYELF: 创建一个技能，每天自动抓取 Polymarket 热门市场数据，
       分析鲸鱼动向，生成报告发给我。
```

### Step 2: 太一分析职责域

```
太一分析:
- 关键词：Polymarket、数据、分析、鲸鱼、报告
- 匹配 Bot: 知几（交易/数据）+ 罔两（市场/情报）
- 主责 Bot: 知几
```

### Step 3: 提取工作流

```
工作流:
1. 抓取 Polymarket 热门市场数据
2. 分析鲸鱼钱包动向
3. 生成分析报告
4. 发送给 SAYELF

输入：Polymarket API
输出：分析报告
工具：web_search, browser
```

### Step 4: 生成技能

```
生成文件:
- skills/zhiji/polymarket-whale-monitor/skill.json
- skills/zhiji/polymarket-whale-monitor/main.py
- skills/zhiji/polymarket-whale-monitor/README.md
```

### Step 5: Git 版本管理

```bash
git add skills/zhiji/polymarket-whale-monitor/
git commit -m "[技能创建] Polymarket 鲸鱼监控"
git push
```

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-055` | 需求分析器 | ✅ 完成 | 16:51 |
| `TASK-20260325-056` | 工作流提取器 | ✅ 完成 | 16:51 |
| `TASK-20260325-057` | 技能生成器 | ✅ 完成 | 16:51 |
| `TASK-20260325-058` | 实际测试 | 🟡 待执行 | - |
| `TASK-20260325-059` | UI/UX 设计 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:51 | 执行：太一 + 素问*
