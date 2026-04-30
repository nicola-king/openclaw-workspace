#!/usr/bin/env python3
"""
太一搜索 Agent v3 - 基于 Playwright 的可靠搜索
功能：网页搜索 + 内容提取
技术栈：Playwright + Trafilatura
"""

import json
import sys
import os
import time
import logging
from pathlib import Path
from datetime import datetime

# 内容提取
import trafilatura
from bs4 import BeautifulSoup

# Playwright
from playwright.sync_api import sync_playwright

# 日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SearchAgent')


class SearchAgent:
    """太一搜索 Agent v3"""
    
    def __init__(self):
        self.results = []
        
    def search_duckduckgo(self, query: str, max_results: int = 10) -> list:
        """
        使用 Playwright 抓取 DuckDuckGo 搜索结果
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            搜索结果列表
        """
        logger.info(f"搜索: {query}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                context = browser.new_context()
                context.set_default_timeout(30000)
                
                page = context.new_page()
                
                # 设置 User-Agent
                page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                })
                
                # 访问 DuckDuckGo
                url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
                logger.info(f"访问: {url}")
                
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)
                
                # 提取搜索结果
                results = page.evaluate('''() => {
                    const items = document.querySelectorAll('.result');
                    return Array.from(items).map(item => {
                        const titleEl = item.querySelector('.result__title a');
                        const snippetEl = item.querySelector('.result__snippet');
                        const urlEl = item.querySelector('.result__url');
                        return {
                            title: titleEl ? titleEl.textContent.trim() : '',
                            snippet: snippetEl ? snippetEl.textContent.trim() : '',
                            url: urlEl ? urlEl.textContent.trim() : ''
                        };
                    });
                }''')
                
                browser.close()
                
                if results:
                    logger.info(f"✅ 获取 {len(results)} 条结果")
                    return results[:max_results]
                else:
                    logger.warning("⚠️ 未找到结果，尝试备用方案")
                    return self._search_bing(query, max_results)
                    
        except Exception as e:
            logger.error(f"❌ DuckDuckGo 搜索失败: {e}")
            return self._search_bing(query, max_results)
    
    def _search_bing(self, query: str, max_results: int = 10) -> list:
        """备用方案：使用 Bing 搜索"""
        logger.info(f"备用搜索: {query}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                context = browser.new_context()
                context.set_default_timeout(30000)
                
                page = context.new_page()
                page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                })
                
                url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(3)
                
                results = page.evaluate('''() => {
                    const items = document.querySelectorAll('.b_algo');
                    return Array.from(items).map(item => {
                        const titleEl = item.querySelector('h2 a');
                        const snippetEl = item.querySelector('.b_caption p, .b_lineclamp2');
                        return {
                            title: titleEl ? titleEl.textContent.trim() : '',
                            snippet: snippetEl ? snippetEl.textContent.trim() : '',
                            url: titleEl ? titleEl.href : ''
                        };
                    });
                }''')
                
                browser.close()
                
                if results:
                    logger.info(f"✅ Bing 获取 {len(results)} 条结果")
                    return results[:max_results]
                    
        except Exception as e:
            logger.error(f"❌ Bing 搜索失败: {e}")
        
        return []
    
    def extract_content(self, url: str) -> dict:
        """
        提取网页内容
        
        Args:
            url: 网页 URL
        
        Returns:
            提取结果
        """
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
        
        # 策略 2: Playwright
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                page = browser.new_page()
                page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                })
                
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)
                
                content = page.evaluate('''() => {
                    document.querySelectorAll('script, style, nav, header, footer, aside, .sidebar, .ad, .popup').forEach(el => el.remove());
                    const article = document.querySelector('article, main, .content, .post, body');
                    return article ? article.innerText : document.body.innerText;
                }''')
                
                title = page.title()
                browser.close()
                
                if content and len(content) > 100:
                    return {
                        'title': title[:200] if title else '',
                        'content': content[:5000],
                        'method': 'playwright'
                    }
        except Exception as e:
            logger.error(f"Playwright 提取失败: {e}")
        
        return {'content': '', 'method': 'failed'}
    
    def search_and_extract(self, query: str, max_results: int = 5) -> list:
        """
        搜索 + 提取内容
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            完整搜索结果
        """
        logger.info(f"搜索并提取: {query}")
        
        # 搜索
        results = self.search_duckduckgo(query, max_results)
        
        # 提取内容
        extracted = []
        for i, result in enumerate(results):
            url = result.get('url', '')
            if not url:
                continue
            
            logger.info(f"提取 [{i+1}/{len(results)}]: {url}")
            
            content = self.extract_content(url)
            extracted.append({
                'title': result.get('title', ''),
                'url': url,
                'snippet': result.get('snippet', '')[:500],
                'full_content': content.get('content', '')[:3000],
                'method': content.get('method', 'unknown')
            })
            
            # 礼貌延迟
            time.sleep(1)
        
        return extracted


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='太一搜索 Agent v3')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--max-results', '-n', type=int, default=5, help='最大结果数')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 创建搜索 Agent
    agent = SearchAgent()
    
    # 搜索并提取
    results = agent.search_and_extract(args.query, args.max_results)
    
    # 输出
    if args.format == 'json':
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output = f"🔍 搜索结果: {args.query}\n"
        output += "=" * 60 + "\n\n"
        for i, result in enumerate(results, 1):
            output += f"## {i}. {result['title']}\n"
            output += f"🔗 {result['url']}\n"
            output += f"📝 {result['snippet']}\n"
            if result.get('full_content'):
                output += f"\n{result['full_content'][:1000]}...\n"
            output += "\n" + "-" * 40 + "\n\n"
    
    # 输出到文件或 stdout
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        logger.info(f"✅ 结果已保存到: {args.output}")
    else:
        print(output)
    
    return results


if __name__ == '__main__':
    main()
