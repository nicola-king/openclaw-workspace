#!/usr/bin/env python3
"""
定制产品 Agent — 调度编排器
精准渗透，建立深度信任
"""
import sys, json, os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("custom-products-agent")

SKILLS = {
    "persona_builder": "联系人深度画像",
    "solution_composer": "定制方案文档生成",
    "rfq_parser": "RFQ解析+技术参数提取",
    "relationship_log": "长周期跟进记录",
    "sample_tracker": "打样进度管理",
    "tech_doc_pack": "技术文档/认证资料打包",
}

CATEGORIES = {
    "steel-structure": {"name": "钢结构集成房", "skills": ["project_radar", "spec_builder", "compliance_check"]},
    "transformer": {"name": "变压器", "skills": ["tender_monitor", "cert_tracker", "load_calculator"]},
    "auto-parts": {"name": "摩配汽配", "skills": ["oem_matcher", "catalog_builder", "warranty_tracker"]},
    "energy-storage": {"name": "储能", "skills": ["policy_radar", "roi_calculator", "bms_spec_parser"]},
}

def run_skill(skill_name, **params):
    path = os.path.join(os.path.dirname(__file__), "skills", skill_name)
    if os.path.exists(os.path.join(path, "core.py")):
        logger.info(f"执行技能: {skill_name}")
        return {"status": "ok", "skill": skill_name}
    # 检查品类skills
    for cat, info in CATEGORIES.items():
        if skill_name in info["skills"]:
            cat_path = os.path.join(os.path.dirname(__file__), "categories", cat, "skills", skill_name)
            if os.path.exists(os.path.join(cat_path, "core.py")):
                return {"status": "ok", "skill": skill_name, "category": cat}
    return {"status": "error", "message": f"技能 {skill_name} 尚未实现"}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print("🔧 定制产品 Agent")
        print("\n通用技能:")
        for k, v in SKILLS.items():
            print(f"  {k:25s} - {v}")
        print("\n品类技能:")
        for cat, info in CATEGORIES.items():
            print(f"\n  {info['name']}:")
            for s in info["skills"]:
                print(f"    {s}")
    elif cmd in SKILLS:
        result = run_skill(cmd)
        print(json.dumps(result, ensure_ascii=False))
    else:
        cats = sum([info["skills"] for info in CATEGORIES.values()], [])
        if cmd in cats:
            result = run_skill(cmd)
            print(json.dumps(result, ensure_ascii=False))
        else:
            all_skills = list(SKILLS.keys()) + cats
            print(f"用法: python3 orchestrator.py [list|{'|'.join(all_skills[:5)]}...]")
