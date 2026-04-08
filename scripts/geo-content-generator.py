#!/usr/bin/env python3
"""
GEO 内容生成器
功能：基于问题库，生成 SEO 优化的内容
使用：python3 geo-content-generator.py

开源免费，基于 OpenClaw 生态
"""

import json
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    'questions_dir': '/home/nicola/.openclaw/workspace/geo-questions',
    'output_dir': '/home/nicola/.openclaw/workspace/geo-content',
    'topic': '番茄种植',
}

# 内容模板
CONTENT_TEMPLATE = """# {title}

> 更新时间：{date}
> 领域：{topic}
> 阅读时间：约 5 分钟

---

## 简短答案

{short_answer}

---

## 详细分析

{detailed_analysis}

---

## 数据来源

- {data_source}

---

## 行动建议

{action_steps}

---

## 相关问题

{related_questions}

---

*如果觉得有用，欢迎点赞/收藏/关注*
"""

class GeoContentGenerator:
    """GEO 内容生成器"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_questions(self) -> dict:
        """加载问题库"""
        questions_dir = Path(self.config['questions_dir'])
        
        # 查找最新的问题文件
        json_files = list(questions_dir.glob('*.json'))
        if not json_files:
            raise FileNotFoundError("未找到问题库文件，请先运行 geo-question-generator.py")
        
        latest = max(json_files, key=lambda p: p.stat().st_mtime)
        
        with open(latest, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_content(self, question: str, category: str) -> str:
        """
        为单个问题生成内容
        
        实际使用时可以：
        1. 调用 AI 生成
        2. 人工撰写
        3. 从现有内容改编
        """
        # 这里是模板示例
        # 实际应调用 AI 或人工撰写
        
        content = CONTENT_TEMPLATE.format(
            title=question,
            date=datetime.now().strftime('%Y-%m-%d'),
            topic=self.config['topic'],
            short_answer=f"这是关于'{question}'的简短答案（50-100 字）。",
            detailed_analysis="""### 原因分析

详细分析内容...

### 解决方案

1. 第一步...
2. 第二步...
3. 第三步...

### 注意事项

- 注意 1...
- 注意 2...""",
            data_source="中国农业科学院番茄种植指南 / 10 年种植经验总结",
            action_steps="""1. 检查症状
2. 对照判断
3. 采取措施
4. 观察效果""",
            related_questions=f"- 相关问题 1\n- 相关问题 2\n- 相关问题 3"
        )
        
        return content
    
    def generate_all(self, questions: dict):
        """为所有问题生成内容"""
        print(f"📝 开始生成内容...")
        print(f"📂 输出目录：{self.output_dir}")
        print('-' * 60)
        
        total = 0
        
        for category, question_list in questions.items():
            print(f"\n📋 类别：{category}")
            
            for i, question in enumerate(question_list[:5], 1):  # 每个类别生成 5 个示例
                # 生成文件名
                filename = f"q_{total+1:03d}_{question[:20]}.md"
                filepath = self.output_dir / filename
                
                # 生成内容
                content = self.generate_content(question, category)
                
                # 保存
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ {question[:30]}...")
                total += 1
        
        print(f"\n💾 已生成 {total} 篇内容")
        print(f"📂 保存至：{self.output_dir}")


def main():
    """主程序"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  GEO 内容生成器 v1.0                                      ║')
    print('║  开源免费 | 基于 OpenClaw 生态                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    generator = GeoContentGenerator(CONFIG)
    
    # 加载问题库
    questions = generator.load_questions()
    print(f"📊 加载问题库：{sum(len(q) for q in questions.values())} 个问题")
    print('')
    
    # 生成内容
    generator.generate_all(questions)
    
    print('')
    print('✅ 完成！')
    print('')
    print('下一步：')
    print('1. 检查生成的内容，优化质量')
    print('2. 运行 geo-publisher.py 生成多平台版本')
    print('3. 发布到各平台')
    print('')


if __name__ == '__main__':
    main()
