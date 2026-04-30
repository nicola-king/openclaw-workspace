#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT 图表生成器 - 核心脚本
版本：1.0 | 创建时间：2026-04-02 12:21
用途：生成专业级 PPT 图表（PNG + HTML + SVG）
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 尝试导入 playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright 未安装，运行：pip install playwright && playwright install chromium")


class ChartGenerator:
    """图表生成器核心类"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_files = []
        
    def create_flowchart(self, title: str, nodes: List[str], edges: List[tuple], 
                         output_name: str = "flowchart") -> Dict[str, Path]:
        """
        创建流程图
        
        Args:
            title: 图表标题
            nodes: 节点列表 ["节点 A", "节点 B", ...]
            edges: 边列表 [("A", "B"), ("B", "C"), ...]
            output_name: 输出文件名
            
        Returns:
            生成的文件路径 {png: ..., html: ..., svg: ...}
        """
        # 生成 Mermaid DSL
        mermaid_code = self._generate_flowchart_mermaid(title, nodes, edges)
        
        # 渲染输出
        return self._render_mermaid(mermaid_code, output_name)
    
    def create_gantt_chart(self, title: str, tasks: List[Dict], 
                           output_name: str = "gantt") -> Dict[str, Path]:
        """
        创建甘特图
        
        Args:
            title: 图表标题
            tasks: 任务列表 [{"name": "任务 1", "start": "2026-04-01", "end": "2026-04-05"}, ...]
            output_name: 输出文件名
            
        Returns:
            生成的文件路径
        """
        mermaid_code = self._generate_gantt_mermaid(title, tasks)
        return self._render_mermaid(mermaid_code, output_name)
    
    def create_architecture_diagram(self, title: str, components: Dict[str, List[str]],
                                    connections: List[tuple], 
                                    output_name: str = "architecture") -> Dict[str, Path]:
        """
        创建架构图
        
        Args:
            title: 图表标题
            components: 组件字典 {"层名": ["组件 1", "组件 2"], ...}
            connections: 连接列表 [("组件 A", "组件 B"), ...]
            output_name: 输出文件名
        """
        mermaid_code = self._generate_architecture_mermaid(title, components, connections)
        return self._render_mermaid(mermaid_code, output_name)
    
    def _generate_flowchart_mermaid(self, title: str, nodes: List[str], 
                                    edges: List[tuple]) -> str:
        """生成流程图 Mermaid 代码"""
        lines = [f"graph TD", f"  title[{title}]"]
        
        # 添加节点
        for i, node in enumerate(nodes):
            lines.append(f"  N{i}[{node}]")
        
        # 添加边
        for src, dst in edges:
            src_idx = nodes.index(src) if src in nodes else 0
            dst_idx = nodes.index(dst) if dst in nodes else 0
            lines.append(f"  N{src_idx} --> N{dst_idx}")
        
        return "\n".join(lines)
    
    def _generate_gantt_mermaid(self, title: str, tasks: List[Dict]) -> str:
        """生成甘特图 Mermaid 代码"""
        lines = [
            "gantt",
            f"    title {title}",
            "    dateFormat  YYYY-MM-DD",
        ]
        
        for i, task in enumerate(tasks):
            name = task.get("name", f"任务{i}")
            start = task.get("start", "2026-04-01")
            end = task.get("end", "2026-04-07")
            lines.append(f"    {name} :task{i}, {start}, {end}")
        
        return "\n".join(lines)
    
    def _generate_architecture_mermaid(self, title: str, components: Dict[str, List[str]],
                                       connections: List[tuple]) -> str:
        """生成架构图 Mermaid 代码"""
        lines = ["graph LR", f"  title[{title}]"]
        
        # 添加子图（层）
        for layer_name, comps in components.items():
            lines.append(f"  subgraph {layer_name.replace(' ', '_')}")
            for comp in comps:
                lines.append(f"    {comp.replace(' ', '_')}[{comp}]")
            lines.append("  end")
        
        # 添加连接
        for src, dst in connections:
            lines.append(f"  {src.replace(' ', '_')} --> {dst.replace(' ', '_')}")
        
        return "\n".join(lines)
    
    def _render_mermaid(self, mermaid_code: str, output_name: str) -> Dict[str, Path]:
        """
        渲染 Mermaid 代码为图片
        
        使用 Playwright + mermaid.js 本地渲染
        """
        if not PLAYWRIGHT_AVAILABLE:
            # Fallback: 生成纯文本说明
            print(f"⚠️  Playwright 不可用，生成文本说明")
            return self._fallback_text_output(mermaid_code, output_name)
        
        try:
            # 创建 HTML 模板（使用 CDN 加载 mermaid.js）
            html_content = self._create_mermaid_html(mermaid_code)
            
            # 保存临时 HTML 文件
            html_file = self.output_dir / f"{output_name}.html"
            html_file.write_text(html_content, encoding='utf-8')
            
            # 使用 Playwright 渲染
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1200, "height": 800})
                
                # 加载 HTML 文件
                page.goto(f"file://{html_file.absolute()}")
                
                # 等待 Mermaid 渲染完成
                page.wait_for_selector(".mermaid svg", timeout=5000)
                
                # 截图保存为 PNG
                png_file = self.output_dir / f"{output_name}.png"
                page.screenshot(path=str(png_file), full_page=True)
                
                # 导出 SVG
                svg_content = page.query_selector(".mermaid svg").inner_html()
                svg_file = self.output_dir / f"{output_name}.svg"
                svg_file.write_text(f'<svg xmlns="http://www.w3.org/2000/svg">{svg_content}</svg>', encoding='utf-8')
                
                browser.close()
            
            print(f"✅ PNG 渲染完成：{png_file}")
            print(f"✅ SVG 导出完成：{svg_file}")
            
            self.generated_files.extend([html_file, png_file, svg_file])
            
            return {
                "html": html_file,
                "png": png_file,
                "svg": svg_file,
                "mmd": self.output_dir / f"{output_name}.mmd"
            }
            
        except Exception as e:
            print(f"⚠️  Playwright 渲染失败：{e}")
            print("回退到文本输出模式")
            return self._fallback_text_output(mermaid_code, output_name)
    
    def _create_mermaid_html(self, mermaid_code: str) -> str:
        """创建 Mermaid HTML 模板"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #f0f0f0;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
        }});
    </script>
