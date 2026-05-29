#!/usr/bin/env python3
"""
guizang-bridge — art-agent 归藏 PPT 引擎桥接模块 (v1.0)
=====================================================
将 op7418/guizang-ppt-skill (12.7K⭐) 的 HTML 演示文稿能力
注入 art-agent 的统一调度系统。

两种风格：
  A - 电子杂志 × 电子墨水（衬线 + WebGL 流体背景 + 暖色）
  B - 瑞士国际主义（无衬线 + 网格点阵 + IKB/柠檬黄/柠檬绿/安全橙）
"""

import json, os, shutil, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent.parent
GUIZANG_DIR = SKILL_DIR / "guizang-ppt-skill"
TEMPLATES = {
    "magazine": GUIZANG_DIR / "assets" / "template.html",
    "swiss": GUIZANG_DIR / "assets" / "template-swiss.html",
}
REFERENCES = {
    "magazine": {
        "layouts": GUIZANG_DIR / "references" / "layouts.md",
        "themes": GUIZANG_DIR / "references" / "themes.md",
    },
    "swiss": {
        "layouts": GUIZANG_DIR / "references" / "layouts-swiss.md",
        "themes": GUIZANG_DIR / "references" / "themes-swiss.md",
    }
}

STYLE_THEMES = {
    "magazine": [
        {"id": "1", "name": "墨水经典", "desc": "通用 / 商业发布"},
        {"id": "2", "name": "靛蓝瓷", "desc": "科技 / 数据 / 技术发布会"},
        {"id": "3", "name": "森林墨", "desc": "自然 / 可持续 / 文化"},
        {"id": "4", "name": "牛皮纸", "desc": "怀旧 / 人文 / 文学"},
        {"id": "5", "name": "沙丘", "desc": "艺术 / 设计 / 创意"},
    ],
    "swiss": [
        {"id": "ikb", "name": "克莱因蓝 IKB", "desc": "瑞士风格经典蓝"},
        {"id": "lemonyellow", "name": "柠檬黄", "desc": "高反差醒目黄"},
        {"id": "lemongreen", "name": "柠檬绿", "desc": "科技/环保绿"},
        {"id": "safetyorange", "name": "安全橙", "desc": "警示/数据橙"},
    ]
}


class GuizangBridge:
    """归藏 PPT 桥接 — 在 art-agent 中被调度器自动路由调用"""
    
    def __init__(self):
        self.name = "归藏PPT引擎"
        self.version = "1.0.0"
    
    def list_styles(self) -> dict:
        return {
            "magazine": {
                "name": "电子杂志 × 电子墨水",
                "themes": STYLE_THEMES["magazine"],
                "layouts_count": 10,
            },
            "swiss": {
                "name": "瑞士国际主义 Swiss Style",
                "themes": STYLE_THEMES["swiss"],
                "layouts_count": 10,
            }
        }
    
    def recommend_style(self, content: str) -> str:
        swiss_kw = ["数据", "科技", "技术", "产品", "KPI", "swiss", "瑞士", "极简"]
        magazine_kw = ["人文", "故事", "文化", "杂志", "趋势", "分享", "设计"]
        return "swiss" if sum(1 for k in swiss_kw if k in content.lower()) >= \
                           sum(1 for k in magazine_kw if k in content.lower()) else "magazine"
    
    def create_project(self, output_dir: str, style: str = "magazine") -> dict:
        out = Path(output_dir)
        ppt_dir = out / "ppt"
        images_dir = ppt_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        template = TEMPLATES.get(style)
        if not template or not template.exists():
            return {"error": f"Template '{style}' not found at {template}"}
        
        dest = ppt_dir / "index.html"
        shutil.copy2(str(template), str(dest))
        
        return {
            "success": True, "path": str(ppt_dir),
            "template": str(dest), "images": str(images_dir),
        }
    
    def process(self, task: str = "", **kwargs) -> dict:
        """art-agent dispatcher 调用的统一入口（接收所有**kwargs）"""
        params = kwargs
        
        style = params.get("style", "auto")
        if style == "auto":
            style = self.recommend_style(task + str(params))
        
        output_dir = params.get("output_dir", "/tmp/guizang-ppt")
        project = self.create_project(output_dir, style)
        
        if "error" in project:
            return project
        
        # Replace template title
        title = params.get("title", "未命名演示文稿")
        index_path = Path(project["template"])
        html = index_path.read_text(encoding="utf-8")
        html = html.replace("[必填] 替换为 PPT 标题", title)
        index_path.write_text(html, encoding="utf-8")
        
        return {
            "success": True,
            "style": style,
            "project": project,
            "styles": self.list_styles(),
            "reference_files": {
                "layouts": str(REFERENCES.get(style, {}).get("layouts", "")),
                "themes": str(REFERENCES.get(style, {}).get("themes", "")),
                "image_prompts": str(GUIZANG_DIR / "references" / "image-prompts.md"),
            },
            "instructions": [
                "1. Read template CSS before editing slides (class names differ per style)",
                "2. Use layouts from references/layouts.md or layouts-swiss.md",
                "3. Each section needs: light/dark/hero light/hero dark class for rhythm",
                "4. No custom hex colors — pick from 5 (magazine) or 4 (swiss) presets",
                "5. Images in images/ dir, named {page}-{name}.{ext}",
                "6. Validate with: node scripts/validate-swiss-deck.mjs",
            ],
            "disclaimer": "guizang-ppt-skill by 歸藏 (op7418, 12.7K⭐, AGPL-3.0)"
        }
