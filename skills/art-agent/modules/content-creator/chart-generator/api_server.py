#!/usr/bin/env python3
"""
Chart Generator - API 服务
支持：REST API、批量处理、Web 界面
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import sys
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 导入 Chart Generator
sys.path.insert(0, str(Path(__file__).parent.parent))
from chart_generator import ChartGenerator
from exporter import ChartExporter
from templates import StyleTemplates

generator = ChartGenerator()
exporter = ChartExporter()
templates = StyleTemplates()

@app.route('/')
def index():
    """Web 界面"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Chart Generator - 图表生成器</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 200px; border: 1px solid #ddd; border-radius: 5px; padding: 10px; font-family: monospace; }
        button { background: #1E88E5; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #1565C0; }
        select { padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
        .preview { background: white; padding: 20px; border-radius: 10px; min-height: 300px; }
    </style>
</head>
<body>
    <h1>📊 Chart Generator - 图表生成器</h1>
    
    <div class="container">
        <div class="panel">
            <h2>输入</h2>
            <textarea id="chartText" placeholder="输入图表描述，例如：开始→处理→结束"></textarea>
            
            <div>
                <label>图表类型：</label>
                <select id="chartType">
                    <option value="flowchart">流程图</option>
                    <option value="sequence">时序图</option>
                    <option value="mindmap">思维导图</option>
                    <option value="gantt">甘特图</option>
                </select>
            </div>
            
            <div>
                <label>主题：</label>
                <select id="theme">
                    <option value="professional">专业</option>
                    <option value="creative">创意</option>
                    <option value="minimalist">极简</option>
                    <option value="tech">科技</option>
                    <option value="forest">森林</option>
                    <option value="dark">深色</option>
                </select>
            </div>
            
            <button onclick="generateChart()">生成图表</button>
            <button onclick="exportChart('png')">导出 PNG</button>
            <button onclick="exportChart('pdf')">导出 PDF</button>
        </div>
        
        <div class="panel">
            <h2>预览</h2>
            <div id="preview" class="preview"></div>
        </div>
    </div>
    
    <script>
        function generateChart() {
            const text = document.getElementById('chartText').value;
            const type = document.getElementById('chartType').value;
            const theme = document.getElementById('theme').value;
            
            fetch('/api/chart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, type, theme })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('preview').innerHTML = data.html;
                } else {
                    alert('生成失败：' + data.error);
                }
            });
        }
        
        function exportChart(format) {
            alert('导出功能开发中...');
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/chart', methods=['POST'])
def create_chart():
    """创建图表 API"""
    data = request.json
    text = data.get('text', '')
    chart_type = data.get('type', 'flowchart')
    theme = data.get('theme', 'professional')
    
    try:
        # 生成图表
        chart = generator.create_chart(text, chart_type)
        
        # 应用模板
        from templates import StyleTemplates
        templates = StyleTemplates()
        styled_code = templates.apply_template(chart['mermaid_code'], theme)
        
        return jsonify({
            'success': True,
            'mermaid': styled_code,
            'html_file': chart['html_file'],
            'message': '图表生成成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export', methods=['POST'])
def export_chart():
    """导出图表 API"""
    data = request.json
    html_file = data.get('html_file')
    format = data.get('format', 'png')
    
    try:
        if format == 'png':
            file_path = exporter.export_to_png(html_file)
        elif format == 'pdf':
            from pdf_exporter import PDFExporter
            pdf_exporter = PDFExporter()
            file_path = pdf_exporter.export_to_pdf(html_file)
        else:
            return jsonify({'success': False, 'error': '不支持的格式'}), 400
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/templates', methods=['GET'])
def list_templates():
    """列出模板 API"""
    return jsonify({
        'success': True,
        'templates': list(templates.TEMPLATES.keys())
    })

@app.route('/api/recommend', methods=['POST'])
def recommend_template():
    """推荐模板 API"""
    data = request.json
    content = data.get('content', '')
    
    recommended = templates.recommend_template(content)
    
    return jsonify({
        'success': True,
        'recommended': recommended,
        'description': templates.TEMPLATES[recommended]['description']
    })

if __name__ == '__main__':
    print("🚀 Chart Generator API Server 启动...")
    print("📊 Web 界面：http://localhost:5000")
    print("🔌 API 端点：http://localhost:5000/api")
    app.run(host='0.0.0.0', port=5000, debug=True)
