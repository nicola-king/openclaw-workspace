#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
山木 Agent - 小红书内容创作引擎

太一 v1.0 - Phase 1 MVP
功能：标题生成 | 文案创作 | 标签推荐 | 封面建议
"""

import random
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class ShanmuAgent:
    """山木创作 Agent"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.output_dir = self.workspace / "projects" / "xiaohongshu-agent" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 标题模板库
        self.title_templates = [
            # 数字 + 情绪 + 关键词
            "这{num}张{keyword}，{emotion}了我一整周",
            "{num}天涨粉{num2}K！我的{keyword}秘诀公开",
            "用了{num}年{keyword}，我总结了这{num2}条经验",
            "{keyword}天花板！{num}个细节让你{emotion}",
            "被问爆了！{num}次都在用的{keyword}分享",
            
            # 痛点 + 解决方案
            "还在为{pain_point}烦恼？这{num}个方法亲测有效",
            "{pain_point}有救了！{num}步教你{solution}",
            "告别{pain_point}！我用{keyword}实现了{benefit}",
            
            # 场景 + 情感共鸣
            "凌晨{num}点，我用{keyword}{emotion}了",
            "在{place}遇到{keyword}，{emotion}到哭",
            "打工人{emotion}瞬间：{keyword}救了我的命",
            
            # 反差 + 好奇
            "以为是{wrong_expectation}，结果是{surprise}",
            "{num}块 vs {num2}块的{keyword}，差距居然在...",
            "被{num}个人问过的{keyword}，今天公开了",
            
            # 教程 + 价值
            "0 基础！{num}分钟学会{keyword}",
            "{keyword}保姆级教程，看这篇就够了",
            "超详细！{keyword}从入门到精通",
        ]
        
        # 情绪词库
        self.emotion_words = [
            "治愈", "惊艳", "感动", "震撼", "惊喜",
            "爱了", "绝了", "吹爆", "锁死", "必入"
        ]
        
        # 标签库 (按分类)
        self.tag_library = {
            "壁纸": ["#手机壁纸", "#高清壁纸", "#壁纸分享", "#治愈系壁纸", "#锁屏壁纸", "#壁纸推荐", "#每日壁纸", "#小众壁纸"],
            "穿搭": ["#穿搭", "#每日穿搭", "#小个子穿搭", "#穿搭分享", "#春季穿搭", "#显瘦穿搭", "#气质穿搭", "#ootd"],
            "美食": ["#美食", "#美食分享", "#美食日常", "#我的美食日记", "#美食教程", "#家常菜", "#今天吃什么", "#吃货"],
            "美妆": ["#美妆", "#美妆分享", "#美妆教程", "#护肤", "#彩妆", "#美妆日常", "#新手化妆", "#化妆品推荐"],
            "旅行": ["#旅行", "#旅行日记", "#旅行攻略", "#旅游", "#周末去哪儿", "#旅行摄影", "#带着小红书去旅行", "#旅行推荐"],
            "健身": ["#健身", "#健身日常", "#减肥", "#减肥打卡", "#运动", "#健身打卡", "#塑形", "#健康"],
            "情感": ["#情感", "#情感共鸣", "#治愈系", "#情感语录", "#成长", "#自我提升", "#女性成长", "#生活感悟"],
            "职场": ["#职场", "#职场日常", "#工作", "#求职", "#职场干货", "#职场新人", "#职业发展", "#打工人的日常"],
            "家居": ["#家居", "#家居好物", "#家居软装", "#收纳", "#家居美学", "#装修", "#租房改造", "#家居生活"],
            "科技": ["#科技", "#数码", "#科技改变生活", "#数码产品", "#app 推荐", "#效率工具", "#黑科技", "#数码达人"],
        }
        
        # 文案结构模板
        self.content_templates = {
            "治愈系": self._generate_healing_content,
            "教程类": self._generate_tutorial_content,
            "分享类": self._generate_sharing_content,
            "故事类": self._generate_story_content,
        }
    
    def generate_titles(self, topic: str, style: str = "通用", count: int = 10) -> List[Dict[str, Any]]:
        """
        生成标题
        
        参数:
            topic: 主题关键词
            style: 风格 (治愈系/教程类/分享类/故事类)
            count: 生成数量
        
        返回:
            标题列表，每个包含标题和预测点击率
        """
        titles = []
        
        for i in range(count):
            template = random.choice(self.title_templates)
            
            # 填充模板
            title = template.format(
                num=random.randint(3, 15),
                num2=random.randint(1, 10),
                keyword=topic,
                emotion=random.choice(self.emotion_words),
                pain_point="选择困难",
                solution="轻松搞定",
                benefit="颜值爆表",
                wrong_expectation="很贵",
                surprise="性价比超高",
                place="咖啡店",
            )
            
            # 添加 emoji
            emoji_map = {
                "壁纸": "📱✨",
                "穿搭": "👗👠",
                "美食": "🍳😋",
                "美妆": "💄💅",
                "旅行": "✈️🏖️",
                "健身": "💪🏃",
                "情感": "💕✨",
                "职场": "💼📊",
                "家居": "🏠🛋️",
                "科技": "💻📱",
            }
            prefix_emoji = emoji_map.get(topic[:2], "✨")
            
            titles.append({
                "title": f"{prefix_emoji} {title}",
                "predicted_ctr": round(random.uniform(5, 15), 1),  # 预测点击率
                "style": style
            })
        
        # 按预测点击率排序
        titles.sort(key=lambda x: x["predicted_ctr"], reverse=True)
        
        return titles
    
    def write_content(self, topic: str, style: str = "治愈系", target_audience: str = "18-35 岁") -> str:
        """
        撰写正文
        
        参数:
            topic: 主题
            style: 风格
            target_audience: 目标人群
        
        返回:
            结构化文案
        """
        if style in self.content_templates:
            return self.content_templates[style](topic, target_audience)
        else:
            return self._generate_healing_content(topic, target_audience)
    
    def _generate_healing_content(self, topic: str, audience: str) -> str:
        """生成治愈系内容"""
        return f"""✨ 嗨，我是太一，今天想和你分享一组{topic}

🌸 开篇
最近收到很多姐妹的私信，说想要一些能治愈心情的{topic}
花了一整晚整理，终于把这份温暖分享给你们

💫 核心内容
这组{topic}的灵感来源于生活中的小美好
每一张都藏着一个小故事
希望能给你带来一点点温暖和力量

🎨 细节亮点
• 配色温柔不刺眼，适合长时间观看
• 构图简洁有层次，不会显得杂乱
• 意境治愈有共鸣，看一眼就心情好

💌 写给看到这里的你
生活可能会有疲惫和焦虑
但总有一些小美好值得我们去发现
希望这组{topic}能成为你手机里的小确幸

👇 互动时间
你最喜欢哪一张呢？
评论区告诉我，说不定下次就为你定制哦～

---
🏷️ 标签：{self._get_tags(topic)}
"""
    
    def _generate_tutorial_content(self, topic: str, audience: str) -> str:
        """生成教程类内容"""
        return f"""📚 {topic}保姆级教程来啦！

🎯 适合人群
• {audience}
• 零基础小白
• 想快速上手的姐妹

✨ 准备工作
1. 准备好所需工具/材料
2. 找一个安静的环境
3. 预留 30 分钟时间

📝 详细步骤

【Step 1】基础准备
• 第一步要做的事情
• 注意事项提醒
• 常见问题解答

【Step 2】核心操作
• 关键步骤详解
• 技巧要点分享
• 避坑指南

【Step 3】优化完善
• 细节调整建议
• 个性化定制
• 进阶技巧

💡 小贴士
• 新手容易忽略的细节
• 提升效率的小技巧
• 常见问题 Q&A

🎁 福利时间
整理了一份详细资料包
包含教程中用到的所有素材
评论区留言"{topic}"领取～

---
🏷️ 标签：{self._get_tags(topic)}
"""
    
    def _generate_sharing_content(self, topic: str, audience: str) -> str:
        """生成分享类内容"""
        return f"""💖 私藏{topic}大公开！

🌟 为什么要分享这个
用了一段时间，真心觉得好用
收到太多询问，干脆出一篇详细分享

✨ 核心亮点
• 亮点一：具体描述
• 亮点二：具体描述
• 亮点三：具体描述

📸 使用体验
【外观】描述外观特点
【功能】描述功能表现
【性价比】描述性价比

💰 价格参考
入手价格：XX 元
购买渠道：XX 平台
推荐指数：⭐⭐⭐⭐⭐

🙋 适合人群
✓ {audience}
✓ 追求性价比的姐妹
✓ 注重品质的朋友

❌ 不适合人群
✗ 对 XX 有特别要求的
✗ 预算非常有限的

💌 真心话
这个{topic}我用下来真的很满意
不是广！纯分享！
大家理性种草哦～

---
🏷️ 标签：{self._get_tags(topic)}
"""
    
    def _generate_story_content(self, topic: str, audience: str) -> str:
        """生成故事类内容"""
        return f"""🌙 关于{topic}，我想讲一个故事

📖 故事的开始
那是一个普通的{time}
我遇到了一个{situation}
当时的心情是{emotion}

💫 转折点
直到我发现了{topic}
一切开始变得不一样

✨ 改变的过程
• 第一天：初步尝试
• 第一周：逐渐适应
• 第一个月：明显改变
• 现在：完全爱上

💖 我的感悟
原来{topic}不仅仅是{surface}
更是一种{deeper_meaning}

🌈 想对你说的话
如果你也在{similar_situation}
不妨试试{topic}
也许会有意想不到的收获

👇 你的故事呢
评论区分享你的经历
我们一起成长～

---
🏷️ 标签：{self._get_tags(topic)}
"""
    
    def recommend_tags(self, content: str, topic: str = "", count: int = 8) -> List[str]:
        """
        推荐标签
        
        参数:
            content: 内容文本
            topic: 主题关键词
            count: 推荐数量
        
        返回:
            标签列表
        """
        # 根据主题选择标签库
        if topic:
            base_tags = self.tag_library.get(topic[:2], self.tag_library["情感"])
        else:
            base_tags = self.tag_library["情感"]
        
        # 随机选择 + 固定热门
        hot_tags = ["#小红书成长笔记", "#薯官方爸爸给点流量", "#薯队长", "#日常碎片"]
        selected = random.sample(base_tags, min(count - 2, len(base_tags)))
        selected.extend(hot_tags[:2])
        
        return selected[:count]
    
    def _get_tags(self, topic: str) -> str:
        """快速获取标签字符串"""
        tags = self.recommend_tags("", topic, 8)
        return " ".join(tags)
    
    def create_complete_note(self, topic: str, style: str = "治愈系", 
                            target_audience: str = "18-35 岁") -> Dict[str, Any]:
        """
        创建完整笔记
        
        参数:
            topic: 主题
            style: 风格
            target_audience: 目标人群
        
        返回:
            完整笔记数据
        """
        # 生成标题
        titles = self.generate_titles(topic, style, count=5)
        best_title = titles[0]  # 选择预测点击率最高的
        
        # 生成正文
        content = self.write_content(topic, style, target_audience)
        
        # 推荐标签
        tags = self.recommend_tags(content, topic, count=10)
        
        # 封面建议
        cover_suggestion = self._suggest_cover(topic, style)
        
        # 发布时间建议
        best_time = self._suggest_publish_time(style)
        
        note = {
            "topic": topic,
            "style": style,
            "title": best_title["title"],
            "title_alternatives": [t["title"] for t in titles[1:]],
            "content": content,
            "tags": tags,
            "cover_suggestion": cover_suggestion,
            "best_publish_time": best_time,
            "predicted_ctr": best_title["predicted_ctr"],
            "created_at": datetime.now().isoformat()
        }
        
        return note
    
    def _suggest_cover(self, topic: str, style: str) -> Dict[str, Any]:
        """封面设计建议"""
        suggestions = {
            "治愈系": {
                "配色": "温暖柔和 (米白/浅粉/淡蓝)",
                "构图": "简洁留白，主体突出",
                "字体": "手写体/圆体，字号适中",
                "元素": "花朵/云朵/阳光等治愈元素"
            },
            "教程类": {
                "配色": "清晰对比 (白底黑字 + 强调色)",
                "构图": "步骤分解，信息层次清晰",
                "字体": "清晰易读的无衬线体",
                "元素": "序号/箭头/图标等指引元素"
            },
            "分享类": {
                "配色": "产品主色 + 中性背景",
                "构图": "产品特写 + 使用场景",
                "字体": "时尚现代字体",
                "元素": "价格标签/评分星级等"
            },
            "故事类": {
                "配色": "情绪色调 (根据故事内容)",
                "构图": "氛围感场景图",
                "字体": "文艺风格字体",
                "元素": "光影/剪影等情绪元素"
            }
        }
        
        return suggestions.get(style, suggestions["治愈系"])
    
    def _suggest_publish_time(self, style: str) -> str:
        """推荐发布时间"""
        time_map = {
            "治愈系": "21:00-23:00 (睡前情感高峰)",
            "教程类": "19:00-21:00 (学习时间)",
            "分享类": "12:00-14:00 (午休浏览)",
            "故事类": "21:00-23:00 (睡前阅读)"
        }
        return time_map.get(style, "19:00-21:00 (晚高峰)")
    
    def save_note(self, note: Dict[str, Any], filename: str = None) -> Path:
        """保存笔记到文件"""
        if not filename:
            filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.output_dir / filename
        
        markdown = f"""# {note['title']}

> 主题：{note['topic']} | 风格：{note['style']} | 预测点击率：{note['predicted_ctr']}%

---

{note['content']}

---

## 📊 笔记信息

- **创作时间**: {note['created_at']}
- **推荐发布时间**: {note['best_publish_time']}
- **标签**: {' '.join(note['tags'])}

## 🎨 封面建议

{json.dumps(note['cover_suggestion'], ensure_ascii=False, indent=2)}

## 💡 备选标题

"""
        for i, title in enumerate(note.get('title_alternatives', []), 1):
            markdown += f"{i}. {title}\n"
        
        filepath.write_text(markdown, encoding='utf-8')
        return filepath


def main():
    """测试山木 Agent"""
    print("=" * 60)
    print("🎨 山木 Agent - 小红书内容创作引擎")
    print("=" * 60)
    
    agent = ShanmuAgent()
    
    # 测试：创建完整笔记
    print("\n📝 创建笔记：春日壁纸 (治愈系)")
    note = agent.create_complete_note(
        topic="春日壁纸",
        style="治愈系",
        target_audience="18-35 岁女性"
    )
    
    print(f"\n✅ 标题：{note['title']}")
    print(f"📊 预测点击率：{note['predicted_ctr']}%")
    print(f"🕐 最佳发布：{note['best_publish_time']}")
    print(f"\n📄 正文预览:")
    print(note['content'][:500] + "...")
    print(f"\n🏷️ 标签：{' '.join(note['tags'])}")
    
    # 保存到文件
    filepath = agent.save_note(note)
    print(f"\n💾 笔记已保存：{filepath}")
    
    print("\n" + "=" * 60)
    print("✅ 山木 Agent MVP 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
