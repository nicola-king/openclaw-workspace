#!/usr/bin/env python3
"""
道 Agent - 每日道之智慧 v1.0
太一 AGI · 2026-04-15

每日一条道之智慧，生成精美信息卡片
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class DaoAgent:
    """道 Agent - 每日道之智慧"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.dao_dir = self.skills_dir / "05-content" / "dao-agent"
        self.config_path = self.dao_dir / "config" / "dao-agent-config.json"
        self.data_dir = self.dao_dir / "data"
        self.output_dir = self.data_dir / "output"
        
        # 配置
        self.config = {
            "daily_time": "08:00",
            "card_style": "minimalist",
            "source_pool": ["道德经", "庄子", "列子", "文始真经"],
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
            "道德经": [
                {"chapter": 1, "text": "道可道，非常道。名可名，非常名。", "interpretation": "真正的道是无法言说的，真正的名是无法命名的。"},
                {"chapter": 2, "text": "天下皆知美之为美，斯恶已。皆知善之为善，斯不善已。", "interpretation": "美与恶、善与不善，都是相对而言的。"},
                {"chapter": 8, "text": "上善若水。水善利万物而不争。", "interpretation": "最高的善像水一样，滋养万物而不与万物相争。"},
                {"chapter": 25, "text": "人法地，地法天，天法道，道法自然。", "interpretation": "人、地、天、道，都遵循自然的规律。"},
                {"chapter": 40, "text": "反者道之动，弱者道之用。", "interpretation": "道的运动是循环往复的，道的作用是柔弱不争的。"},
                {"chapter": 42, "text": "道生一，一生二，二生三，三生万物。", "interpretation": "道是万物的本源，从简单到复杂，生成万物。"},
                {"chapter": 64, "text": "千里之行，始于足下。", "interpretation": "再远的路程，也是从脚下第一步开始的。"},
                {"chapter": 81, "text": "天之道，利而不害。圣人之道，为而不争。", "interpretation": "自然的规律是利物而不害，圣人的准则是作为而不争。"},
            ],
            "庄子": [
                {"chapter": "逍遥游", "text": "北冥有鱼，其名为鲲。鲲之大，不知其几千里也。", "interpretation": "超越世俗的束缚，追求精神的自由。"},
                {"chapter": "齐物论", "text": "天地与我并生，而万物与我为一。", "interpretation": "天地万物与我同为一体，没有分别。"},
                {"chapter": "养生主", "text": "吾生也有涯，而知也无涯。以有涯随无涯，殆已。", "interpretation": "生命有限，知识无限，不要用有限的生命追求无限的知识。"},
                {"chapter": "人间世", "text": "来世不可待，往世不可追也。", "interpretation": "未来不可等待，过去不可追回，珍惜当下。"},
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
            "chapter": wisdom["chapter"],
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
│   🌿 道 Agent · 每日智慧                │
│                                         │
│   ─────────────────────────────────     │
│                                         │
│   「{wisdom['text']}」                  │
│                                         │
│   {wisdom['interpretation']}            │
│                                         │
│   ─────────────────────────────────     │
│                                         │
│   📖 {wisdom['source']} · {wisdom['chapter']}  │
│   📅 {wisdom['date']}                   │
│                                         │
└─────────────────────────────────────────┘
"""
        
        return card
    
    def generate_markdown_card(self, wisdom: Dict = None) -> str:
        """生成 Markdown 格式卡片"""
        if wisdom is None:
            wisdom = self.today_wisdom or self.get_daily_wisdom()
        
        md = f"""# 🌿 道 Agent · 每日智慧

> **{wisdom['date']}**

---

## 「{wisdom['text']}」


{wisdom['interpretation']}

---

📖 **{wisdom['source']} · {wisdom['chapter']}**  
🌿 **道 Agent · 太一 AGI**

---

*转发此卡片，分享道之智慧*
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
        output_file = self.output_dir / f"dao-{date_str}.md"
        
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
        print("🌿 道 Agent - 每日智慧")
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
        temp_file = self.output_dir / "temp_dao_card.md"
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
        print(f"📜 道 Agent - 最近{days}天智慧")
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
            print(f"📖 {source} · {wisdom['chapter']}")
            print(f"「{wisdom['text']}」")
        
        print("\n" + "="*60)


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    dao_agent = DaoAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--daily":
            dao_agent.send_daily()
        elif command == "--history":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            dao_agent.show_history(days)
        elif command == "--date":
            date_str = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
            date = datetime.strptime(date_str, "%Y-%m-%d")
            wisdom = dao_agent.get_daily_wisdom(date)
            card = dao_agent.generate_markdown_card(wisdom)
            print(card)
        else:
            print(f"未知命令：{command}")
    else:
        dao_agent.send_daily()


if __name__ == "__main__":
    import sys
    main()
