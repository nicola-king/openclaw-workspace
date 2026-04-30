#!/usr/bin/env python3
"""
Chart Generator - 样式模板库
支持：professional/creative/minimalist/tech 等主题
"""

import os
import sys
from pathlib import Path
from datetime import datetime

class StyleTemplates:
    """样式模板库"""
    
    TEMPLATES = {
        'professional': {
            'name': '专业',
            'primaryColor': '#1E88E5',
            'secondaryColor': '#0D47A1',
            'backgroundColor': '#FFFFFF',
            'fontFamily': 'Arial, sans-serif',
            'borderRadius': '5px',
            'description': '适合商务文档、报告',
        },
        'creative': {
            'name': '创意',
            'primaryColor': '#FF6B6B',
            'secondaryColor': '#4ECDC4',
            'backgroundColor': '#FFF7F0',
            'fontFamily': 'Comic Sans MS, cursive',
            'borderRadius': '15px',
            'description': '适合创意展示、教育',
        },
        'minimalist': {
            'name': '极简',
            'primaryColor': '#333333',
            'secondaryColor': '#666666',
            'backgroundColor': '#FAFAFA',
            'fontFamily': 'Helvetica, Arial, sans-serif',
            'borderRadius': '0px',
            'description': '适合简约设计、文档',
        },
        'tech': {
            'name': '科技',
            'primaryColor': '#00E5FF',
            'secondaryColor': '#00B8D4',
            'backgroundColor': '#000000',
            'fontFamily': 'Courier New, monospace',
            'borderRadius': '3px',
            'description': '适合技术文档、代码',
        },
        'forest': {
            'name': '森林',
            'primaryColor': '#4CAF50',
            'secondaryColor': '#2E7D32',
            'backgroundColor': '#F1F8E9',
            'fontFamily': 'Arial, sans-serif',
            'borderRadius': '10px',
            'description': '适合自然、环保主题',
        },
        'dark': {
            'name': '深色',
            'primaryColor': '#64B5F6',
            'secondaryColor': '#1976D2',
            'backgroundColor': '#1A1A2E',
            'fontFamily': 'Arial, sans-serif',
            'borderRadius': '5px',
            'description': '适合演示、夜间模式',
        },
    }
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "chart-templates"
        self.output_dir.mkdir(exist_ok=True)
    
    def apply_template(self, mermaid_code, template_name='professional'):
        """应用模板"""
        template = self.TEMPLATES.get(template_name, self.TEMPLATES['professional'])
        
        # 添加 Mermaid 初始化配置
        config = f"""%%{{
  init: {{
    'theme': 'base',
    'themeVariables': {{
      'primaryColor': '{template['primaryColor']}',
      'primaryBorderColor': '{template['primaryColor']}',
      'primaryTextColor': '#fff',
      'secondaryColor': '{template['secondaryColor']}',
      'secondaryBorderColor': '{template['secondaryColor']}',
      'secondaryTextColor': '#fff',
      'tertiaryColor': '{template['primaryColor']}',
      'tertiaryBorderColor': '{template['primaryColor']}',
      'lineColor': '{template['secondaryColor']}',
      'fontFamily': '{template['fontFamily']}',
      'fontSize': '14px',
    }}
  }}
}}%%
"""
        return config + mermaid_code
    
    def generate_template_preview(self, template_name=None):
        """生成模板预览"""
        if template_name:
            templates = {template_name: self.TEMPLATES[template_name]}
        else:
            templates = self.TEMPLATES
        
        preview_file = self.output_dir / "template_preview.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>样式模板预览</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .template-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; }
        .template-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .template-card h3 { margin-top: 0; }
        .color-preview { display: flex; gap: 10px; margin: 10px 0; }
        .color-box { width: 50px; height: 50px; border-radius: 5px; border: 1px solid #ddd; }
        .template-info { margin: 10px 0; }
        .template-info p { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>🎨 样式模板预览</h1>
    <div class="template-grid">
"""
        for name, template in templates.items():
            html += f"""
        <div class="template-card">
            <h3>{template['name']} ({name})</h3>
            <div class="color-preview">
                <div class="color-box" style="background: {template['primaryColor']}" title="主色"></div>
                <div class="color-box" style="background: {template['secondaryColor']}" title="辅助色"></div>
                <div class="color-box" style="background: {template['backgroundColor']}" title="背景色"></div>
            </div>
            <div class="template-info">
                <p><strong>字体:</strong> {template['fontFamily']}</p>
                <p><strong>圆角:</strong> {template['borderRadius']}</p>
                <p><strong>描述:</strong> {template['description']}</p>
            </div>
            <div class="mermaid">
flowchart TD
    A[开始] --> B[处理]
    B --> C[结束]
            </div>
        </div>
"""
        
        html += """    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>"""
        
        preview_file.write_text(html, encoding='utf-8')
        return str(preview_file)
    
    def batch_apply(self, mermaid_files, template_name='professional'):
        """批量应用模板"""
        print(f"📦 批量应用模板：{template_name}")
        
        results = []
        for mermaid_file in mermaid_files:
            mermaid_path = Path(mermaid_file)
            if not mermaid_path.exists():
                print(f"⚠️  文件不存在：{mermaid_file}")
                continue
            
            mermaid_code = mermaid_path.read_text(encoding='utf-8')
            styled_code = self.apply_template(mermaid_code, template_name)
            
            # 保存
            output_file = self.output_dir / f"{mermaid_path.stem}_{template_name}.mmd"
            output_file.write_text(styled_code, encoding='utf-8')
            
            results.append({
                'source': str(mermaid_file),
                'styled': str(output_file),
                'template': template_name
            })
        
        print(f"✅ 批量应用完成！处理 {len(results)} 个文件")
        
        return results
    
    def recommend_template(self, content, context=None):
        """推荐模板"""
        # 基于内容分析推荐
        if not content:
            return 'professional'
        
        content_lower = content.lower()
        
        # 商务/专业内容
        if any(kw in content_lower for kw in ['报告', '商务', '专业', 'business', 'report']):
            return 'professional'
        
        # 技术/代码内容
        if any(kw in content_lower for kw in ['技术', '代码', 'tech', 'code', 'api']):
            return 'tech'
        
        # 创意/教育内容
        if any(kw in content_lower for kw in ['创意', '教育', 'creative', 'education']):
            return 'creative'
        
        # 自然/环保内容
        if any(kw in content_lower for kw in ['自然', '环保', 'green', 'nature']):
            return 'forest'
        
        # 默认
        return 'professional'
    
    def list_templates(self):
        """列出所有模板"""
        print("\n🎨 可用样式模板:")
        print("=" * 60)
        
        for name, template in self.TEMPLATES.items():
            print(f"\n{name.upper()} - {template['name']}")
            print(f"  主色：{template['primaryColor']}")
            print(f"  辅助色：{template['secondaryColor']}")
            print(f"  背景：{template['backgroundColor']}")
            print(f"  字体：{template['fontFamily']}")
            print(f"  描述：{template['description']}")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    templates = StyleTemplates()
    
    if len(sys.argv) < 2:
        templates.list_templates()
        print("\n用法：python3 templates.py <命令> [参数]")
        print("\n命令:")
        print("  list                 列出所有模板")
        print("  preview              生成模板预览")
        print("  apply <文件> <模板>  应用模板")
        print("  recommend <文字>     推荐模板")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'list':
        templates.list_templates()
    
    elif command == 'preview':
        preview_file = templates.generate_template_preview()
        print(f"✅ 模板预览已生成：{preview_file}")
    
    elif command == 'apply':
        if len(sys.argv) < 4:
            print("用法：python3 templates.py apply <文件> <模板>")
            sys.exit(1)
        
        mermaid_file = sys.argv[2]
        template_name = sys.argv[3]
        
        mermaid_code = Path(mermaid_file).read_text(encoding='utf-8')
        styled_code = templates.apply_template(mermaid_code, template_name)
        
        output_file = templates.output_dir / f"{Path(mermaid_file).stem}_{template_name}.mmd"
        output_file.write_text(styled_code, encoding='utf-8')
        
        print(f"✅ 模板已应用：{output_file}")
    
    elif command == 'recommend':
        if len(sys.argv) < 3:
            print("用法：python3 templates.py recommend <文字>")
            sys.exit(1)
        
        content = ' '.join(sys.argv[2:])
        recommended = templates.recommend_template(content)
        
        print(f"💡 推荐模板：{recommended}")
        print(f"   说明：{templates.TEMPLATES[recommended]['description']}")
    
    else:
        print(f"❌ 未知命令：{command}")
        templates.list_templates()


if __name__ == "__main__":
    main()
