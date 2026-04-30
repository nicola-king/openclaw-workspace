#!/usr/bin/env python3
"""
太一 GitHub 完全智能自动化发布系统 v2.0
自主智能 · 记忆存储 · 一键发布 · 无需重复配置

核心特性:
- ✅ 配置记忆存储
- ✅ 自动检测已发布项目
- ✅ 自动创建仓库
- ✅ 自动推送代码
- ✅ 自动创建 Release
- ✅ 状态持久化
- ✅ 无需重复配置
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class TaiyiGitHubAutoPublisher:
    """太一 GitHub 完全智能自动化发布器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.config_dir = self.workspace / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # 配置文件路径
        self.config_file = self.config_dir / "github-publish-config.json"
        self.memory_file = self.config_dir / "github-publish-memory.json"
        self.log_file = self.config_dir / "github-publish-log.json"
        
        # 加载配置和记忆
        self.config = self._load_config()
        self.memory = self._load_memory()
        self.log = self._load_log()
        
        # GitHub 用户
        self.github_user = self.config.get('github_user', 'nicola-king')
        self.default_branch = self.config.get('default_branch', 'main')
        
        print("=" * 70)
        print("太一 GitHub 完全智能自动化发布系统 v2.0")
        print("=" * 70)
        print(f"\n👤 GitHub 用户：{self.github_user}")
        print(f"📚 已发布项目：{self.memory.get('total_published', 0)} 个")
        print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
        print()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            'version': '1.0',
            'github_user': 'nicola-king',
            'default_branch': 'main',
            'auto_create_release': True,
            'auto_push': True,
            'auto_commit': True,
            'memory_enabled': True
        }
    
    def _load_memory(self) -> Dict:
        """加载发布记忆"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            'published_projects': [],
            'pending_projects': [],
            'failed_projects': [],
            'last_publish': None,
            'total_published': 0
        }
    
    def _load_log(self) -> Dict:
        """加载日志"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'logs': []}
    
    def _save_memory(self):
        """保存发布记忆"""
        self.memory['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.memory['total_published'] = len(self.memory['published_projects'])
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def _save_log(self):
        """保存日志"""
        self.log['logs'] = self.log['logs'][-100:]  # 保留最近 100 条
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)
    
    def _log_action(self, action: str, project: str, status: str, details: str = ""):
        """记录操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'project': project,
            'status': status,
            'details': details
        }
        self.log['logs'].append(log_entry)
        self._save_log()
    
    def check_github_cli(self) -> bool:
        """检查 GitHub CLI"""
        print("🔍 检查 GitHub CLI...")
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ GitHub CLI 已安装：{result.stdout.split()[1]}")
                self._log_action('check_github_cli', 'system', 'success')
                return True
            else:
                print("❌ GitHub CLI 未安装")
                self._log_action('check_github_cli', 'system', 'failed')
                return False
        except FileNotFoundError:
            print("❌ GitHub CLI 未找到")
            self._log_action('check_github_cli', 'system', 'failed', 'CLI not found')
            return False
    
    def authenticate_github(self) -> bool:
        """认证 GitHub"""
        print("\n🔐 认证 GitHub...")
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print("✅ GitHub 已认证")
                self._log_action('authenticate_github', 'system', 'success')
                return True
            else:
                print("⚠️  GitHub 未认证，开始认证...")
                subprocess.run(["gh", "auth", "login"], timeout=300)
                self._log_action('authenticate_github', 'system', 'success', 'Login completed')
                return True
        except Exception as e:
            print(f"❌ 认证失败：{e}")
            self._log_action('authenticate_github', 'system', 'failed', str(e))
            return False
    
    def is_project_published(self, project_name: str) -> bool:
        """检查项目是否已发布"""
        for project in self.memory.get('published_projects', []):
            if project.get('name') == project_name:
                return True
        return False
    
    def get_pending_projects(self) -> List[Dict]:
        """获取待发布项目"""
        pending = []
        
        # 检查 publish-all-agents.sh 中的项目
        agents_script = self.workspace / "scripts" / "publish-all-agents.sh"
        if agents_script.exists():
            with open(agents_script, 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析 AGENTS 数组
                import re
                agents = re.findall(r'\["([^"]+)"\]="([^"]+)"', content)
                
                for dir_name, repo_name in agents:
                    if not self.is_project_published(dir_name):
                        project_path = self.workspace / "skills" / dir_name
                        if project_path.exists():
                            pending.append({
                                'name': dir_name,
                                'repo': repo_name,
                                'path': str(project_path),
                                'type': 'agent'
                            })
        
        # 检查 github-release 目录
        release_dir = self.workspace / "github-release"
        if release_dir.exists():
            for project_dir in release_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    if not self.is_project_published(project_dir.name):
                        pending.append({
                            'name': project_dir.name,
                            'repo': project_dir.name,
                            'path': str(project_dir),
                            'type': 'release'
                        })
        
        return pending
    
    def publish_project(self, project: Dict) -> bool:
        """发布单个项目"""
        name = project.get('name')
        repo = project.get('repo')
        path = project.get('path')
        
        print(f"\n📦 发布项目：{name}")
        print("-" * 70)
        
        try:
            os.chdir(path)
            
            # 1. Git 初始化
            print("  1️⃣ Git 初始化...")
            if not (Path(path) / ".git").exists():
                subprocess.run(["git", "init"], check=True, timeout=10)
                print("     ✅ Git 仓库已初始化")
            else:
                print("     ✅ Git 仓库已存在")
            
            # 2. 提交代码
            if self.config.get('auto_commit', True):
                print("  2️⃣ 提交代码...")
                subprocess.run(["git", "add", "-A"], check=True, timeout=10)
                
                result = subprocess.run(
                    ["git", "diff", "--cached", "--quiet"],
                    capture_output=True
                )
                
                if result.returncode != 0:  # 有更改
                    subprocess.run(
                        ["git", "commit", "-m", f"🚀 Initial commit - {name}"],
                        check=True,
                        timeout=10
                    )
                    print("     ✅ 代码已提交")
                else:
                    print("     ⏭️  无更改，跳过提交")
            
            # 3. 设置分支
            print("  3️⃣ 设置分支...")
            subprocess.run(["git", "branch", "-M", self.default_branch], check=True, timeout=10)
            
            # 4. 添加/更新远程仓库
            print("  4️⃣ 设置远程仓库...")
            repo_url = f"https://github.com/{self.github_user}/{repo}.git"
            
            subprocess.run(["git", "remote", "remove", "origin"], capture_output=True, timeout=10)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True, timeout=10)
            print(f"     ✅ 远程仓库：{repo_url}")
            
            # 5. 创建 GitHub 仓库并推送
            print("  5️⃣ 创建仓库并推送...")
            result = subprocess.run(
                [
                    "gh", "repo", "create", f"{self.github_user}/{repo}",
                    "--public",
                    "--description", f"{name} - 太一 AGI",
                    "--source", ".",
                    "--remote", "origin",
                    "--push"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 or "already exists" in result.stderr:
                if result.returncode == 0:
                    print(f"     ✅ 仓库已创建并推送")
                else:
                    print(f"     ⏭️  仓库已存在，推送代码...")
                    subprocess.run(["git", "push", "-u", "origin", self.default_branch, "--force"], check=True, timeout=60)
                
                self._log_action('publish_project', name, 'success', 'Repository created and pushed')
            else:
                print(f"     ❌ 创建失败：{result.stderr}")
                self._log_action('publish_project', name, 'failed', result.stderr)
                return False
            
            # 6. 创建 Release
            if self.config.get('auto_create_release', True):
                print("  6️⃣ 创建 Release...")
                version = "v1.0.0"
                
                result = subprocess.run(
                    [
                        "gh", "release", "create", version,
                        "--title", f"{name} v1.0.0",
                        "--notes", f"🚀 {name} 正式发布！",
                        "--repo", f"{self.github_user}/{repo}"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0 or "already exists" in result.stderr:
                    print(f"     ✅ Release 已创建：{version}")
                    self._log_action('create_release', name, 'success', version)
                else:
                    print(f"     ⚠️  Release 创建失败：{result.stderr}")
            
            # 7. 更新记忆
            print("  7️⃣ 更新发布记忆...")
            self.memory['published_projects'].append({
                'name': name,
                'repo': repo,
                'path': path,
                'version': 'v1.0.0',
                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'status': 'published',
                'repo_url': f"https://github.com/{self.github_user}/{repo}",
                'release_url': f"https://github.com/{self.github_user}/{repo}/releases/tag/v1.0.0"
            })
            self._save_memory()
            print("     ✅ 记忆已更新")
            
            print(f"\n✅ {name} 发布成功！")
            print(f"   仓库：https://github.com/{self.github_user}/{repo}")
            print(f"   Release: https://github.com/{self.github_user}/{repo}/releases/tag/v1.0.0")
            
            return True
            
        except Exception as e:
            print(f"\n❌ {name} 发布失败：{e}")
            self._log_action('publish_project', name, 'failed', str(e))
            
            # 添加到失败列表
            self.memory['failed_projects'].append({
                'name': name,
                'repo': repo,
                'path': path,
                'failed_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'error': str(e)
            })
            self._save_memory()
            
            return False
    
    def publish_all(self):
        """发布所有待发布项目"""
        print("\n🚀 开始智能自动化发布流程...\n")
        
        # 步骤 1: 检查 GitHub CLI
        if not self.check_github_cli():
            print("\n⚠️  需要安装 GitHub CLI 才能继续")
            print("   请访问：https://cli.github.com/")
            return False
        
        # 步骤 2: 认证 GitHub
        if not self.authenticate_github():
            print("\n❌ GitHub 认证失败")
            return False
        
        # 步骤 3: 获取待发布项目
        print("\n📋 扫描待发布项目...")
        pending = self.get_pending_projects()
        
        if not pending:
            print("✅ 所有项目已发布，无需发布")
            print(f"\n📊 已发布项目：{self.memory.get('total_published', 0)} 个")
            print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
            return True
        
        print(f"✅ 发现 {len(pending)} 个待发布项目:\n")
        for i, project in enumerate(pending, 1):
            print(f"   {i}. {project['name']} ({project['type']})")
        
        # 步骤 4: 逐个发布
        print("\n" + "=" * 70)
        print("开始发布项目...")
        print("=" * 70)
        
        success_count = 0
        fail_count = 0
        
        for project in pending:
            if self.publish_project(project):
                success_count += 1
            else:
                fail_count += 1
            
            print("\n" + "=" * 70)
        
        # 步骤 5: 发布总结
        print("\n" + "=" * 70)
        print("🎉 发布完成！")
        print("=" * 70)
        print(f"\n📊 发布统计:")
        print(f"   成功：{success_count} 个")
        print(f"   失败：{fail_count} 个")
        print(f"   总计：{len(pending)} 个")
        print(f"\n📚 累计发布：{self.memory.get('total_published', 0)} 个")
        print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
        
        if success_count > 0:
            print(f"\n✅ 发布记忆已保存：{self.memory_file}")
            print(f"📝 发布日志：{self.log_file}")
        
        return True
    
    def show_status(self):
        """显示发布状态"""
        print("\n📊 太一 GitHub 发布状态")
        print("=" * 70)
        
        print(f"\n👤 GitHub 用户：{self.github_user}")
        print(f"📚 已发布项目：{self.memory.get('total_published', 0)} 个")
        print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
        
        # 已发布项目
        published = self.memory.get('published_projects', [])
        if published:
            print(f"\n✅ 已发布项目 ({len(published)} 个):")
            for project in published[-10:]:  # 显示最近 10 个
                print(f"   • {project['name']} - {project.get('published_at', '未知')}")
        
        # 待发布项目
        pending = self.get_pending_projects()
        if pending:
            print(f"\n⏳ 待发布项目 ({len(pending)} 个):")
            for project in pending:
                print(f"   • {project['name']}")
        
        # 失败项目
        failed = self.memory.get('failed_projects', [])
        if failed:
            print(f"\n❌ 失败项目 ({len(failed)} 个):")
            for project in failed:
                print(f"   • {project['name']} - {project.get('error', '未知错误')}")
        
        print("\n" + "=" * 70)
    
    def reset_memory(self):
        """重置发布记忆"""
        print("\n⚠️  确认要重置发布记忆吗？")
        print("   这将清除所有已发布项目记录")
        print("   但不会影响 GitHub 上的实际仓库")
        
        confirm = input("\n   输入 'yes' 确认：")
        if confirm.lower() == 'yes':
            self.memory = {
                'published_projects': [],
                'pending_projects': [],
                'failed_projects': [],
                'last_publish': None,
                'total_published': 0
            }
            self._save_memory()
            print("\n✅ 发布记忆已重置")
        else:
            print("\n❌ 已取消重置")


def main():
    """主函数"""
    import sys
    
    publisher = TaiyiGitHubAutoPublisher()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'status':
            publisher.show_status()
        elif command == 'reset':
            publisher.reset_memory()
        elif command == 'publish':
            publisher.publish_all()
        else:
            print(f"未知命令：{command}")
            print("可用命令：status, reset, publish")
    else:
        # 默认执行发布
        publisher.publish_all()


if __name__ == "__main__":
    main()
