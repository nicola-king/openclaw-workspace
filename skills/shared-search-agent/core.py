"""
太一 · 共享搜索 Agent v3.0
============================
三大 OpenHuman 借鉴特性集成：
  1. 🗜️ TokenJuice — 智能压缩（skills/token-juice/）
  2. 🧠 AutoMemory — 自动记忆（skills/auto-memory/）
  3. 🔍 MultiEngine — 多引擎反爬搜索

用法：
  from skills.shared_search_agent.core import search, compress, remember, get_tj_stats, get_memory_stats
  
  result = search("Kovalska Ukraine construction")
  # 自动调用：
  #   1. AntiScrapeSearch → DuckDuckGo + Bing
  #   2. TokenJuice → 压缩结果
  #   3. AutoMemory → 自动记忆
"""

import cloudscraper
import logging
import re
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger("taiyi.shared-search")

# 自动加载子模块
_SKILLS_DIR = Path(__file__).resolve().parent.parent

def _load_module(mod_name, file_path):
    import importlib.util as iu
    spec = iu.spec_from_file_location(mod_name, str(file_path))
    mod = iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

try:
    _tj_mod = _load_module("token_juice", _SKILLS_DIR / "token-juice" / "core.py")
    tj = _tj_mod.get_compressor()
    TOKEN_JUICE_READY = True
except Exception as e:
    tj = None
    TOKEN_JUICE_READY = False
    logger.warning(f"TokenJuice not available: {e}")

try:
    _am_mod = _load_module("auto_memory", _SKILLS_DIR / "auto-memory" / "core.py")
    am = _am_mod.get_memory()
    AUTO_MEMORY_READY = True
except Exception as e:
    am = None
    AUTO_MEMORY_READY = False
    logger.warning(f"AutoMemory not available: {e}")

_SEARCH_CACHE = {}


class MultiEngineSearch:
    """多引擎反爬搜索（集成压缩 + 自动记忆）"""

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.stats = {"searches": 0, "cache_hits": 0}

    def search(self, query: str, timeout: int = 15, 
               compress: bool = True, remember: bool = True) -> dict:
        """搜索（自动多引擎 + 压缩 + 记忆）"""
        self.stats["searches"] += 1
        
        # 缓存检查
        import hashlib
        cache_key = hashlib.md5(query.encode()).hexdigest()[:12]
        if cache_key in _SEARCH_CACHE:
            self.stats["cache_hits"] += 1
            return _SEARCH_CACHE[cache_key]
        
        # 多引擎搜索
        result = self._search_all_engines(query, timeout)
        
        # TokenJuice 压缩
        if compress and tj and result.get("raw_html"):
            result["raw_html"] = tj.compress("search_result", result["raw_html"])
        
        # AutoMemory 自动记忆
        if remember and am and result.get("emails"):
            am.ingest("search", f"Query: {query}\nEmails: {result['emails']}\nLinkedIn: {result['linkedin']}",
                     {"query": query})
        
        _SEARCH_CACHE[cache_key] = result
        return result

    def _search_all_engines(self, query: str, timeout: int) -> dict:
        """多引擎自动切换搜索"""
        engines = [
            ("DuckDuckGo", f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"),
            ("Bing", f"https://www.bing.com/search?q={query.replace(' ', '+')}"),
        ]
        
        all_emails, all_phones, all_linkedin, raw_html = [], [], [], ""
        
        for name, url in engines:
            try:
                time.sleep(1.5)
                r = self.scraper.get(url, timeout=timeout)
                if r.status_code != 200:
                    continue
                
                html = r.text
                raw_html += f"\n<!-- {name} -->\n{html[:10000]}"
                
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
                emails = [e for e in set(emails) if not any(
                    x in e for x in ['.png','.jpg','.gif','google','bing',
                    'duckduckgo','gstatic','w3.org','schema','example',
                    'microsoft','github','facebook','twitter','youtube'])]
                
                linkedin = re.findall(r'linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+', html)
                phones = re.findall(r'(?:\+?\d{1,3}[-.]?\s*)?\(?\d{2,4}\)?[-.\s]*\d{2,4}[-.\s]*\d{2,4}(?:[-.\s]*\d{2,4})?', html)
                phones = [p for p in set(phones) if 7 < len(re.sub(r'\D', '', p)) < 16]
                
                all_emails.extend(emails)
                all_linkedin.extend(linkedin)
                all_phones.extend(phones)
                
                if emails or linkedin:
                    break
            except Exception:
                continue
        
        return {
            "emails": list(set(all_emails))[:10],
            "linkedin": [f"https://www.{l}" for l in set(all_linkedin)][:5],
            "phones": list(set(all_phones))[:5],
            "source": "duckduckgo+bing",
            "raw_html": raw_html[:5000],
        }


_engine_instance = None

def get_engine() -> MultiEngineSearch:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = MultiEngineSearch()
    return _engine_instance


# 统一 API
def search(query: str, **kwargs) -> dict:
    return get_engine().search(query, **kwargs)


def compress(tool_name: str, output: str) -> str:
    """TokenJuice 压缩"""
    if tj:
        return tj.compress(tool_name, output)
    return output


def remember(source: str, content: str, metadata: dict = None):
    """AutoMemory 记忆"""
    if am:
        return am.ingest(source, content, metadata)
    return None


def get_tj_stats() -> dict:
    if tj:
        return tj.stats_report()
    return {"processed": 0, "saved_chars": 0}


def get_memory_stats() -> dict:
    if am:
        return am.stats()
    return {"total_chunks": 0}


if __name__ == "__main__":
    import json
    
    print("╔═══════════════════════════════════════════╗")
    print("║  太一共享搜索Agent v3.0                   ║")
    print("║  三合一: 🗜️TokenJuice + 🧠AutoMemory + 🔍MultiEngine")
    print("╚═══════════════════════════════════════════╝")
    print()
    
    print(f"TokenJuice: {'✅' if TOKEN_JUICE_READY else '❌'}")
    print(f"AutoMemory: {'✅' if AUTO_MEMORY_READY else '❌'}")
    print()
    
    # 测试搜索
    result = search("Kovalska Ukraine steel construction", remember=True)
    print("🔍 搜索:")
    if result.get("linkedin"):
        print(f"   LinkedIn: {result['linkedin'][0]}")
    if result.get("emails"):
        print(f"   📧 {result.get('emails',[''])[0]}")
    print()
    
    # 测试压缩
    long_text = "\n".join([f"debug: line {i}" for i in range(200)])
    compressed = compress("search_result", long_text)
    print(f"🗜️ TokenJuice: {len(long_text)} → {len(compressed)} chars")
    print()
    
    # 测试记忆
    remember("test", "Ukraine reconstruction: $500B opportunity", {"country": "Ukraine"})
    stats = get_memory_stats()
    print(f"🧠 AutoMemory: {stats['total_chunks']} 条记忆")
    print(f"   来源: {stats.get('by_source', {})}")
