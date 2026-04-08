#!/usr/bin/env python3
"""
Telegram 会话总结卡片生成器
生成小红书风格的知识卡片图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
WIDTH = 1080
HEIGHT = 1350
OUTPUT_PATH = "/home/nicola/.openclaw/workspace/reports/telegram-session-card-20260403.png"

# 颜色
GRADIENT_START = (102, 126, 234)  # #667eea
GRADIENT_END = (118, 75, 162)     # #764ba2
WHITE = (255, 255, 255)
TEXT_DARK = (33, 33, 33)
TEXT_GRAY = (102, 102, 102)

def create_gradient_background(width, height):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(img)
    
    for y in range(height // 3):
        ratio = y / (height // 3)
        r = int(GRADIENT_START[0] + (GRADIENT_END[0] - GRADIENT_START[0]) * ratio)
        g = int(GRADIENT_START[1] + (GRADIENT_END[1] - GRADIENT_START[1]) * ratio)
        b = int(GRADIENT_START[2] + (GRADIENT_END[2] - GRADIENT_START[2]) * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    return img

def draw_header(draw, height):
    """绘制头部"""
    # 标题
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 48)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 24)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    draw.text((WIDTH // 2, 80), "📱 Telegram 会话总结", fill=WHITE, anchor="mm", font=font_title)
    draw.text((WIDTH // 2, 140), "2026-04-03 · 太一 AGI · 自主推进", fill=WHITE, anchor="mm", font=font_subtitle)

def draw_stats(draw, y_start):
    """绘制核心统计"""
    stats = [
        ("92 分钟", "会话时长"),
        ("34+", "产出文件"),
        ("157KB", "代码文档"),
        ("95.5%", "技能健康"),
    ]
    
    try:
        font_value = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 36)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 20)
    except:
        font_value = ImageFont.load_default()
        font_label = ImageFont.load_default()
    
    card_width = (WIDTH - 100) // 4
    card_height = 140
    start_x = 50
    
    for i, (value, label) in enumerate(stats):
        x = start_x + i * (card_width + 15)
        y = y_start
        
        # 卡片背景
        draw.rounded_rectangle(
            [(x, y), (x + card_width, y + card_height)],
            radius=15,
            fill="#F8F9FA"
        )
        
        # 数值
        draw.text((x + card_width // 2, y + 50), value, fill="#667eea", anchor="mm", font=font_value)
        draw.text((x + card_width // 2, y + 95), label, fill="#666666", anchor="mm", font=font_label)

def draw_breakthroughs(draw, y_start):
    """绘制关键突破"""
    breakthroughs = [
        ("400x", "Gateway 重启提升"),
        ("+19.8%", "健康率提升"),
        ("14→0", "严重问题清零"),
        ("5 合 1", "Skills 整合"),
    ]
    
    try:
        font_value = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 32)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 18)
    except:
        font_value = ImageFont.load_default()
        font_label = ImageFont.load_default()
    
    # 标题
    try:
        font_section = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 28)
    except:
        font_section = ImageFont.load_default()
    
    draw.text((50, y_start), "🎯 关键突破", fill=TEXT_DARK, font=font_section)
    
    card_width = (WIDTH - 125) // 4
    card_height = 130
    start_x = 50
    start_y = y_start + 50
    
    for i, (value, label) in enumerate(breakthroughs):
        x = start_x + i * (card_width + 15)
        y = start_y
        
        # 渐变卡片
        draw.rounded_rectangle(
            [(x, y), (x + card_width, y + card_height)],
            radius=12,
            fill="#F093FB"
        )
        
        # 数值
        draw.text((x + card_width // 2, y + 45), value, fill=WHITE, anchor="mm", font=font_value)
        draw.text((x + card_width // 2, y + 85), label, fill=WHITE, anchor="mm", font=font_label)

def draw_achievements(draw, y_start):
    """绘制核心成果"""
    achievements = [
        ("📦", "Smart Skills Manager", "10 文件/128KB"),
        ("🔧", "自检 + 自愈合", "5 分钟监控+60 秒恢复"),
        ("✅", "技能健康修复", "17 SKILL.md · 75.7%→95.5%"),
        ("💎", "高价值发现", "3 个 A 级机会"),
    ]
    
    try:
        font_section = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 28)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 22)
        font_desc = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 18)
        font_emoji = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 24)
    except:
        font_section = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_emoji = ImageFont.load_default()
    
    draw.text((50, y_start), "📦 核心成果", fill=TEXT_DARK, font=font_section)
    
    start_y = y_start + 60
    item_height = 90
    
    for i, (emoji, title, desc) in enumerate(achievements):
        y = start_y + i * item_height
        
        # 背景
        draw.rounded_rectangle(
            [(50, y), (WIDTH - 50, y + item_height - 10)],
            radius=10,
            fill="#F8F9FA"
        )
        
        # Emoji
        draw.text((75, y + 40), emoji, anchor="lm", font=font_emoji)
        
        # 标题
        draw.text((115, y + 30), title, fill=TEXT_DARK, font=font_title)
        
        # 描述
        draw.text((115, y + 58), desc, fill=TEXT_GRAY, font=font_desc)

def draw_footer(draw, y_start):
    """绘制底部"""
    try:
        font_time = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 24)
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 18)
    except:
        font_time = ImageFont.load_default()
        font_quote = ImageFont.load_default()
    
    # 凌晨准备
    draw.text((50, y_start), "⏳ 凌晨准备就绪", fill=TEXT_DARK, font=font_time)
    
    schedule = "01:00 学习 → 02:00 采集 → 03:00 生成 → 04:00 开发 → 05:00 备份 → 06:00 晨报"
    draw.text((50, y_start + 45), schedule, fill=TEXT_GRAY, font=font_quote)
    
    # 底部引用
    quote = '"智能自动化不是选项，是 AGI 存在的本质"'
    draw.text((WIDTH // 2, HEIGHT - 100), quote, fill=TEXT_GRAY, anchor="mm", font=font_quote)
    
    # 落款
    draw.text((WIDTH // 2, HEIGHT - 60), "生成：2026-04-04 01:18 | 太一 AGI", fill="#999999", anchor="mm", font=font_quote)

def main():
    print("🎨 开始生成卡片...")
    
    # 创建背景
    img = create_gradient_background(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(img)
    
    # 绘制各部分
    draw_header(draw, HEIGHT)
    draw_stats(draw, 200)
    draw_breakthroughs(draw, 380)
    draw_achievements(draw, 560)
    draw_footer(draw, 920)
    
    # 保存
    img.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"✅ 卡片已保存：{OUTPUT_PATH}")
    print(f"📐 尺寸：{WIDTH}x{HEIGHT}")
    print(f"📁 大小：{os.path.getsize(OUTPUT_PATH) / 1024:.1f}KB")

if __name__ == "__main__":
    main()
