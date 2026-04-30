#!/usr/bin/env python3
"""
GEO 自动问题生成器
功能：基于种子关键词，批量生成用户问题库
使用：python3 geo-question-generator.py

开源免费，基于 OpenClaw 生态
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    'topic': '番茄种植',  # 主题
    'output_dir': '/home/nicola/.openclaw/workspace/geo-questions',
    'categories': [
        '选购问题',
        '种植技巧',
        '病虫害防治',
        '水肥管理',
        '收获储存',
        '常见问题'
    ],
    'questions_per_category': 15,
    'model': 'qwen3.5-plus'  # 使用百炼免费额度
}

# 提示词模板
PROMPT_TEMPLATE = """你是一名{topic}领域的专家，有 10 年实践经验。

请生成{count}个用户在这个领域会问的问题，类别是：{category}

要求：
1. 问题要具体，像真实用户会问的（口语化）
2. 包含不同场景（新手/有经验/遇到问题）
3. 包含不同意图（信息收集/购买决策/问题解决）
4. 避免过于宽泛的问题

示例格式（不要包含在输出中）：
- 新手第一次种番茄，应该买什么品种？
- 番茄苗叶子发黄是什么原因？
- 阳台种植番茄需要多大盆？

直接输出问题列表，每行一个问题，不要编号。
"""

class GeoQuestionGenerator:
    """GEO 问题生成器"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 问题库
        self.questions = {cat: [] for cat in config['categories']}
    
    def generate_questions(self, category: str, count: int) -> list:
        """
        生成某类别的问题
        
        使用 OpenClaw sessions_spawn 调用 AI 生成
        或者直接返回内置示例问题库
        """
        # 注意：实际使用时可以用 OpenClaw 调用 AI
        # 这里使用内置示例问题库（无需 API）
        sample_questions = {
            '选购问题': [
                '新手第一次种番茄，应该买什么品种？',
                '番茄苗多少钱一棵算正常？',
                '网上买番茄苗靠谱吗？',
                '番茄种子和苗哪个更适合新手？',
                '矮生番茄和高生番茄有什么区别？',
                '樱桃番茄和大番茄哪个更好种？',
                '番茄苗多大可以移栽？',
                '买番茄苗要看哪些特征？',
                '什么季节买番茄苗最合适？',
                '盆栽番茄苗选多大的盆？',
                '番茄苗叶子多少片算健康？',
                '如何判断番茄苗有没有病害？',
                '番茄品种那么多，怎么选适合自己地区的？',
                '有机番茄苗和普通苗有什么区别？',
                '番茄苗需要买嫁接的吗？'
            ],
            '种植技巧': [
                '番茄苗多久浇一次水？',
                '番茄需要搭架子吗？',
                '番茄什么时候打顶最好？',
                '阳台种植番茄需要多大光照？',
                '番茄苗移栽后多久能结果？',
                '番茄种植株距多少合适？',
                '番茄什么时候施肥效果最好？',
                '番茄需要人工授粉吗？',
                '番茄叶子太多要不要修剪？',
                '番茄结果后多久摘一次？',
                '盆栽番茄怎么防止倒伏？',
                '番茄苗期需要遮阴吗？',
                '番茄连续种植需要轮作吗？',
                '番茄和什么蔬菜可以套种？',
                '番茄种植需要覆盖地膜吗？'
            ],
            '病虫害防治': [
                '番茄叶子发黄是什么原因？',
                '番茄叶子长黑斑怎么办？',
                '番茄苗徒长了怎么补救？',
                '番茄果实开裂是怎么回事？',
                '番茄长蚜虫用什么药？',
                '番茄青枯病怎么防治？',
                '番茄叶子卷曲是什么问题？',
                '番茄脐腐病怎么预防？',
                '番茄白粉病用什么药？',
                '番茄苗倒了还能救吗？',
                '番茄叶子有虫洞怎么办？',
                '番茄根腐病怎么治疗？',
                '番茄落花是什么原因？',
                '番茄果实有黑点能吃吗？',
                '如何预防番茄病虫害？'
            ],
            '水肥管理': [
                '番茄多久施一次肥？',
                '番茄用什么肥料最好？',
                '番茄浇水多了怎么办？',
                '番茄需要施有机肥还是化肥？',
                '番茄结果期需要追肥吗？',
                '番茄叶子发黄是缺什么肥？',
                '番茄浇水是早上还是晚上好？',
                '番茄可以用淘米水浇吗？',
                '番茄施肥离根部多远？',
                '番茄苗期需要施肥吗？',
                '番茄缺氮缺磷缺钾怎么判断？',
                '番茄可以叶面施肥吗？',
                '番茄浇水要浇透吗？',
                '番茄用什么有机肥最好？',
                '番茄施肥过量怎么补救？'
            ],
            '收获储存': [
                '番茄什么时候采摘最好？',
                '番茄摘下来能放多久？',
                '青番茄怎么催熟？',
                '番茄可以放冰箱保存吗？',
                '番茄一次摘太多怎么保存？',
                '番茄怎么判断熟没熟？',
                '番茄摘的时候要不要留蒂？',
                '番茄可以冷冻保存吗？',
                '番茄做酱怎么保存时间长？',
                '番茄和什么一起存放会坏得快？',
                '番茄摘下来后还能继续变红吗？',
                '番茄常温能放几天？',
                '番茄怎么保存最新鲜？',
                '番茄可以做干保存吗？',
                '番茄种子怎么保存明年种？'
            ],
            '常见问题': [
                '番茄苗多久能成活？',
                '番茄为什么只开花不结果？',
                '番茄一棵能结多少果？',
                '番茄种植多久能收获？',
                '番茄可以种在室内吗？',
                '番茄夏天会热死吗？',
                '番茄冬天能过冬吗？',
                '番茄叶子发黄掉叶子怎么办？',
                '番茄苗长太高了怎么办？',
                '番茄结果后植株死了正常吗？',
                '番茄可以扦插繁殖吗？',
                '番茄一年能种几季？',
                '番茄种植失败最常见原因？',
                '新手种番茄最容易犯什么错？',
                '番茄种植需要买专用土吗？'
            ]
        }
        
        return sample_questions.get(category, [])[:count]
    
    def generate_all(self):
        """生成所有类别的问题"""
        print(f"🚀 开始生成 [{self.config['topic']}] 问题库...")
        print(f"📂 输出目录：{self.output_dir}")
        print('-' * 60)
        
        for category in self.config['categories']:
            print(f"\n📋 生成类别：{category}")
            questions = self.generate_questions(
                category, 
                self.config['questions_per_category']
            )
            self.questions[category] = questions
            print(f"   ✅ 生成 {len(questions)} 个问题")
        
        # 保存结果
        self.save()
        
        # 打印统计
        self.print_summary()
    
    def save(self):
        """保存问题库"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON 格式
        json_file = self.output_dir / f"questions_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=2)
        print(f"\n💾 JSON 已保存：{json_file}")
        
        # Markdown 格式
        md_file = self.output_dir / f"questions_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.config['topic']} - GEO 问题库\n\n")
            f.write(f"> 生成时间：{datetime.now().isoformat()}\n")
            f.write(f"> 问题总数：{sum(len(q) for q in self.questions.values())}\n\n")
            
            for category, questions in self.questions.items():
                f.write(f"## {category}\n\n")
                for q in questions:
                    f.write(f"- {q}\n")
                f.write("\n")
        print(f"💾 Markdown 已保存：{md_file}")
        
        # 纯文本格式（方便复制）
        txt_file = self.output_dir / f"questions_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            for category, questions in self.questions.items():
                f.write(f"=== {category} ===\n")
                for q in questions:
                    f.write(f"{q}\n")
                f.write("\n")
        print(f"💾 文本已保存：{txt_file}")
    
    def print_summary(self):
        """打印统计摘要"""
        print('\n' + '=' * 60)
        print('📊 问题库统计')
        print('=' * 60)
        
        total = 0
        for category, questions in self.questions.items():
            count = len(questions)
            total += count
            bar = '█' * (count // 2)
            print(f"{category:<12} │{bar}│ {count}个")
        
        print('-' * 60)
        print(f"{'总计':<12} │{'█' * (total // 2)}│ {total}个")
        print('=' * 60)


def main():
    """主程序"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  GEO 自动问题生成器 v1.0                                  ║')
    print('║  开源免费 | 基于 OpenClaw 生态                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    generator = GeoQuestionGenerator(CONFIG)
    generator.generate_all()
    
    print('')
    print('✅ 完成！')
    print('')
    print('下一步：')
    print('1. 查看生成的问题库')
    print('2. 用 geo-content-generator.py 生成内容')
    print('3. 用 geo-publisher.py 发布到多平台')
    print('')


if __name__ == '__main__':
    main()
