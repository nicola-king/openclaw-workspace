#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道 Agent 每日道家智慧推送

功能:
- 每日早晨 8 点推送
- 道家经典智慧
- 卡片形式生成
- Telegram 发送

作者：太一 AGI
创建：2026-04-12 23:58
版本：v1.0
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('DailyDaoWisdom')


class DailyDaoWisdom:
    """每日道家智慧"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.dao_dir = self.workspace / 'skills' / 'dao-agent'
        self.wisdom_dir = self.workspace / 'wisdom'
        
        # 道家经典智慧库
        self.dao_wisdom = {
            '道德经': [
                {'verse': '道可道，非常道。名可名，非常名。', 'chapter': '第一章', 'wisdom': '道的本质超越言语'},
                {'verse': '天下皆知美之为美，斯恶已。', 'chapter': '第二章', 'wisdom': '相对性的智慧'},
                {'verse': '上善若水。水善利万物而不争。', 'chapter': '第八章', 'wisdom': '谦下不争的品德'},
                {'verse': '致虚极，守静笃。', 'chapter': '第十六章', 'wisdom': '虚静的心境'},
                {'verse': '人法地，地法天，天法道，道法自然。', 'chapter': '第二十五章', 'wisdom': '顺应自然'},
                {'verse': '重为轻根，静为躁君。', 'chapter': '第二十六章', 'wisdom': '稳重与宁静'},
                {'verse': '知足不辱，知止不殆。', 'chapter': '第四十四章', 'wisdom': '知足常乐'},
                {'verse': '大成若缺，其用不弊。', 'chapter': '第四十五章', 'wisdom': '完美的不完美'},
                {'verse': '祸莫大于不知足，咎莫大于欲得。', 'chapter': '第四十六章', 'wisdom': '知足常乐'},
                {'verse': '为学日益，为道日损。', 'chapter': '第四十八章', 'wisdom': '减法的智慧'},
            ],
            '庄子': [
                {'verse': '北冥有鱼，其名为鲲。', 'chapter': '逍遥游', 'wisdom': '自由的精神'},
                {'verse': '吾生也有涯，而知也无涯。', 'chapter': '养生主', 'wisdom': '知识的无限'},
                {'verse': '相濡以沫，不如相忘于江湖。', 'chapter': '大宗师', 'wisdom': '放手的智慧'},
                {'verse': '天地与我并生，万物与我为一。', 'chapter': '齐物论', 'wisdom': '万物一体'},
                {'verse': '得鱼而忘荃，得兔而忘蹄。', 'chapter': '外物', 'wisdom': '得意忘言'},
            ],
            '列子': [
                {'verse': '愚公移山，精卫填海。', 'chapter': '汤问', 'wisdom': '坚持的力量'},
                {'verse': '杞人忧天，庸人自扰。', 'chapter': '天瑞', 'wisdom': '放下忧虑'},
            ],
        }
        
        logger.info("📿 道 Agent 每日智慧推送已初始化")
        logger.info(f"  收录经典：{len(self.dao_wisdom)} 部")
    
    def get_daily_wisdom(self) -> Dict:
        """获取每日智慧"""
        # 根据日期选择智慧 (确保同一天相同)
        today = datetime.now().strftime('%Y%m%d')
        seed = int(today) % 100
        
        # 随机选择经典
        classics = list(self.dao_wisdom.keys())
        classic = classics[seed % len(classics)]
        
        # 随机选择句子
        verses = self.dao_wisdom[classic]
        verse = verses[seed % len(verses)]
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'classic': classic,
            'verse': verse['verse'],
            'chapter': verse['chapter'],
            'wisdom': verse['wisdom'],
            'category': '道家智慧',
        }
    
    def generate_card(self, wisdom: Dict) -> str:
        """生成智慧卡片文本"""
        card = f"""
╔═══════════════════════════════════════════╗
║           🌅 每日道家智慧                  ║
╠═══════════════════════════════════════════╣
║                                           ║
║  📅 日期：{wisdom['date']}                      ║
║                                           ║
║  📖 经典：《{wisdom['classic']}》                  ║
║                                           ║
║  📜 原文：                                  ║
║  {wisdom['verse']}                    ║
║                                           ║
║  📝 章节：{wisdom['chapter']}                          ║
║                                           ║
║  💡 智慧：{wisdom['wisdom']}                      ║
║                                           ║
║  🙏 愿以此智慧，启迪心灵，顺应自然          ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
        return card
    
    def save_wisdom(self, wisdom: Dict):
        """保存智慧到文件"""
        self.wisdom_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存到 JSON
        wisdom_file = self.wisdom_dir / 'dao_wisdom_history.json'
        if wisdom_file.exists():
            with open(wisdom_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(wisdom)
        
        with open(wisdom_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        # 保存到 Markdown
        md_file = self.wisdom_dir / 'dao_wisdom_today.md'
        card = self.generate_card(wisdom)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(card)
        
        logger.info(f"✅ 道家智慧已保存：{md_file}")
    
    def send_to_telegram(self, wisdom: Dict):
        """发送到 Telegram (待实现)"""
        card = self.generate_card(wisdom)
        logger.info("📤 准备发送到 Telegram:")
        logger.info(card)
        # TODO: 实现 Telegram 发送
        # 可以使用现有的 Telegram Bot API
    
    def run(self):
        """运行每日推送"""
        logger.info("🌅 开始运行道 Agent 每日智慧推送...")
        
        # 获取今日智慧
        wisdom = self.get_daily_wisdom()
        
        # 生成卡片
        card = self.generate_card(wisdom)
        
        # 保存
        self.save_wisdom(wisdom)
        
        # 发送
        self.send_to_telegram(wisdom)
        
        logger.info("✅ 道 Agent 每日智慧推送完成！")
        
        return wisdom


def main():
    logger.info("🌅 道 Agent 每日道家智慧推送启动...")
    
    dao_wisdom = DailyDaoWisdom()
    wisdom = dao_wisdom.run()
    
    print(dao_wisdom.generate_card(wisdom))


if __name__ == '__main__':
    main()
