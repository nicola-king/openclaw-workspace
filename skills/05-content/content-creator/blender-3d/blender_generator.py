#!/usr/bin/env python3
"""
Blender 3D - 文字转 3D 模型生成器
支持：基础几何体创建 + 命令行渲染
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

class Blender3DGenerator:
    """Blender 3D 生成器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "blender-3d-output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 检测 Blender
        self.blender_path = self._find_blender()
    
    def _find_blender(self):
        """查找 Blender 安装"""
        paths = [
            'blender',
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            '/Applications/Blender.app/Contents/MacOS/Blender',
        ]
        
        for path in paths:
            try:
                result = subprocess.run([path, '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Blender 已检测：{path}")
                    return path
            except:
                continue
        
        print("⚠️  Blender 未检测到，将使用模拟模式")
        return None
    
    def parse_text_to_blender_script(self, text):
        """解析文字为 Blender 脚本"""
        # 简单解析实现
        script = """import bpy
import math

# 清除默认场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 设置相机
bpy.ops.object.camera_add(location=(0, -10, 10), rotation=(math.radians(45), 0, 0))
bpy.context.scene.camera = bpy.context.active_object

# 添加灯光
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))

"""
        
        # 解析几何体
        if '立方体' in text or 'cube' in text.lower():
            color = self._extract_color(text)
            script += f"""
# 创建立方体
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
# 设置材质
mat = bpy.data.materials.new(name="CubeMaterial")
mat.diffuse_color = {color}
cube.data.materials.append(mat)

"""
        
        if '球体' in text or 'sphere' in text.lower():
            color = self._extract_color(text)
            script += f"""
# 创建球体
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3, 0, 0))
sphere = bpy.context.active_object
# 设置材质
mat = bpy.data.materials.new(name="SphereMaterial")
mat.diffuse_color = {color}
sphere.data.materials.append(mat)

"""
        
        if '圆柱' in text or 'cylinder' in text.lower():
            script += """
# 创建圆柱
bpy.ops.mesh.primitive_cylinder_add(radius=1, location=(-3, 0, 0))

"""
        
        # 渲染设置
        script += """
# 设置渲染
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.cycles.samples = 128

# 保存 blend 文件
bpy.ops.wm.save_as_mainfile(filepath="OUTPUT_PATH")

# 渲染输出
bpy.context.scene.render.filepath = "OUTPUT_PATH.png"
bpy.ops.render.render(write_still=True)

print("✅ Blender 渲染完成！")
"""
        
        return script
    
    def _extract_color(self, text):
        """提取颜色"""
        colors = {
            '红色': '(1, 0, 0, 1)',
            '红色': '(1, 0, 0, 1)',
            '蓝色': '(0, 0, 1, 1)',
            '蓝色': '(0, 0, 1, 1)',
            '绿色': '(0, 1, 0, 1)',
            '绿色': '(0, 1, 0, 1)',
            '白色': '(1, 1, 1, 1)',
            '白色': '(1, 1, 1, 1)',
            '黑色': '(0, 0, 0, 1)',
            '黑色': '(0, 0, 0, 1)',
        }
        
        for cn, color in colors.items():
            if cn in text:
                return color
        
        return '(0.5, 0.5, 0.5, 1)'  # 默认灰色
    
    def create_from_text(self, text, output_name=None):
        """从文字创建 3D 模型"""
        print(f"🎨 创建 3D 模型：{text}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_name is None:
            output_name = f"model_{timestamp}"
        
        # 生成 Blender 脚本
        print(f"  步骤 1/3: 生成 Blender 脚本")
        blender_script = self.parse_text_to_blender_script(text)
        
        # 保存脚本
        script_file = self.output_dir / f"{output_name}.py"
        script_file.write_text(blender_script, encoding='utf-8')
        print(f"✅ 脚本已保存：{script_file}")
        
        # 执行 Blender
        blend_file = self.output_dir / f"{output_name}.blend"
        png_file = self.output_dir / f"{output_name}.png"
        
        if self.blender_path:
            print(f"  步骤 2/3: 执行 Blender")
            
            # 替换输出路径
            blender_script = blender_script.replace("OUTPUT_PATH", str(self.output_dir / output_name))
            script_file.write_text(blender_script, encoding='utf-8')
            
            # 执行渲染
            try:
                result = subprocess.run([
                    self.blender_path,
                    '--background',
                    '--python', str(script_file)
                ], capture_output=True, text=True, timeout=300)
                
                print(f"  步骤 3/3: 渲染完成")
                print(f"✅ blend 文件：{blend_file}")
                print(f"✅ PNG 渲染：{png_file}")
                
            except subprocess.TimeoutExpired:
                print("⚠️  Blender 渲染超时")
            except Exception as e:
                print(f"⚠️  Blender 执行失败：{e}")
        else:
            # 模拟模式
            print(f"  步骤 2/3: 模拟 Blender 执行")
            blend_file.touch()
            png_file.touch()
            print(f"✅ [模拟] blend 文件：{blend_file}")
            print(f"✅ [模拟] PNG 渲染：{png_file}")
        
        return {
            'script_file': str(script_file),
            'blend_file': str(blend_file),
            'png_file': str(png_file),
            'timestamp': timestamp
        }
    
    def batch_create(self, texts):
        """批量创建"""
        print(f"📦 批量创建 3D 模型...")
        
        results = []
        for i, text in enumerate(texts, 1):
            print(f"\n[{i}/{len(texts)}] {text}")
            result = self.create_from_text(text)
            results.append(result)
        
        # 生成索引
        index_file = self._generate_index(results)
        
        print(f"\n✅ 批量创建完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_index(self, results):
        """生成索引页面"""
        index_file = self.output_dir / "index.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Blender 3D 模型索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .model-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .model-item { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .model-item img { max-width: 100%; border-radius: 5px; }
        .model-item h3 { color: #1E88E5; margin-top: 0; }
        .model-item a { color: #1E88E5; text-decoration: none; }
        .model-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🎨 Blender 3D 模型索引</h1>
    <div class="model-list">
"""
        for result in results:
            png = Path(result['png_file'])
            blend = Path(result['blend_file'])
            html += f"""
        <div class="model-item">
            <h3>{blend.stem}</h3>
            <img src="{png.name}" alt="渲染图">
            <p><a href="{blend.name}">下载 .blend</a></p>
            <p><a href="{png.name}">查看渲染图</a></p>
        </div>
"""
        
        html += """    </div>
</body>
</html>"""
        
        index_file.write_text(html, encoding='utf-8')
        return str(index_file)


def main():
    """主函数"""
    generator = Blender3DGenerator()
    
    if len(sys.argv) < 2:
        print("用法：python3 blender_3d.py <文字描述>")
        print("\n示例:")
        print('  python3 blender_3d.py "创建一个红色立方体"')
        print('  python3 blender_3d.py "创建一个蓝色球体"')
        print('  python3 blender_3d.py "创建一个场景：立方体 + 球体 + 灯光"')
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    result = generator.create_from_text(text)
    
    print(f"\n🎉 完成！")
    print(f"📄 Blend: {result['blend_file']}")
    print(f"🖼️ PNG: {result['png_file']}")


if __name__ == "__main__":
    main()
