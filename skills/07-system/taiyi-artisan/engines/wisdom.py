#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wisdom Card Engine - 智慧卡片引擎

整合自：generate-wisdom-zen.py
遵循宪法美学原则：存在即艺术 / 形式追随功能 / 克制即优雅 / 一致性和谐
"""

import random
import re
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

from ..core.style import TaiyiStyle, StyleCategory, ColorPalette


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


class WisdomCardEngine:
    """智慧卡片引擎"""
    
    def __init__(self, output_dir: str = "~/.openclaw/workspace/skills/taiyi-artisan/outputs/wisdom"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.style = TaiyiStyle()
    
    def get_random_quote(self, category: str) -> Tuple[str, str]:
        """随机获取一句智慧语录"""
        quotes = QUOTES.get(category, QUOTES["道家"])
        return random.choice(quotes)
    
    def create_gradient_background(self, width: int, height: int, 
                                   palette: ColorPalette) -> Image.Image:
        """创建渐变背景"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            ratio = y / height
            r = int(palette.background_top[0] + (palette.background_bottom[0] - palette.background_top[0]) * ratio)
            g = int(palette.background_top[1] + (palette.background_bottom[1] - palette.background_top[1]) * ratio)
            b = int(palette.background_top[2] + (palette.background_bottom[2] - palette.background_top[2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img
    
    def draw_minimal_border(self, draw: ImageDraw.Draw, width: int, height: int, 
                           color: Tuple[int, int, int], opacity: int = 60):
        """绘制极简边框"""
        margin = 40
        draw.rectangle([margin, margin, width-margin, height-margin], 
                      outline=(*color, opacity), width=1)
        
        # 顶部短横线
        line_width = 60
        draw.line([(width//2 - line_width//2, margin + 15), 
                   (width//2 + line_width//2, margin + 15)], 
                  fill=(*color, 80), width=2)
    
    def draw_ink_circle(self, draw: ImageDraw.Draw, x: int, y: int, 
                       radius: int, color: Tuple[int, int, int], opacity: int = 15):
        """绘制水墨圆"""
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    fill=(*color, opacity))
    
    def draw_simple_bamboo(self, draw: ImageDraw.Draw, width: int, height: int, 
                          color: Tuple[int, int, int]):
        """绘制极简竹枝"""
        bamboo_x = width - 120
        bamboo_y = height - 180
        
        draw.line([(bamboo_x, bamboo_y), (bamboo_x, height-60)], 
                 fill=(*color, 70), width=3)
        
        # 两片竹叶
        draw.polygon([(bamboo_x, bamboo_y+30), (bamboo_x-35, bamboo_y+15), 
                      (bamboo_x-30, bamboo_y+35)], fill=(*color, 60))
        draw.polygon([(bamboo_x, bamboo_y+60), (bamboo_x-35, bamboo_y+45), 
                      (bamboo_x-30, bamboo_y+65)], fill=(*color, 50))
    
    def draw_plum_branch(self, draw: ImageDraw.Draw, width: int, height: int, 
                        color: Tuple[int, int, int]):
        """绘制极简梅枝"""
        branch_x = width - 140
        branch_y = height - 200
        
        points = [(branch_x, branch_y), 
                  (branch_x-30, branch_y+40),
                  (branch_x-50, branch_y+90)]
        
        draw.line(points, fill=(*color, 70), width=3)
        
        # 三朵梅花
        for i, (mx, my) in enumerate([(branch_x-20, branch_y+30),
                                       (branch_x-40, branch_y+70),
                                       (branch_x-55, branch_y+100)]):
            draw.ellipse([mx-4, my-4, mx+4, my+4], fill=(*color, 60))
    
    def draw_seal(self, draw: ImageDraw.Draw, x: int, y: int, text: str, 
                 size: int = 70, color: Tuple[int, int, int] = (155, 55, 55)):
        """绘制印章"""
        draw.rectangle([x, y, x+size, y+size], fill=(*color, 85))
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 36)
        except:
            font = ImageFont.load_default()
        
        draw.text((x+size//2, y+size//2), text, fill=(255, 255, 255), 
                 font=font, anchor="mm")
    
    def wrap_text(self, text: str, max_chars: int = 18) -> list:
        """自动换行处理"""
        lines = []
        parts = re.split(r'([,.!?.,;,.])', text)
        current_line = ""
        
        for part in parts:
            if len(current_line + part) <= max_chars + 2:
                current_line += part
            else:
                if current_line:
                    lines.append(current_line)
                current_line = part
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def create_card(self, category: str, quote: str, source: str, 
                   output_name: Optional[str] = None) -> str:
        """
        创建智慧卡片
        
        Args:
            category: 分类（道家/佛家）
            quote: 语录
            source: 出处
            output_name: 输出文件名（可选）
        
        Returns:
            输出文件路径
        """
        # 画布尺寸
        width, height = self.style.get_canvas('mobile_portrait')
        
        # 获取配色方案
        cat = StyleCategory.DAOIST if category == "道家" else StyleCategory.BUDDHIST
        palette = self.style.get_palette(cat)
        
        # 1. 创建背景
        img = self.create_gradient_background(width, height, palette)
        draw = ImageDraw.Draw(img)
        
        # 2. 极简边框
        self.draw_minimal_border(draw, width, height, palette.accent)
        
        # 3. 加载字体
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 48)
            font_date = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 28)
            font_category = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 32)
            font_quote = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 52)
            font_source = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 32)
            font_footer = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc", 26)
        except:
            font_title = ImageFont.load_default()
            font_date = ImageFont.load_default()
            font_category = ImageFont.load_default()
            font_quote = ImageFont.load_default()
            font_source = ImageFont.load_default()
            font_footer = ImageFont.load_default()
        
        # 4. 顶部标题
        title_y = 120
        draw.text((width//2, title_y), "晨间智慧", fill=palette.accent, 
                 font=font_title, anchor="mm")
        
        # 日期
        date_str = datetime.now().strftime("%Y.%m.%d")
        weekday = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][datetime.now().weekday()]
        draw.text((width//2, title_y + 50), f"{date_str}  {weekday}", 
                 fill=(*palette.accent, 60), font=font_date, anchor="mm")
        
        # 5. 分类标签
        category_y = 280
        draw.text((width//2, category_y), f"【{category}】", 
                 fill=palette.accent, font=font_category, anchor="mm")
        
        # 6. 水墨圆装饰
        self.draw_ink_circle(draw, width//2, category_y + 80, 6, palette.accent, opacity=20)
        
        # 7. 核心语录
        quote_y_start = 520
        quote_lines = self.wrap_text(quote, max_chars=18)
        
        line_height = 88
        total_height = len(quote_lines) * line_height
        quote_y_center = quote_y_start + (300 - total_height) // 2
        
        for i, line in enumerate(quote_lines):
            y = quote_y_center + i * line_height
            draw.text((width//2, y), line, fill=palette.ink, 
                     font=font_quote, anchor="mm")
        
        # 8. 出处
        source_y = quote_y_start + 380
        draw.text((width//2, source_y), source, fill=(*palette.accent, 70), 
                 font=font_source, anchor="mm")
        
        # 9. 底部装饰
        if category == "道家":
            self.draw_simple_bamboo(draw, width, height, palette.accent)
        else:
            self.draw_plum_branch(draw, width, height, palette.accent)
        
        # 10. 底部署名
        footer_y = height - 140
        draw.text((width//2, footer_y), "太一 · 晨起静心", 
                 fill=(*palette.accent, 60), font=font_footer, anchor="mm")
        
        # 11. 印章
        seal_char = "道" if category == "道家" else "禅"
        self.draw_seal(draw, width - 110, height - 180, seal_char, size=70)
        
        # 保存
        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"zen_{category}_{timestamp}.png"
        
        output_path = self.output_dir / output_name
        img.save(output_path, 'PNG', quality=98)
        
        return str(output_path)
    
    def generate_daily(self, category: Optional[str] = None) -> str:
        """
        生成每日智慧卡片
        
        Args:
            category: 分类（可选，默认随机）
        
        Returns:
            输出文件路径
        """
        # 随机选择分类
        if category is None:
            category = random.choice(["道家", "佛家"])
        
        # 获取语录
        quote, source = self.get_random_quote(category)
        
        # 生成卡片
        return self.create_card(category, quote, source)
