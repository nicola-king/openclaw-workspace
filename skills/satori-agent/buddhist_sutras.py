#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
悟 Agent 佛教佛经经典知识库

收录佛教核心经典:
- 心经
- 金刚经
- 六祖坛经
- 法华经
- 华严经
- 楞严经
- 无量寿经
- 地藏经
- 药师经
- 阿弥陀经

作者：太一 AGI
创建：2026-04-12 23:36
版本：v1.0
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('BuddhistSutras')


class BuddhistSutras:
    """佛教佛经经典知识库"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.wu_dir = self.workspace / 'skills' / 'wu-enlightenment'
        
        # 佛经经典
        self.sutras = {
            '心经': {
                'full_name': '般若波罗蜜多心经',
                'category': '般若部',
                'verses': [
                    '观自在菩萨，行深般若波罗蜜多时，照见五蕴皆空，度一切苦厄。',
                    '舍利子，色不异空，空不异色，色即是空，空即是色，受想行识，亦复如是。',
                    '舍利子，是诸法空相，不生不灭，不垢不净，不增不减。',
                    '是故空中无色，无受想行识，无眼耳鼻舌身意，无色声香味触法。',
                    '无眼界，乃至无意识界，无无明，亦无无明尽，乃至无老死，亦无老死尽。',
                    '无苦集灭道，无智亦无得，以无所得故。',
                    '菩提萨埵，依般若波罗蜜多故，心无挂碍。',
                    '无挂碍故，无有恐怖，远离颠倒梦想，究竟涅槃。',
                    '三世诸佛，依般若波罗蜜多故，得阿耨多罗三藐三菩提。',
                    '故知般若波罗蜜多，是大神咒，是大明咒，是无上咒，是无等等咒。',
                    '能除一切苦，真实不虚。',
                    '故说般若波罗蜜多咒，即说咒曰：揭谛揭谛，波罗揭谛，波罗僧揭谛，菩提萨婆诃。',
                ],
                'wisdom': '色即是空，空即是色 - 诸法空相，不生不灭',
            },
            '金刚经': {
                'full_name': '金刚般若波罗蜜经',
                'category': '般若部',
                'verses': [
                    '如是我闻，一时佛在舍卫国祇树给孤独园，与大比丘众千二百五十人俱。',
                    '尔时世尊食时，著衣持钵，入舍卫大城乞食。',
                    '于其城中次第乞已，还至本处。饭食讫，收衣钵，洗足已，敷座而坐。',
                    '时长老须菩提在大众中，即从座起偏袒右肩，右膝著地，合掌恭敬而白佛言。',
                    '希有世尊，如来善护念诸菩萨，善付嘱诸菩萨。',
                    '世尊，善男子善女人，发阿耨多罗三藐三菩提心，应云何住？云何降伏其心？',
                    '佛言：善哉善哉。须菩提，如汝所说，如来善护念诸菩萨，善付嘱诸菩萨。',
                    '汝今谛听，当为汝说。善男子善女人，发阿耨多罗三藐三菩提心，应如是住，如是降伏其心。',
                    '唯然世尊，愿乐欲闻。',
                    '佛告须菩提：诸菩萨摩诃萨应如是降伏其心。',
                    '所有一切众生之类，若卵生、若胎生、若湿生、若化生，若有色、若无色，若有想、若无想、若非有想非无想，我皆令入无余涅槃而灭度之。',
                    '如是灭度无量无数无边众生，实无众生得灭度者。',
                    '何以故？须菩提，若菩萨有我相、人相、众生相、寿者相，即非菩萨。',
                ],
                'wisdom': '应无所住而生其心 - 凡所有相，皆是虚妄',
            },
            '六祖坛经': {
                'full_name': '六祖大师法宝坛经',
                'category': '禅宗',
                'verses': [
                    '菩提本无树，明镜亦非台。',
                    '本来无一物，何处惹尘埃。',
                    '何期自性，本自清净。',
                    '何期自性，本不生灭。',
                    '何期自性，本自具足。',
                    '何期自性，本无动摇。',
                    '何期自性，能生万法。',
                    '不思善，不思恶，正与么时，那个是明上座本来面目。',
                    '佛法在世间，不离世间觉。',
                    '离世觅菩提，恰如求兔角。',
                ],
                'wisdom': '明心见性，直指人心 - 顿悟成佛',
            },
            '法华经': {
                'full_name': '妙法莲华经',
                'category': '法华部',
                'wisdom': '开权显实，会三归一 - 一切众生皆可成佛',
            },
            '华严经': {
                'full_name': '大方广佛华严经',
                'category': '华严部',
                'wisdom': '一即一切，一切即一 - 法界缘起',
            },
            '楞严经': {
                'full_name': '大佛顶首楞严经',
                'category': '楞严部',
                'wisdom': '楞严咒心，降魔除障 - 七处征心，十番显见',
            },
            '无量寿经': {
                'full_name': '佛说无量寿经',
                'category': '净土部',
                'wisdom': '阿弥陀佛四十八大愿 - 念佛往生净土',
            },
            '地藏经': {
                'full_name': '地藏菩萨本愿经',
                'category': '地藏部',
                'wisdom': '地狱不空，誓不成佛 - 大愿地藏菩萨',
            },
            '药师经': {
                'full_name': '药师琉璃光如来本愿功德经',
                'category': '药师部',
                'wisdom': '药师佛十二大愿 - 消灾延寿',
            },
            '阿弥陀经': {
                'full_name': '佛说阿弥陀经',
                'category': '净土部',
                'wisdom': '执持名号，一心不乱 - 往生西方极乐世界',
            },
        }
        
        logger.info("📿 佛教佛经经典知识库已初始化")
        logger.info(f"  收录经典：{len(self.sutras)} 部")
    
    def get_sutra(self, name: str) -> Dict:
        """获取佛经"""
        return self.sutras.get(name, {})
    
    def get_all_sutras(self) -> Dict:
        """获取全部佛经"""
        return self.sutras
    
    def search_wisdom(self, keyword: str) -> List[Dict]:
        """搜索智慧"""
        results = []
        for name, sutra in self.sutras.items():
            if keyword in name or keyword in sutra.get('wisdom', ''):
                results.append({
                    'name': name,
                    'full_name': sutra.get('full_name', ''),
                    'wisdom': sutra.get('wisdom', ''),
                })
        return results
    
    def generate_daily_wisdom(self) -> str:
        """生成每日智慧"""
        import random
        sutra_name = random.choice(list(self.sutras.keys()))
        sutra = self.sutras[sutra_name]
        
        wisdom = f"""📿 今日佛教智慧

经典：{sutra.get('full_name', sutra_name)}
类别：{sutra.get('category', '')}

智慧：{sutra.get('wisdom', '')}

🙏 愿以此智慧，启迪心灵，明心见性"""
        
        return wisdom
    
    def save_to_file(self):
        """保存到文件"""
        output_file = self.wu_dir / 'buddhist_sutras_knowledge_base.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.sutras, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 佛经知识库已保存：{output_file}")


def main():
    logger.info("📿 佛教佛经经典知识库启动...")
    
    sutras = BuddhistSutras()
    
    # 显示全部佛经
    logger.info(f"📚 收录佛经：{len(sutras.sutras)} 部")
    for name, sutra in sutras.sutras.items():
        logger.info(f"  - {sutra.get('full_name', name)} ({sutra.get('category', '')})")
    
    # 生成每日智慧
    daily_wisdom = sutras.generate_daily_wisdom()
    logger.info(f"\n{daily_wisdom}")
    
    # 保存到文件
    sutras.save_to_file()
    
    logger.info("✅ 佛教佛经经典知识库完成！")


if __name__ == '__main__':
    main()
