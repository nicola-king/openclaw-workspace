#!/usr/bin/env python3
"""
TurboQuant 文章配图生成脚本
使用 Unsplash 免费图库 + Pillow 生成 5 张示意图
"""

import requests
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

OUTPUT_DIR = "/home/nicola/.openclaw/workspace/content/ai-images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Unsplash 搜索关键词
IMAGE_QUERIES = {
    "fig1_kv_cache": "data visualization graph technology",
    "fig2_flow": "flowchart diagram process",
    "fig3_comparison": "bar chart comparison technology",
    "fig4_scenes": "server computer smartphone technology",
    "fig5_performance": "speed performance metrics"
}

def get_unsplash_image(query, width=1920, height=1080):
    """从 Unsplash Source 获取免费图片"""
    url = f"https://source.unsplash.com/{width}x{height}/?{query}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Unsplash 获取失败：{e}")
    return None

def create_text_image(title, subtitle, bg_color="#1a1a1a", text_color="#ffffff"):
    """创建文字主导的图片（极简黑客风）"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 尝试使用系统字体
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # 绘制标题
    bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) / 2, height / 2 - 60), title, fill=text_color, font=font_large)
    
    # 绘制副标题
    bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(((width - subtitle_width) / 2, height / 2 + 20), subtitle, fill="#888888", font=font_medium)
    
    # 添加装饰线条
    draw.line([(width/2 - 100, height/2 - 80), (width/2 + 100, height/2 - 80)], fill="#07c160", width=3)
    
    return img

def create_kv_cache_chart():
    """图 1: KV Cache 增长示意图"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    # 绘制坐标轴
    margin = 100
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin
    
    # X 轴
    draw.line([(margin, height - margin), (width - margin, height - margin)], fill="#666666", width=2)
    # Y 轴
    draw.line([(margin, margin), (margin, height - margin)], fill="#666666", width=2)
    
    # 绘制两条线
    # 传统方案（红色，线性增长）
    traditional_points = [
        (margin + i * chart_width / 7, height - margin - i * chart_height / 7 * 0.9)
        for i in range(8)
    ]
    draw.line(traditional_points, fill="#ff4444", width=4)
    
    # TurboQuant（绿色，压缩后增长）
    tq_points = [
        (margin + i * chart_width / 7, height - margin - i * chart_height / 7 * 0.15)
        for i in range(8)
    ]
    draw.line(tq_points, fill="#07c160", width=4)
    
    # 添加标签
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((margin, margin - 40), "KV Cache 内存占用对比", fill="#ffffff", font=font)
    draw.text((width/2 - 50, height - 40), "上下文长度 →", fill="#888888", font=font)
    draw.text((margin - 60, margin), "↑ 内存", fill="#888888", font=font)
    
    # 图例
    draw.text((margin + 50, margin + 50), "■ 传统方案", fill="#ff4444", font=font)
    draw.text((margin + 200, margin + 50), "■ TurboQuant (6 倍压缩)", fill="#07c160", font=font)
    
    return img

