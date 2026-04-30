#!/usr/bin/env python3
"""
悟 Agent - 每日悟之智慧 v1.0
太一 AGI · 2026-04-15

每日一条悟之智慧，生成精美信息卡片
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WuAgent:
    """悟 Agent - 每日悟之智慧"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.wu_dir = self.skills_dir / "05-content" / "wu-agent"
        self.config_path = self.wu_dir / "config" / "wu-agent-config.json"
        self.data_dir = self.wu_dir / "data"
        self.output_dir = self.data_dir / "output"
        
        # 配置
        self.config = {
            "daily_time": "20:00",
            "card_style": "zen",
            "source_pool": ["心经", "金刚经", "六祖坛经", "禅宗公案"],
            "output_formats": ["markdown", "image"],
            "auto_send": True,
        }
        
        # 加载配置
        self._load_config()
        
        # 智慧库
        self.wisdom_db = self._load_wisdom_db()
        
        # 今日智慧
        self.today_wisdom = None
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass
        
        # 保存配置
        self.config_path.parent.mkdir(exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def _load_wisdom_db(self) -> Dict:
        """加载智慧库"""
        return {
            "心经": [
                {"text": "色不异空，空不异色。色即是空，空即是色。", "interpretation": "色与空本质上没有差别，都是缘起性空的。"},
                {"text": "受想行识，亦复如是。", "interpretation": "受、想、行、识四蕴，也是如此。"},
                {"text": "是诸法空相，不生不灭，不垢不净，不增不减。", "interpretation": "一切法的空性，没有生灭、垢净、增减的分别。"},
                {"text": "心无挂碍。无挂碍故，无有恐怖。", "interpretation": "心中没有执着，就没有恐惧。"},
                {"text": "揭谛揭谛，波罗揭谛，波罗僧揭谛，菩提萨婆诃。", "interpretation": "去吧，去吧，到彼岸去吧，大家都到彼岸，觉悟圆满。"},
            ],
            "金刚经": [
                {"chapter": 1, "text": "一切有为法，如梦幻泡影。如露亦如电，应作如是观。", "interpretation": "一切有为法都是虚幻的，像梦境、泡沫、露水、闪电一样短暂。"},
                {"chapter": 5, "text": "凡所有相，皆是虚妄。若见诸相非相，即见如来。", "interpretation": "一切相都是虚妄的，若能看透相的本质，就能见到真理。"},
                {"chapter": 32, "text": "应无所住而生其心。", "interpretation": "应该不执着于任何事物，而生起清净的心。"},
            ],
            "六祖坛经": [
                {"text": "菩提本无树，明镜亦非台。本来无一物，何处惹尘埃。", "interpretation": "菩提本不是树，明镜也不是台，本来什么都没有，哪里会沾染尘埃呢。"},
                {"text": "迷时师度，悟了自度。", "interpretation": "迷惑时靠老师度化，觉悟后要自己度化自己。"},
            ],
            "禅宗公案": [
                {"text": "吃茶去。", "interpretation": "赵州禅师的公案，放下执着，活在当下。"},
                {"text": "父母未生前的本来面目是什么？", "interpretation": "参究自己的本性，超越生死的束缚。"},
                {"text": "万法归一，一归何处？", "interpretation": "一切法归于空性，空性又归于何处？"},
            ],
        }
    
    def get_daily_wisdom(self, date: datetime = None) -> Dict:
        """获取每日智慧"""
        if date is None:
            date = datetime.now()
        
        # 使用日期作为种子，确保同一天的智慧相同
        seed = int(date.strftime("%Y%m%d"))
        random.seed(seed)
        
        # 随机选择来源
        source = random.choice(list(self.wisdom_db.keys()))
        wisdom_list = self.wisdom_db[source]
        
        # 随机选择一条智慧
        wisdom = random.choice(wisdom_list)
        
        self.today_wisdom = {
            "date": date.strftime("%Y-%m-%d"),
            "source": source,
            "chapter": wisdom.get("chapter", ""),
            "text": wisdom["text"],
            "interpretation": wisdom["interpretation"],
            "timestamp": datetime.now().isoformat(),
        }
        
        return self.today_wisdom
    
    def generate_card(self, wisdom: Dict = None) -> str:
        """生成信息卡片"""
        if wisdom is None:
            wisdom = self.today_wisdom or self.get_daily_wisdom()
        
        # Markdown 卡片
        card = f"""
┌─────────────────────────────────────────┐
│                                         │
│   🪷 悟 Agent · 每日智慧                │
│                                         │
│   ─────────────────────────────────     │
│                                         │
│   「{wisdom['text']}」                  │
│                                         │
│   {wisdom['interpretation']}            │
│                                         │
│   ─────────────────────────────────     │
│                                         │
│   📖 {wisdom['source']} {wisdom.get('chapter', '')}  │
│   📅 {wisdom['date']}                   │
│                                         │
└─────────────────────────────────────────┘
"""
        
        return card
    
    def generate_markdown_card(self, wisdom: Dict = None) -> str:
        """生成 Markdown 格式卡片"""
        if wisdom is None:
            wisdom = self.today_wisdom or self.get_daily_wisdom()
        
        md = f"""# 🪷 悟 Agent · 每日智慧

> **{wisdom['date']}**

---

## 「{wisdom['text']}」


{wisdom['interpretation']}

---

📖 **{wisdom['source']}** {wisdom.get('chapter', '')}  
🪷 **悟 Agent · 太一 AGI**

---

*转发此卡片，分享悟之智慧*
"""
        
        return md
    
    def save_card(self, card: str = None, wisdom: Dict = None):
        """保存卡片"""
        if wisdom is None:
            wisdom = self.today_wisdom or self.get_daily_wisdom()
        
        if card is None:
            card = self.generate_markdown_card(wisdom)
        
        # 保存目录
        date_str = wisdom["date"].replace("-", "")
        output_file = self.output_dir / f"wu-{date_str}.md"
        
        self.output_dir.mkdir(exist_ok=True)
        output_file.write_text(card, encoding="utf-8")
        
        print(f"💾 卡片已保存：{output_file}")
        return output_file
    
    def _get_last_sent_date(self) -> str:
        """获取上次发送日期"""
        state_file = self.output_dir / ".last_sent.json"
        if state_file.exists():
            try:
                import json
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                return state.get('last_sent_date', '')
            except (json.JSONDecodeError, IOError):
                return ''
        return ''
    
    def _mark_sent(self):
        """标记今日已发送"""
        state_file = self.output_dir / ".last_sent.json"
        try:
            import json
            state = {
                'last_sent_date': datetime.now().strftime('%Y-%m-%d'),
                'last_sent_at': datetime.now().isoformat()
            }
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def send_daily(self):
        """发送每日智慧"""
        print("\n" + "="*60)
        print("🪷 悟 Agent - 每日智慧")
        print("="*60)
        
        # 检查今日是否已发送
        today = datetime.now().strftime('%Y-%m-%d')
        last_sent = self._get_last_sent_date()
        if last_sent == today:
            print(f"⏭️  今日智慧已发送过 ({today})，跳过")
            return None
        
        # 获取今日智慧
        wisdom = self.get_daily_wisdom()
        
        # 生成卡片
        card = self.generate_markdown_card(wisdom)
        
        # 显示
        print(card)
        
        # 保存
        self.save_card(card, wisdom)
        
        # 发送到 Telegram
        if self.config.get("auto_send", True):
            self._send_to_telegram(card)
            # 标记已发送
            self._mark_sent()
        
        print("="*60)
        
        return wisdom
    
    def _send_to_telegram(self, card: str):
        """发送到 Telegram"""
        # 临时保存卡片
        temp_file = self.output_dir / "temp_wu_card.md"
        temp_file.write_text(card, encoding="utf-8")
        
        # 调用发送脚本
        send_script = self.workspace_root / "scripts" / "send-md-to-telegram.py"
        if send_script.exists():
            try:
                import subprocess
                result = subprocess.run(
                    ["python3", str(send_script), str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print("✅ 已发送到 Telegram")
                else:
                    print(f"⚠️  发送失败：{result.stderr[:100]}")
            except Exception as e:
                print(f"⚠️  发送异常：{str(e)[:100]}")
    
    def show_history(self, days: int = 7):
        """显示历史智慧"""
        print("\n" + "="*60)
        print(f"📜 悟 Agent - 最近{days}天智慧")
        print("="*60)
        
        today = datetime.now()
        for i in range(days):
            date = today - timedelta(days=i)
            seed = int(date.strftime("%Y%m%d"))
            random.seed(seed)
            
            source = random.choice(list(self.wisdom_db.keys()))
            wisdom_list = self.wisdom_db[source]
            wisdom = random.choice(wisdom_list)
            
            print(f"\n📅 {date.strftime('%Y-%m-%d')}")
            print(f"📖 {source}")
            print(f"「{wisdom['text']}」")
        
        print("\n" + "="*60)


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    wu_agent = WuAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--daily":
            wu_agent.send_daily()
        elif command == "--history":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            wu_agent.show_history(days)
        elif command == "--date":
            date_str = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
            date = datetime.strptime(date_str, "%Y-%m-%d")
            wisdom = wu_agent.get_daily_wisdom(date)
            card = wu_agent.generate_markdown_card(wisdom)
            print(card)
        else:
            print(f"未知命令：{command}")
    else:
        wu_agent.send_daily()


if __name__ == "__main__":
    import sys
    main()
