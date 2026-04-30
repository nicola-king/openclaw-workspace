"""Azure CLI Wrapper - VM/AKS/Functions/Storage operations"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class AzureClient:
    """Azure CLI 客户端 - 封装 Azure 命令行操作"""
    
    def __init__(self, subscription: Optional[str] = None):
        self.subscription = subscription
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 Azure CLI 命令"""
        cmd = ['az'] + args
        if self.subscription:
            cmd.extend(['--subscription', self.subscription])
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    # ========== Virtual Machines ==========
    
    def vm_list(self, resource_group: Optional[str] = None, output: str = 'table') -> Dict[str, Any]:
        """列出 VM"""
        args = ['vm', 'list', '-o', output]
        if resource_group:
            args.extend(['--resource-group', resource_group])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def vm_create(self, resource_group: str, name: str, image: str = 'UbuntuLTS') -> Dict[str, Any]:
        """创建 VM"""
        args = ['vm', 'create', '--resource-group', resource_group, '--name', name, '--image', image]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def vm_start(self, resource_group: str, name: str) -> Dict[str, Any]:
        """启动 VM"""
        args = ['vm', 'start', '--resource-group', resource_group, '--name', name]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def vm_stop(self, resource_group: str, name: str) -> Dict[str, Any]:
        """停止 VM"""
        args = ['vm', 'stop', '--resource-group', resource_group, '--name', name]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def vm_delete(self, resource_group: str, name: str) -> Dict[str, Any]:
        """删除 VM (需要确认)"""
        args = ['vm', 'delete', '--resource-group', resource_group, '--name', name, '--yes']
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== AKS (Kubernetes) ==========
    
    def aks_list(self, resource_group: Optional[str] = None, output: str = 'table') -> Dict[str, Any]:
        """列出 AKS 集群"""
        args = ['aks', 'list', '-o', output]
        if resource_group:
            args.extend(['--resource-group', resource_group])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def aks_get_credentials(self, resource_group: str, name: str) -> Dict[str, Any]:
        """获取 AKS 凭证"""
        args = ['aks', 'get-credentials', '--resource-group', resource_group, '--name', name]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Azure Functions ==========
    
    def functionapp_list(self, resource_group: Optional[str] = None) -> Dict[str, Any]:
        """列出 Function Apps"""
        args = ['functionapp', 'list']
        if resource_group:
            args.extend(['--resource-group', resource_group])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Storage ==========
    
    def storage_account_list(self, output: str = 'table') -> Dict[str, Any]:
        """列出存储账户"""
        args = ['storage', 'account', 'list', '-o', output]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def storage_blob_upload(self, account_name: str, container: str, file_path: str) -> Dict[str, Any]:
        """上传文件到 Blob 存储"""
        args = ['storage', 'blob', 'upload', '--account-name', account_name, 
                '--container-name', container, '--file', file_path]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def storage_blob_download(self, account_name: str, container: str, blob_name: str, file_path: str) -> Dict[str, Any]:
        """从 Blob 存储下载文件"""
        args = ['storage', 'blob', 'download', '--account-name', account_name,
                '--container-name', container, '--name', blob_name, '--file', file_path]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Generic Command ==========
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """执行任意 Azure CLI 命令"""
        args = command.split()
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
