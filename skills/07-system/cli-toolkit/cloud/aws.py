"""AWS CLI Wrapper - EC2/S3/Lambda/RDS operations"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class AWSClient:
    """AWS CLI 客户端 - 封装 AWS 命令行操作"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行 AWS CLI 命令"""
        cmd = ['aws'] + args + ['--region', self.region]
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    # ========== EC2 Operations ==========
    
    def describe_instances(self, instance_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """列出 EC2 实例"""
        args = ['ec2', 'describe-instances']
        if instance_ids:
            for iid in instance_ids:
                args.extend(['--instance-ids', iid])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def run_instances(self, image_id: str, instance_type: str = 't3.micro', count: int = 1) -> Dict[str, Any]:
        """创建 EC2 实例"""
        args = ['ec2', 'run-instances', '--image-id', image_id, '--instance-type', instance_type, '--count', str(count)]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def stop_instances(self, instance_ids: List[str]) -> Dict[str, Any]:
        """停止实例"""
        args = ['ec2', 'stop-instances'] + ['--instance-ids'] + instance_ids
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def start_instances(self, instance_ids: List[str]) -> Dict[str, Any]:
        """启动实例"""
        args = ['ec2', 'start-instances'] + ['--instance-ids'] + instance_ids
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def terminate_instances(self, instance_ids: List[str]) -> Dict[str, Any]:
        """终止实例 (需要确认)"""
        args = ['ec2', 'terminate-instances'] + ['--instance-ids'] + instance_ids
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== S3 Operations ==========
    
    def s3_ls(self, bucket: Optional[str] = None) -> Dict[str, Any]:
        """列出 S3 桶或内容"""
        args = ['s3', 'ls']
        if bucket:
            args.append(bucket)
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def s3_cp(self, source: str, destination: str) -> Dict[str, Any]:
        """复制文件到/从 S3"""
        args = ['s3', 'cp', source, destination]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def s3_sync(self, source: str, destination: str) -> Dict[str, Any]:
        """同步目录到 S3"""
        args = ['s3', 'sync', source, destination]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def s3_mb(self, bucket: str) -> Dict[str, Any]:
        """创建 S3 桶"""
        args = ['s3', 'mb', f's3://{bucket}']
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def s3_rb(self, bucket: str, force: bool = False) -> Dict[str, Any]:
        """删除 S3 桶 (需要确认)"""
        args = ['s3', 'rb', f's3://{bucket}']
        if force:
            args.append('--force')
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Lambda Operations ==========
    
    def list_functions(self) -> Dict[str, Any]:
        """列出 Lambda 函数"""
        args = ['lambda', 'list-functions']
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def invoke_function(self, function_name: str, payload: Optional[str] = None) -> Dict[str, Any]:
        """调用 Lambda 函数"""
        args = ['lambda', 'invoke', '--function-name', function_name, 'output.json']
        if payload:
            args.extend(['--payload', payload])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== RDS Operations ==========
    
    def describe_db_instances(self) -> Dict[str, Any]:
        """列出 RDS 实例"""
        args = ['rds', 'describe-db-instances']
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    # ========== Generic Command ==========
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """执行任意 AWS CLI 命令"""
        args = command.split()
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
