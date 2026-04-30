"""Gemini CLI Wrapper - Google Gemini AI integration"""

import subprocess
import os
import json
from typing import Optional, Dict, Any, List


class GeminiClient:
    """Gemini CLI 客户端 - 封装 Google Gemini CLI 操作"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = 'gemini-2.0-flash'):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = model
        self.env = os.environ.copy()
        if self.api_key:
            self.env['GEMINI_API_KEY'] = self.api_key
        
    def _run(self, args: List[str], capture: bool = True, input_text: Optional[str] = None) -> subprocess.CompletedProcess:
        """执行 Gemini CLI 命令"""
        cmd = ['gemini'] + args
        if input_text:
            result = subprocess.run(cmd, capture_output=capture, text=True, env=self.env, input=input_text)
        else:
            result = subprocess.run(cmd, capture_output=capture, text=True, env=self.env)
        return result
    
    def ask(self, prompt: str) -> Dict[str, Any]:
        """询问 Gemini (单次查询)"""
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def code_generate(self, description: str, language: str = 'python') -> Dict[str, Any]:
        """生成代码"""
        prompt = f"Create a {language} solution for: {description}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def code_review(self, file_path: str) -> Dict[str, Any]:
        """审查代码"""
        prompt = f"Review this code for bugs and best practices: @file {file_path}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def explain_code(self, file_path: str) -> Dict[str, Any]:
        """解释代码"""
        prompt = f"Explain what this code does: @file {file_path}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def debug_error(self, error_log: str) -> Dict[str, Any]:
        """调试错误"""
        prompt = f"Help me fix this error: {error_log}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def generate_docs(self, file_path: str) -> Dict[str, Any]:
        """生成文档"""
        prompt = f"Generate documentation for: @file {file_path}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def write_tests(self, file_path: str) -> Dict[str, Any]:
        """编写测试"""
        prompt = f"Write unit tests for: @file {file_path}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """读取文件内容"""
        prompt = f"Read the contents of: @file {file_path}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def run_shell(self, command: str) -> Dict[str, Any]:
        """执行 Shell 命令"""
        prompt = f"Run this command: @shell {command}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def fetch_url(self, url: str) -> Dict[str, Any]:
        """抓取网页内容"""
        prompt = f"Get content from: @fetch {url}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def google_search(self, query: str) -> Dict[str, Any]:
        """Google 搜索"""
        prompt = f"Search for: @google {query}"
        result = self._run([prompt])
        return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
    
    def interactive(self) -> subprocess.Popen:
        """启动交互模式"""
        return subprocess.Popen(['gemini'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, text=True, env=self.env)
    
    def check_installation(self) -> Dict[str, Any]:
        """检查 Gemini CLI 是否已安装"""
        result = subprocess.run(['gemini', '--version'], capture_output=True, text=True)
        return {
            'installed': result.returncode == 0,
            'version': result.stdout.strip() if result.returncode == 0 else None,
            'error': result.stderr.strip() if result.returncode != 0 else None
        }
