#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双账号内容生成器 - 小红书智能自进化系统

太一 v2.1 - 双账号特别版
功能：双账号配置 | MJ Prompt 生成 | 内容包输出
"""

import json
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.shanmu_agent import ShanmuAgent


class DualAccountGenerator:
    """双账号内容生成器"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.config_dir = self.workspace / "projects" / "xiaohongshu-agent" / "config"
        self.output_dir = self.workspace / "projects" / "xiaohongshu-agent" / "output"
        self.mj_output_dir = self.output_dir / "mj_prompts"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.mj_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载账号配置
        self.accounts = self._load_accounts()
        
        # 初始化山木 Agent
        self.shanmu = ShanmuAgent(workspace)
        
        # MJ Prompt 模板库
        self.mj_prompts = self._load_mj_prompts()
    
    def _load_accounts(self) -> Dict[str, Any]:
        """加载账号配置"""
        config_file = self.config_dir / "accounts.json"
        if config_file.exists():
            return json.loads(config_file.read_text(encoding='utf-8'))
        
        # 默认配置
        return {
            "account1": {
                "name": "SAYELF 山野精灵",
                "positioning": "AI + 交易 + 壁纸",
                "style": "极简黑客风",
                "target_audience": "25-40 岁 搞钱青年",
                "content_direction": "AI 工具/交易信号/极简壁纸",
                "best_publish_time": "19:00-21:00"
            },
            "account2": {
                "name": "SAYELF 壁纸屋",
                "positioning": "治愈系壁纸",
                "style": "温暖治愈风",
                "target_audience": "18-35 岁 女性",
                "content_direction": "治愈系壁纸/情感共鸣",
                "best_publish_time": "21:00-23:00"
            }
        }
    
    def _load_mj_prompts(self) -> Dict[str, Any]:
        """加载 MJ Prompt 模板"""
        return {
            "山野精灵": {
                "base_style": "minimalist, hacker aesthetic, dark mode, clean lines, monochrome, tech vibe",
                "templates": {
                    "AI 工具": "minimalist AI technology illustration, {topic}, dark background, neon accent colors, futuristic, clean composition, --ar 3:4 --v 6",
                    "交易": "financial data visualization, {topic}, dark theme, green and red accents, professional, minimal, --ar 3:4 --v 6",
                    "壁纸": "abstract minimalist wallpaper, {topic}, dark mode, geometric shapes, monochrome with one accent color, --ar 3:4 --v 6"
                }
            },
            "壁纸屋": {
                "base_style": "healing, warm tones, soft colors, dreamy, emotional, cozy",
                "templates": {
                    "春日": "soft spring theme wallpaper, {topic}, pastel colors, cherry blossoms, gentle lighting, dreamy atmosphere, healing vibe, --ar 3:4 --v 6",
                    "治愈": "healing landscape illustration, {topic}, warm colors, soft clouds, peaceful, serene, cozy feeling, --ar 3:4 --v 6",
                    "情感": "emotional abstract art, {topic}, soft gradient, warm tones, dreamy, romantic, gentle mood, --ar 3:4 --v 6",
                    "风景": "beautiful scenery wallpaper, {topic}, soft focus, warm sunset colors, peaceful, healing, --ar 3:4 --v 6"
                }
            }
        }
    
    def generate_daily_content(self, hot_topics: List[str] = None) -> Dict[str, Any]:
        """
        生成双账号每日内容
        
        参数:
            hot_topics: 热搜话题列表 (可选)
        
        返回:
            双账号内容包
        """
        print("=" * 80)
        print("🎨 双账号内容生成器")
        print("=" * 80)
        print(f"📅 日期：{datetime.now().strftime('%Y-%m-%d')}")
        print(f"📱 账号 1: {self.accounts['account1']['name']}")
        print(f"📱 账号 2: {self.accounts['account2']['name']}")
        print("=" * 80)
        
        # 如果没有热搜，使用默认话题
        if not hot_topics:
            hot_topics = ["春日壁纸", "AI 工具", "治愈系", "交易信号", "极简生活"]
        
        content_package = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "account1": self._generate_account_content("account1", hot_topics),
            "account2": self._generate_account_content("account2", hot_topics),
            "mj_prompts": []
        }
        
        # 生成 MJ Prompts
        print("\n🎨 生成 MJ Prompts...")
        content_package["mj_prompts"] = self._generate_mj_prompts(content_package)
        
        # 保存内容包
        package_path = self._save_content_package(content_package)
        print(f"\n✅ 内容包已保存：{package_path}")
        
        # 保存 MJ Prompts 单独文件
        mj_path = self._save_mj_prompts(content_package["mj_prompts"])
        print(f"✅ MJ Prompts 已保存：{mj_path}")
        
        print("\n" + "=" * 80)
        print("✅ 双账号内容生成完成！")
        print("=" * 80)
        
        return content_package
    
    def _generate_account_content(self, account_key: str, hot_topics: List[str]) -> Dict[str, Any]:
        """生成单个账号内容"""
        account = self.accounts[account_key]
        print(f"\n📱 生成 {account['name']} 内容...")
        
        # 根据账号定位选择话题
        selected_topics = self._select_topics_for_account(account, hot_topics)
        
        notes = []
        for topic in selected_topics[:2]:  # 每个账号生成 2 篇
            # 确定风格
            style = self._determine_style(account, topic)
            
            # 创作笔记
            note = self.shanmu.create_complete_note(
                topic=topic,
                style=style,
                target_audience=account["target_audience"]
            )
            
            # 添加账号信息
            note["account"] = account["name"]
            note["account_style"] = account["style"]
            
            # 生成 MJ Prompt
            mj_prompt = self._create_mj_prompt(account, topic, note)
            note["mj_prompt"] = mj_prompt
            
            notes.append(note)
            print(f"  ✅ {topic}: {note['title'][:40]}...")
        
        return {
            "account_info": account,
            "notes": notes,
            "total_notes": len(notes)
        }
    
    def _select_topics_for_account(self, account: Dict, topics: List[str]) -> List[str]:
        """根据账号定位选择话题"""
        if account["name"] == "SAYELF 山野精灵":
            # 山野精灵：AI/交易/科技类
            priority = ["AI", "交易", "科技", "壁纸", "副业"]
        else:
            # 壁纸屋：治愈/情感/风景类
            priority = ["壁纸", "治愈", "情感", "风景", "春日"]
        
        # 排序话题
        sorted_topics = []
        for p in priority:
            for t in topics:
                if p in t and t not in sorted_topics:
                    sorted_topics.append(t)
        
        # 添加剩余话题
        for t in topics:
            if t not in sorted_topics:
                sorted_topics.append(t)
        
        return sorted_topics[:3]
    
    def _determine_style(self, account: Dict, topic: str) -> str:
        """确定内容风格"""
        if account["name"] == "SAYELF 山野精灵":
            if "AI" in topic or "教程" in topic:
                return "教程类"
            elif "交易" in topic:
                return "分享类"
            else:
                return "分享类"
        else:
            if "情感" in topic or "治愈" in topic:
                return "治愈系"
            elif "风景" in topic:
                return "治愈系"
            else:
                return "治愈系"
    
    def _create_mj_prompt(self, account: Dict, topic: str, note: Dict) -> Dict[str, str]:
        """创建 MJ Prompt"""
        account_name = account["name"]
        
        # 确定模板类型
        if account_name == "SAYELF 山野精灵":
            if "AI" in topic:
                template_type = "AI 工具"
            elif "交易" in topic:
                template_type = "交易"
            else:
                template_type = "壁纸"
        else:
            if "春日" in topic or "春" in topic:
                template_type = "春日"
            elif "情感" in topic:
                template_type = "情感"
            elif "风景" in topic:
                template_type = "风景"
            else:
                template_type = "治愈"
        
        # 获取模板
        base_template = self.mj_prompts.get(account_name.split()[-1], {}).get("templates", {})
        template = base_template.get(template_type, base_template.get("治愈", ""))
        
        # 替换话题
        prompt = template.format(topic=topic) if "{topic}" in template else f"{template}, {topic}"
        
        # 添加风格修饰词
        if account_name == "SAYELF 山野精灵":
            prompt += " --style raw --q 2"
        else:
            prompt += " --style scenic --q 2"
        
        return {
            "prompt": prompt,
            "style": account["style"],
            "topic": topic,
            "account": account_name
        }
    
    def _generate_mj_prompts(self, content_package: Dict) -> List[Dict]:
        """汇总所有 MJ Prompts"""
        prompts = []
        
        for account_key in ["account1", "account2"]:
            account_data = content_package[account_key]
            for note in account_data["notes"]:
                if "mj_prompt" in note:
                    prompts.append(note["mj_prompt"])
        
        return prompts
    
    def _save_content_package(self, package: Dict) -> Path:
        """保存内容包"""
        date = package["date"]
        
        # 生成 Markdown 格式的内容包
        md_content = self._format_content_package(package)
        
        filepath = self.output_dir / f"dual_account_{date}.md"
        filepath.write_text(md_content, encoding='utf-8')
        
        # 同时保存 JSON 格式
        json_path = self.output_dir / f"dual_account_{date}.json"
        json_path.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding='utf-8')
        
        return filepath
    
    def _format_content_package(self, package: Dict) -> str:
        """格式化内容包为 Markdown"""
        date = package["date"]
        
        md = f"""# 小红书双账号内容包

> **日期**: {date}  
> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **账号**: {self.accounts['account1']['name']} | {self.accounts['account2']['name']}

---

## 📱 账号 1: {self.accounts['account1']['name']}

**定位**: {self.accounts['account1']['positioning']}  
**风格**: {self.accounts['account1']['style']}  
**最佳发布**: {self.accounts['account1']['best_publish_time']}

"""
        # 账号 1 笔记
        for i, note in enumerate(package["account1"]["notes"], 1):
            md += f"""
### 笔记 {i}: {note['topic']}

**标题**: {note['title']}

**正文**:
```
{note['content']}
```

**标签**: {' '.join(note['tags'])}

**MJ Prompt**:
```
{note['mj_prompt']['prompt']}
```

**发布建议**: {note['best_publish_time']}

---
"""
        
        # 账号 2
        md += f"""
## 📱 账号 2: {self.accounts['account2']['name']}

**定位**: {self.accounts['account2']['positioning']}  
**风格**: {self.accounts['account2']['style']}  
**最佳发布**: {self.accounts['account2']['best_publish_time']}

"""
        for i, note in enumerate(package["account2"]["notes"], 1):
            md += f"""
### 笔记 {i}: {note['topic']}

**标题**: {note['title']}

**正文**:
```
{note['content']}
```

**标签**: {' '.join(note['tags'])}

**MJ Prompt**:
```
{note['mj_prompt']['prompt']}
```

**发布建议**: {note['best_publish_time']}

---
"""
        
        # MJ Prompts 汇总
        md += """
## 🎨 MJ Prompts 汇总

直接复制以下 Prompts 到 Midjourney 生成图片：

"""
        for i, prompt_data in enumerate(package["mj_prompts"], 1):
            md += f"""
### Prompt {i} ({prompt_data['account']})

```
{prompt_data['prompt']}
```

"""
        
        md += """
---

## 📋 发布清单

- [ ] 复制文案到小红书
- [ ] 使用 MJ Prompt 生成图片
- [ ] 上传图片到小红书
- [ ] 添加标签
- [ ] 选择最佳时间发布
- [ ] 回复评论互动

---

*内容包生成：太一 AGI · 小红书双账号系统*
*版本：v2.1 | {date}*
"""
        
        return md
    
    def _save_mj_prompts(self, prompts: List[Dict]) -> Path:
        """单独保存 MJ Prompts"""
        date = datetime.now().strftime('%Y%m%d')
        
        content = "# MJ Prompts - 小红书双账号\n\n"
        content += f"**日期**: {date}\n\n"
        content += "直接复制以下 Prompts 到 Midjourney 生成图片：\n\n"
        
        for i, prompt_data in enumerate(prompts, 1):
            content += f"### {i}. {prompt_data['account']} - {prompt_data['topic']}\n\n"
            content += "```\n"
            content += f"{prompt_data['prompt']}\n"
            content += "```\n\n"
        
        filepath = self.mj_output_dir / f"mj_prompts_{date}.md"
        filepath.write_text(content, encoding='utf-8')
        
        return filepath


def main():
    """测试双账号生成器"""
    generator = DualAccountGenerator()
    
    # 生成每日内容
    package = generator.generate_daily_content()
    
    print(f"\n📊 汇总:")
    print(f"- 账号 1 笔记：{package['account1']['total_notes']} 篇")
    print(f"- 账号 2 笔记：{package['account2']['total_notes']} 篇")
    print(f"- MJ Prompts: {len(package['mj_prompts'])} 个")


if __name__ == "__main__":
    generator = DualAccountGenerator()
    generator.generate_daily_content()