def create_flow_diagram():
    """图 2: TurboQuant 两步流程图"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    # 绘制流程框
    boxes = [
        (100, 440, 300, 640, "原始向量"),
        (400, 440, 600, 640, "随机旋转"),
        (700, 440, 900, 640, "极坐标分解"),
        (1000, 340, 1200, 540, "主成分\n(3-bit)"),
        (1000, 540, 1200, 740, "残差\n(1-bit)"),
        (1300, 440, 1500, 640, "压缩输出\n(4-bit)"),
    ]
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
        font_bold = font
    
    # 绘制框和文字
    for i, (x1, y1, x2, y2, text) in enumerate(boxes):
        # 框
        draw.rectangle([x1, y1, x2, y2], outline="#07c160", width=3)
        # 文字
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(((x1 + x2 - text_width) / 2, (y1 + y2 - text_height) / 2), 
                  text, fill="#ffffff", font=font)
        
        # 箭头
        if i < len(boxes) - 1 and i != 3:
            arrow_start = (x2, (y1 + y2) / 2)
            arrow_end = (boxes[i+1][0], (boxes[i+1][1] + boxes[i+1][3]) / 2)
            draw.line([arrow_start, arrow_end], fill="#666666", width=2)
    
    # 标题
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        title_font = font_bold
    
    draw.text((width/2 - 150, 50), "TurboQuant 压缩流程", fill="#ffffff", font=title_font)
    
    return img

def create_comparison_chart():
    """图 3: 压缩率对比柱状图"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    # 数据
    methods = ["FP16", "INT8", "INT4", "TurboQuant"]
    values = [100, 50, 25, 16.7]  # 相对内存占用
    colors = ["#666666", "#888888", "#aaaaaa", "#07c160"]
    
    margin = 100
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin
    bar_width = chart_width / len(methods) / 2
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
        title_font = font
    
    # 绘制柱状图
    for i, (method, value, color) in enumerate(zip(methods, values, colors)):
        x = margin + i * (chart_width / len(methods)) + (chart_width / len(methods) - bar_width) / 2
        bar_height = (value / 100) * chart_height * 0.8
        y = height - margin - bar_height
        
        draw.rectangle([x, y, x + bar_width, height - margin], fill=color)
        
        # 文字标签
        bbox = draw.textbbox((0, 0), method, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((x + bar_width/2 - text_width/2, height - margin + 20), 
                  method, fill="#ffffff", font=font)
        
        # 数值
        value_text = f"{value}%"
        bbox = draw.textbbox((0, 0), value_text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((x + bar_width/2 - text_width/2, y - 40), 
                  value_text, fill="#ffffff", font=font)
    
    # 标题
    draw.text((width/2 - 180, 50), "压缩方案对比（内存占用）", fill="#ffffff", font=title_font)
    
    return img

def create_scene_image():
    """图 4: 实际应用场景"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    # 三个场景
    scenes = [
        (200, "本地电脑", "70B 模型\n48GB 显存"),
        (700, "云服务器", "成本降低 50%\n延迟降低 8 倍"),
        (1200, "手机设备", "7B 模型\n离线运行"),
    ]
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
        small_font = font
        title_font = font
    
    for x, title, desc in scenes:
        # 设备图标（简单矩形）
        draw.rectangle([x, 300, x + 400, 600], outline="#07c160", width=3)
        
        # 标题
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((x + 200 - text_width/2, 650), title, fill="#ffffff", font=font)
        
        # 描述
        bbox = draw.textbbox((0, 0), desc, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x + 200 - text_width/2, 700), desc, fill="#888888", font=small_font)
    
    # 总标题
    draw.text((width/2 - 200, 50), "TurboQuant 应用场景", fill="#ffffff", font=title_font)
    
    return img

def create_performance_card():
    """图 5: 性能提升总结"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color="#0a0a0a")
    draw = ImageDraw.Draw(img)
    
    try:
        huge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        huge_font = ImageFont.load_default()
        large_font = huge_font
        title_font = huge_font
    
    # 三个指标
    metrics = [
        ("6x", "内存压缩", 400),
        ("8x", "速度提升", 960),
        ("0%", "精度损失", 1520),
    ]
    
    for value, label, x in metrics:
        # 数值
        bbox = draw.textbbox((0, 0), value, font=huge_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width/2, 350), value, fill="#07c160", font=huge_font)
        
        # 标签
        bbox = draw.textbbox((0, 0), label, font=large_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width/2, 520), label, fill="#ffffff", font=large_font)
    
    # 标题
    draw.text((width/2 - 250, 100), "TurboQuant 性能总结", fill="#ffffff", font=title_font)
    
    # 装饰线
    draw.line([(200, 650), (1720, 650)], fill="#333333", width=2)
    
    return img

def main():
    print("=== TurboQuant 配图生成 ===\n")
    
    generators = [
        ("fig1_kv_cache.png", "KV Cache 增长示意图", create_kv_cache_chart),
        ("fig2_flow.png", "TurboQuant 流程图", create_flow_diagram),
        ("fig3_comparison.png", "压缩率对比图", create_comparison_chart),
        ("fig4_scenes.png", "应用场景图", create_scene_image),
        ("fig5_performance.png", "性能总结卡片", create_performance_card),
    ]
    
    generated = []
    for filename, description, generator in generators:
        print(f"生成：{filename} - {description}")
        try:
            img = generator()
            filepath = os.path.join(OUTPUT_DIR, filename)
            img.save(filepath, "PNG")
            print(f"  ✅ 已保存：{filepath}\n")
            generated.append(filepath)
        except Exception as e:
            print(f"  ❌ 生成失败：{e}\n")
    
    print(f"=== 完成：生成 {len(generated)}/5 张图片 ===")
    return generated

if __name__ == "__main__":
    main()
