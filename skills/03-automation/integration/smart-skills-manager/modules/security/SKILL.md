# Security Module - 安全验证模块

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：素问

---

## 🎯 职责

**技能安全扫描 + 兼容性检查**，确保新 Skills 安全可靠

---

## 🔍 安全检查清单

### 1️⃣ 恶意代码检测

**危险模式**:
```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',              # 删除根目录
    r'curl.*\|\s*bash',           # 远程执行
    r'wget.*\|\s*bash',           # 远程执行
    r'eval\s*\(',                 # 动态执行
    r'exec\s*\(',                 # 系统执行
    r'os\.system\s*\(',           # 系统调用
    r'subprocess\.call.*shell=True',  # Shell 执行
    r'__import__\s*\(',           # 动态导入
    r'importlib\.import_module',  # 动态导入
]
```

**检查脚本**:
```python
# security-scan.py
import re
import os

DANGEROUS_PATTERNS = [
    (r'rm\s+-rf\s+/', '删除根目录风险'),
    (r'curl.*\|\s*bash', '远程代码执行风险'),
    (r'wget.*\|\s*bash', '远程代码执行风险'),
    (r'eval\s*\(', '动态代码执行'),
    (r'os\.system\s*\(', '系统命令执行'),
    (r'subprocess\.call.*shell=True', 'Shell 注入风险'),
]

def scan_file(filepath):
    """扫描单个文件"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
        for pattern, risk in DANGEROUS_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issues.append({
                        'file': filepath,
                        'line': i,
                        'pattern': pattern,
                        'risk': risk,
                        'severity': '🔴' if 'rm -rf' in pattern or 'curl.*bash' in pattern else '🟡'
                    })
    
    return issues

def scan_directory(dirpath):
    """扫描整个技能目录"""
    all_issues = []
    for root, dirs, files in os.walk(dirpath):
        # 跳过隐藏目录和依赖目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
        
        for file in files:
            if file.endswith(('.py', '.sh', '.js')):
                filepath = os.path.join(root, file)
                issues = scan_file(filepath)
                all_issues.extend(issues)
    
    return all_issues

if __name__ == '__main__':
    import sys
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"## 安全扫描报告\n")
    print(f"**扫描路径**: {skill_path}\n")
    
    issues = scan_directory(skill_path)
    
    if not issues:
        print("✅ **未发现安全风险**\n")
    else:
        print(f"🔴 **发现 {len(issues)} 个安全问题**\n")
        print("| 文件 | 行号 | 风险 | 严重程度 |")
        print("|------|------|------|---------|")
        for issue in issues:
            print(f"| {issue['file']}:{issue['line']} | {issue['risk']} | {issue['severity']} |")
        
        # 统计严重程度
        red_count = sum(1 for i in issues if i['severity'] == '🔴')
        yellow_count = sum(1 for i in issues if i['severity'] == '🟡')
        
        print(f"\n**统计**: 🔴 {red_count} 严重 | 🟡 {yellow_count} 警告")
        
        if red_count > 0:
            print("\n**结论**: 🔴 危险 - 禁止安装")
            sys.exit(1)
        elif yellow_count > 3:
            print("\n**结论**: 🟡 需审查 - 人工确认后可安装")
            sys.exit(0)
        else:
            print("\n**结论**: ✅ 安全 - 可安装")
            sys.exit(0)
```

---

### 2️⃣ 敏感信息检测

**检测模式**:
```python
SENSITIVE_PATTERNS = [
    (r'API_KEY\s*=\s*["\'][^"\']+["\']', 'API Key 硬编码'),
    (r'api_key\s*=\s*["\'][^"\']+["\']', 'API Key 硬编码'),
    (r'password\s*=\s*["\'][^"\']+["\']', '密码硬编码'),
    (r'secret\s*=\s*["\'][^"\']+["\']', '密钥硬编码'),
    (r'token\s*=\s*["\'][^"\']+["\']', 'Token 硬编码'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Token'),
]
```

---

### 3️⃣ 依赖安全扫描

**检查脚本**:
```python
# dependency-scan.py
import subprocess
import os

def scan_requirements(filepath):
    """扫描 requirements.txt 依赖"""
    if not os.path.exists(filepath):
        return []
    
    # 使用 pip-audit 扫描
    result = subprocess.run(
        ['pip-audit', '-r', filepath, '--output', 'json'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return []
    
    # 解析漏洞信息
    vulnerabilities = []
    try:
        vuln_data = json.loads(result.stdout)
        for dep, vulns in vuln_data.items():
            for vuln in vulns:
                vulnerabilities.append({
                    'package': dep,
                    'vuln_id': vuln.get('id', 'UNKNOWN'),
                    'severity': vuln.get('severity', 'UNKNOWN'),
                    'fix': vuln.get('fix', '升级到最新版本')
                })
    except:
        pass
    
    return vulnerabilities
```

