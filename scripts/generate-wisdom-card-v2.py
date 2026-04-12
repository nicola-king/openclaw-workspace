#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-wisdom-card-v2.py - 生成精美智慧卡片图片（精致版）
用法：python3 scripts/generate-wisdom-card-v2.py [道家|佛家]
"""

import sys
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
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
        ("独与天地精神往来。", "《庄子》"),
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
        ("明心见性。", "禅宗"),
    ]
}

def get_random_quote(category):
    """随机获取一句智慧语录"""
    quotes = QUOTES.get(category, QUOTES["道家"])
    return random.choice(quotes)

def create_gradient_background(width, height, colors):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / height)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / height)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def draw_cloud_pattern(draw, width, height, color, opacity=30):
    """绘制祥云纹样"""
    import random as rnd
    rnd.seed(42)  # 固定种子，保证一致性
    
    cloud_positions = [
        (width * 0.1, height * 0.15),
        (width * 0.9, height * 0.2),
        (width * 0.15, height * 0.85),
        (width * 0.85, height * 0.8),
    ]
    
    for cx, cy in cloud_positions:
        for i in range(3):
            size = 40 + rnd.randint(0, 20)
            x = cx + rnd.randint(-20, 20)
            y = cy + rnd.randint(-10, 10)
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        fill=(*color, opacity))

def draw_border_pattern(draw, width, height, color):
    """绘制精美边框"""
    # 外边框
    margin = 30
    draw.rectangle([margin, margin, width-margin, height-margin], 
                   outline=color, width=4)
    
    # 内边框（双线）
    margin2 = 45
    draw.rectangle([margin2, margin2, width-margin2, height-margin2], 
                   outline=color, width=2)
    
    # 四角装饰
    corner_size = 60
    corner_thickness = 3
    
    # 左上角
    draw.line([(margin2, margin2+corner_size), (margin2, margin2)], 
              fill=color, width=corner_thickness)
    draw.line([(margin2, margin2), (margin2+corner_size, margin2)], 
              fill=color, width=corner_thickness)
    
    # 右上角
    draw.line([(width-margin2, margin2+corner_size), (width-margin2, margin2)], 
              fill=color, width=corner_thickness)
    draw.line([(width-margin2, margin2), (width-margin2-corner_size, margin2)], 
              fill=color, width=corner_thickness)
    
    # 左下角
    draw.line([(margin2, height-margin2-corner_size), (margin2, height-margin2)], 
              fill=color, width=corner_thickness)
    draw.line([(margin2, height-margin2), (margin2+corner_size, height-margin2)], 
              fill=color, width=corner_thickness)
    
    # 右下角
    draw.line([(width-margin2, height-margin2-corner_size), (width-margin2, height-margin2)], 
              fill=color, width=corner_thickness)
    draw.line([(width-margin2, height-margin2), (width-margin2-corner_size, height-margin2)], 
              fill=color, width=corner_thickness)
    
    # 四角圆点
    dot_radius = 6
    for x, y in [(margin2, margin2), (width-margin2, margin2),
                 (margin2, height-margin2), (width-margin2, height-margin2)]:
        draw.ellipse([x-dot_radius, y-dot_radius, x+dot_radius, y+dot_radius], 
                    fill=color)

def draw_seal(draw, x, y, text, color=(180, 50, 50)):
    """绘制印章"""
    seal_size = 80
    padding = 10
    
    # 印章背景
    draw.rectangle([x, y, x+seal_size, y+seal_size], fill=color, outline=(150, 40, 40), width=2)
    
    # 印章边框
    draw.rectangle([x+padding, y+padding, x+seal_size-padding, y+seal_size-padding], 
                   outline=(255, 255, 255), width=2)
    
    # 印章文字（简化为单字）
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((x+seal_size//2, y+seal_size//2), text, fill=(255, 255, 255), 
              font=font, anchor="mm")

def draw_bamboo_decoration(draw, width, height, color):
    """绘制竹叶装饰"""
    # 底部竹叶装饰
    bamboo_x = width - 150
    bamboo_y = height - 200
    
    # 竹竿
    draw.line([(bamboo_x, bamboo_y), (bamboo_x, height-80)], 
              fill=color, width=4)
    
    # 竹叶
    leaf_positions = [
        (bamboo_x, bamboo_y + 30),
        (bamboo_x, bamboo_y + 60),
        (bamboo_x, bamboo_y + 90),
    ]
    
    for lx, ly in leaf_positions:
        # 左竹叶
        draw.polygon([(lx, ly), (lx-30, ly-15), (lx-25, ly+5)], fill=color)
        # 右竹叶
        draw.polygon([(lx, ly), (lx+30, ly-10), (lx+25, ly+10)], fill=color)

def create_wisdom_card(category, quote, source, output_path):
    """创建精美智慧卡片图片"""
    
    # 图片尺寸（适合手机）
    width = 900
    height = 1400
    
    # 创建渐变背景
    if category == "道家":
        bg_colors = [(250, 248, 240), (245, 240, 230)]  # 米白→淡茶色
        accent_color = (139, 115, 85)  # 古铜色
        ink_color = (50, 50, 50)  # 墨色
    else:
        bg_colors = [(250, 248, 245), (248, 245, 240)]  # 米白→淡褐色
        accent_color = (128, 100, 80)  # 深褐色
        ink_color = (45, 45, 45)  # 深墨色
    
    img = create_gradient_background(width, height, bg_colors)
    draw = ImageDraw.Draw(img)
    
    # 绘制祥云纹样（底层）
    draw_cloud_pattern(draw, width, height, accent_color, opacity=20)
    
    # 绘制精美边框
    draw_border_pattern(draw, width, height, accent_color)
    
    # 顶部标题区域
    title_y = 120
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 56)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 32)
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 52)
        font_source = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 36)
        font_footer = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 28)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_quote = ImageFont.load_default()
        font_source = ImageFont.load_default()
        font_footer = ImageFont.load_default()
    
    # 标题
    title = "晨间智慧"
    draw.text((width//2, title_y), title, fill=accent_color, font=font_title, anchor="mm")
    
    # 日期
    date_str = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["一", "二", "三", "四", "五", "六", "日"][datetime.now().weekday()]
    date_with_weekday = f"{date_str} 周{weekday}"
    draw.text((width//2, title_y + 60), date_with_weekday, fill=(160, 145, 130), 
              font=font_subtitle, anchor="mm")
    
    # 顶部装饰横线
    line_y = title_y + 110
    draw.line([(width//2 - 100, line_y), (width//2 + 100, line_y)], 
              fill=accent_color, width=2)
    
    # 分类标签（带背景）
    category_y = 280
    category_bg_width = 200
    category_bg_height = 50
    draw.rounded_rectangle([width//2 - category_bg_width//2, category_y - category_bg_height//2,
                           width//2 + category_bg_width//2, category_y + category_bg_height//2],
                          radius=25, fill=(*accent_color, 30), outline=accent_color, width=2)
    
    category_text = f"【{category}】"
    draw.text((width//2, category_y), category_text, fill=accent_color, 
              font=font_subtitle, anchor="mm")
    
    # 出处
    draw.text((width//2, category_y + 70), source, fill=(160, 145, 130), 
              font=font_subtitle, anchor="mm")
    
    # 中间装饰分隔符
    separator_y = category_y + 130
    draw.text((width//2, separator_y), "❖", fill=accent_color, 
              font=font_subtitle, anchor="mm")
    
    # 核心语录区域（带淡色背景）
    quote_start_y = 500
    quote_bg_margin = 60
    quote_bg_height = 350
    
    # 语录背景（半透明矩形）
    draw.rounded_rectangle([quote_bg_margin, quote_start_y, 
                           width - quote_bg_margin, quote_start_y + quote_bg_height],
                          radius=20, fill=(*accent_color, 15), outline=accent_color, width=2)
    
    # 语录文字（自动换行）
    max_chars = 18
    quote_lines = []
    
    # 按标点分割
    import re
    parts = re.split(r'([,.!?.,;,.])', quote)
    current_line = ""
    for part in parts:
        if len(current_line + part) <= max_chars + 2:
            current_line += part
        else:
            if current_line:
                quote_lines.append(current_line)
            current_line = part
    if current_line:
        quote_lines.append(current_line)
    
    # 绘制语录
    line_height = 75
    total_quote_height = len(quote_lines) * line_height
    quote_y_start = quote_start_y + (quote_bg_height - total_quote_height) // 2 + line_height
    
    for i, line in enumerate(quote_lines):
        y = quote_y_start + i * line_height
        draw.text((width//2, y), line, fill=ink_color, font=font_quote, anchor="mm")
    
    # 底部署名
    footer_y = quote_start_y + quote_bg_height + 80
    draw.text((width//2, footer_y), "—— 太一 · 晨起静心", fill=(160, 145, 130), 
              font=font_footer, anchor="mm")
    
    # 底部装饰横线
    draw.line([(width//2 - 80, footer_y + 40), (width//2 + 80, footer_y + 40)], 
              fill=accent_color, width=2)
    
    # 祝福语
    draw.text((width//2, footer_y + 90), "🙏 愿您今日 心安自在", fill=accent_color, 
              font=font_subtitle, anchor="mm")
    
    # 底部竹叶装饰
    draw_bamboo_decoration(draw, width, height, accent_color)
    
    # 印章（右下角）
    seal_char = "道" if category == "道家" else "禅"
    draw_seal(draw, width - 150, height - 180, seal_char, color=(160, 45, 45))
    
    # 顶部角落装饰（左上和右上小印章）
    draw_seal(draw, 80, 80, "智", color=(140, 120, 100))
    draw_seal(draw, width - 130, 80, "慧", color=(140, 120, 100))
    
    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 已生成：{output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        categories = ["道家", "佛家"]
    else:
        categories = [sys.argv[1]]
    
    output_files = []
    
    for category in categories:
        quote, source = get_random_quote(category)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"wisdom_{category}_{timestamp}_v2.png")
        
        create_wisdom_card(category, quote, source, output_file)
        output_files.append(output_file)
        
        print(f"\n📿 {category}智慧")
        print(f"   {quote}")
        print(f"   —— {source}")
    
    print(f"\n✅ 共生成 {len(output_files)} 张精美卡片")
    return output_files

if __name__ == "__main__":
    main()
