#!/usr/bin/env python3
# Meta-Skill-Creator · Python 版本 v1.0
# 用法：python3 create-skill.py <skill-name> <功能描述>

import os
import sys
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

# 技能模板库 - 使用列表存储避免三引号嵌套问题
DATA_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 数据采集脚本

import requests
import json
from datetime import datetime

def fetch_data():
    # TODO: 实现数据采集逻辑
    print("📊 正在采集数据...")
    return []

def save_data(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ 数据已保存：" + output_file)

if __name__ == "__main__":
    data = fetch_data()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = "data_" + ts + ".json"
    save_data(data, output_file)
'''

CONTENT_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 内容生成脚本

from pathlib import Path

def generate_content(input_file, output_file):
    # TODO: 实现内容生成逻辑
    print("📝 正在处理：" + input_file)
    print("📤 输出到：" + output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法：python3 " + sys.argv[0] + " <input> <output>")
        sys.exit(1)
    generate_content(sys.argv[1], sys.argv[2])
'''

TOOL_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 工具集成脚本

import os
import requests
from pathlib import Path

class Client:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('API_KEY')
        self.base_url = os.getenv('BASE_URL', 'https://api.example.com')
    
    def request(self, endpoint, **kwargs):
        headers = {'Authorization': 'Bearer ' + self.api_key}
        url = self.base_url + '/' + endpoint
        response = requests.get(url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    client = Client()
    print("🔧 {skill_name} 已就绪")
'''

VIDEO_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 视频处理脚本

import subprocess
from pathlib import Path

def process_video(input_file, output_file, options=None):
    """使用 ffmpeg 处理视频"""
    # TODO: 实现视频处理逻辑
    print("🎬 正在处理视频：" + input_file)
    cmd = ["ffmpeg", "-i", input_file, "-y"]
    if options:
        cmd.extend(options)
    cmd.append(output_file)
    subprocess.run(cmd, check=True)
    print("✅ 视频处理完成：" + output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法：python3 " + sys.argv[0] + " <input> <output>")
        sys.exit(1)
    process_video(sys.argv[1], sys.argv[2])
'''

IMAGE_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 图片生成/处理脚本

from PIL import Image, ImageDraw, ImageFont
import os

def process_image(input_file, output_file, options=None):
    """处理图片"""
    # TODO: 实现图片处理逻辑
    print("🖼️ 正在处理图片：" + input_file)
    img = Image.open(input_file)
    if options and options.get("resize"):
        img = img.resize(options["resize"])
    img.save(output_file)
    print("✅ 图片处理完成：" + output_file)

def generate_image(text, output_file, size=(1200, 630), bg_color="#0a0a0a", text_color="#00ff88"):
    """生成文字图片"""
    print("🎨 正在生成图片：" + output_file)
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    # TODO: 添加文字
    img.save(output_file)
    print("✅ 图片生成完成：" + output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法：python3 " + sys.argv[0] + " <input> <output>")
        sys.exit(1)
    process_image(sys.argv[1], sys.argv[2])
'''

WORKFLOW_SCRIPT = '''#!/usr/bin/env python3
# {skill_name} - 工作流自动化脚本

import json
from pathlib import Path
from datetime import datetime

def run_workflow(workflow_config, inputs=None):
    """执行工作流"""
    # TODO: 实现工作流逻辑
    print("⚙️ 正在执行工作流..." )
    results = []
    for step in workflow_config.get("steps", []):
        print("  执行步骤：" + step.get("name", "Unknown"))
        # TODO: 执行具体步骤
    print("✅ 工作流执行完成")
    return results

if __name__ == "__main__":
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "workflow.json"
    with open(config_file) as f:
        config = json.load(f)
    run_workflow(config)
'''

TEMPLATES = {
    "data": {
        "name": "数据采集类",
        "description": "从数据源采集数据，支持定时任务",
        "dependencies": ["requests", "beautifulsoup4", "pandas"],
        "triggers": ["采集数据", "抓取内容", "监控变化"],
        "script": DATA_SCRIPT
    },
    "content": {
        "name": "内容生成类",
        "description": "将输入内容转换为目标格式",
        "dependencies": ["jinja2", "markdown", "pypandoc"],
        "triggers": ["生成内容", "制作电子书", "转换格式"],
        "script": CONTENT_SCRIPT
    },
    "tool": {
        "name": "工具集成类",
        "description": "封装外部工具或 API",
        "dependencies": ["requests", "click"],
        "triggers": ["使用工具", "调用 API", "执行操作"],
        "script": TOOL_SCRIPT
    },
    "video": {
        "name": "视频处理类",
        "description": "视频剪辑/转换/压缩",
        "dependencies": ["ffmpeg-python"],
        "triggers": ["处理视频", "剪辑视频", "转换视频格式"],
        "script": VIDEO_SCRIPT
    },
    "image": {
        "name": "图片处理类",
        "description": "图片生成/编辑/优化",
        "dependencies": ["Pillow"],
        "triggers": ["处理图片", "生成图片", "制作封面"],
        "script": IMAGE_SCRIPT
    },
    "workflow": {
        "name": "工作流自动化类",
        "description": "多步骤任务自动化",
        "dependencies": ["pyyaml"],
        "triggers": ["执行工作流", "自动化任务", "批量处理"],
        "script": WORKFLOW_SCRIPT
    }
}

def detect_template_type(description: str) -> str:
    description_lower = description.lower()
    if any(kw in description_lower for kw in ['采集', '抓取', '监控', '数据', 'crawl', 'scrape']):
        return 'data'
    elif any(kw in description_lower for kw in ['视频', '剪辑', 'ffmpeg', 'video']):
        return 'video'
    elif any(kw in description_lower for kw in ['图片', '图像', '封面', 'image', 'photo']):
        return 'image'
    elif any(kw in description_lower for kw in ['工作流', '自动化', '批量', 'workflow', 'automation']):
        return 'workflow'
    elif any(kw in description_lower for kw in ['生成', '制作', '转换', '创建', 'generate', 'create']):
        return 'content'
    else:
        return 'tool'

def create_skill(skill_name: str, description: str, template_type: str = None):
    if not template_type:
        template_type = detect_template_type(description)
    
    template = TEMPLATES[template_type]
    skill_path = SKILLS_DIR / skill_name
    
    if skill_path.exists():
        print(f"❌ 技能已存在：{skill_path}")
        return False
    
    print(f"🔨 创建技能：{skill_name}")
    print(f"📋 类型：{template['name']}")
    print(f"📁 路径：{skill_path}")
    
    # 创建目录结构
    skill_path.mkdir(parents=True)
    (skill_path / "scripts").mkdir()
    (skill_path / "references").mkdir()
    (skill_path / "agents").mkdir()
    
    # 生成 SKILL.md
    triggers_md = "\n".join([f'- "{t}"' for t in template['triggers']])
    deps_md = "\n".join([f"- {d}" for d in template['dependencies']])
    
    skill_md = f"""# {skill_name} - {description}

> 创建时间：{datetime.now().strftime('%Y-%m-%d')} | 状态：🟡 开发中

---

## 🎯 核心功能

- 输入：待定义
- 输出：待定义
- 支持：{template['description']}

---

## 🎬 触发场景

{triggers_md}

---

## 🛠️ 使用方法

```bash
python3 scripts/{skill_name}.py
```

---

## 📦 依赖项

{deps_md}

---

## 📝 开发笔记

- [ ] 完善核心功能
- [ ] 添加测试用例
- [ ] 编写使用文档

---

*创建时间：{datetime.now().strftime('%Y-%m-%d')} | 版本：v0.1 | 状态：🟡 开发中*
"""
    
    (skill_path / "SKILL.md").write_text(skill_md, encoding='utf-8')
    
    # 生成主脚本
    script_content = template['script'].format(skill_name=skill_name)
    main_script = skill_path / "scripts" / f"{skill_name}.py"
    main_script.write_text(script_content, encoding='utf-8')
    os.chmod(main_script, 0o755)
    
    # 生成 README.md
    readme_md = f"""# {skill_name}

## 快速开始

```bash
pip install -r requirements.txt
python3 scripts/{skill_name}.py
```

## 开发中

本技能正在开发中，请参考 SKILL.md 了解规划。
"""
    (skill_path / "README.md").write_text(readme_md, encoding='utf-8')
    
    # 生成 .env.example
    (skill_path / ".env.example").write_text(
        f"# {skill_name} 配置示例\nAPI_KEY=your_api_key_here\nBASE_URL=https://api.example.com\n",
        encoding='utf-8'
    )
    
    # 生成 requirements.txt
    requirements = f"# {skill_name} 依赖\n\n" + "\n".join(template['dependencies']) + "\n"
    (skill_path / "requirements.txt").write_text(requirements, encoding='utf-8')
    
    # 生成 .gitignore
    (skill_path / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n.env\nvenv/\n.DS_Store\n",
        encoding='utf-8'
    )
    
    print("\n✅ 技能创建成功！")
    print("\n📁 目录结构:")
    for root, dirs, files in os.walk(skill_path):
        level = root.replace(str(skill_path), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')
    
    print(f"\n📝 下一步:")
    print(f"1. 编辑 {skill_path}/SKILL.md 完善功能定义")
    print(f"2. 在 {skill_path}/scripts/ 中实现核心逻辑")
    print(f"3. 测试：cd {skill_path} && python3 scripts/{skill_name}.py")
    print(f"4. Git 提交：cd ~/.openclaw/workspace && git add skills/{skill_name}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 用法：python3 create-skill.py <skill-name> [功能描述]")
        print("示例：python3 create-skill.py epub-generator 'Markdown 转 EPUB 电子书'")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else "功能待定义"
    create_skill(skill_name, description)
