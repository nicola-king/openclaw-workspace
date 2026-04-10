#!/usr/bin/env python3
"""
百度网盘客户端 - 太一集成版

作者：太一 AGI
创建：2026-04-10
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class BaiduNetDiskClient:
    """百度网盘客户端"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.backup_dir = Path("/tmp/baidu-backup")
        self.backup_dir.mkdir(exist_ok=True)
    
    def run_bypy(self, *args, timeout=300):
        """运行 bypy 命令"""
        try:
            cmd = ["bypy"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.workspace)
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "命令执行超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_quota(self):
        """获取网盘配额"""
        result = self.run_bypy("quota")
        if result["success"]:
            # 解析输出
            output = result["stdout"]
            lines = output.strip().split('\n')
            quota_info = {}
            for line in lines:
                if "Quota:" in line:
                    quota_info["quota"] = line.split(":")[1].strip()
                elif "Used:" in line:
                    quota_info["used"] = line.split(":")[1].strip()
            return quota_info
        return {"error": result.get("stderr", "未知错误")}
    
    def upload(self, local_path, remote_path="/apps/taiyi"):
        """上传文件"""
        local_file = Path(local_path)
        if not local_file.exists():
            return {"success": False, "error": f"文件不存在：{local_path}"}
        
        return self.run_bypy("upload", str(local_file), remote_path)
    
    def download(self, remote_path, local_path=None):
        """下载文件"""
        if local_path is None:
            local_path = str(self.backup_dir / Path(remote_path).name)
        
        return self.run_bypy("download", remote_path, local_path)
    
    def list_dir(self, remote_path="/apps/taiyi"):
        """列出目录"""
        result = self.run_bypy("list", remote_path)
        if result["success"]:
            return {"success": True, "files": result["stdout"].strip().split('\n')}
        return result
    
    def create_dir(self, remote_path):
        """创建目录"""
        return self.run_bypy("mkdir", remote_path)
    
    def remove(self, remote_path):
        """删除文件"""
        return self.run_bypy("remove", remote_path)
    
    def search(self, keyword):
        """搜索文件"""
        return self.run_bypy("search", keyword)
    
    def backup_workspace(self, exclude_dirs=None):
        """备份工作区"""
        if exclude_dirs is None:
            exclude_dirs = [
                "__pycache__", "node_modules", ".git", "venv", 
                ".pytest_cache", ".vscode", ".idea"
            ]
        
        backup_list = []
        
        # 遍历工作区
        for item in self.workspace.rglob("*"):
            # 跳过排除目录
            if any(exclude in str(item) for exclude in exclude_dirs):
                continue
            
            if item.is_file():
                rel_path = item.relative_to(self.workspace)
                remote_path = f"/apps/taiyi/workspace/{rel_path}"
                
                result = self.upload(str(item), remote_path)
                if result["success"]:
                    backup_list.append(str(rel_path))
        
        return {
            "success": True,
            "backed_up": len(backup_list),
            "files": backup_list[:100]  # 只返回前 100 个
        }
    
    def sync_from_netdisk(self, remote_dir="/apps/taiyi/workspace"):
        """从网盘同步"""
        result = self.list_dir(remote_dir)
        if not result["success"]:
            return result
        
        synced = []
        for file_line in result.get("files", []):
            if file_line.strip():
                # 解析文件名
                parts = file_line.split()
                if parts:
                    filename = parts[-1]
                    if filename not in [".", ".."]:
                        local_path = self.workspace / filename
                        remote_path = f"{remote_dir}/{filename}"
                        
                        download_result = self.download(remote_path, str(local_path))
                        if download_result["success"]:
                            synced.append(filename)
        
        return {"success": True, "synced": synced}
    
    def get_status(self):
        """获取百度网盘状态"""
        import subprocess
        
        # 检查客户端是否运行
        try:
            result = subprocess.run(
                ["pgrep", "-f", "baidunetdisk"],
                capture_output=True
            )
            client_running = result.returncode == 0
        except:
            client_running = False
        
        # 检查 bypy 配置
        bypy_config = Path.home() / ".bypy.json"
        bypy_configured = bypy_config.exists()
        
        # 获取配额
        quota = self.get_quota()
        
        return {
            "client_running": client_running,
            "bypy_configured": bypy_configured,
            "quota": quota,
            "backup_dir": str(self.backup_dir)
        }

# 单例
client = BaiduNetDiskClient()

if __name__ == "__main__":
    # 测试
    print("百度网盘客户端测试")
    print("=" * 50)
    
    status = client.get_status()
    print(f"客户端运行：{'✅' if status['client_running'] else '❌'}")
    print(f"bypy 配置：{'✅' if status['bypy_configured'] else '❌'}")
    print(f"配额信息：{status['quota']}")
