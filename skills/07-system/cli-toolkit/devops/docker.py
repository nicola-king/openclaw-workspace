"""Docker CLI Wrapper - Container/Image/Compose operations"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class DockerClient:
    """Docker CLI 客户端 - 封装 Docker 命令行操作"""
    
    def __init__(self):
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 Docker 命令"""
        cmd = ['docker'] + args
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    # ========== Container Management ==========
    
    def ps(self, all_containers: bool = False) -> Dict[str, Any]:
        """列出容器"""
        args = ['ps']
        if all_containers:
            args.append('-a')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def run(self, image: str, name: Optional[str] = None, ports: Optional[List[str]] = None, 
            volumes: Optional[List[str]] = None, detach: bool = True) -> Dict[str, Any]:
        """运行容器"""
        args = ['run']
        if detach:
            args.append('-d')
        if name:
            args.extend(['--name', name])
        if ports:
            for port in ports:
                args.extend(['-p', port])
        if volumes:
            for vol in volumes:
                args.extend(['-v', vol])
        args.append(image)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def start(self, container: str) -> Dict[str, Any]:
        """启动容器"""
        result = self._run(['start', container])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def stop(self, container: str) -> Dict[str, Any]:
        """停止容器"""
        result = self._run(['stop', container])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def restart(self, container: str) -> Dict[str, Any]:
        """重启容器"""
        result = self._run(['restart', container])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def rm(self, container: str, force: bool = False) -> Dict[str, Any]:
        """删除容器"""
        args = ['rm']
        if force:
            args.append('-f')
        args.append(container)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def exec(self, container: str, command: str, interactive: bool = False) -> Dict[str, Any]:
        """在容器中执行命令"""
        args = ['exec']
        if interactive:
            args.append('-it')
        args.extend([container] + command.split())
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def logs(self, container: str, follow: bool = False, tail: Optional[int] = None) -> Dict[str, Any]:
        """查看容器日志"""
        args = ['logs']
        if follow:
            args.append('-f')
        if tail:
            args.extend(['--tail', str(tail)])
        args.append(container)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def inspect(self, container: str) -> Dict[str, Any]:
        """查看容器详情"""
        result = self._run(['inspect', container])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def stats(self, no_stream: bool = False) -> Dict[str, Any]:
        """查看容器资源统计"""
        args = ['stats']
        if no_stream:
            args.append('--no-stream')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Image Management ==========
    
    def images(self, all_images: bool = False) -> Dict[str, Any]:
        """列出镜像"""
        args = ['images']
        if all_images:
            args.append('-a')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def pull(self, image: str) -> Dict[str, Any]:
        """拉取镜像"""
        result = self._run(['pull', image])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def push(self, image: str) -> Dict[str, Any]:
        """推送镜像"""
        result = self._run(['push', image])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def build(self, context: str, tag: str, dockerfile: Optional[str] = None) -> Dict[str, Any]:
        """构建镜像"""
        args = ['build', '-t', tag, context]
        if dockerfile:
            args.extend(['-f', dockerfile])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def rmi(self, image: str, force: bool = False) -> Dict[str, Any]:
        """删除镜像"""
        args = ['rmi']
        if force:
            args.append('-f')
        args.append(image)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Docker Compose ==========
    
    def compose_up(self, file: Optional[str] = None, detach: bool = True) -> Dict[str, Any]:
        """启动 Compose 服务"""
        args = ['compose']
        if file:
            args.extend(['-f', file])
        args.append('up')
        if detach:
            args.append('-d')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compose_down(self, file: Optional[str] = None) -> Dict[str, Any]:
        """停止 Compose 服务"""
        args = ['compose']
        if file:
            args.extend(['-f', file])
        args.append('down')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compose_ps(self, file: Optional[str] = None) -> Dict[str, Any]:
        """列出 Compose 服务"""
        args = ['compose']
        if file:
            args.extend(['-f', file])
        args.append('ps')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compose_logs(self, service: Optional[str] = None, follow: bool = False) -> Dict[str, Any]:
        """查看 Compose 服务日志"""
        args = ['compose', 'logs']
        if follow:
            args.append('-f')
        if service:
            args.append(service)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def compose_build(self, service: Optional[str] = None) -> Dict[str, Any]:
        """构建 Compose 服务"""
        args = ['compose', 'build']
        if service:
            args.append(service)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Network Management ==========
    
    def network_ls(self) -> Dict[str, Any]:
        """列出网络"""
        result = self._run(['network', 'ls'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def network_create(self, name: str) -> Dict[str, Any]:
        """创建网络"""
        result = self._run(['network', 'create', name])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def network_rm(self, name: str) -> Dict[str, Any]:
        """删除网络"""
        result = self._run(['network', 'rm', name])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Volume Management ==========
    
    def volume_ls(self) -> Dict[str, Any]:
        """列出卷"""
        result = self._run(['volume', 'ls'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def volume_create(self, name: str) -> Dict[str, Any]:
        """创建卷"""
        result = self._run(['volume', 'create', name])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def volume_rm(self, name: str) -> Dict[str, Any]:
        """删除卷"""
        result = self._run(['volume', 'rm', name])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== System Management ==========
    
    def info(self) -> Dict[str, Any]:
        """查看系统信息"""
        result = self._run(['info'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def version(self) -> Dict[str, Any]:
        """查看版本信息"""
        result = self._run(['version'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def system_prune(self, all_volumes: bool = False) -> Dict[str, Any]:
        """清理系统 (需要确认)"""
        args = ['system', 'prune', '-f']
        if all_volumes:
            args.append('--volumes')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Generic Command ==========
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """执行任意 Docker 命令"""
        args = command.split()
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
