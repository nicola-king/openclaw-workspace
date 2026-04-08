#!/usr/bin/env python3
"""
API 监控 Web Dashboard
执行：python scripts/api-dashboard.py --port 8080
访问：http://localhost:8080
"""

from flask import Flask, render_template_string, jsonify
import requests
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# API 配置
API_CONFIG = {
    'coingecko': {
        'name': 'CoinGecko',
        'base_url': 'https://api.coingecko.com/api/v3',
        'health_endpoint': '/simple/price?ids=bitcoin&vs_currencies=usd',
        'rate_limit': 60,
        'category': 'Cryptocurrency'
    },
    'newsapi': {
        'name': 'NewsAPI',
        'base_url': 'https://newsapi.org/v2',
        'health_endpoint': '/top-headlines?country=us',
        'rate_limit': 100,
        'category': 'News'
    },
    'open-meteo': {
        'name': 'Open-Meteo',
        'base_url': 'https://api.open-meteo.com/v1',
        'health_endpoint': '/forecast?latitude=31.23&longitude=121.47&current_weather=true',
        'rate_limit': 99999,
        'category': 'Weather'
    },
    'alpha-vantage': {
        'name': 'Alpha Vantage',
        'base_url': 'https://www.alphavantage.co/query',
        'health_endpoint': '?function=GLOBAL_QUOTE&symbol=IBM',
        'rate_limit': 5,
        'category': 'Finance'
    },
    'unsplash': {
        'name': 'Unsplash',
        'base_url': 'https://api.unsplash.com',
        'health_endpoint': '/photos/random?count=1',
        'rate_limit': 50,
        'category': 'Images'
    }
}

RATE_LIMIT_FILE = Path('/tmp/api-rate-limits.json')

def load_rate_limits():
    if RATE_LIMIT_FILE.exists():
        with open(RATE_LIMIT_FILE, 'r') as f:
            return json.load(f)
    return {}

def check_health(api_id):
    config = API_CONFIG[api_id]
    api_key = os.getenv(f"{api_id.replace('-', '_').upper()}_API_KEY", "")
    
    url = config['base_url'] + config['health_endpoint']
    if '{API_KEY}' in url:
        url = url.replace('{API_KEY}', api_key)
    
    start_time = datetime.now()
    try:
        response = requests.get(url, timeout=10)
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            'status': 'healthy' if response.status_code == 200 else 'error',
            'response_time': round(response_time, 0),
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'status': 'error',
            'response_time': 0,
            'error': str(e)
        }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔧 API Monitor Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { margin-top: 0; color: #333; }
        .status { display: inline-block; padding: 4px 12px; border-radius: 4px; font-weight: bold; }
        .status.healthy { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .metric { margin: 10px 0; }
        .metric-label { color: #666; font-size: 14px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #333; }
        .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 4px; overflow: hidden; }
        .progress-fill { height: 100%; background: #28a745; transition: width 0.3s; }
        .progress-fill.warning { background: #ffc107; }
        .progress-fill.danger { background: #dc3545; }
        .updated { color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 API Monitor Dashboard</h1>
        <div class="grid">
            {% for api_id, api in apis.items() %}
            <div class="card">
                <h2>{{ api.name }}</h2>
                <p><span class="status {{ api.health.status }}">{{ api.health.status }}</span></p>
                <div class="metric">
                    <div class="metric-label">响应时间</div>
                    <div class="metric-value">{{ api.health.response_time }}ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">限流使用率</div>
                    <div class="progress-bar">
                        <div class="progress-fill {{ api.rate_class }}" style="width: {{ api.rate_percentage }}%"></div>
                    </div>
                    <small>{{ api.rate_used }}/{{ api.rate_limit }} ({{ api.rate_percentage }}%)</small>
                </div>
                <div class="metric">
                    <div class="metric-label">类别</div>
                    <div>{{ api.category }}</div>
                </div>
            </div>
            {% endfor %}
        </div>
        <p class="updated">最后更新：{{ updated_at }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    apis = {}
    limits = load_rate_limits()
    
    for api_id, config in API_CONFIG.items():
        health = check_health(api_id)
        rate_info = limits.get(api_id, {'used': 0})
        rate_percentage = (rate_info.get('used', 0) / config['rate_limit']) * 100
        
        # 确定进度条颜色
        if rate_percentage > 95:
            rate_class = 'danger'
        elif rate_percentage > 80:
            rate_class = 'warning'
        else:
            rate_class = 'normal'
        
        apis[api_id] = {
            'name': config['name'],
            'category': config['category'],
            'health': health,
            'rate_limit': config['rate_limit'],
            'rate_used': rate_info.get('used', 0),
            'rate_percentage': round(rate_percentage, 1),
            'rate_class': rate_class
        }
    
    return render_template_string(HTML_TEMPLATE, apis=apis, updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    """JSON API for status"""
    apis = {}
    for api_id, config in API_CONFIG.items():
        apis[api_id] = check_health(api_id)
    return jsonify({
        'updated_at': datetime.now().isoformat(),
        'apis': apis
    })

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080, help='Port number')
    args = parser.parse_args()
    
    print(f"🚀 Starting API Dashboard on http://localhost:{args.port}")
    print("Auto-refresh: 30 seconds")
    app.run(host='0.0.0.0', port=args.port, debug=False)
