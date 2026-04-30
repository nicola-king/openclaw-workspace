#!/usr/bin/env python3
"""
太一 GitHub 发布系统 - QQ 邮箱自动配置版 v4.0
自动从太一记忆读取 QQ 邮箱授权 · 完全智能自动化

核心特性:
- ✅ 自动读取太一记忆中的 QQ 邮箱授权
- ✅ 无需手动配置
- ✅ 配置永久存储
- ✅ 自动发送邮件通知
"""

import os
import json
import smtplib
import subprocess
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Dict, List, Optional

class TaiyiGitHubPublisherAutoConfig:
    """太一 GitHub 发布系统 - QQ 邮箱自动配置版"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.taiyi_workspace = Path("/home/nicola/.openclaw/workspace-taiyi")
        self.config_dir = self.workspace / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # 配置文件路径
        self.github_config_file = self.config_dir / "github-publish-config.json"
        self.memory_file = self.config_dir / "github-publish-memory.json"
        self.email_memory_file = self.config_dir / "qq-email-memory.json"
        self.log_file = self.config_dir / "github-publish-log.json"
        
        # 太一记忆配置文件
        self.taiyi_wechat_config = self.taiyi_workspace / "config" / "wechat.json"
        
        # 加载配置和记忆
        self.github_config = self._load_github_config()
        self.memory = self._load_memory()
        self.email_memory = self._load_email_memory()
        self.log = self._load_log()
        
        # GitHub 用户
        self.github_user = self.github_config.get('github_user', 'nicola-king')
        self.default_branch = self.github_config.get('default_branch', 'main')
        
        # QQ 邮箱配置
        self.email_config = self.email_memory.get('email_config', {})
        self.email_provider = self.email_config.get('provider', 'qq')
        self.smtp_server = self.email_config.get('smtp_server', 'smtp.qq.com')
        self.smtp_port = self.email_config.get('smtp_port', 465)
        self.use_ssl = self.email_config.get('use_ssl', True)
        
        print("=" * 70)
        print("太一 GitHub 发布系统 - QQ 邮箱自动配置版 v4.0")
        print("=" * 70)
        print(f"\n👤 GitHub 用户：{self.github_user}")
        print(f"📧 邮箱提供商：{self.email_provider}")
        print(f"📧 发件人：{self.email_config.get('sender_email', '未配置')}")
        print(f"📊 已发布项目：{self.memory.get('total_published', 0)} 个")
        print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
        print()
    
    def _load_github_config(self) -> Dict:
        """加载 GitHub 配置"""
        if self.github_config_file.exists():
            with open(self.github_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_github_config()
    
    def _create_default_github_config(self) -> Dict:
        """创建默认 GitHub 配置"""
        config = {
            'version': '3.0',
            'github_user': 'nicola-king',
            'default_branch': 'main',
            'auto_create_release': True,
            'auto_push': True,
            'auto_commit': True,
            'memory_enabled': True,
            'email_notification': {
                'enabled': True,
                'provider': 'qq',
                'smtp_server': 'smtp.qq.com',
                'smtp_port': 465,
                'use_ssl': True,
                'auto_send': True,
                'auto_configured': True
            }
        }
        
        with open(self.github_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return config
    
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
    
    def _load_email_memory(self) -> Dict:
        """加载邮箱记忆"""
        if self.email_memory_file.exists():
            with open(self.email_memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_email_memory()
    
    def _create_default_email_memory(self) -> Dict:
        """创建默认邮箱记忆 - 自动从太一记忆读取"""
        print("\n🔍 从太一记忆读取 QQ 邮箱配置...")
        
        # 尝试从太一记忆读取
        email_config = self._load_email_from_taiyi_memory()
        
        if email_config:
            print("✅ 已从太一记忆自动配置 QQ 邮箱")
            print(f"   发件人：{email_config.get('sender_email', '未知')}")
            print(f"   SMTP: {email_config.get('smtp_server', '未知')}:{email_config.get('smtp_port', '未知')}")
        else:
            print("⚠️  太一记忆中未找到 QQ 邮箱配置")
            email_config = {
                'provider': 'qq',
                'smtp_server': 'smtp.qq.com',
                'smtp_port': 465,
                'use_ssl': True,
                'sender_name': '太一 AGI GitHub 发布系统'
            }
        
        memory = {
            'email_config': email_config,
            'notification_templates': {
                'publish_success': {
                    'subject': '✅ GitHub 发布成功 - {project_name}',
                    'body': '项目 {project_name} 已成功发布到 GitHub\n\n仓库：{repo_url}\nRelease: {release_url}\n发布时间：{published_at}'
                },
                'publish_failed': {
                    'subject': '❌ GitHub 发布失败 - {project_name}',
                    'body': '项目 {project_name} 发布失败\n\n错误信息：{error}\n请检查后重试'
                },
                'daily_summary': {
                    'subject': '📊 GitHub 发布日报 - {date}',
                    'body': '今日发布统计:\n成功：{success_count} 个\n失败：{fail_count} 个\n总计：{total_count} 个\n\n累计发布：{total_published} 个'
                }
            },
            'recipients': [
                {
                    'name': 'nicola king',
                    'email': email_config.get('sender_email', '7073481596@qq.com'),
                    'notify_on': ['publish_success', 'publish_failed', 'daily_summary']
                }
            ],
            'last_email_sent': None,
            'email_history': []
        }
        
        with open(self.email_memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        
        return memory
    
    def _load_email_from_taiyi_memory(self) -> Optional[Dict]:
        """从太一记忆读取邮箱配置"""
        try:
            # 尝试从 wechat.json 读取 SMTP 配置
            if self.taiyi_wechat_config.exists():
                with open(self.taiyi_wechat_config, 'r', encoding='utf-8') as f:
                    wechat_config = json.load(f)
                
                smtp_config = wechat_config.get('smtp', {})
                if smtp_config and smtp_config.get('enabled', False):
                    return {
                        'provider': 'qq',
                        'smtp_server': smtp_config.get('smtp_server', 'smtp.qq.com'),
                        'smtp_port': 465,
                        'use_ssl': True,
                        'sender_name': '太一 AGI GitHub 发布系统',
                        'sender_email': smtp_config.get('sender_email', ''),
                        'sender_password': smtp_config.get('smtp_password', ''),
                        'auto_configured': True,
                        'configured_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'source': '太一记忆 - wechat.json'
                    }
            
            return None
            
        except Exception as e:
            print(f"⚠️  读取太一记忆失败：{e}")
            return None
    
    def _save_memory(self):
        """保存发布记忆"""
        self.memory['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.memory['total_published'] = len(self.memory['published_projects'])
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def _save_email_memory(self):
        """保存邮箱记忆"""
        with open(self.email_memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.email_memory, f, ensure_ascii=False, indent=2)
    
    def _load_log(self) -> Dict:
        """加载日志"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'logs': []}
    
    def _save_log(self):
        """保存日志"""
        self.log['logs'] = self.log['logs'][-100:]
        
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
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """发送邮件"""
        print(f"\n📧 发送邮件到：{to_email}")
        
        try:
            sender_email = self.email_memory['email_config'].get('sender_email', '')
            sender_password = self.email_memory['email_config'].get('sender_password', '')
            
            if not sender_email or not sender_password:
                print("⚠️  QQ 邮箱未配置，跳过邮件发送")
                return False
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = f"{self.email_config.get('sender_name', '太一 AGI')} <{sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加正文
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 连接 SMTP 服务器
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())
            server.quit()
            
            print(f"✅ 邮件发送成功")
            
            # 记录邮件历史
            self.email_memory['email_history'].append({
                'timestamp': datetime.now().isoformat(),
                'to': to_email,
                'subject': subject,
                'status': 'success'
            })
            self.email_memory['email_history'] = self.email_memory['email_history'][-50:]
            self.email_memory['last_email_sent'] = datetime.now().isoformat()
            self._save_email_memory()
            
            self._log_action('send_email', to_email, 'success', subject)
            
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")
            
            # 记录失败
            self.email_memory['email_history'].append({
                'timestamp': datetime.now().isoformat(),
                'to': to_email,
                'subject': subject,
                'status': 'failed',
                'error': str(e)
            })
            self._save_email_memory()
            
            self._log_action('send_email', to_email, 'failed', str(e))
            
            return False
    
    def send_publish_notification(self, project: Dict, status: str, error: str = ""):
        """发送发布通知邮件"""
        print("\n📧 准备发送发布通知...")
        
        recipients = self.email_memory.get('recipients', [])
        templates = self.email_memory.get('notification_templates', {})
        
        if status == 'success':
            template = templates.get('publish_success', {})
            subject = template.get('subject', '✅ GitHub 发布成功 - {project_name}')
            body = template.get('body', '项目 {project_name} 已成功发布')
            
            # 替换变量
            subject = subject.replace('{project_name}', project.get('name', ''))
            body = body.replace('{project_name}', project.get('name', ''))
            body = body.replace('{repo_url}', project.get('repo_url', ''))
            body = body.replace('{release_url}', project.get('release_url', ''))
            body = body.replace('{published_at}', project.get('published_at', ''))
        else:
            template = templates.get('publish_failed', {})
            subject = template.get('subject', '❌ GitHub 发布失败 - {project_name}')
            body = template.get('body', '项目 {project_name} 发布失败')
            
            # 替换变量
            subject = subject.replace('{project_name}', project.get('name', ''))
            body = body.replace('{project_name}', project.get('name', ''))
            body = body.replace('{error}', error)
        
        # 发送给所有收件人
        for recipient in recipients:
            if status in recipient.get('notify_on', []):
                self.send_email(recipient['email'], subject, body)
    
    def send_daily_summary(self, success_count: int, fail_count: int):
        """发送每日汇总邮件"""
        print("\n📧 准备发送每日汇总...")
        
        recipients = self.email_memory.get('recipients', [])
        templates = self.email_memory.get('notification_templates', {})
        
        template = templates.get('daily_summary', {})
        subject = template.get('subject', '📊 GitHub 发布日报 - {date}')
        body = template.get('body', '今日发布统计')
        
        # 替换变量
        today = datetime.now().strftime('%Y-%m-%d')
        subject = subject.replace('{date}', today)
        body = body.replace('{date}', today)
        body = body.replace('{success_count}', str(success_count))
        body = body.replace('{fail_count}', str(fail_count))
        body = body.replace('{total_count}', str(success_count + fail_count))
        body = body.replace('{total_published}', str(self.memory.get('total_published', 0)))
        
        # 发送给所有收件人
        for recipient in recipients:
            if 'daily_summary' in recipient.get('notify_on', []):
                self.send_email(recipient['email'], subject, body)
    
    def check_github_cli(self) -> bool:
        """检查 GitHub CLI"""
        print("\n🔍 检查 GitHub CLI...")
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
            if self.github_config.get('auto_commit', True):
                print("  2️⃣ 提交代码...")
                subprocess.run(["git", "add", "-A"], check=True, timeout=10)
                
                result = subprocess.run(
                    ["git", "diff", "--cached", "--quiet"],
                    capture_output=True
                )
                
                if result.returncode != 0:
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
                
                # 发送失败通知
                project['repo_url'] = f"https://github.com/{self.github_user}/{repo}"
                project['published_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                self.send_publish_notification(project, 'failed', result.stderr)
                return False
            
            # 6. 创建 Release
            if self.github_config.get('auto_create_release', True):
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
            project_data = {
                'name': name,
                'repo': repo,
                'path': path,
                'version': 'v1.0.0',
                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'status': 'published',
                'repo_url': f"https://github.com/{self.github_user}/{repo}",
                'release_url': f"https://github.com/{self.github_user}/{repo}/releases/tag/v1.0.0"
            }
            
            self.memory['published_projects'].append(project_data)
            self._save_memory()
            print("     ✅ 记忆已更新")
            
            # 8. 发送通知邮件
            print("  8️⃣ 发送通知邮件...")
            self.send_publish_notification(project_data, 'success')
            
            print(f"\n✅ {name} 发布成功！")
            print(f"   仓库：{project_data['repo_url']}")
            print(f"   Release: {project_data['release_url']}")
            
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
            
            # 发送失败通知
            project['repo_url'] = f"https://github.com/{self.github_user}/{repo}"
            project['published_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.send_publish_notification(project, 'failed', str(e))
            
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
        
        # 步骤 5: 发送每日汇总
        if success_count > 0 or fail_count > 0:
            self.send_daily_summary(success_count, fail_count)
        
        # 步骤 6: 发布总结
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
            print(f"📧 邮箱记忆：{self.email_memory_file}")
            print(f"📝 发布日志：{self.log_file}")
        
        return True
    
    def show_status(self):
        """显示发布状态"""
        print("\n📊 太一 GitHub 发布状态 (QQ 邮箱自动配置版)")
        print("=" * 70)
        
        print(f"\n👤 GitHub 用户：{self.github_user}")
        print(f"📧 邮箱提供商：{self.email_provider}")
        print(f"📧 发件人：{self.email_config.get('sender_email', '未配置')}")
        print(f"📚 已发布项目：{self.memory.get('total_published', 0)} 个")
        print(f"🕐 最后发布：{self.memory.get('last_publish', '无')}")
        
        # 已发布项目
        published = self.memory.get('published_projects', [])
        if published:
            print(f"\n✅ 已发布项目 ({len(published)} 个):")
            for project in published[-10:]:
                print(f"   • {project['name']} - {project.get('published_at', '未知')}")
        
        # 待发布项目
        pending = self.get_pending_projects()
        if pending:
            print(f"\n⏳ 待发布项目 ({len(pending)} 个):")
            for project in pending:
                print(f"   • {project['name']}")
        
        # 邮箱配置
        print(f"\n📧 邮箱配置:")
        print(f"   SMTP: {self.smtp_server}:{self.smtp_port}")
        print(f"   自动配置：{'✅' if self.email_config.get('auto_configured') else '❌'}")
        if self.email_config.get('auto_configured'):
            print(f"   配置来源：{self.email_config.get('source', '未知')}")
            print(f"   配置时间：{self.email_config.get('configured_at', '未知')}")
        
        # 最后邮件
        last_email = self.email_memory.get('last_email_sent', '无')
        print(f"   最后邮件：{last_email}")
        
        print("\n" + "=" * 70)


def main():
    """主函数"""
    import sys
    
    publisher = TaiyiGitHubPublisherAutoConfig()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'status':
            publisher.show_status()
        elif command == 'publish':
            publisher.publish_all()
        else:
            print(f"未知命令：{command}")
            print("可用命令：status, publish")
    else:
        # 默认执行发布
        publisher.publish_all()


if __name__ == "__main__":
    main()
