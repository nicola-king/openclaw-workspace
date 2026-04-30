# Creator Module - 技能创建模块

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：太一 / 素问

---

## 🎯 职责

**技能模板生成 + 质量门禁**，快速创建标准化 Skills

---

## 📋 技能模板类型

### 1️⃣ 数据采集型
**用途**: 定时采集 API/网页数据
**代表**: weather, gmgn-market

**模板结构**:
```
skills/{skill-name}/
├── SKILL.md              # 技能说明
├── collector.py          # 数据采集脚本
├── requirements.txt      # Python 依赖
└── cron.json             # Cron 配置模板
```

**生成命令**:
```bash
python3 modules/creator/template-generator.py --type collector --name my-skill
```

---

### 2️⃣ 内容生成型
**用途**: LLM 生成文章/报告/创意
**代表**: shanmu-reporter, qiaomu-info-card-designer

**模板结构**:
```
skills/{skill-name}/
├── SKILL.md              # 技能说明
├── generator.py          # 内容生成脚本
├── templates/            # 内容模板
│   └── article.md.jinja
└── requirements.txt      # Python 依赖
```

**生成命令**:
```bash
python3 modules/creator/template-generator.py --type generator --name my-skill
```

---

### 3️⃣ 交易执行型
**用途**: 执行交易/下单/链上操作
**代表**: gmgn-swap, zhiji

**模板结构**:
```
skills/{skill-name}/
├── SKILL.md              # 技能说明
├── trader.py             # 交易执行脚本
├── config.py             # 配置管理
├── requirements.txt      # Python 依赖
└── confirmations/        # 确认流程
    └── pre-trade-check.py
```

**生成命令**:
```bash
python3 modules/creator/template-generator.py --type trader --name my-skill
```

---

### 4️⃣ 监控告警型
**用途**: 监控系统状态 + 异常告警
**代表**: self-check, healthcheck

**模板结构**:
```
skills/{skill-name}/
├── SKILL.md              # 技能说明
├── monitor.py            # 监控脚本
├── alerts.py             # 告警逻辑
├── requirements.txt      # Python 依赖
└── thresholds.json       # 阈值配置
```

**生成命令**:
```bash
python3 modules/creator/template-generator.py --type monitor --name my-skill
```

---

### 5️⃣ 工具增强型
**用途**: 封装外部服务/工具
**代表**: feishu, ssh-control

**模板结构**:
```
skills/{skill-name}/
├── SKILL.md              # 技能说明
├── tools.py              # 工具封装
├── config.py             # 配置管理
├── requirements.txt      # Python 依赖
└── examples/             # 使用示例
    └── example.md
```

**生成命令**:
```bash
python3 modules/creator/template-generator.py --type tool --name my-skill
```

---

## 🔧 模板生成器

```python
# template-generator.py
import os
import argparse
from datetime import datetime

TEMPLATES = {
    'collector': {
        'files': ['SKILL.md', 'collector.py', 'requirements.txt', 'cron.json'],
        'content': {
            'SKILL.md': '''# {skill_name} - 数据采集技能

> 版本：v1.0 | 创建：{date} | 负责 Bot：{bot}

---

## 🎯 职责

[技能描述]

---

## 🔧 使用命令

```bash
python3 collector.py [options]
```

---

## 📊 输出格式

[输出说明]

---

*创建：{date} | 太一 AGI*
''',
            'collector.py': '''#!/usr/bin/env python3
# {skill_name} 数据采集脚本

import requests
import json
from datetime import datetime

def collect_data():
    """采集数据主函数"""
    # TODO: 实现数据采集逻辑
    pass

if __name__ == '__main__':
    collect_data()
''',
            'requirements.txt': 'requests\n',
            'cron.json': '{\n  "schedule": "0 * * * *",\n  "command": "python3 collector.py"\n}\n'
        }
    },
    'generator': {
        'files': ['SKILL.md', 'generator.py', 'requirements.txt', 'templates/article.md.jinja'],
        'content': {
            'SKILL.md': '''# {skill_name} - 内容生成技能

> 版本：v1.0 | 创建：{date} | 负责 Bot：{bot}

---

## 🎯 职责

[技能描述]

---

## 🔧 使用命令

```bash
python3 generator.py --topic "主题"
```

---

*创建：{date} | 太一 AGI*
''',
            'generator.py': '''#!/usr/bin/env python3
# {skill_name} 内容生成脚本

def generate_content(topic):
    """生成内容主函数"""
    # TODO: 实现内容生成逻辑
    pass

if __name__ == '__main__':
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "默认主题"
    generate_content(topic)
''',
        }
    },
    # ... 其他模板类型
}

def generate_skill(skill_name, skill_type, bot='太一'):
    """生成技能文件结构"""
    base_path = f"skills/{skill_name}"
    os.makedirs(base_path, exist_ok=True)
    
    template = TEMPLATES.get(skill_type, TEMPLATES['collector'])
    
    for filename, content in template['content'].items():
        filepath = os.path.join(base_path, filename)
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else base_path, exist_ok=True)
        
        # 替换模板变量
        content = content.replace('{skill_name}', skill_name)
        content = content.replace('{date}', datetime.now().strftime('%Y-%m-%d %H:%M'))
        content = content.replace('{bot}', bot)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 创建：{filepath}")
    
    print(f"\n🎉 技能 '{skill_name}' 创建完成!")
    print(f"📁 位置：{base_path}")
    print(f"📝 下一步：编辑 SKILL.md 完善说明")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='技能模板生成器')
    parser.add_argument('--type', choices=['collector', 'generator', 'trader', 'monitor', 'tool'], required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--bot', default='太一')
    
    args = parser.parse_args()
    generate_skill(args.name, args.type, args.bot)
```

