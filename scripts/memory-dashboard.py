#!/usr/bin/env python3
"""
Memory Dashboard (记忆可视化仪表板)

功能:
1. 记忆统计可视化
2. 时间线导航
3. 回填控制
4. 洞察搜索
5. Web UI (端口 5003)

灵感来源：OpenClaw v2026.4.9 Control UI/Dreaming

作者：太一 AGI
创建：2026-04-10
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"
DASHBOARD_PORT = 5003


def get_memory_stats():
    """获取记忆统计"""
    
    stats = {
        'core_entries': 0,
        'residual_entries': 0,
        'memory_entries': 0,
        'daily_logs': 0,
        'emergence_count': 0,
        'last_updated': None
    }
    
    # 统计核心记忆
    core_file = MEMORY_DIR / "core.md"
    if core_file.exists():
        with open(core_file, "r", encoding="utf-8") as f:
            content = f.read()
        stats['core_entries'] = len(re.findall(r'^##', content, re.MULTILINE))
    
    # 统计残差记忆
    residual_file = MEMORY_DIR / "residual.md"
    if residual_file.exists():
        with open(residual_file, "r", encoding="utf-8") as f:
            content = f.read()
        stats['residual_entries'] = len(re.findall(r'^##', content, re.MULTILINE))
    
    # 统计长期记忆
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
        stats['memory_entries'] = len(re.findall(r'^##', content, re.MULTILINE))
    
    # 统计原始日志
    daily_files = list(MEMORY_DIR.glob("*.md"))
    stats['daily_logs'] = len([f for f in daily_files if re.match(r'\d{4}-\d{2}-\d{2}\.md', f.name)])
    
    # 统计能力涌现
    emergence_files = list((WORKSPACE / "skills").glob("emerged-skill-*/SKILL.md"))
    stats['emergence_count'] = len(emergence_files)
    
    # 最后更新时间
    today_file = MEMORY_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    if today_file.exists():
        stats['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return stats


def get_timeline_data(days=7):
    """获取时间线数据"""
    
    timeline = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{date_str}.md"
        
        day_data = {
            'date': date_str,
            'exists': daily_file.exists(),
            'decisions': 0,
            'tasks': 0,
            'insights': 0,
            'emergence': 0
        }
        
        if daily_file.exists():
            with open(daily_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            day_data['decisions'] = len(re.findall(r'【决策】', content))
            day_data['tasks'] = len(re.findall(r'【任务】', content))
            day_data['insights'] = len(re.findall(r'【洞察】', content))
            day_data['emergence'] = len(re.findall(r'【能力涌现】', content))
        
        timeline.append(day_data)
        current += timedelta(days=1)
    
    return timeline


def get_emergence_history():
    """获取能力涌现历史"""
    
    emergence_dir = WORKSPACE / "skills"
    emergence_list = []
    
    for skill_dir in emergence_dir.glob("emerged-skill-*/"):
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            # 从目录名提取时间
            match = re.search(r'emerged-skill-(\d{4}\d{2}\d{2}-\d{6})', skill_dir.name)
            if match:
                timestamp_str = match.group(1)
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                    emergence_list.append({
                        'id': skill_dir.name,
                        'timestamp': timestamp.isoformat(),
                        'date': timestamp.strftime("%Y-%m-%d %H:%M"),
                        'path': str(skill_dir)
                    })
                except:
                    pass
    
    # 按时间排序
    emergence_list.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return emergence_list[:20]  # 返回最近 20 个


def generate_dashboard_html():
    """生成 Dashboard HTML"""
    
    stats = get_memory_stats()
    timeline = get_timeline_data(7)
    emergence = get_emergence_history()
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>太一 AGI · 记忆仪表板</title>
    <style>
        :root {{
            --apple-gray: #8E8E93;
            --apple-white: #FFFFFF;
            --apple-silver: #C0C0C0;
            --sky-blue: #87CEEB;
            --ink: #2C2C2C;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: var(--ink);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2em;
            color: var(--ink);
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: var(--apple-gray);
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid var(--sky-blue);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--sky-blue);
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: var(--apple-gray);
            font-size: 0.95em;
        }}
        
        .section {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .section h2 {{
            color: var(--ink);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--apple-silver);
        }}
        
        .timeline {{
            overflow-x: auto;
        }}
        
        .timeline-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .timeline-table th,
        .timeline-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--apple-silver);
        }}
        
        .timeline-table th {{
            background: var(--sky-blue);
            color: white;
        }}
        
        .timeline-table tr:hover {{
            background: #f5f5f5;
        }}
        
        .tag {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            margin-right: 5px;
        }}
        
        .tag-decision {{ background: #e3f2fd; color: #1976d2; }}
        .tag-task {{ background: #fff3e0; color: #f57c00; }}
        .tag-insight {{ background: #f3e5f5; color: #7b1fa2; }}
        .tag-emergence {{ background: #e8f5e9; color: #388e3c; }}
        
        .emergence-list {{
            list-style: none;
        }}
        
        .emergence-item {{
            padding: 10px;
            border-left: 3px solid var(--sky-blue);
            margin-bottom: 10px;
            background: #f9f9f9;
            border-radius: 0 8px 8px 0;
        }}
        
        .emergence-date {{
            color: var(--apple-gray);
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .controls {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }}
        
        .btn-primary {{
            background: var(--sky-blue);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #6bb6e8;
        }}
        
        .btn-secondary {{
            background: var(--apple-gray);
            color: white;
        }}
        
        .btn-secondary:hover {{
            background: #6e6e73;
        }}
        
        footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: var(--apple-gray);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 太一 AGI · 记忆仪表板</h1>
            <p class="subtitle">Memory Dashboard · 灵感：OpenClaw v2026.4.9 Diary Timeline UI</p>
            <p class="subtitle">最后更新：{stats['last_updated'] or 'N/A'}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['core_entries']}</div>
                <div class="stat-label">核心记忆条目</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['residual_entries']}</div>
                <div class="stat-label">残差记忆条目</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['memory_entries']}</div>
                <div class="stat-label">长期记忆条目</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['daily_logs']}</div>
                <div class="stat-label">原始日志天数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['emergence_count']}</div>
                <div class="stat-label">能力涌现总数</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📅 时间线 (最近 7 天)</h2>
            <div class="timeline">
                <table class="timeline-table">
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>状态</th>
                            <th>决策</th>
                            <th>任务</th>
                            <th>洞察</th>
                            <th>能力涌现</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    for day in timeline:
        status = "✅" if day['exists'] else "⚪"
        html += f"""
                        <tr>
                            <td>{day['date']}</td>
                            <td>{status}</td>
                            <td><span class="tag tag-decision">{day['decisions']}</span></td>
                            <td><span class="tag tag-task">{day['tasks']}</span></td>
                            <td><span class="tag tag-insight">{day['insights']}</span></td>
                            <td><span class="tag tag-emergence">{day['emergence']}</span></td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="section">
            <h2>🧬 能力涌现历史 (最近 20 个)</h2>
            <ul class="emergence-list">
