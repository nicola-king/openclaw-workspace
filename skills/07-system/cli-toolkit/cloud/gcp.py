"""GCP CLI Wrapper - Compute/GKE/Cloud Run/Storage operations"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class GCPClient:
    """GCP CLI 客户端 - 封装 Google Cloud 命令行操作"""
    
    def __init__(self, project: Optional[str] = None):
        self.project = project
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 GCP CLI 命令"""
        cmd = ['gcloud'] + args
        if self.project:
            cmd.extend(['--project', self.project])
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    def _gsutil_run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 gsutil 命令"""
        cmd = ['gsutil'] + args
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    # ========== Compute Engine ==========
    
    def compute_instances_list(self, zone: Optional[str] = None) -> Dict[str, Any]:
        """列出 Compute 实例"""
        args = ['compute', 'instances', 'list']
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compute_instances_create(self, name: str, machine_type: str = 'e2-micro', zone: Optional[str] = None) -> Dict[str, Any]:
        """创建 Compute 实例"""
        args = ['compute', 'instances', 'create', name, '--machine-type', machine_type]
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compute_instances_start(self, name: str, zone: Optional[str] = None) -> Dict[str, Any]:
        """启动实例"""
        args = ['compute', 'instances', 'start', name]
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compute_instances_stop(self, name: str, zone: Optional[str] = None) -> Dict[str, Any]:
        """停止实例"""
        args = ['compute', 'instances', 'stop', name]
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compute_instances_delete(self, name: str, zone: Optional[str] = None) -> Dict[str, Any]:
        """删除实例 (需要确认)"""
        args = ['compute', 'instances', 'delete', name]
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== GKE (Kubernetes) ==========
    
    def container_clusters_list(self) -> Dict[str, Any]:
        """列出 GKE 集群"""
        args = ['container', 'clusters', 'list']
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def container_clusters_get_credentials(self, name: str, zone: Optional[str] = None) -> Dict[str, Any]:
        """获取 GKE 集群凭证"""
        args = ['container', 'clusters', 'get-credentials', name]
        if zone:
            args.extend(['--zone', zone])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Cloud Run ==========
    
    def run_services_list(self, region: Optional[str] = None) -> Dict[str, Any]:
        """列出 Cloud Run 服务"""
        args = ['run', 'services', 'list']
        if region:
            args.extend(['--region', region])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def run_deploy(self, service: str, image: str, region: Optional[str] = None) -> Dict[str, Any]:
        """部署 Cloud Run 服务"""
        args = ['run', 'deploy', service, '--image', image]
        if region:
            args.extend(['--region', region])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Cloud Storage (gsutil) ==========
    
    def gsutil_ls(self, bucket: Optional[str] = None) -> Dict[str, Any]:
        """列出 Cloud Storage 桶"""
        args = ['ls']
        if bucket:
            args.append(bucket)
        result = self._gsutil_run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def gsutil_cp(self, source: str, destination: str) -> Dict[str, Any]:
        """复制文件到/从 Cloud Storage"""
        args = ['cp', source, destination]
        result = self._gsutil_run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def gsutil_rsync(self, source: str, destination: str) -> Dict[str, Any]:
        """同步目录到 Cloud Storage"""
        args = ['rsync', '-r', source, destination]
        result = self._gsutil_run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def gsutil_mb(self, bucket: str) -> Dict[str, Any]:
        """创建 Cloud Storage 桶"""
        args = ['mb', f'gs://{bucket}']
        result = self._gsutil_run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def gsutil_rb(self, bucket: str) -> Dict[str, Any]:
        """删除 Cloud Storage 桶 (需要确认)"""
        args = ['rb', f'gs://{bucket}']
        result = self._gsutil_run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Generic Command ==========
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """执行任意 gcloud 命令"""
        args = command.split()
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
