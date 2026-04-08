#!/usr/bin/env python3
# scripts/validate-skill-metadata.py
# 用途：验证技能元数据是否符合标准

import yaml
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "skill", "version", "author", "created",
    "status", "triggers", "permissions",
    "max_context_tokens", "priority", "description"
]

VALID_STATUS = ["stable", "beta", "experimental", "deprecated"]
VALID_PERMISSIONS = [
    "exec", "web_fetch", "canvas", "message",
    "file_read", "file_write", "file_delete",
    "web_search", "image_generate"
]

def validate_skill(skill_path):
    """验证技能元数据"""
    content = Path(skill_path).read_text()
    
    if not content.startswith("---"):
        return False, "缺少 YAML Frontmatter"
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "YAML Frontmatter 格式错误"
    
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return False, f"YAML 解析错误：{e}"
    
    # 检查必填字段
    missing = [f for f in REQUIRED_FIELDS if f not in meta]
    if missing:
        return False, f"缺少必填字段：{', '.join(missing)}"
    
    # 验证 status
    if meta["status"] not in VALID_STATUS:
        return False, f"无效 status: {meta['status']}"
    
    # 验证 permissions
    invalid_perms = [p for p in meta["permissions"] if p not in VALID_PERMISSIONS]
    if invalid_perms:
        return False, f"无效权限：{', '.join(invalid_perms)}"
    
    # 验证 priority
    if meta["priority"] not in [1, 2, 3]:
        return False, f"无效 priority: {meta['priority']}"
    
    # 验证 triggers 数量
    if len(meta["triggers"]) < 3:
        return False, f"triggers 过少 ({len(meta['triggers'])} < 3)"
    
    return True, "验证通过"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-skill-metadata.py <skill.md>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    valid, message = validate_skill(skill_path)
    
    if valid:
        print(f"✅ {skill_path}: {message}")
        sys.exit(0)
    else:
        print(f"❌ {skill_path}: {message}")
        sys.exit(1)
