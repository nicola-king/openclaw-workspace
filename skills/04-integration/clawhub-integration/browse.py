#!/usr/bin/env python3
"""
ClawHub 技能市场浏览

功能:
1. 浏览 ClawHub 技能市场
2. 获取 GitHub AI Agent 榜单
3. 筛选高星技能
4. 分析技能价值

作者：太一 AGI
创建：2026-04-10
"""

import json
import requests
from pathlib import Path
from datetime import datetime

# ClawHub API
CLAWHUB_API = "https://clawhub.com/api/skills"
GITHUB_TRENDING_API = "https://api.github.com/search/repositories"

# 筛选标准
MIN_STARS = 1000
MIN_DOWNLOADS = 100
MAX_AGE_DAYS = 90


def browse_clawhub():
    """浏览 ClawHub 技能市场"""
    try:
        response = requests.get(CLAWHUB_API, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"⚠️  访问 ClawHub 失败：{e}")
    
    # 返回本地缓存
    cache_file = Path(__file__).parent / "cache" / "clawhub_skills.json"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {"skills": []}


def get_github_trending(min_stars=MIN_STARS):
    """获取 GitHub  trending AI Agent"""
    query = "AI agent stars:>1000 pushed:>2026-01-01"
    
    try:
        response = requests.get(
            GITHUB_TRENDING_API,
            params={"q": query, "sort": "stars", "order": "desc"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])[:20]
    except Exception as e:
        print(f"⚠️  获取 GitHub trending 失败：{e}")
    
    return []


def filter_skills(skills):
    """筛选高质量技能"""
    filtered = []
    
    for skill in skills:
        # 检查星级
        if skill.get("stars", 0) < MIN_STARS:
            continue
        
        # 检查更新时间
        updated_at = skill.get("updated_at", "")
        if updated_at:
            try:
                updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                age_days = (datetime.now(updated_date.tzinfo) - updated_date).days
                if age_days > MAX_AGE_DAYS:
                    continue
            except:
                pass
        
        # 检查下载量
        if skill.get("downloads", 0) < MIN_DOWNLOADS:
            continue
        
        filtered.append(skill)
    
    return filtered


def analyze_skill(skill):
    """分析技能价值"""
    score = 0
    
    # 星级评分 (0-40 分)
    stars = skill.get("stars", 0)
    if stars > 10000:
        score += 40
    elif stars > 5000:
        score += 30
    elif stars > 1000:
        score += 20
    elif stars > 100:
        score += 10
    
    # 更新频率 (0-20 分)
    updated_at = skill.get("updated_at", "")
    if updated_at:
        try:
            updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            age_days = (datetime.now(updated_date.tzinfo) - updated_date).days
            if age_days < 7:
                score += 20
            elif age_days < 30:
                score += 15
            elif age_days < 90:
                score += 10
        except:
            pass
    
    # 下载量 (0-20 分)
    downloads = skill.get("downloads", 0)
    if downloads > 1000:
        score += 20
    elif downloads > 100:
        score += 15
    elif downloads > 10:
        score += 10
    
    # 文档质量 (0-10 分)
    has_readme = skill.get("has_readme", False)
    has_license = skill.get("has_license", False)
    if has_readme and has_license:
        score += 10
    elif has_readme:
        score += 5
    
    # 社区活跃度 (0-10 分)
    issues = skill.get("open_issues", 0)
    forks = skill.get("forks", 0)
    if forks > 100 or issues > 50:
        score += 10
    elif forks > 10 or issues > 10:
        score += 5
    
    return {
        "skill": skill,
        "score": score,
        "recommendation": get_recommendation(score)
    }


def get_recommendation(score):
    """获取推荐等级"""
    if score >= 80:
        return "强烈推荐 - 立即安装"
    elif score >= 60:
        return "推荐 - 建议安装"
    elif score >= 40:
        return "可考虑 - 按需安装"
    else:
        return "不推荐 - 跳过"


def main():
    """主函数"""
    print("🛍️  ClawHub 技能市场浏览")
    print("="*60)
    print()
    
    # 浏览 ClawHub
    print("📦 浏览 ClawHub 技能市场...")
    clawhub_data = browse_clawhub()
    clawhub_skills = clawhub_data.get("skills", [])
    print(f"   找到 {len(clawhub_skills)} 个技能")
    
    # 获取 GitHub trending
    print("\n📈 获取 GitHub AI Agent 榜单...")
    github_skills = get_github_trending()
    print(f"   找到 {len(github_skills)} 个 trending 项目")
    
    # 合并技能列表
    all_skills = clawhub_skills + github_skills
    
    # 筛选
    print("\n🔍 筛选高质量技能...")
    filtered_skills = filter_skills(all_skills)
    print(f"   通过筛选：{len(filtered_skills)} 个")
    
    # 分析
    print("\n📊 分析技能价值...")
    analyzed = []
    for skill in filtered_skills[:20]:
        analysis = analyze_skill(skill)
        analyzed.append(analysis)
        
        if analysis["score"] >= 80:
            print(f"   ⭐ {skill.get('name', 'Unknown')} - {analysis['score']}分 - {analysis['recommendation']}")
    
    # 排序
    analyzed.sort(key=lambda x: x["score"], reverse=True)
    
    # 保存结果
    result_file = Path(__file__).parent / "cache" / "skill_analysis.json"
    result_file.parent.mkdir(exist_ok=True)
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_skills": len(all_skills),
            "filtered_skills": len(filtered_skills),
            "analyzed_skills": analyzed
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 分析结果已保存：{result_file}")
    print()
    
    # 显示 Top 10
    print("🏆 Top 10 推荐技能:")
    print("-"*60)
    for i, item in enumerate(analyzed[:10], 1):
        skill = item["skill"]
        print(f"{i}. {skill.get('name', 'Unknown')}")
        print(f"   评分：{item['score']}分 - {item['recommendation']}")
        print(f"   星级：{skill.get('stars', 0)} | 下载：{skill.get('downloads', 0)} | 更新：{skill.get('updated_at', 'Unknown')[:10]}")
        print()
    
    return analyzed


if __name__ == "__main__":
    import sys
    sys.exit(main())
