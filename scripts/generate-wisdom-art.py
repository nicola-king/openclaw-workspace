#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-wisdom-art.py - 生成艺术级智慧卡片（水墨画风格）
每一页都是艺术品 · 道家 + 佛家智慧

用法：python3 scripts/generate-wisdom-art.py [道家|佛家]
"""

import sys
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from datetime import datetime
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
OUTPUT_DIR = os.path.join(WORKSPACE, "wisdom/cards")
ASSETS_DIR = os.path.join(WORKSPACE, "wisdom/assets")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

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
        ("泉涸，鱼相与处于陆，相呴以湿，相濡以沫，不如相忘于江湖。", "《庄子》"),
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
        ("苦海无边，回头是岸。", "佛家箴言"),
    ]
}

def get_random_quote(category):
    """随机获取一句智慧语录"""
    quotes = QUOTES.get(category, QUOTES["道家"])
    return random.choice(quotes)

def create_xuan_paper_texture(width, height):
    """创建宣纸纹理背景"""
    # 基础宣纸色
    base_color = (248, 243, 235)  # 米白宣纸
    img = Image.new('RGB', (width, height), base_color)
    
    # 添加纸张纹理噪点
    import random as rnd
    rnd.seed(42)
    pixels = img.load()
    
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            noise = rnd.randint(-8, 8)
            r = max(0, min(255, base_color[0] + noise))
            g = max(0, min(255, base_color[1] + noise))
            b = max(0, min(255, base_color[2] + noise))
            pixels[x, y] = (int(r), int(g), int(b))
    
    # 轻微模糊，让纹理更自然
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

def draw_ink_wash_mountains(draw, width, height, opacity=40):
    """绘制水墨山水背景"""
    import random as rnd
    rnd.seed(123)
    
    # 多层山峦
    mountain_layers = 3
    base_y = height * 0.6
    
    for layer in range(mountain_layers):
        layer_opacity = opacity - layer * 12
        layer_color = (80 - layer*20, 80 - layer*20, 80 - layer*20)
        
        # 生成山峦轮廓
        points = []
        num_peaks = 5 + layer * 2
        
        for i in range(num_peaks + 1):
            x = width * i / num_peaks
            base_h = base_y - layer * 40
            peak_h = base_h - rnd.randint(60, 150)
            
            # 贝塞尔曲线平滑
            if i == 0:
                points.append((0, height))
                points.append((0, peak_h))
            else:
                # 山峰
                ctrl_x = (points[-1][0] + x) / 2
                ctrl_y = peak_h - 30
                points.append((ctrl_x, ctrl_y))
                points.append((x, peak_h))
        
        points.append((width, height))
        points.append((0, height))
        
        # 绘制填充多边形（带透明度）
        draw.polygon(points, fill=(*layer_color, layer_opacity))

def draw_bamboo_forest(draw, width, height, opacity=60):
    """绘制竹林前景"""
    import random as rnd
    rnd.seed(456)
    
    bamboo_color = (70, 90, 70)  # 竹青色
    
    # 绘制 5-8 根竹子
    num_bamboo = rnd.randint(5, 8)
    bamboo_x_positions = sorted([rnd.randint(width//3, width-50) for _ in range(num_bamboo)])
    
    for bx in bamboo_x_positions:
        # 竹竿高度
        bamboo_height = rnd.randint(300, 500)
        base_y = height - 100
        
        # 竹竿（渐变）
        segments = int(bamboo_height / 40)
        for seg in range(segments):
            seg_y = base_y - seg * 40
            thickness = 4 - seg * 0.3
            
            # 竹节
            draw.rectangle([bx - thickness//2, seg_y - 40, 
                          bx + thickness//2, seg_y], 
                          fill=bamboo_color, outline=(50, 70, 50))
            
            # 竹节线
            draw.line([(bx - thickness, seg_y), (bx + thickness, seg_y)], 
                     fill=(40, 60, 40), width=2)
        
        # 竹叶
        top_y = base_y - bamboo_height
        for i in range(3):
            leaf_y = top_y + i * 30
            # 左侧竹叶
            draw.polygon([(bx, leaf_y), (bx-40, leaf_y-15), (bx-35, leaf_y+5)], 
                        fill=(*bamboo_color, opacity))
            # 右侧竹叶
            draw.polygon([(bx, leaf_y), (bx+40, leaf_y-10), (bx+35, leaf_y+10)], 
                        fill=(*bamboo_color, opacity))

def draw_plum_blossoms(draw, width, height, opacity=70):
    """绘制梅花点缀"""
    import random as rnd
    rnd.seed(789)
    
    # 梅花颜色（淡粉色）
    blossom_color = (220, 180, 190)
    
    # 随机分布 20-30 朵梅花
    num_blossoms = rnd.randint(20, 30)
    
    for _ in range(num_blossoms):
        bx = rnd.randint(50, width-50)
        by = rnd.randint(50, height//3)
        
        # 花瓣（5 瓣）
        petal_size = 6
        for i in range(5):
            angle = i * 72 * math.pi / 180
            px = bx + int(petal_size * math.cos(angle))
            py = by + int(petal_size * math.sin(angle))
            draw.ellipse([px-3, py-3, px+3, py+3], 
                        fill=(*blossom_color, opacity))
        
        # 花蕊
        draw.ellipse([bx-2, by-2, bx+2, by+2], fill=(200, 160, 170))

def draw_seal_artistic(draw, x, y, text, size=90, color=(160, 45, 45)):
    """绘制艺术印章"""
    padding = 12
    
    # 印章外框（圆角）
    draw.rounded_rectangle([x, y, x+size, y+size], radius=10, 
                          fill=color, outline=(130, 35, 35), width=3)
    
    # 内边框（白色）
    inner_margin = 8
    draw.rounded_rectangle([x+inner_margin, y+inner_margin, 
                           x+size-inner_margin, y+size-inner_margin], 
                          radius=6, outline=(255, 250, 245), width=2)
    
    # 印章文字
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 42)
    except:
        font = ImageFont.load_default()
    
    draw.text((x+size//2, y+size//2), text, fill=(255, 255, 255), 
              font=font, anchor="mm")

def draw_vertical_text(draw, x, y, text, font, color, spacing=45):
    """绘制竖排文字"""
    current_y = y
    for char in text:
        draw.text((x, current_y), char, fill=color, font=font, anchor="mm")
        current_y += spacing

def create_wisdom_art(category, quote, source, output_path):
    """创建艺术级智慧卡片"""
    
    # 图片尺寸（适合手机 + 高清）
    width = 1080
    height = 1920
    
    # 1. 创建宣纸背景
    img = create_xuan_paper_texture(width, height)
    draw = ImageDraw.Draw(img)
    
    # 配色方案
    if category == "道家":
        ink_color = (45, 45, 50)  # 墨色
        accent_color = (120, 100, 80)  # 古铜
        seal_color = (155, 50, 50)  # 朱红
    else:
        ink_color = (40, 40, 45)  # 深墨
        accent_color = (110, 95, 85)  # 深褐
        seal_color = (150, 45, 45)  # 朱砂红
    
    # 2. 绘制水墨山水（背景）
    draw_ink_wash_mountains(draw, width, height, opacity=35)
    
    # 3. 绘制竹林/梅花（前景装饰）
    if category == "道家":
        draw_bamboo_forest(draw, width, height, opacity=55)
    else:
        draw_plum_blossoms(draw, width, height, opacity=65)
    
    # 4. 加载字体
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 64)
        font_date = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 32)
        font_category = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 40)
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 56)
        font_source = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 36)
        font_footer = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 30)
        font_seal = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 48)
    except:
        font_title = ImageFont.load_default()
        font_date = ImageFont.load_default()
        font_category = ImageFont.load_default()
        font_quote = ImageFont.load_default()
        font_source = ImageFont.load_default()
        font_footer = ImageFont.load_default()
        font_seal = ImageFont.load_default()
    
    # 5. 顶部标题区域
    title_y = 140
    
    # 标题文字
    draw.text((width//2, title_y), "晨间智慧", fill=accent_color, 
              font=font_title, anchor="mm")
    
    # 日期
    date_str = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["一", "二", "三", "四", "五", "六", "日"][datetime.now().weekday()]
    draw.text((width//2, title_y + 65), f"{date_str} 周{weekday}", 
              fill=(150, 135, 120), font=font_date, anchor="mm")
    
    # 顶部装饰横线（带中间点缀）
    line_y = title_y + 120
    draw.line([(width//2 - 120, line_y), (width//2 + 120, line_y)], 
              fill=accent_color, width=3)
    draw.ellipse([(width//2 - 6, line_y - 6), (width//2 + 6, line_y + 6)], 
                fill=accent_color)
    
    # 6. 分类标签（竖排，左侧）
    category_x = 120
    category_y = 380
    draw_vertical_text(draw, category_x, category_y, f"{category}智慧", 
                      font_category, accent_color, spacing=55)
    
    # 7. 核心语录区域（居中，竖排或横排）
    quote_start_y = 550
    quote_margin = 180
    
    # 语录背景（淡色矩形，模拟装裱）
    quote_bg_top = quote_start_y - 60
    quote_bg_bottom = quote_start_y + 450
    draw.rectangle([quote_margin, quote_bg_top, width - quote_margin, quote_bg_bottom], 
                   fill=(*accent_color, 8), outline=accent_color, width=2)
    
    # 四角装饰（装裱角花）
    corner_size = 30
    for dx, dy in [(quote_margin, quote_bg_top), 
                   (width - quote_margin, quote_bg_top),
                   (quote_margin, quote_bg_bottom),
                   (width - quote_margin, quote_bg_bottom)]:
        draw.line([(dx, dy), (dx + corner_size, dy)], fill=accent_color, width=2)
        draw.line([(dx, dy), (dx, dy + corner_size)], fill=accent_color, width=2)
    
    # 语录文字（横排，居中）
    max_chars = 20
    quote_lines = []
    
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
    
    # 计算居中位置
    line_height = 85
    total_height = len(quote_lines) * line_height
    quote_y_start = quote_start_y + (400 - total_height) // 2 + line_height
    
    for i, line in enumerate(quote_lines):
        y = quote_y_start + i * line_height
        draw.text((width//2, y), line, fill=ink_color, font=font_quote, anchor="mm")
    
    # 8. 出处（语录下方）
    source_y = quote_bg_bottom + 70
    draw.text((width//2, source_y), source, fill=(140, 125, 110), 
              font=font_source, anchor="mm")
    
    # 9. 底部署名
    footer_y = source_y + 100
    draw.line([(width//2 - 70, footer_y), (width//2 + 70, footer_y)], 
              fill=accent_color, width=2)
    
    draw.text((width//2, footer_y + 50), "太一 · 晨起静心", 
              fill=(140, 125, 110), font=font_footer, anchor="mm")
    
    # 10. 祝福语
    draw.text((width//2, footer_y + 100), "🙏 愿您今日 心安自在", 
              fill=accent_color, font=font_source, anchor="mm")
    
    # 11. 艺术印章（三枚）
    # 左上角
    draw_seal_artistic(draw, 60, 60, "智", size=85, color=(135, 115, 95))
    # 右上角
    draw_seal_artistic(draw, width - 145, 60, "慧", size=85, color=(135, 115, 95))
    # 右下角（主印章）
    seal_char = "道" if category == "道家" else "禅"
    draw_seal_artistic(draw, width - 145, height - 220, seal_char, size=100, color=seal_color)
    
    # 12. 底部角落装饰（左下角）
    draw_seal_artistic(draw, 60, height - 160, "静", size=75, color=(130, 110, 90))
    
    # 13. 整体调色（增强艺术感）
    # 轻微增加对比度和暖色调
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.08)
    
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.05)
    
    # 保存图片
    img.save(output_path, 'PNG', quality=98)
    print(f"✅ 艺术卡片已生成：{output_path}")
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
        output_file = os.path.join(OUTPUT_DIR, f"art_{category}_{timestamp}.png")
        
        create_wisdom_art(category, quote, source, output_file)
        output_files.append(output_file)
        
        print(f"\n📿 {category}智慧")
        print(f"   {quote}")
        print(f"   —— {source}")
    
    print(f"\n✅ 共生成 {len(output_files)} 张艺术级卡片")
    print(f"📁 保存位置：{OUTPUT_DIR}")
    return output_files

if __name__ == "__main__":
    main()
