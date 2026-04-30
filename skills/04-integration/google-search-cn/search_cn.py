#!/usr/bin/env python3
"""
Google 搜索国内网站代理

功能：通过 Google 搜索访问国内网站
原理：使用 Google 搜索 + 代理转发

作者：太一 AGI
创建：2026-04-11
"""

import os
import re
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from urllib.parse import quote, urlparse, parse_qs
import subprocess

APP = Flask(__name__, template_folder='templates')

# 配置
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 7890
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 代理配置
proxies = {
    'http': f'http://{PROXY_HOST}:{PROXY_PORT}',
    'https': f'http://{PROXY_HOST}:{PROXY_PORT}',
}

def check_proxy():
    """检查代理是否可用"""
    try:
        # 测试访问国内网站 (通过代理)
        response = requests.get('https://www.baidu.com', proxies=proxies, timeout=5, headers=HEADERS)
        return response.status_code == 200
    except:
        return False

def google_search(query, num=10):
    """执行 Google 搜索"""
    url = 'https://www.google.com/search'
    params = {
        'q': query,
        'num': num,
        'hl': 'zh-CN',
        'gl': 'cn',
    }
    
    try:
        response = requests.get(url, params=params, proxies=proxies, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # 提取搜索结果
        results = []
        html = response.text
        
        # 查找搜索结果 (Google 搜索结果在 div.g 或 div.yuRUbf 中)
        pattern = r'<a href="([^"]+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for href, title in matches[:num]:
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            
            # 提取真实 URL (Google 会重定向)
            if href.startswith('/url?q='):
                parsed = parse_qs(href[7:])
                if 'q' in parsed:
                    href = parsed['q'][0]
            
            # 只保留 HTTP/HTTPS 链接
            if href.startswith(('http://', 'https://')):
                # 排除 Google 自己的链接
                if not any(x in href for x in ['google.com', 'youtube.com', 'googleusercontent']):
                    results.append({
                        'title': title,
                        'url': href,
                        'domain': urlparse(href).netloc
                    })
        
        return results
    except Exception as e:
        print(f'搜索失败：{e}')
        return []

def fetch_via_proxy(url):
    """通过代理获取网页内容"""
    try:
        response = requests.get(url, proxies=proxies, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return None

@APP.route('/')
def index():
    """搜索首页"""
    return render_template('search_cn.html')

@APP.route('/search')
def search():
    """执行搜索"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    results = google_search(query)
    return render_template('search_cn.html', query=query, results=results)

@APP.route('/api/search')
def api_search():
    """搜索 API"""
    query = request.args.get('q', '')
    num = request.args.get('num', 10, type=int)
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    results = google_search(query, num)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })

@APP.route('/proxy/<path:url>')
def proxy_url(url):
    """代理访问网页"""
    # 重构完整 URL
    full_url = f"http://{url}"
    if '://' in url:
        full_url = url
    
    content = fetch_via_proxy(full_url)
    if content:
        return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    else:
        return '无法访问该网页', 502

@APP.route('/api/proxy-status')
def api_proxy_status():
    """检查代理状态"""
    status = check_proxy()
    return jsonify({
        'proxy_available': status,
        'proxy_host': PROXY_HOST,
        'proxy_port': PROXY_PORT
    })

if __name__ == '__main__':
    print("🔍 Google 搜索国内网站代理启动中...")
    print("="*50)
    print(f"🌐 访问地址：http://localhost:5004")
    print(f"🔗 代理地址：{PROXY_HOST}:{PROXY_PORT}")
    print()
    
    # 检查代理
    if check_proxy():
        print("✅ 代理可用")
    else:
        print("⚠️  代理不可用，请确保 Clash 正在运行")
    
    print()
    APP.run(host='0.0.0.0', port=5004, debug=False)
