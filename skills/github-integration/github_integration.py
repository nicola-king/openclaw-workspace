#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 GitHub 集成核心类
采用系统内部信息架构，不依赖外部 API
"""

import os
import json
import subprocess
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GitCommit:
    """Git 提交数据类"""
    hash: str
    message: str
    author: str
    date: str
    files_changed: List[str] = field(default_factory=list)


@dataclass
class GitBranch:
    """Git 分支数据类"""
    name: str
    is_current: bool = False
    remote: Optional[str] = None


class GitHubIntegration:
    """
    太一 GitHub 集成类
    
    采用系统内部信息架构:
    - 使用 Git CLI 操作本地仓库
    - 可选使用 GitHub API 进行远程操作
    - 记录系统内部状态
    """
    
    def __init__(self, config_path: str = "config/github.yaml"):
        self.config = self._load_config(config_path)
        self.token = os.getenv("GITHUB_TOKEN") or self.config.get("token", "")
        self.username = self.config.get("username", "")
        self.default_repo = self.config.get("default_repo", "")
        self.workspace = "/home/sayelf/.openclaw/workspace"
        
        # 验证 Git 安装
        self._verify_git()
        
        logger.info("✅ GitHub 集成初始化完成")
    
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"⚠️ 配置文件不存在: {path}，使用默认配置")
            return self._default_config()
        except json.JSONDecodeError:
            logger.warning(f"⚠️ 配置文件格式错误: {path}，使用默认配置")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "token": "",
            "username": "",
            "default_repo": "",
            "auth_type": "token"
        }
    
    def _verify_git(self):
        """验证 Git 安装"""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"✅ Git 版本: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            raise RuntimeError("❌ Git 未安装")
    
    def _run_git_command(self, args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """
        运行 Git 命令
        
        Args:
            args: Git 命令参数
            cwd: 工作目录
        
        Returns:
            Tuple[bool, str]: (是否成功, 输出)
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                cwd=cwd or self.workspace,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Git 命令失败: {' '.join(args)}")
            logger.error(f"   错误: {e.stderr}")
            return False, e.stderr
    
    # ==================== 仓库操作 ====================
    
    def clone_repo(self, url: str, target_dir: Optional[str] = None) -> bool:
        """
        克隆仓库
        
        Args:
            url: 仓库 URL
            target_dir: 目标目录
        
        Returns:
            bool: 是否成功
        """
        args = ["clone", url]
        if target_dir:
            args.append(target_dir)
        
        success, output = self._run_git_command(args, cwd="/home/sayelf")
        
        if success:
            logger.info(f"✅ 仓库克隆成功: {url}")
            return True
        else:
            logger.error(f"❌ 仓库克隆失败: {url}")
            return False
    
    def get_status(self, repo_path: Optional[str] = None) -> Dict:
        """
        获取仓库状态
        
        Args:
            repo_path: 仓库路径
        
        Returns:
            Dict: 状态信息
        """
        success, output = self._run_git_command(
            ["status", "--short"],
            cwd=repo_path
        )
        
        if not success:
            return {"error": output}
        
        modified = []
        added = []
        deleted = []
        untracked = []
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            status = line[:2]
            file = line[3:]
            
            if status.startswith('M') or status.endswith('M'):
                modified.append(file)
            elif status.startswith('A'):
                added.append(file)
            elif status.startswith('D'):
                deleted.append(file)
            elif status.startswith('??'):
                untracked.append(file)
        
        return {
            "modified": modified,
            "added": added,
            "deleted": deleted,
            "untracked": untracked,
            "has_changes": any([modified, added, deleted, untracked])
        }
    
    def commit(self, message: str, files: Optional[List[str]] = None, repo_path: Optional[str] = None) -> bool:
        """
        提交代码
        
        Args:
            message: 提交信息
            files: 要提交的文件列表，None 表示提交所有
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        # 添加文件
        if files:
            for file in files:
                self._run_git_command(["add", file], cwd=repo_path)
        else:
            self._run_git_command(["add", "-A"], cwd=repo_path)
        
        # 提交
        success, output = self._run_git_command(
            ["commit", "-m", message],
            cwd=repo_path
        )
        
        if success:
            logger.info(f"✅ 代码提交成功: {message}")
            return True
        else:
            logger.error(f"❌ 代码提交失败: {output}")
            return False
    
    def push(self, branch: str = "main", repo_path: Optional[str] = None) -> bool:
        """
        推送代码
        
        Args:
            branch: 分支名
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        success, output = self._run_git_command(
            ["push", "origin", branch],
            cwd=repo_path
        )
        
        if success:
            logger.info(f"✅ 代码推送成功: {branch}")
            return True
        else:
            logger.error(f"❌ 代码推送失败: {output}")
            return False
    
    def pull(self, branch: str = "main", repo_path: Optional[str] = None) -> bool:
        """
        拉取代码
        
        Args:
            branch: 分支名
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        success, output = self._run_git_command(
            ["pull", "origin", branch],
            cwd=repo_path
        )
        
        if success:
            logger.info(f"✅ 代码拉取成功: {branch}")
            return True
        else:
            logger.error(f"❌ 代码拉取失败: {output}")
            return False
    
    def create_branch(self, branch_name: str, base: str = "main", repo_path: Optional[str] = None) -> bool:
        """
        创建分支
        
        Args:
            branch_name: 分支名
            base: 基础分支
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        # 创建并切换分支
        success, output = self._run_git_command(
            ["checkout", "-b", branch_name, base],
            cwd=repo_path
        )
        
        if success:
            logger.info(f"✅ 分支创建成功: {branch_name}")
            return True
        else:
            logger.error(f"❌ 分支创建失败: {output}")
            return False
    
    def get_branches(self, repo_path: Optional[str] = None) -> List[GitBranch]:
        """
        获取分支列表
        
        Args:
            repo_path: 仓库路径
        
        Returns:
            List[GitBranch]: 分支列表
        """
        success, output = self._run_git_command(
            ["branch", "-a"],
            cwd=repo_path
        )
        
        if not success:
            return []
        
        branches = []
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            name = line.strip()
            is_current = name.startswith('*')
            if is_current:
                name = name[2:]
            
            branches.append(GitBranch(
                name=name,
                is_current=is_current
            ))
        
        return branches
    
    def get_commits(self, n: int = 10, repo_path: Optional[str] = None) -> List[GitCommit]:
        """
        获取提交历史
        
        Args:
            n: 获取数量
            repo_path: 仓库路径
        
        Returns:
            List[GitCommit]: 提交列表
        """
        success, output = self._run_git_command(
            ["log", f"-{n}", "--pretty=format:%H|%s|%an|%ad", "--date=short"],
            cwd=repo_path
        )
        
        if not success:
            return []
        
        commits = []
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                commits.append(GitCommit(
                    hash=parts[0][:7],
                    message=parts[1],
                    author=parts[2],
                    date=parts[3]
                ))
        
        return commits
    
    # ==================== 系统内部信息获取 ====================
    
    def get_repo_info(self, repo_path: Optional[str] = None) -> Dict:
        """
        获取仓库信息
        
        Args:
            repo_path: 仓库路径
        
        Returns:
            Dict: 仓库信息
        """
        # 获取远程 URL
        success, remote_url = self._run_git_command(
            ["remote", "get-url", "origin"],
            cwd=repo_path
        )
        
        # 获取当前分支
        success, branch = self._run_git_command(
            ["branch", "--show-current"],
            cwd=repo_path
        )
        
        # 获取提交数量
        success, commit_count = self._run_git_command(
            ["rev-list", "--count", "HEAD"],
            cwd=repo_path
        )
        
        # 获取最后提交时间
        success, last_commit = self._run_git_command(
            ["log", "-1", "--pretty=format:%ad", "--date=iso"],
            cwd=repo_path
        )
        
        return {
            "remote_url": remote_url.strip() if success else "",
            "current_branch": branch.strip() if success else "",
            "commit_count": int(commit_count.strip()) if success else 0,
            "last_commit": last_commit.strip() if success else "",
            "status": self.get_status(repo_path)
        }
    
    def get_code_stats(self, repo_path: Optional[str] = None) -> Dict:
        """
        获取代码统计
        
        Args:
            repo_path: 仓库路径
        
        Returns:
            Dict: 代码统计
        """
        # 获取代码行数
        success, output = self._run_git_command(
            ["ls-files"],
            cwd=repo_path
        )
        
        if not success:
            return {}
        
        files = output.strip().split('\n')
        total_lines = 0
        file_types = {}
        
        for file in files:
            if not file:
                continue
            
            # 统计文件类型
            ext = os.path.splitext(file)[1] or "no_extension"
            file_types[ext] = file_types.get(ext, 0) + 1
            
            # 统计行数
            file_path = os.path.join(repo_path or self.workspace, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
        
        return {
            "total_files": len(files),
            "total_lines": total_lines,
            "file_types": file_types
        }
    
    # ==================== 便捷操作 ====================
    
    def sync_config(self, repo_path: Optional[str] = None) -> bool:
        """
        同步系统配置到 GitHub
        
        Args:
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        # 获取当前状态
        status = self.get_status(repo_path)
        
        if not status.get("has_changes"):
            logger.info("ℹ️ 没有变更需要同步")
            return True
        
        # 提交变更
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[同步] 系统配置更新 - {timestamp}"
        
        if self.commit(message, repo_path=repo_path):
            return self.push(repo_path=repo_path)
        
        return False
    
    def create_backup(self, backup_name: Optional[str] = None, repo_path: Optional[str] = None) -> bool:
        """
        创建备份分支
        
        Args:
            backup_name: 备份分支名
            repo_path: 仓库路径
        
        Returns:
            bool: 是否成功
        """
        if not backup_name:
            backup_name = f"backup/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        return self.create_branch(backup_name, repo_path=repo_path)


# ==================== 便捷函数 ====================

def get_github_integration() -> GitHubIntegration:
    """获取 GitHub 集成实例 (单例)"""
    if not hasattr(get_github_integration, "_instance"):
        get_github_integration._instance = GitHubIntegration()
    return get_github_integration._instance


def quick_commit(message: str, files: Optional[List[str]] = None, repo_path: Optional[str] = None) -> bool:
    """便捷函数: 快速提交"""
    github = get_github_integration()
    
    if github.commit(message, files, repo_path):
        return github.push(repo_path=repo_path)
    
    return False


def sync_system_config(repo_path: Optional[str] = None) -> bool:
    """便捷函数: 同步系统配置"""
    github = get_github_integration()
    return github.sync_config(repo_path)


# ==================== 测试 ====================

if __name__ == "__main__":
    print("🚀 太一 GitHub 集成测试")
    
    # 初始化
    github = GitHubIntegration()
    
    # 测试1: 获取仓库状态
    print("\n📊 测试1: 获取仓库状态")
    status = github.get_status()
    print(f"   修改: {len(status.get('modified', []))} 个文件")
    print(f"   新增: {len(status.get('added', []))} 个文件")
    print(f"   删除: {len(status.get('deleted', []))} 个文件")
    
    # 测试2: 获取分支列表
    print("\n🌿 测试2: 获取分支列表")
    branches = github.get_branches()
    for branch in branches:
        current = "*" if branch.is_current else " "
        print(f"   {current} {branch.name}")
    
    # 测试3: 获取提交历史
    print("\n📝 测试3: 获取提交历史")
    commits = github.get_commits(5)
    for commit in commits:
        print(f"   {commit.hash} - {commit.message[:50]}...")
    
    # 测试4: 获取仓库信息
    print("\n📁 测试4: 获取仓库信息")
    info = github.get_repo_info()
    print(f"   远程: {info.get('remote_url', 'N/A')}")
    print(f"   分支: {info.get('current_branch', 'N/A')}")
    print(f"   提交数: {info.get('commit_count', 0)}")
    
    # 测试5: 获取代码统计
    print("\n📈 测试5: 获取代码统计")
    stats = github.get_code_stats()
    print(f"   文件数: {stats.get('total_files', 0)}")
    print(f"   代码行: {stats.get('total_lines', 0)}")
    
    print("\n✅ 所有测试完成")
