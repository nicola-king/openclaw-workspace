#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
悟 Agent 每日佛家智慧推送

功能:
- 每日早晨 8 点推送
- 佛家经典智慧
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
logger = logging.getLogger('DailyBuddhistWisdom')


class DailyBuddhistWisdom:
    """每日佛家智慧"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.wu_dir = self.workspace / 'skills' / 'wu-enlightenment'
        self.wisdom_dir = self.workspace / 'wisdom'
        
        # 佛家经典智慧库
        self.buddhist_wisdom = {
            '心经': [
                {'verse': '观自在菩萨，行深般若波罗蜜多时，照见五蕴皆空，度一切苦厄。', 'wisdom': '观照内心，超越苦难'},
                {'verse': '色不异空，空不异色，色即是空，空即是色。', 'wisdom': '空有不二的智慧'},
                {'verse': '心无挂碍，无挂碍故，无有恐怖。', 'wisdom': '放下执着，心得自在'},
                {'verse': '揭谛揭谛，波罗揭谛，波罗僧揭谛，菩提萨婆诃。', 'wisdom': '渡到彼岸的咒语'},
            ],
            '金刚经': [
                {'verse': '应无所住而生其心。', 'wisdom': '不执着的心'},
                {'verse': '凡所有相，皆是虚妄。', 'wisdom': '超越表象'},
                {'verse': '一切有为法，如梦幻泡影。', 'wisdom': '诸法空相'},
                {'verse': '若菩萨有我相、人相、众生相、寿者相，即非菩萨。', 'wisdom': '无四相'},
            ],
            '六祖坛经': [
                {'verse': '菩提本无树，明镜亦非台。本来无一物，何处惹尘埃。', 'wisdom': '本自清净'},
                {'verse': '何期自性，本自清净。', 'wisdom': '自性本净'},
                {'verse': '佛法在世间，不离世间觉。', 'wisdom': '入世修行'},
                {'verse': '不思善，不思恶，正与么时，那个是明上座本来面目。', 'wisdom': '明心见性'},
            ],
            '法华经': [
                {'verse': '一切众生皆可成佛。', 'wisdom': '众生平等'},
                {'verse': '开权显实，会三归一。', 'wisdom': '究竟一乘'},
            ],
            '华严经': [
                {'verse': '一即一切，一切即一。', 'wisdom': '法界缘起'},
                {'verse': '心、佛、众生，三无差别。', 'wisdom': '平等无二'},
            ],
            '地藏经': [
                {'verse': '地狱不空，誓不成佛。', 'wisdom': '大愿精神'},
                {'verse': '众生度尽，方证菩提。', 'wisdom': '利他精神'},
            ],
        }
        
        logger.info("📿 悟 Agent 每日佛家智慧推送已初始化")
        logger.info(f"  收录经典：{len(self.buddhist_wisdom)} 部")
    
    def get_daily_wisdom(self) -> Dict:
        """获取每日智慧"""
        # 根据日期选择智慧 (确保同一天相同)
        today = datetime.now().strftime('%Y%m%d')
        seed = int(today) % 100
        
        # 随机选择经典
        classics = list(self.buddhist_wisdom.keys())
        classic = classics[seed % len(classics)]
        
        # 随机选择句子
        verses = self.buddhist_wisdom[classic]
        verse = verses[seed % len(verses)]
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'classic': classic,
            'verse': verse['verse'],
            'wisdom': verse['wisdom'],
            'category': '佛家智慧',
        }
    
    def generate_card(self, wisdom: Dict) -> str:
        """生成智慧卡片文本"""
        card = f"""
╔═══════════════════════════════════════════╗
║           🌸 每日佛家智慧                  ║
╠═══════════════════════════════════════════╣
║                                           ║
║  📅 日期：{wisdom['date']}                      ║
║                                           ║
║  📖 经典：《{wisdom['classic']}》                  ║
║                                           ║
║  📜 原文：                                  ║
║  {wisdom['verse']}                    ║
║                                           ║
║  💡 智慧：{wisdom['wisdom']}                      ║
║                                           ║
║  🙏 愿以此智慧，启迪心灵，明心见性          ║
║  🪷 南无阿弥陀佛                          ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
        return card
    
    def save_wisdom(self, wisdom: Dict):
        """保存智慧到文件"""
        self.wisdom_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存到 JSON
        wisdom_file = self.wisdom_dir / 'buddhist_wisdom_history.json'
        if wisdom_file.exists():
            with open(wisdom_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(wisdom)
        
        with open(wisdom_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        # 保存到 Markdown
        md_file = self.wisdom_dir / 'buddhist_wisdom_today.md'
        card = self.generate_card(wisdom)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(card)
        
        logger.info(f"✅ 佛家智慧已保存：{md_file}")
    
    def send_to_telegram(self, wisdom: Dict):
        """发送到 Telegram (待实现)"""
        card = self.generate_card(wisdom)
        logger.info("📤 准备发送到 Telegram:")
        logger.info(card)
        # TODO: 实现 Telegram 发送
    
    def run(self):
        """运行每日推送"""
        logger.info("🌸 开始运行悟 Agent 每日佛家智慧推送...")
        
        # 获取今日智慧
        wisdom = self.get_daily_wisdom()
        
        # 生成卡片
        card = self.generate_card(wisdom)
        
        # 保存
        self.save_wisdom(wisdom)
        
        # 发送
        self.send_to_telegram(wisdom)
        
        logger.info("✅ 悟 Agent 每日佛家智慧推送完成！")
        
        return wisdom


def main():
    logger.info("🌸 悟 Agent 每日佛家智慧推送启动...")
    
    buddhist_wisdom = DailyBuddhistWisdom()
    wisdom = buddhist_wisdom.run()
    
    print(buddhist_wisdom.generate_card(wisdom))


if __name__ == '__main__':
    main()
