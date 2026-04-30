"""Kubernetes CLI Wrapper - Deployment/Scaling/Logs/Monitoring operations"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class K8sClient:
    """Kubernetes CLI 客户端 - 封装 kubectl 命令行操作"""
    
    def __init__(self, namespace: str = 'default', context: Optional[str] = None):
        self.namespace = namespace
        self.context = context
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 kubectl 命令"""
        cmd = ['kubectl'] + args
        if self.context:
            cmd.extend(['--context', self.context])
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    # ========== Workload Management ==========
    
    def apply(self, file: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """应用配置文件"""
        args = ['apply', '-f', file]
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_pods(self, namespace: Optional[str] = None, labels: Optional[str] = None, all_namespaces: bool = False) -> Dict[str, Any]:
        """列出 Pod"""
        args = ['get', 'pods']
        if all_namespaces:
            args.append('-A')
        elif namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        if labels:
            args.extend(['-l', labels])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_deployments(self, namespace: Optional[str] = None, all_namespaces: bool = False) -> Dict[str, Any]:
        """列出部署"""
        args = ['get', 'deployments']
        if all_namespaces:
            args.append('-A')
        elif namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_services(self, namespace: Optional[str] = None, all_namespaces: bool = False) -> Dict[str, Any]:
        """列出服务"""
        args = ['get', 'services']
        if all_namespaces:
            args.append('-A')
        elif namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def describe(self, resource_type: str, name: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """查看资源详情"""
        args = ['describe', resource_type, name]
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def delete(self, resource_type: str, name: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """删除资源"""
        args = ['delete', resource_type, name]
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def scale(self, deployment: str, replicas: int, namespace: Optional[str] = None) -> Dict[str, Any]:
        """扩缩容"""
        args = ['scale', f'deployment/{deployment}', f'--replicas={replicas}']
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def rollout_status(self, deployment: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """查看滚动更新状态"""
        args = ['rollout', 'status', f'deployment/{deployment}']
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def rollout_undo(self, deployment: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """回滚部署"""
        args = ['rollout', 'undo', f'deployment/{deployment}']
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Logs & Debugging ==========
    
    def logs(self, pod: str, follow: bool = False, namespace: Optional[str] = None, 
             container: Optional[str] = None) -> Dict[str, Any]:
        """查看日志"""
        args = ['logs']
        if follow:
            args.append('-f')
        if container:
            args.extend(['-c', container])
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        args.append(pod)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def exec(self, pod: str, command: str, namespace: Optional[str] = None, 
             container: Optional[str] = None, interactive: bool = False) -> Dict[str, Any]:
        """在 Pod 中执行命令"""
        args = ['exec', pod]
        if interactive:
            args.append('-it')
        if container:
            args.extend(['-c', container])
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        args.extend(['--'] + command.split())
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def cp(self, source: str, destination: str, namespace: Optional[str] = None, 
           container: Optional[str] = None) -> Dict[str, Any]:
        """复制文件到/从 Pod"""
        args = ['cp', source, destination]
        if container:
            args.extend(['-c', container])
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def port_forward(self, pod: str, local_port: int, remote_port: int, 
                     namespace: Optional[str] = None) -> Dict[str, Any]:
        """端口转发"""
        args = ['port-forward', pod, f'{local_port}:{remote_port}']
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def top_pods(self, namespace: Optional[str] = None, all_namespaces: bool = False) -> Dict[str, Any]:
        """查看 Pod 资源使用"""
        args = ['top', 'pods']
        if all_namespaces:
            args.append('-A')
        elif namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Configuration Management ==========
    
    def get_configmap(self, namespace: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
        """列出/查看 ConfigMap"""
        args = ['get', 'configmap']
        if name:
            args.append(name)
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_secret(self, namespace: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
        """列出/查看 Secret"""
        args = ['get', 'secret']
        if name:
            args.append(name)
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def create_configmap(self, name: str, data: Dict[str, str], namespace: Optional[str] = None) -> Dict[str, Any]:
        """创建 ConfigMap"""
        args = ['create', 'configmap', name]
        for key, value in data.items():
            args.extend(['--from-literal', f'{key}={value}'])
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def create_secret(self, name: str, data: Dict[str, str], namespace: Optional[str] = None) -> Dict[str, Any]:
        """创建 Secret"""
        args = ['create', 'secret', 'generic', name]
        for key, value in data.items():
            args.extend(['--from-literal', f'{key}={value}'])
        if namespace or self.namespace:
            args.extend(['-n', namespace or self.namespace])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Cluster Management ==========
    
    def cluster_info(self) -> Dict[str, Any]:
        """查看集群信息"""
        result = self._run(['cluster-info'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_nodes(self) -> Dict[str, Any]:
        """列出节点"""
        result = self._run(['get', 'nodes'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def get_namespaces(self) -> Dict[str, Any]:
        """列出命名空间"""
        result = self._run(['get', 'namespaces'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def create_namespace(self, name: str) -> Dict[str, Any]:
        """创建命名空间"""
        result = self._run(['create', 'namespace', name])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Generic Command ==========
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """执行任意 kubectl 命令"""
        args = command.split()
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
