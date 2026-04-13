"""Jimeng CLI Wrapper - ByteDance Jimeng AI video/image generation"""

import subprocess
import os
from typing import Optional, List, Dict, Any


class JimengClient:
    """即梦 CLI 客户端 - 封装字节即梦 AI 命令行操作"""
    
    def __init__(self, access_key_id: Optional[str] = None, secret_access_key: Optional[str] = None,
                 model: str = 'seedance-2.0'):
        self.access_key_id = access_key_id or os.environ.get('JIMENG_ACCESS_KEY_ID')
        self.secret_access_key = secret_access_key or os.environ.get('JIMENG_SECRET_ACCESS_KEY')
        self.model = model
        self.env = os.environ.copy()
        
    def _run(self, args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """执行即梦 CLI 命令"""
        cmd = ['jimeng'] + args
        return subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
    
    def check_installation(self) -> Dict[str, Any]:
        """检查即梦 CLI 是否已安装"""
        result = subprocess.run(['jimeng', '--version'], capture_output=True, text=True)
        return {
            'installed': result.returncode == 0,
            'version': result.stdout.strip() if result.returncode == 0 else None,
            'error': result.stderr.strip() if result.returncode != 0 else None
        }
    
    def check_balance(self) -> Dict[str, Any]:
        """查看余额/配额"""
        result = self._run(['balance'])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def generate_video(self, prompt: str, duration: int = 10, resolution: str = '1080p', 
                       fps: int = 30, model: Optional[str] = None) -> Dict[str, Any]:
        """文生视频"""
        args = ['generate', 'video', '--prompt', prompt, '--duration', str(duration),
                '--resolution', resolution, '--fps', str(fps)]
        if model or self.model:
            args.extend(['--model', model or self.model])
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def generate_image(self, prompt: str, resolution: str = '4k', style: str = 'artistic') -> Dict[str, Any]:
        """文生图"""
        args = ['generate', 'image', '--prompt', prompt, '--resolution', resolution, '--style', style]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def generate_video_from_image(self, image_path: str, prompt: str, duration: int = 5) -> Dict[str, Any]:
        """图生视频"""
        args = ['generate', 'video', '--image', image_path, '--prompt', prompt, '--duration', str(duration)]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def generate_image_from_image(self, image_path: str, prompt: str, resolution: str = '4k') -> Dict[str, Any]:
        """图生图"""
        args = ['generate', 'image', '--image', image_path, '--prompt', prompt, '--resolution', resolution]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def batch_generate(self, prompts_file: str, output_dir: str, gen_type: str = 'video') -> Dict[str, Any]:
        """批量生成"""
        args = ['batch', 'generate', '--prompts', prompts_file, '--type', gen_type, '--output', output_dir]
        result = self._run(args)
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def configure(self, access_key_id: str, secret_access_key: str, model: Optional[str] = None) -> Dict[str, Any]:
        """配置认证信息"""
        # 设置 Access Key ID
        result1 = self._run(['config', 'set', 'access_key_id', access_key_id])
        # 设置 Secret Access Key
        result2 = self._run(['config', 'set', 'secret_access_key', secret_access_key])
        # 设置模型
        result3 = None
        if model:
            result3 = self._run(['config', 'set', 'model', model])
        
        return {
            'access_key': {'stdout': result1.stdout, 'stderr': result1.stderr, 'returncode': result1.returncode},
            'secret_key': {'stdout': result2.stdout, 'stderr': result2.stderr, 'returncode': result2.returncode},
            'model': {'stdout': result3.stdout, 'stderr': result3.stderr, 'returncode': result3.returncode} if result3 else None
        }
    
    def login_interactive(self) -> subprocess.Popen:
        """启动交互式登录"""
        return subprocess.Popen(['jimeng', 'login'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
