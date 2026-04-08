# Discovery Module - 技能发现模块

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：守藏吏

---

## 🎯 职责

**发现并评估新 Skills**，来源包括:
- ClawHub 技能市场
- GitHub OpenClaw 仓库
- 社区推荐 (Telegram/Discord)

---

## 🔧 核心功能

### 1️⃣ ClawHub 搜索

```python
# clawhub-search.py
import subprocess
import json

def search_clawhub(keyword):
    """搜索 ClawHub 技能市场"""
    result = subprocess.run(
        ['clawhub', 'search', keyword],
        capture_output=True,
        text=True
    )
    return parse_clawhub_output(result.stdout)

def parse_clawhub_output(output):
    """解析 ClawHub 输出为结构化数据"""
    skills = []
    for line in output.split('\n'):
        if line.strip():
            parts = line.split('|')
            if len(parts) >= 3:
                skills.append({
                    'name': parts[0].strip(),
                    'description': parts[1].strip(),
                    'rating': parts[2].strip(),
                    'source': 'ClawHub'
                })
    return skills

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else 'auto'
    results = search_clawhub(keyword)
    
    print(f"## ClawHub 搜索结果：{keyword}\n")
    print("| 技能名 | 描述 | 评分 |")
    print("|--------|------|------|")
    for skill in results[:10]:
        print(f"| {skill['name']} | {skill['description'][:30]}... | {skill['rating']} |")
```

---

### 2️⃣ GitHub 扫描

```python
# github-scan.py
import requests
import json

def search_github(keyword):
    """搜索 GitHub OpenClaw Skills"""
    url = "https://api.github.com/search/repositories"
    params = {
        'q': f'openclaw-skill {keyword}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def analyze_repo(repo):
    """分析仓库质量"""
    return {
        'name': repo['name'],
        'stars': repo['stargazers_count'],
        'forks': repo['forks_count'],
        'updated': repo['updated_at'],
        'description': repo['description'] or '无描述',
        'url': repo['html_url'],
        'has_skill_md': False,  # 需进一步检查
        'score': calculate_score(repo)
    }

def calculate_score(repo):
    """计算技能评分 (0-5 星)"""
    score = 0
    if repo['stargazers_count'] > 100:
        score += 2
    elif repo['stargazers_count'] > 50:
        score += 1
    
    if repo['forks_count'] > 20:
        score += 1
    
    if repo['description']:
        score += 1
    
    # 最近 3 个月更新
    from datetime import datetime
    updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
    if (datetime.now() - updated).days < 90:
        score += 1
    
    return min(score, 5)

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else 'auto'
    repos = search_github(keyword)
    
    print(f"## GitHub 搜索结果：{keyword}\n")
    print("| 技能名 | ⭐ | 🔀 | 更新时间 | 描述 |")
    print("|--------|----|----|---------|------|")
    
    for repo in repos[:10]:
        analysis = analyze_repo(repo)
        stars = '⭐' * analysis['score']
        print(f"| [{analysis['name']}]({analysis['url']}) | {stars} | {analysis['forks']} | {analysis['updated'][:10]} | {analysis['description'][:20]}... |")
```

---

## 📋 使用命令

```bash
# 搜索 ClawHub
python3 modules/discovery/clawhub-search.py <keyword>

# 搜索 GitHub
python3 modules/discovery/github-scan.py <keyword>

# 综合搜索 (双平台)
python3 modules/discovery/clawhub-search.py <keyword> && python3 modules/discovery/github-scan.py <keyword>
```

---

## 📊 输出格式

```markdown
## 技能发现报告

**关键词**: {keyword}
**时间**: {timestamp}
**来源**: ClawHub + GitHub

### ClawHub 结果
| 技能名 | 描述 | 评分 |
|--------|------|------|
| skill-x | 描述... | ⭐⭐⭐⭐ |

### GitHub 结果
| 技能名 | ⭐ | 🔀 | 更新时间 |
|--------|----|----|---------|
| openclaw-skill-y | ⭐⭐⭐ | 15 | 2026-04-01 |

### 推荐 Top 3
1. **skill-x** - 理由：高评分 + 活跃维护
2. **skill-y** - 理由：GitHub 星标多
3. **skill-z** - 理由：填补功能空白

### 下一步
- [ ] 安全扫描 (素问)
- [ ] 兼容性检查 (素问)
- [ ] 质量门禁 (太一)
- [ ] 安装决策 (SAYELF)
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `modules/discovery/SKILL.md` | 本文档 |
| `modules/discovery/clawhub-search.py` | ClawHub 搜索脚本 |
| `modules/discovery/github-scan.py` | GitHub 扫描脚本 |
| `SKILL.md` (父级) | 主入口文档 |

---

*创建：2026-04-03 22:17 | 太一 AGI · 守藏吏主责*
