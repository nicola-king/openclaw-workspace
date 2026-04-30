#!/usr/bin/env python3
"""
GEO 自动化发布工作流
功能：将内容自动发布到多平台（知乎/公众号/小红书等）
使用：python3 geo-publisher.py

开源免费，基于 OpenClaw 生态
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 配置
CONFIG = {
    'content_dir': '/home/nicola/.openclaw/workspace/geo-content',
    'output_dir': '/home/nicola/.openclaw/workspace/geo-published',
    'platforms': [
        'zhihu',      # 知乎专栏
        'wechat',     # 微信公众号
        'xiaohongshu', # 小红书
        'juejin',     # 掘金
        'douban',     # 豆瓣小组
    ],
    'auto_publish': False,  # True=自动发布，False=生成待发布文件
}

# 平台配置模板
PLATFORM_TEMPLATES = {
    'zhihu': {
        'name': '知乎专栏',
        'url': 'https://zhuanlan.zhihu.com/',
        'format': 'markdown',
        'max_length': 50000,
        'supports_images': True,
        'supports_links': True,
        'tips': '标题要吸引，开头 50 字决定点击率'
    },
    'wechat': {
        'name': '微信公众号',
        'url': 'https://mp.weixin.qq.com/',
        'format': 'markdown',
        'max_length': 20000,
        'supports_images': True,
        'supports_links': False,  # 公众号外链受限
        'tips': '排版要精美，适合手机阅读'
    },
    'xiaohongshu': {
        'name': '小红书',
        'url': 'https://www.xiaohongshu.com/',
        'format': 'text + images',
        'max_length': 1000,
        'supports_images': True,
        'supports_links': False,
        'tips': '图文结合，加 emoji，标签很重要'
    },
    'juejin': {
        'name': '掘金',
        'url': 'https://juejin.cn/',
        'format': 'markdown',
        'max_length': 50000,
        'supports_images': True,
        'supports_links': True,
        'tips': '技术内容优先，代码块支持好'
    },
    'douban': {
        'name': '豆瓣小组',
        'url': 'https://www.douban.com/group/',
        'format': 'text',
        'max_length': 10000,
        'supports_images': True,
        'supports_links': True,
        'tips': '语气要亲切，像朋友分享'
    }
}


class GeoPublisher:
    """GEO 内容发布器"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 发布记录
        self.publish_log = []
    
    def load_content(self, content_file: str) -> Dict:
        """加载内容文件"""
        path = Path(content_file)
        
        if not path.exists():
            raise FileNotFoundError(f"内容文件不存在：{path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix == '.json':
                return json.load(f)
            else:
                # Markdown/文本
                return {'content': f.read()}
    
    def adapt_for_platform(self, content: Dict, platform: str) -> str:
        """
        为平台适配内容格式
        
        不同平台有不同要求：
        - 知乎：长文，markdown
        - 公众号：中等长度，精美排版
        - 小红书：短文 + 多图，emoji
        - 掘金：技术文，代码块
        - 豆瓣：亲切语气
        """
        template = PLATFORM_TEMPLATES.get(platform, {})
        max_length = template.get('max_length', 10000)
        
        # 获取原始内容
        raw_content = content.get('content', '')
        title = content.get('title', '')
        
        # 适配逻辑
        if platform == 'xiaohongshu':
            # 小红书：短内容 + emoji
            adapted = self._adapt_xiaohongshu(title, raw_content)
        elif platform == 'wechat':
            # 公众号：精美排版
            adapted = self._adapt_wechat(title, raw_content)
        elif platform == 'zhihu':
            # 知乎：完整内容
            adapted = self._adapt_zhihu(title, raw_content)
        else:
            # 默认：截断到最大长度
            adapted = raw_content[:max_length]
        
        return adapted
    
    def _adapt_xiaohongshu(self, title: str, content: str) -> str:
        """适配小红书格式"""
        # 提取关键点
        lines = content.split('\n')
        key_points = []
        for line in lines[:10]:
            if line.strip() and not line.startswith('#'):
                key_points.append(line.strip())
        
        # 生成小红书风格
        output = f"🍅 {title}\n\n"
        output += "✨ 核心要点：\n"
        for i, point in enumerate(key_points[:5], 1):
            output += f"{i}. {point}\n"
        output += "\n"
        output += "#番茄种植 #园艺 #种植技巧 #阳台种菜 #生活小妙招"
        
        return output[:1000]
    
    def _adapt_wechat(self, title: str, content: str) -> str:
        """适配公众号格式"""
        # 添加公众号风格的排版标记
        output = f"# {title}\n\n"
        output += "---\n\n"
        output += content
        output += "\n\n---\n"
        output += "🌱 更多种植技巧，关注公众号【XXX】\n"
        
        return output[:20000]
    
    def _adapt_zhihu(self, title: str, content: str) -> str:
        """适配知乎格式"""
        # 知乎偏好深度内容
        output = f"# {title}\n\n"
        output += f"> 更新时间：{datetime.now().strftime('%Y-%m-%d')}\n\n"
        output += content
        output += "\n\n---\n"
        output += "*如果觉得有用，欢迎点赞/收藏/关注*\n"
        
        return output[:50000]
    
    def generate_publish_files(self, content: Dict):
        """为各平台生成发布文件"""
        print(f"📤 生成多平台发布文件...")
        print('-' * 60)
        
        for platform in self.config['platforms']:
            template = PLATFORM_TEMPLATES.get(platform, {})
            platform_name = template.get('name', platform)
            
            # 适配内容
            adapted = self.adapt_for_platform(content, platform)
            
            # 保存文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{platform}_{timestamp}.md"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 发布平台：{platform_name}\n")
                f.write(f"# 生成时间：{datetime.now().isoformat()}\n")
                f.write(f"# 发布地址：{template.get('url', 'N/A')}\n")
                f.write(f"# 提示：{template.get('tips', '')}\n\n")
                f.write(adapted)
            
            print(f"   ✅ {platform_name}: {filepath}")
            
            # 记录
            self.publish_log.append({
                'platform': platform,
                'platform_name': platform_name,
                'file': str(filepath),
                'url': template.get('url', ''),
                'length': len(adapted),
                'status': 'pending'
            })
    
    def auto_publish(self, content: Dict):
        """
        自动发布到各平台
        
        注意：这需要各平台的 API 权限
        目前生成待发布文件，手动发布更可靠
        """
        print("⚠️  自动发布功能需要配置各平台 API")
        print("   建议：使用生成的文件手动发布，更稳定")
        print("")
        
        # TODO: 实现各平台 API 集成
        # - 知乎：需要知乎开放平台
        # - 公众号：需要微信开放平台
        # - 小红书：无官方 API，需手动
        # - 掘金：有开放 API
        # - 豆瓣：有开放 API
    
    def save_publish_log(self):
        """保存发布记录"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.output_dir / f"publish_log_{timestamp}.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.publish_log, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 发布记录已保存：{log_file}")
    
    def print_instructions(self):
        """打印发布说明"""
        print('\n' + '=' * 60)
        print('📋 发布说明')
        print('=' * 60)
        print('')
        
        for log in self.publish_log:
            print(f"📍 {log['platform_name']}")
            print(f"   文件：{log['file']}")
            print(f"   地址：{log['url']}")
            print(f"   字数：{log['length']}")
            print(f"   状态：{log['status']}")
            print('')
        
        print('下一步：')
        print('1. 打开生成的文件，检查内容')
        print('2. 访问对应平台，复制粘贴发布')
        print('3. 记录发布链接，用于后续监测')
        print('')
        print('💡 提示：可以配合 OpenClaw 定时任务自动发布')
        print('   配置 crontab: 0 10 * * * python3 geo-publisher.py')
        print('=' * 60)


def main():
    """主程序"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  GEO 自动化发布工作流 v1.0                                ║')
    print('║  开源免费 | 基于 OpenClaw 生态                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    # 检查内容文件
    content_dir = Path(CONFIG['content_dir'])
    if not content_dir.exists():
        print(f"⚠️  内容目录不存在：{content_dir}")
        print("   请先运行 geo-question-generator.py 生成问题")
        print("   然后用 geo-content-generator.py 生成内容")
        return
    
    # 查找最新的内容文件
    content_files = list(content_dir.glob('*.md')) + list(content_dir.glob('*.json'))
    if not content_files:
        print(f"⚠️  内容目录为空：{content_dir}")
        return
    
    latest_content = max(content_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 使用内容文件：{latest_content}")
    print('')
    
    # 加载内容
    publisher = GeoPublisher(CONFIG)
    content = publisher.load_content(str(latest_content))
    
    # 生成发布文件
    publisher.generate_publish_files(content)
    
    # 保存记录
    publisher.save_publish_log()
    
    # 打印说明
    publisher.print_instructions()


if __name__ == '__main__':
    main()
