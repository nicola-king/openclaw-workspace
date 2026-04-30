#!/usr/bin/env python3
"""
太一搜索 Agent - 生产版
功能：网页搜索 + 内容提取
技术栈：curl + DuckDuckGo(代理) + Trafilatura
"""

import json
import sys
import os
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 内容提取
import trafilatura
from bs4 import BeautifulSoup

# 日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SearchAgent')

# 过滤不良域名
BLOCKED_DOMAINS = {
    'forumgratuit.org', 'zhihu.com', 'reddit.com', 'quora.com',
    'youtube.com', 'facebook.com', 'twitter.com', 'instagram.com',
    'linkedin.com', 'tiktok.com', 'pinterest.com'
}


def is_blocked(url: str) -> bool:
    for domain in BLOCKED_DOMAINS:
        if domain in url:
            return True
    return False


def search_duckduckgo(query: str, max_results: int = 10, proxy: str = 'http://127.0.0.1:7890') -> List[Dict]:
    """DuckDuckGo HTML 搜索 (通过代理)"""
    logger.info(f"搜索: {query}")
    
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    
    try:
        result = subprocess.run(
            [
                'curl', '-s', '-L',
                '--proxy', proxy,
                '-H', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '-H', 'Accept: text/html,application/xhtml+xml',
                '-H', 'Accept-Language: en-US,en;q=0.9',
                url
            ],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode != 0:
            logger.error(f"curl 失败: {result.stderr}")
            return []
        
        soup = BeautifulSoup(result.stdout, 'html.parser')
        results = []
        
        for item in soup.select('.result'):
            title_el = item.select_one('.result__title a')
            snippet_el = item.select_one('.result__snippet')
            url_el = item.select_one('.result__url')
            
            if not title_el or not url_el:
                continue
            
            title = title_el.get_text(strip=True)
            url = url_el.get_text(strip=True)
            snippet = snippet_el.get_text(strip=True) if snippet_el else ''
            
            if url and title and not is_blocked(url):
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet[:500]
                })
        
        logger.info(f"✅ 获取 {len(results)} 条结果")
        return results[:max_results]
        
    except Exception as e:
        logger.error(f"❌ 搜索失败: {e}")
        return []


def extract_content(url: str) -> Dict:
    """提取网页内容"""
    logger.info(f"提取: {url}")
    
    # 策略 1: Trafilatura
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            content = trafilatura.extract(downloaded, include_comments=False)
            if content and len(content) > 100:
                return {'content': content[:5000], 'method': 'trafilatura'}
    except Exception as e:
        logger.warning(f"Trafilatura 失败: {e}")
    
    # 策略 2: 通过代理 curl + trafilatura
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--proxy', 'http://127.0.0.1:7890',
             '-H', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
             '-m', '15', url],
            capture_output=True, text=True, timeout=20
        )
        if result.stdout:
            content = trafilatura.extract(result.stdout, include_comments=False)
            if content and len(content) > 100:
                return {'content': content[:5000], 'method': 'curl+trafilatura'}
    except Exception as e:
        logger.warning(f"curl+trafilatura 失败: {e}")
    
    return {'content': '', 'method': 'failed'}


def search_and_extract(query: str, max_results: int = 5) -> List[Dict]:
    """搜索 + 提取完整内容"""
    logger.info(f"搜索并提取: {query}")
    
    # 搜索
    results = search_duckduckgo(query, max_results * 2)
    
    # 提取内容
    extracted = []
    for i, result in enumerate(results[:max_results]):
        logger.info(f"提取 [{i+1}/{len(results[:max_results])}]: {result['url']}")
        content = extract_content(result['url'])
        result['content'] = content.get('content', '')[:3000]
        result['method'] = content.get('method', 'unknown')
        extracted.append(result)
        time.sleep(1)  # 礼貌延迟
    
    return extracted


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='太一搜索 Agent')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--max-results', '-n', type=int, default=5, help='最大结果数')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    results = search_and_extract(args.query, args.max_results)
    
    # 输出
    if args.format == 'json':
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output = f"🔍 搜索结果: {args.query}\n"
        output += "=" * 60 + "\n\n"
        for i, r in enumerate(results, 1):
            output += f"## {i}. {r['title']}\n"
            output += f"🔗 {r['url']}\n"
            output += f"📝 {r['snippet']}\n"
            if r.get('content'):
                output += f"\n{r['content'][:1000]}...\n"
            output += "\n" + "-" * 40 + "\n\n"
    
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        logger.info(f"✅ 已保存: {args.output}")
    else:
        print(output)
    
    return results


if __name__ == '__main__':
    main()
