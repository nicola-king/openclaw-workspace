#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-wisdom-card.py - 生成智慧卡片图片
用法：python3 scripts/generate-wisdom-card.py [道家|佛家] [输出文件名]
"""

import sys
import random
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
WISDOM_FILE = os.path.join(WORKSPACE, "wisdom/dao-buddha-quotes.md")
OUTPUT_DIR = os.path.join(WORKSPACE, "wisdom/cards")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 智慧语录库
QUOTES = {
    "道家": [
        ("道可道，非常道；名可名，非常名。", "《道德经》"),
        ("上善若水，水善利万物而不争。", "《道德经》"),
        ("致虚极，守静笃。", "《道德经》"),
        ("知人者智，自知者明。胜人者有力，自胜者强。", "《道德经》"),
        ("大道至简，无为而治。", "《道德经》"),
        ("反者道之动，弱者道之用。", "《道德经》"),
        ("祸兮福之所倚，福兮祸之所伏。", "《道德经》"),
        ("人法地，地法天，天法道，道法自然。", "《道德经》"),
        ("人生天地之间，若白驹过隙，忽然而已。", "《庄子》"),
        ("相濡以沫，不如相忘于江湖。", "《庄子》"),
        ("天地与我并生，万物与我为一。", "《庄子》"),
        ("朴素而天下莫能与之争美。", "《庄子》"),
        ("大知闲闲，小知间间。", "《庄子》"),
    ],
    "佛家": [
        ("色不异空，空不异色；色即是空，空即是色。", "《心经》"),
        ("心无挂碍，无挂碍故，无有恐怖。", "《心经》"),
        ("一切有为法，如梦幻泡影，如露亦如电，应作如是观。", "《金刚经》"),
        ("应无所住而生其心。", "《金刚经》"),
        ("凡所有相，皆是虚妄。", "《金刚经》"),
        ("过去心不可得，现在心不可得，未来心不可得。", "《金刚经》"),
        ("菩提本无树，明镜亦非台。本来无一物，何处惹尘埃。", "慧能"),
        ("日日是好日。", "禅宗"),
        ("平常心是道。", "禅宗"),
        ("烦恼即菩提。", "禅宗"),
        ("一花一世界，一叶一菩提。", "佛家箴言"),
        ("命由己造，相由心生。", "佛家箴言"),
        ("缘起性空。", "佛家箴言"),
    ]
}

def get_random_quote(category):
    """随机获取一句智慧语录"""
    quotes = QUOTES.get(category, QUOTES["道家"])
    return random.choice(quotes)

def create_wisdom_card(category, quote, source, output_path):
    """创建智慧卡片图片"""
    
    # 图片尺寸
    width = 800
    height = 1200
    
    # 创建图片（米白色背景）
    img = Image.new('RGB', (width, height), color='#FDFBF7')
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体（使用系统字体）
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:\\Windows\\Fonts\\simhei.ttf",
    ]
    
    # 使用默认字体
    try:
        font_large = ImageFont.truetype(font_paths[0], 48)
        font_medium = ImageFont.truetype(font_paths[0], 32)
        font_small = ImageFont.truetype(font_paths[0], 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制边框（双线边框）
    border_color = "#8B7355"  # 古铜色
    draw.rectangle([20, 20, width-20, height-20], outline=border_color, width=3)
    draw.rectangle([30, 30, width-30, height-30], outline=border_color, width=1)
    
    # 顶部装饰线
    draw.line([(50, 60), (width-50, 60)], fill=border_color, width=2)
    
    # 标题
    title = "📿 晨间智慧"
    draw.text((width//2, 100), title, fill=border_color, font=font_large, anchor="mm")
    
    # 日期
    date_str = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["一", "二", "三", "四", "五", "六", "日"][datetime.now().weekday()]
    date_with_weekday = f"{date_str} 周{weekday}"
    draw.text((width//2, 170), date_with_weekday, fill="#A09080", font=font_small, anchor="mm")
    
    # 顶部装饰线
    draw.line([(50, 210), (width-50, 210)], fill=border_color, width=2)
    
    # 分类标签
    category_text = f"【{category}】"
    draw.text((width//2, 280), category_text, fill=border_color, font=font_medium, anchor="mm")
    
    # 出处
    draw.text((width//2, 330), source, fill="#A09080", font=font_small, anchor="mm")
    
    # 中间装饰图案（简单的水墨风格圆点）
    draw.ellipse([(width//2-5, 380), (width//2+5, 390)], fill=border_color)
    
    # 核心语录（居中，大字体）
    # 自动换行处理
    quote_lines = []
    max_chars_per_line = 20
    quote_text = quote
    
    # 简单按标点分割
    if len(quote_text) > max_chars_per_line:
        # 尝试按逗号、句号分割
        import re
        parts = re.split(r'([,.!?.,])', quote_text)
        current_line = ""
        for part in parts:
            if len(current_line + part) <= max_chars_per_line + 2:
                current_line += part
            else:
                if current_line:
                    quote_lines.append(current_line)
                current_line = part
        if current_line:
            quote_lines.append(current_line)
    else:
        quote_lines = [quote_text]
    
    # 绘制语录
    y_start = 480
    line_height = 70
    for i, line in enumerate(quote_lines):
        y = y_start + i * line_height
        draw.text((width//2, y), line, fill="#2C2C2C", font=font_large, anchor="mm")
    
    # 底部装饰
    bottom_y = y_start + len(quote_lines) * line_height + 50
    
    # 底部署名
    draw.text((width//2, bottom_y), "—— 太一 · 晨起静心", fill="#A09080", font=font_small, anchor="mm")
    
    # 底部装饰线
    draw.line([(200, bottom_y + 50), (width-200, bottom_y + 50)], fill=border_color, width=1)
    
    # 祝福语
    draw.text((width//2, bottom_y + 100), "🙏 愿您今日 心安自在", fill=border_color, font=font_medium, anchor="mm")
    
    # 底部角落装饰（四个角的小圆点）
    corner_offset = 40
    for x, y in [(corner_offset, corner_offset), 
                 (width-corner_offset, corner_offset),
                 (corner_offset, height-corner_offset),
                 (width-corner_offset, height-corner_offset)]:
        draw.ellipse([(x-3, y-3), (x+3, y+3)], fill=border_color)
    
    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 已生成：{output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        # 默认生成道家和佛家各一张
        categories = ["道家", "佛家"]
    else:
        categories = [sys.argv[1]]
    
    output_files = []
    
    for category in categories:
        quote, source = get_random_quote(category)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"wisdom_{category}_{timestamp}.png")
        
        create_wisdom_card(category, quote, source, output_file)
        output_files.append(output_file)
        
        # 打印语录信息
        print(f"\n📿 {category}智慧")
        print(f"   {quote}")
        print(f"   —— {source}")
    
    print(f"\n✅ 共生成 {len(output_files)} 张卡片")
    return output_files

if __name__ == "__main__":
    main()
