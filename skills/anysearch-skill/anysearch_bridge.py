"""AnySearch Bridge - 融入太一共享搜索服务
将 AnySearch 统一搜索引擎作为太一系统的默认搜索后端
支持: 通用搜索 / 垂直领域搜索(23域) / 批量搜索 / URL内容提取
"""
import json, os, subprocess, time
from pathlib import Path

SKILL_DIR = Path(__file__).parent
CLI_PY = SKILL_DIR / "scripts" / "anysearch_cli.py"

def search(query, max_results=5, freshness=None, domain=None, sub_domain=None):
    """通用搜索 - 调用 AnySearch CLI
    Args:
        query: 搜索关键词
        max_results: 1-100
        freshness: day/week/month/year
        domain: 垂直领域 (tech/finance/academic等)
        sub_domain: 子域 (如 finance.us_stock)
    Returns:
        list[dict]: 搜索结果列表
    """
    cmd = ["python3", str(CLI_PY), "search", query, "--max_results", str(max_results)]
    if freshness:
        cmd.extend(["--freshness", freshness])
    if domain:
        cmd.extend(["--domain", domain])
    if sub_domain:
        cmd.extend(["--sub_domain", sub_domain])
    
    try:
        t0 = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        elapsed = time.time() - t0
        return _parse_results(result.stdout, query, elapsed)
    except subprocess.TimeoutExpired:
        return {"error": "search timed out", "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}

def extract_url(url, max_chars=5000):
    """URL内容提取"""
    cmd = ["python3", str(CLI_PY), "extract", url, "--max_chars", str(max_chars)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout[:max_chars]
    except:
        return None

def list_domains():
    """列出所有可用垂直领域"""
    cmd = ["python3", str(CLI_PY), "list_domains"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout

def _parse_results(output, query, elapsed):
    """解析 CLI 输出为结构化结果"""
    results = []
    current = {}
    for line in output.split('\n'):
        if line.startswith('### '):
            if current.get('title'):
                results.append(current)
            current = {'title': line.replace('### ', '').strip(), 'score': 0.9}
        elif line.startswith('- **URL**'):
            current['url'] = line.split(': ', 1)[-1].strip()
        elif line.startswith('- **Snippet**') or (current and not line.startswith('#') and line.strip() and 'http' not in line):
            if 'snippet' not in current:
                current['snippet'] = line.strip()[:200]
    if current.get('title'):
        results.append(current)
    
    return {
        "results": results[:20],
        "total": len(results),
        "time_ms": int(elapsed * 1000),
        "provider": "anysearch",
        "query": query
    }

# 快速测试
if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "太一 AGI 系统"
    r = search(q, max_results=3)
    for item in r.get("results", []):
        print(f"  [{item.get('score','?')}] {item.get('title','')[:60]}")
        print(f"      {item.get('url','')[:80]}")
    print(f"\n耗时: {r.get('time_ms',0)}ms | 结果: {r.get('total',0)}条")
