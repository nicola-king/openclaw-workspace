#!/usr/bin/env python3
"""
ROI Dashboard - Web 可视化界面
启动命令：python3 roi_dashboard.py
访问地址：http://localhost:8080
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys
from datetime import datetime, timedelta

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.local/lib/python3.12/site-packages'))

from roi_tracker import ROITracker

# 初始化追踪器
tracker = ROITracker()

# 添加示例数据（如果数据库为空）
def seed_sample_data():
    today = datetime.now().strftime("%Y-%m-%d")
    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    tracker.add_transaction(type='revenue', category='技能销售', amount=500, description='付费技能收入', date=today)
    tracker.add_transaction(type='revenue', category='交易收益', amount=1200, description='Polymarket 收益', date=today)
    tracker.add_transaction(type='cost', category='服务器', amount=100, description='VPS 月租', date=last_week)
    tracker.add_transaction(type='cost', category='API 费用', amount=50, description='百炼 API', date=last_week)

# 生成 HTML
def generate_dashboard_html():
    # 获取最近 30 天数据
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    report = tracker.get_period_summary(start_date, end_date)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROI Tracker Dashboard - 太一 AGI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100">
    <div class="min-h-screen">
        <!-- 顶部导航 -->
        <header class="bg-white shadow-sm">
            <div class="max-w-7xl mx-auto px-4 py-4">
                <h1 class="text-2xl font-bold text-gray-800">💰 ROI Tracker Dashboard</h1>
                <p class="text-sm text-gray-500">太一 AGI · 收益追踪系统</p>
            </div>
        </header>

        <!-- 主内容 -->
        <main class="max-w-7xl mx-auto px-4 py-8">
            <!-- 核心指标卡片 -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-gray-500 text-sm mb-2">总收入</h3>
                    <p class="text-3xl font-bold text-green-600">¥{report.total_revenue:,.2f}</p>
                </div>
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-gray-500 text-sm mb-2">总成本</h3>
                    <p class="text-3xl font-bold text-red-600">¥{report.total_cost:,.2f}</p>
                </div>
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-gray-500 text-sm mb-2">净利润</h3>
                    <p class="text-3xl font-bold text-blue-600">¥{report.net_profit:,.2f}</p>
                </div>
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-gray-500 text-sm mb-2">ROI</h3>
                    <p class="text-3xl font-bold text-purple-600">{report.roi_percentage}</p>
                    <p class="text-sm text-gray-500 mt-1">{report.trend}</p>
                </div>
            </div>

            <!-- 图表区域 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <!-- 收入成本对比 -->
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">📊 收入 vs 成本</h3>
                    <canvas id="revenueCostChart"></canvas>
                </div>
                
                <!-- 收入分类 -->
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">💰 收入分类</h3>
                    <canvas id="revenueBreakdownChart"></canvas>
                </div>
            </div>

            <!-- 明细表格 -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">📋 收支明细</h3>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b">
                                <th class="text-left py-3 px-4 font-semibold text-gray-700">分类</th>
                                <th class="text-right py-3 px-4 font-semibold text-gray-700">金额</th>
                                <th class="text-right py-3 px-4 font-semibold text-gray-700">占比</th>
                                <th class="text-left py-3 px-4 font-semibold text-gray-700">类型</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    # 收入明细
    for category, amount in sorted(report.breakdown['revenue'].items(), key=lambda x: -x[1]):
        pct = amount / report.total_revenue * 100 if report.total_revenue > 0 else 0
        html += f"""
                            <tr class="border-b hover:bg-gray-50">
                                <td class="py-3 px-4 text-gray-800">{category}</td>
                                <td class="py-3 px-4 text-right text-green-600 font-semibold">¥{amount:,.2f}</td>
                                <td class="py-3 px-4 text-right text-gray-600">{pct:.1f}%</td>
                                <td class="py-3 px-4"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">收入</span></td>
                            </tr>
"""
    
    # 成本明细
    for category, amount in sorted(report.breakdown['cost'].items(), key=lambda x: -x[1]):
        pct = amount / report.total_cost * 100 if report.total_cost > 0 else 0
        html += f"""
                            <tr class="border-b hover:bg-gray-50">
                                <td class="py-3 px-4 text-gray-800">{category}</td>
                                <td class="py-3 px-4 text-right text-red-600 font-semibold">¥{amount:,.2f}</td>
                                <td class="py-3 px-4 text-right text-gray-600">{pct:.1f}%</td>
                                <td class="py-3 px-4"><span class="bg-red-100 text-red-800 px-2 py-1 rounded text-xs">成本</span></td>
                            </tr>
"""
    
    # 图表数据
    revenue_labels = list(report.breakdown['revenue'].keys())
    revenue_data = list(report.breakdown['revenue'].values())
    cost_labels = list(report.breakdown['cost'].keys())
    cost_data = list(report.breakdown['cost'].values())
    
    html += f"""
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 期间信息 -->
            <div class="text-center text-gray-500 text-sm">
                <p>统计期间：{report.period} | 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </main>
    </div>

    <!-- Chart.js 图表 -->
    <script>
        // 收入成本对比图
        const revenueCostCtx = document.getElementById('revenueCostChart').getContext('2d');
        new Chart(revenueCostCtx, {{
            type: 'bar',
            data: {{
                labels: ['收入', '成本', '净利润'],
                datasets: [{{
                    label: '金额 (¥)',
                    data: [{report.total_revenue}, {report.total_cost}, {report.net_profit}],
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.7)',
                        'rgba(239, 68, 68, 0.7)',
                        'rgba(59, 130, 246, 0.7)'
                    ],
                    borderColor: [
                        'rgb(34, 197, 94)',
                        'rgb(239, 68, 68)',
                        'rgb(59, 130, 246)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // 收入分类饼图
        const revenueBreakdownCtx = document.getElementById('revenueBreakdownChart').getContext('2d');
        new Chart(revenueBreakdownCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(revenue_labels)},
                datasets: [{{
                    data: {json.dumps(revenue_data)},
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.7)',
                        'rgba(16, 185, 129, 0.7)',
                        'rgba(245, 158, 11, 0.7)',
                        'rgba(139, 92, 246, 0.7)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html

# 自定义请求处理器
class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = generate_dashboard_html()
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

# 启动服务器
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  💰 ROI Dashboard 启动中...                               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 添加示例数据
    seed_sample_data()
    print("✅ 示例数据已加载")
    
    # 启动服务器
    PORT = 8080
    server = HTTPServer(('localhost', PORT), DashboardHandler)
    print(f"🌐 访问地址：http://localhost:{PORT}")
    print("按 Ctrl+C 停止服务器")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
