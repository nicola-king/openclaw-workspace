#!/usr/bin/env python3
"""
先秦经典每日研习
太一 AGI · 2026-04-15

功能：
- 轮询学习先秦经典（道德经、论语、庄子等）
- 生成今日学习摘录
- 写入研习记录
"""

from pathlib import Path
from datetime import datetime

# 先秦经典摘录
CLASSICS = {
    "道德经": [
        ("第一章", "道可道，非常道。名可名，非常名。"),
        ("第八章", "上善若水。水善利万物而不争，处众人之所恶，故几于道。"),
        ("第二十五章", "人法地，地法天，天法道，道法自然。"),
        ("第四十章", "反者道之动，弱者道之用。"),
    ],
    "论语": [
        ("学而篇", "学而时习之，不亦说乎？"),
        ("为政篇", "为政以德，譬如北辰，居其所而众星共之。"),
        ("里仁篇", "里仁为美。择不处仁，焉得知？"),
        ("述而篇", "三人行，必有我师焉。"),
    ],
    "庄子": [
        ("逍遥游", "北冥有鱼，其名为鲲。鲲之大，不知其几千里也。"),
        ("齐物论", "天地与我并生，而万物与我为一。"),
        ("养生主", "吾生也有涯，而知也无涯。"),
    ],
    "孟子": [
        ("公孙丑上", "我善养吾浩然之气。"),
        ("滕文公下", "富贵不能淫，贫贱不能移，威武不能屈。"),
    ],
}

def main():
    workspace = Path("/home/nicola/.openclaw/workspace")
    logs_dir = workspace / "logs" / "xianqin-study"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📖 开始先秦经典研习...")
    
    # 根据日期选择经典和章节（确定性）
    day_of_year = datetime.now().timetuple().tm_yday
    classics_list = list(CLASSICS.items())
    classic_index = day_of_year % len(classics_list)
    classic_name, passages = classics_list[classic_index]
    passage_index = day_of_year % len(passages)
    today_passage = passages[passage_index]
    
    print(f"  📖 今日经典：{classic_name} · {today_passage[0]}")
    print(f"  💡 摘录：{today_passage[1]}")
    
    # 生成研习记录
    study_content = f"""# 先秦经典研习 · {today}

## 📖 今日经典

**典籍**：{classic_name}
**篇章**：{today_passage[0]}

**原文**：

> {today_passage[1]}

---

## 💡 研习心得

{today_passage[1]}

今日宜：
- 反复诵读，体会经典智慧
- 反思如何在现代生活中践行
- 记录心得，持续修炼

---

## 📝 明日预告

明日将学习：{classics_list[(classic_index + 1) % len(classics_list)][0]}

---

*太一 AGI · 先秦经典每日研习*
"""
    
    # 写入研习记录
    reports_dir = workspace / "reports" / "xianqin"
    reports_dir.mkdir(parents=True, exist_ok=True)
    study_file = reports_dir / f"xianqin-{today}.md"
    study_file.write_text(study_content, encoding='utf-8')
    print(f"  ✅ 研习记录已创建：{study_file}")
    
    print(f"\n✅ 先秦经典研习完成！")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
