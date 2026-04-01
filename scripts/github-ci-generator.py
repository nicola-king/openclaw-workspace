#!/usr/bin/env python3
"""
GitHub AI 工程课 - CI 工作流模板生成器
功能：自动生成 GitHub Actions 工作流
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# CI 工作流模板
CI_WORKFLOW = """name: AGI CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Type check with mypy
        run: |
          pip install mypy
          mypy . --ignore-missing-imports
      
      - name: Security scan with bandit
        run: |
          pip install bandit
          bandit -r . -ll

  testing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest tests/ --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  codeql-analysis:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
      
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
"""

# 自动审查工作流
AUTO_REVIEW = """name: Auto Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint Comment
        uses: reviewdog/action-flake8@v3
        with:
          github_token: ${{ secrets.github_token }}
          reporter: github-pr-review
          filter_mode: nofilter
          fail_on_error: true
"""

# 安全扫描工作流
SECURITY_SCAN = """name: Security Scan

on:
  push:
    paths:
      - '**/requirements*.txt'
      - '**/package*.json'
  schedule:
    - cron: '0 0 * * 1'

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
"""

# Pre-commit 配置
PRE_COMMIT_CONFIG = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.12
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
"""

def create_workflow_files(workspace_path):
    """创建工作流文件"""
    workflows_dir = Path(workspace_path) / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    files_created = []
    
    # CI 工作流
    ci_file = workflows_dir / "agi-ci.yml"
    with open(ci_file, 'w', encoding='utf-8') as f:
        f.write(CI_WORKFLOW)
    files_created.append(str(ci_file))
    print(f'✅ 创建：{ci_file}')
    
    # 自动审查
    review_file = workflows_dir / "auto-review.yml"
    with open(review_file, 'w', encoding='utf-8') as f:
        f.write(AUTO_REVIEW)
    files_created.append(str(review_file))
    print(f'✅ 创建：{review_file}')
    
    # 安全扫描
    security_file = workflows_dir / "security-scan.yml"
    with open(security_file, 'w', encoding='utf-8') as f:
        f.write(SECURITY_SCAN)
    files_created.append(str(security_file))
    print(f'✅ 创建：{security_file}')
    
    return files_created

def create_pre_commit_config(workspace_path):
    """创建 Pre-commit 配置"""
    config_file = Path(workspace_path) / ".pre-commit-config.yaml"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(PRE_COMMIT_CONFIG)
    
    print(f'✅ 创建：{config_file}')
    return str(config_file)

def create_config_files(workspace_path):
    """创建配置文件"""
    config_dir = Path(workspace_path) / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Flake8 配置
    flake8_file = config_dir / ".flake8"
    with open(flake8_file, 'w', encoding='utf-8') as f:
        f.write("""[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist
ignore = E203,W503
""")
    print(f'✅ 创建：{flake8_file}')
    
    # MyPy 配置
    mypy_file = config_dir / ".mypy.ini"
    with open(mypy_file, 'w', encoding='utf-8') as f:
        f.write("""[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True
""")
    print(f'✅ 创建：{mypy_file}')
    
    return [str(flake8_file), str(mypy_file)]

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🐙 GitHub AI 工程课 - 工作流生成器                        ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    # 获取工作区路径
    workspace_path = sys.argv[1] if len(sys.argv) > 1 else "/home/nicola/.openclaw/workspace"
    
    print(f'📁 工作区：{workspace_path}')
    print('')
    
    print('📋 创建 GitHub Actions 工作流...')
    workflow_files = create_workflow_files(workspace_path)
    print('')
    
    print('📋 创建 Pre-commit 配置...')
    pre_commit_file = create_pre_commit_config(workspace_path)
    print('')
    
    print('📋 创建代码质量配置...')
    config_files = create_config_files(workspace_path)
    print('')
    
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  ✅ 配置完成                                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'创建文件：{len(workflow_files) + len(config_files) + 1} 个')
    print('')
    print('下一步:')
    print('  1. 安装 pre-commit: pip install pre-commit')
    print('  2. 激活钩子：pre-commit install')
    print('  3. 测试运行：pre-commit run --all-files')
    print('  4. 推送到 GitHub 自动触发 CI')
    print('')

if __name__ == '__main__':
    main()