"""
    
    for item in emergence:
        html += f"""
                <li class="emergence-item">
                    <div class="emergence-date">📅 {item['date']}</div>
                    <div>📁 {item['id']}</div>
                </li>
"""
    
    html += f"""
            </ul>
        </div>
        
        <div class="section">
            <h2>🎮 回填控制</h2>
            <div class="controls">
                <button class="btn btn-primary" onclick="alert('执行回填命令：python3 /home/nicola/.openclaw/workspace/scripts/memory-backfill.py')">
                    🔙 执行回填 (最近 7 天)
                </button>
                <button class="btn btn-secondary" onclick="alert('查看回填报告目录：/home/nicola/.openclaw/workspace/reports/')">
                    📄 查看回填报告
                </button>
                <button class="btn btn-secondary" onclick="alert('编辑时间线：/home/nicola/.openclaw/workspace/memory/timeline.md')">
                    ✏️ 编辑时间线
                </button>
            </div>
        </div>
        
        <footer>
            <p>太一 AGI · 记忆仪表板 | 端口：{DASHBOARD_PORT}</p>
            <p>灵感来源：OpenClaw v2026.4.9 Control UI/Dreaming</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html


class DashboardHandler(SimpleHTTPRequestHandler):
    """Dashboard HTTP 处理器"""
    
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = generate_dashboard_html()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[Dashboard] {args[0]}")


def start_dashboard():
    """启动 Dashboard 服务"""
    
    server = HTTPServer(("0.0.0.0", DASHBOARD_PORT), DashboardHandler)
    print(f"🧠 Memory Dashboard 启动")
    print(f"   端口：{DASHBOARD_PORT}")
    print(f"   访问：http://localhost:{DASHBOARD_PORT}")
    print(f"   访问：http://192.168.3.74:{DASHBOARD_PORT}")
    print()
    print("按 Ctrl+C 停止服务")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard 服务已停止")
        server.shutdown()


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        # 仅生成 HTML 文件
        html = generate_dashboard_html()
        output_file = REPORTS_DIR / "memory-dashboard-preview.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Dashboard HTML 已生成：{output_file}")
        return 0
    else:
        # 启动服务
        start_dashboard()
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