</body>
</html>"""
    
    def _fallback_text_output(self, mermaid_code: str, output_name: str) -> Dict[str, Path]:
        """FALLBACK: Playwright 不可用时生成文本输出"""
        
        # 保存 Mermaid 代码
        mmd_file = self.output_dir / f"{output_name}.mmd"
        mmd_file.write_text(mermaid_code, encoding='utf-8')
        
        # 保存说明文件
        txt_file = self.output_dir / f"{output_name}.txt"
        txt_file.write_text(
            f"# {output_name}\n\n"
            f"Mermaid 代码已保存到：{mmd_file.name}\n\n"
            f"查看方法:\n"
            f"1. 打开 https://mermaid.live\n"
            f"2. 粘贴 {mmd_file.name} 内容\n"
            f"3. 导出 PNG/SVG\n\n"
            f"或安装 Playwright 后自动渲染:\n"
            f"```bash\n"
            f"pip install playwright && playwright install chromium\n"
            f"```\n",
            encoding='utf-8'
        )
        
        self.generated_files.extend([mmd_file, txt_file])
        
        return {
            "mmd": mmd_file,
            "txt": txt_file,
            "note": "安装 Playwright 后自动渲染为 PNG/SVG"
        }
    
    def batch_create(self, charts_config: List[Dict]) -> List[Dict[str, Path]]:
        """
        批量生成图表
        
        Args:
            charts_config: 配置列表
                [{"type": "flowchart", "title": "...", "nodes": [...], "edges": [...]}, ...]
                
        Returns:
            生成的文件列表
        """
        results = []
        
        for config in charts_config:
            chart_type = config.get("type", "flowchart")
            output_name = config.get("output_name", chart_type)
            
            if chart_type == "flowchart":
                result = self.create_flowchart(
                    config.get("title", "流程图"),
                    config.get("nodes", []),
                    config.get("edges", []),
                    output_name
                )
            elif chart_type == "gantt":
                result = self.create_gantt_chart(
                    config.get("title", "甘特图"),
                    config.get("tasks", []),
                    output_name
                )
            elif chart_type == "architecture":
                result = self.create_architecture_diagram(
                    config.get("title", "架构图"),
                    config.get("components", {}),
                    config.get("connections", []),
                    output_name
                )
            else:
                print(f"⚠️  未知图表类型：{chart_type}")
                continue
            
            results.append(result)
        
        return results


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PPT 图表生成器")
    parser.add_argument("command", choices=["flowchart", "gantt", "architecture", "batch"],
                       help="命令类型")
    parser.add_argument("--title", type=str, help="图表标题")
    parser.add_argument("--nodes", type=str, help="节点列表（逗号分隔）")
    parser.add_argument("--edges", type=str, help="边列表（A→B,C→D 格式）")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")
    parser.add_argument("--output-name", type=str, default="chart", help="输出文件名")
    
    args = parser.parse_args()
    
    generator = ChartGenerator(output_dir=args.output)
    
    if args.command == "flowchart":
        if not args.nodes or not args.edges:
            print("❌ 流程图需要 --nodes 和 --edges 参数")
            sys.exit(1)
        
        # 解析节点：支持中文逗号（\uFF0C）和英文逗号分隔
        nodes_str = args.nodes.replace("\uFF0C", ",").replace(",", ",")
        nodes = [n.strip() for n in nodes_str.split(",") if n.strip()]
        
        if not nodes:
            print("❌ 没有有效的节点，示例：--nodes 'A,B,C' 或 --nodes 'A,B,C'")
            sys.exit(1)
        # 解析边：支持多种分隔符（分号/逗号/换行）
        edges = []
        edges_str = args.edges.replace(",", ";").replace(",", ";")
        
        for e in edges_str.split(";"):
            e = e.strip()
            if not e:
                continue
            if "→" in e:
                parts = e.split("→")
                if len(parts) == 2:
                    edges.append((parts[0].strip(), parts[1].strip()))
                else:
                    print(f"⚠️  跳过无效的边：{e} (parts={len(parts)})")
            elif "-" in e:
                parts = e.split("-")
                if len(parts) == 2:
                    edges.append((parts[0].strip(), parts[1].strip()))
                else:
                    print(f"⚠️  跳过无效的边：{e}")
            else:
                print(f"⚠️  跳过无效的边：{e} (无箭头)")
        
        if not edges:
            print("❌ 没有有效的边，示例：--edges 'A→B;C→D' 或 --edges 'A-B,C-D'")
            sys.exit(1)
        
        result = generator.create_flowchart(args.title, nodes, edges, args.output_name)
        print(f"✅ 流程图已生成：{result}")
        
    elif args.command == "batch":
        # 从配置文件读取
        config_file = Path("charts_config.json")
        if not config_file.exists():
            print(f"❌ 配置文件不存在：{config_file}")
            sys.exit(1)
        
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        results = generator.batch_create(config.get("charts", []))
        print(f"✅ 批量生成完成：{len(results)} 个图表")


if __name__ == "__main__":
    main()