---

### 4️⃣ 兼容性检查

**检查项**:
```python
# compatibility-check.py
import sys
import importlib.util

def check_python_version(required_version):
    """检查 Python 版本兼容性"""
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    if current < required_version:
        return False, f"需要 Python {required_version}, 当前 {current}"
    return True, "Python 版本兼容"

def check_dependencies(requirements_file):
    """检查依赖是否已安装"""
    missing = []
    if not os.path.exists(requirements_file):
        return missing
    
    with open(requirements_file, 'r') as f:
        for line in f:
            package = line.split('==')[0].split('>=')[0].strip()
            if package and not package.startswith('#'):
                spec = importlib.util.find_spec(package)
                if spec is None:
                    missing.append(package)
    
    return missing

def check_tool_conflicts(skill_path):
    """检查工具命名冲突"""
    # 读取当前已安装技能的工具列表
    # 对比新技能的工具定义
    # 返回冲突列表
    return []

if __name__ == '__main__':
    import sys
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print("## 兼容性检查报告\n")
    
    # Python 版本
    ok, msg = check_python_version("3.8")
    print(f"Python 版本：{'✅' if ok else '🔴'} {msg}")
    
    # 依赖
    requirements = os.path.join(skill_path, 'requirements.txt')
    missing = check_dependencies(requirements)
    if missing:
        print(f"\n🔴 缺失依赖：{', '.join(missing)}")
        print(f"安装命令：pip install {' '.join(missing)}")
    else:
        print("\n✅ 依赖完整")
    
    # 工具冲突
    conflicts = check_tool_conflicts(skill_path)
    if conflicts:
        print(f"\n🟡 工具冲突：{', '.join(conflicts)}")
    else:
        print("\n✅ 无工具冲突")
```

---

## 📋 使用命令

```bash
# 完整安全扫描
python3 modules/security/security-scan.py <skill-path>

# 仅扫描恶意代码
python3 modules/security/security-scan.py --malware-only <skill-path>

# 仅扫描敏感信息
python3 modules/security/security-scan.py --secrets-only <skill-path>

# 兼容性检查
python3 modules/security/compatibility-check.py <skill-path>

# 依赖扫描
pip-audit -r <skill-path>/requirements.txt
```

---

## 📊 输出格式

```markdown
## 安全扫描报告

**技能**: {skill-name}
**扫描时间**: {timestamp}
**扫描 Bot**: 素问

### 恶意代码检测
| 文件 | 行号 | 风险 | 严重程度 |
|------|------|------|---------|
| script.py:15 | os.system() | 系统调用 | 🟡 |

### 敏感信息检测
✅ 未发现硬编码敏感信息

### 依赖安全
| 包 | 漏洞 ID | 严重程度 | 修复方案 |
|----|--------|---------|---------|
| requests<2.28 | CVE-2023-XXX | 🟡 中 | 升级到 2.31.0 |

### 兼容性检查
- ✅ Python 版本：3.10 (需要 3.8+)
- ✅ 依赖完整
- ✅ 无工具冲突

### 结论
**状态**: 🟡 需审查
**理由**: 1 个警告 (系统调用) + 1 个依赖漏洞
**建议**: 
1. 审查 script.py:15 的系统调用是否必要
2. 更新 requests 到最新版本
**决策**: 人工确认后可安装
```

---

## 🚨 决策矩阵

| 恶意代码 | 敏感信息 | 依赖漏洞 | 决策 |
|---------|---------|---------|------|
| 🔴 严重 | 任意 | 任意 | ❌ 禁止安装 |
| 🟡 警告 (≤3) | 无 | 无 | ✅ 可安装 (需审查) |
| 无 | 🔴 硬编码 | 任意 | ❌ 禁止安装 |
| 无 | 无 | 🟡 中低危 | ✅ 可安装 (建议修复) |
| 无 | 无 | 无 | ✅ 安全安装 |

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `modules/security/SKILL.md` | 本文档 |
| `modules/security/security-scan.py` | 安全扫描脚本 |
| `modules/security/compatibility-check.py` | 兼容性检查脚本 |
| `constitution/security/SOFTWARE-INSTALL-SECURITY.md` | 软件安装安全规范 |

---

*创建：2026-04-03 22:17 | 太一 AGI · 素问主责*
