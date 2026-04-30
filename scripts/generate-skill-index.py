#!/usr/bin/env python3
# scripts/generate-skill-index.py
# 用途：生成技能索引文件

import yaml
import json
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path(__file__).parent.parent / "skills"
OUTPUT_FILE = SKILLS_DIR / "index.json"

def parse_skill_meta(skill_path):
    """解析技能元数据"""
    content = skill_path.read_text()
    if not content.startswith("---"):
        return None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    return yaml.safe_load(parts[1])

def generate_index():
    """生成技能索引"""
    skills = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        meta = parse_skill_meta(skill_md)
        if meta:
            skills.append({
                "name": meta.get("skill", skill_dir.name),
                "version": meta.get("version", "0.0.0"),
                "author": meta.get("author", "unknown"),
                "status": meta.get("status", "unknown"),
                "triggers": meta.get("triggers", []),
                "permissions": meta.get("permissions", []),
                "priority": meta.get("priority", 2),
                "description": meta.get("description", ""),
                "path": str(skill_md.relative_to(SKILLS_DIR.parent)),
                "loaded": False,
                "last_used": None,
                "use_count": 0
            })
    
    index = {
        "skills": skills,
        "count": len(skills),
        "updated": datetime.now().isoformat()
    }
    
    OUTPUT_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"✅ 生成技能索引：{len(skills)} 个技能")
    return index

if __name__ == "__main__":
    generate_index()
