#!/usr/bin/env python3
"""
周易每日研习
太一 AGI · 2026-04-15

功能：
- 读取周易经典
- 生成今日卦象解读
- 写入研习记录
"""

from pathlib import Path
from datetime import datetime
import random

def main():
    workspace = Path("/home/nicola/.openclaw/workspace")
    logs_dir = workspace / "logs" / "yijing-study"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📖 开始周易研习...")
    
    # 六十四卦列表
    hexagrams = [
        ("乾卦", "天行健，君子以自强不息"),
        ("坤卦", "地势坤，君子以厚德载物"),
        ("屯卦", "云雷屯，君子以经纶"),
        ("蒙卦", "山下出泉，君子以果行育德"),
        ("需卦", "云上于天，君子以饮食宴乐"),
        ("讼卦", "天与水违，君子以作事谋始"),
        ("师卦", "地中有水，君子以容民畜众"),
        ("比卦", "地上有水，先王以建万国亲诸侯"),
    ]
    
    # 根据日期选择卦象（确定性）
    day_of_year = datetime.now().timetuple().tm_yday
    hexagram_index = day_of_year % len(hexagrams)
    today_hexagram = hexagrams[hexagram_index]
    
    print(f"  📖 今日卦象：{today_hexagram[0]}")
    print(f"  💡 象曰：{today_hexagram[1]}")
    
    # 生成研习记录
    study_content = f"""# 周易研习 · {today}

## 📖 今日卦象

**卦名**：{today_hexagram[0]}

**象曰**：{today_hexagram[1]}

---

## 💡 研习心得

{today_hexagram[1]}。

今日宜：
- 反思自身行为是否符合天道
- 在工作和生活中践行卦象智慧
- 记录心得，持续修炼

---

## 📝 明日预告

明日卦象：{hexagrams[(hexagram_index + 1) % len(hexagrams)][0]}

---

*太一 AGI · 周易每日研习*
"""
    
    # 写入研习记录
    reports_dir = workspace / "reports" / "yijing"
    reports_dir.mkdir(parents=True, exist_ok=True)
    study_file = reports_dir / f"yijing-{today}.md"
    study_file.write_text(study_content, encoding='utf-8')
    print(f"  ✅ 研习记录已创建：{study_file}")
    
    print(f"\n✅ 周易研习完成！")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
