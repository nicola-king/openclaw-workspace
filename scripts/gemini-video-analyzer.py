#!/usr/bin/env python3
"""
Gemini 视频分析器 v1.0
功能：上传视频 → Gemini 分析 → 生成提示词
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    print("❌ 缺少依赖：pip install google-generativeai")
    sys.exit(1)

# 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-1.5-pro"

def configure_api():
    """配置 API"""
    if not GEMINI_API_KEY:
        print("⚠️  未设置 GEMINI_API_KEY 环境变量")
        print("   获取：https://makersuite.google.com/app/apikey")
        return False
    
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✅ API 配置成功")
    return True

def upload_video(video_path):
    """上传视频到 Gemini"""
    print(f'📹 上传视频：{video_path}')
    
    try:
        video_file = genai.upload_file(path=video_path)
        print(f'✅ 上传成功：{video_file.name}')
        
        # 等待处理完成
        print('⏳ 处理视频中...')
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            print('  ...')
        
        if video_file.state.name == "FAILED":
            print('❌ 视频处理失败')
            return None
        
        print(f'✅ 视频处理完成')
        return video_file
    
    except Exception as e:
        print(f'❌ 上传失败：{e}')
        return None

def analyze_video(video_file):
    """分析视频内容"""
    print('🧠 Gemini 分析中...')
    
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    
    prompt = """
请详细分析这个视频，包括：

1. **场景描述**: 视频中的主要场景和背景
2. **物体识别**: 出现的主要物体和人物
3. **文字提取**: 视频中的任何文字信息
4. **动作分析**: 关键动作和事件
5. **情绪氛围**: 视频的整体情绪和风格
6. **提示词生成**: 基于分析生成 3-5 个图像生成提示词

请用 JSON 格式返回结果。
"""
    
    try:
        response = model.generate_content([video_file, prompt])
        print('✅ 分析完成')
        return response.text
    
    except Exception as e:
        print(f'❌ 分析失败：{e}')
        return None

def save_results(video_path, analysis, output_dir="output/video-analysis"):
    """保存分析结果"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存分析结果
    video_name = Path(video_path).stem
    result_file = output_path / f"{video_name}_analysis.md"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"# 视频分析报告\n\n")
        f.write(f"**视频**: {video_path}\n")
        f.write(f"**分析时间**: {datetime.now().isoformat()}\n\n")
        f.write(f"---\n\n")
        f.write(f"{analysis}\n")
    
    print(f'💾 结果已保存：{result_file}')
    return result_file

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🎬 Gemini 视频分析器 v1.0                                ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    # 检查参数
    if len(sys.argv) < 2:
        print('用法：python3 gemini-video-analyzer.py <video_path>')
        print('')
        print('示例:')
        print('  python3 gemini-video-analyzer.py input/video.mp4')
        return
    
    video_path = sys.argv[1]
    
    if not Path(video_path).exists():
        print(f'❌ 文件不存在：{video_path}')
        return
    
    # 配置 API
    if not configure_api():
        # Demo 模式
        print('')
        print('🔧 进入 Demo 模式（无 API Key）')
        print('')
        print('分析结果示例:')
        print('---')
        print('场景：室内办公环境，自然光线充足')
        print('物体：办公桌、笔记本电脑、文件、咖啡杯')
        print('文字："项目名称：太一 AGI"')
        print('动作：人物正在演示产品功能')
        print('情绪：专业、现代、创新')
        print('')
        print('生成的提示词:')
        print('1. 现代办公场景，自然光，极简风格，专业氛围')
        print('2. 科技产品展示，简洁背景，高质量渲染')
        print('3. 商务会议环境，现代化办公室，专业摄影')
        print('---')
        return
    
    print('')
    
    # 上传视频
    video_file = upload_video(video_path)
    if not video_file:
        return
    
    print('')
    
    # 分析视频
    analysis = analyze_video(video_file)
    if not analysis:
        return
    
    print('')
    
    # 保存结果
    save_results(video_path, analysis)
    
    print('')
    print('✅ 分析完成！')

if __name__ == '__main__':
    main()