---

## 🚪 质量门禁

### 5 项通用检查

```python
# quality-gate.py
import os
import subprocess
import sys

def check_skill_md(filepath):
    """检查 SKILL.md 规范性"""
    required_sections = [
        '# ',           # 标题
        '## 🎯',        # 职责
        '## 🔧',        # 使用命令
        '*创建：',       # 创建信息
    ]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)
    
    return len(missing) == 0, missing

def check_executable(script_path):
    """检查脚本可执行权限"""
    return os.access(script_path, os.X_OK)

def check_python_syntax(filepath):
    """检查 Python 语法"""
    result = subprocess.run(
        ['python3', '-m', 'py_compile', filepath],
        capture_output=True
    )
    return result.returncode == 0

def check_error_handling(filepath):
    """检查错误处理"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_try = 'try:' in content or 'try:' in content
    has_except = 'except' in content or 'catch' in content
    has_log = 'log' in content.lower() or 'print' in content
    
    return has_try and has_except, "缺少错误处理" if not (has_try and has_except) else ""

def run_quality_gate(skill_path):
    """运行质量门禁"""
    results = []
    passed = True
    
    # 1. SKILL.md 检查
    skill_md = os.path.join(skill_path, 'SKILL.md')
    if os.path.exists(skill_md):
        ok, missing = check_skill_md(skill_md)
        if ok:
            results.append("✅ SKILL.md 规范")
        else:
            results.append(f"🔴 SKILL.md 缺失：{', '.join(missing)}")
            passed = False
    else:
        results.append("🔴 SKILL.md 不存在")
        passed = False
    
    # 2. Python 语法检查
    for root, dirs, files in os.walk(skill_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if check_python_syntax(filepath):
                    results.append(f"✅ Python 语法：{file}")
                else:
                    results.append(f"🔴 Python 语法错误：{file}")
                    passed = False
    
    # 3. 错误处理检查
    main_script = os.path.join(skill_path, 'collector.py')
    if os.path.exists(main_script):
        ok, msg = check_error_handling(main_script)
        if ok:
            results.append("✅ 错误处理完整")
        else:
            results.append(f"🟡 {msg}")
    
    # 4. 可执行权限
    for root, dirs, files in os.walk(skill_path):
        for file in files:
            if file.endswith('.sh'):
                filepath = os.path.join(root, file)
                if check_executable(filepath):
                    results.append(f"✅ 可执行：{file}")
                else:
                    results.append(f"🟡 需设置执行权限：{file}")
    
    return passed, results

if __name__ == '__main__':
    import sys
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print("## 质量门禁检查\n")
    
    passed, results = run_quality_gate(skill_path)
    
    for result in results:
        print(result)
    
    print(f"\n{'✅ 通过质量门禁' if passed else '🔴 未通过质量门禁'}")
    sys.exit(0 if passed else 1)
```

---

## 📋 使用命令

```bash
# 创建新技能
python3 modules/creator/template-generator.py --type collector --name my-skill

# 质量门禁检查
python3 modules/creator/quality-gate.py skills/my-skill

# 创建后自动检查
python3 modules/creator/template-generator.py --type collector --name my-skill && python3 modules/creator/quality-gate.py skills/my-skill
```

---

## 📊 输出格式

```markdown
## 质量门禁报告

**技能**: {skill-name}
**检查时间**: {timestamp}
**检查 Bot**: 太一

### 检查结果
| 检查项 | 状态 | 详情 |
|--------|------|------|
| SKILL.md 规范 | ✅ | 包含所有必需章节 |
| Python 语法 | ✅ | 3 个文件全部通过 |
| 错误处理 | 🟡 | 建议增加日志 |
| 可执行权限 | ✅ | 所有脚本已设置 |

### 结论
**状态**: ✅ 通过
**建议**: 1 个优化建议 (增加日志)
**下一步**: 提交 Git 仓库
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `modules/creator/SKILL.md` | 本文档 |
| `modules/creator/template-generator.py` | 模板生成器 |
| `modules/creator/quality-gate.py` | 质量门禁 |
| `skills/skill-creator/SKILL.md` | 系统自带 skill-creator |

---

*创建：2026-04-03 22:17 | 太一 AGI · 太一/素问主责*
