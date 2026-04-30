#!/usr/bin/env python3
"""
Hands - 执行层 (容器化沙箱)

灵感：Claude Managed Agents
作者：太一 AGI
创建：2026-04-09
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SANDBOX_DIR = Path("/tmp/brain-hands-sandbox")


@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    output: str
    error: Optional[str]
    exit_code: int
    duration_ms: int


class Hands:
    """执行层 (Hands)"""
    
    def __init__(self, sandbox: str = "process"):
        """
        初始化
        
        Args:
            sandbox: 沙箱类型 (process/docker)
        """
        self.sandbox = sandbox
        self.sandbox_dir = SANDBOX_DIR / f"sandbox-{os.getpid()}"
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(self, action) -> ExecutionResult:
        """
        执行行动
        
        Args:
            action: Action 对象
        
        Returns:
            ExecutionResult: 执行结果
        """
        start_time = datetime.now()
        
        try:
            if action.tool == "shell":
                result = self._execute_shell(action.command, action.args)
            elif action.tool == "python":
                result = self._execute_python(action.command, action.args)
            elif action.tool == "file_read":
                result = self._execute_file_read(action.command, action.args)
            elif action.tool == "file_write":
                result = self._execute_file_write(action.command, action.args)
            elif action.tool == "bot":
                result = self._execute_bot(action.bot, action.command, action.args)
            else:
                result = ExecutionResult(
                    success=False,
                    output="",
                    error=f"未知工具：{action.tool}",
                    exit_code=1,
                    duration_ms=0
                )
            
            # 记录执行时间
            result.duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return result
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1,
                duration_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )
    
    def _execute_shell(self, command: str, args: Dict) -> ExecutionResult:
        """执行 Shell 命令"""
        try:
            # 安全过滤
            if not self._is_safe_command(command):
                return ExecutionResult(
                    success=False,
                    output="",
                    error="命令被安全策略阻止",
                    exit_code=1,
                    duration_ms=0
                )
            
            # 执行
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=args.get("timeout", 300),
                cwd=str(self.sandbox_dir)
            )
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                exit_code=result.returncode,
                duration_ms=0
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="命令执行超时",
                exit_code=124,
                duration_ms=0
            )
    
    def _execute_python(self, code: str, args: Dict) -> ExecutionResult:
        """执行 Python 代码"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # 执行
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=args.get("timeout", 300),
                cwd=str(self.sandbox_dir)
            )
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                exit_code=result.returncode,
                duration_ms=0
            )
        finally:
            # 清理
            os.unlink(temp_file)
    
    def _execute_file_read(self, path: str, args: Dict) -> ExecutionResult:
        """读取文件"""
        try:
            file_path = Path(path)
            
            # 安全检查
            if not self._is_safe_path(file_path):
                return ExecutionResult(
                    success=False,
                    output="",
                    error="文件路径不在允许范围内",
                    exit_code=1,
                    duration_ms=0
                )
            
            content = file_path.read_text(encoding="utf-8")
            
            return ExecutionResult(
                success=True,
                output=content,
                error=None,
                exit_code=0,
                duration_ms=0
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1,
                duration_ms=0
            )
    
    def _execute_file_write(self, path: str, args: Dict) -> ExecutionResult:
        """写入文件"""
        try:
            file_path = Path(path)
            
            # 安全检查
            if not self._is_safe_path(file_path):
                return ExecutionResult(
                    success=False,
                    output="",
                    error="文件路径不在允许范围内",
                    exit_code=1,
                    duration_ms=0
                )
            
            content = args.get("content", "")
            file_path.write_text(content, encoding="utf-8")
            
            return ExecutionResult(
                success=True,
                output=f"文件已写入：{path}",
                error=None,
                exit_code=0,
                duration_ms=0
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1,
                duration_ms=0
            )
    
    def _execute_bot(self, bot: str, command: str, args: Dict) -> ExecutionResult:
        """调用 Bot 执行"""
        # TODO: 实际应调用 Bot API
        # 这里返回模拟结果
        return ExecutionResult(
            success=True,
            output=f"[{bot}] 执行：{command}",
            error=None,
            exit_code=0,
            duration_ms=100
        )
    
    def _is_safe_command(self, command: str) -> bool:
        """命令安全检查"""
        # 禁止的命令
        forbidden = [
            "rm -rf /",
            "mkfs",
            "dd if=/dev/zero",
            ":(){:|:&};:",
        ]
        
        return not any(f in command for f in forbidden)
    
    def _is_safe_path(self, path: Path) -> bool:
        """路径安全检查"""
        # 允许的路径
        allowed = [
            WORKSPACE,
            self.sandbox_dir,
            Path("/tmp"),
        ]
        
        try:
            resolved = path.resolve()
            return any(str(resolved).startswith(str(a)) for a in allowed)
        except Exception:
            return False
    
    def reset(self):
        """重置沙箱"""
        import shutil
        if self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup(self):
        """清理沙箱"""
        import shutil
        if self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)


def main():
    """测试"""
    hands = Hands()
    
    print("🤚 Hands 执行层测试")
    print()
    
    # 测试 Shell 命令
    from brain import Action
    action = Action(
        tool="shell",
        command="echo 'Hello from Hands'",
        args={}
    )
    
    result = hands.execute(action)
    print(f"执行结果：{'成功' if result.success else '失败'}")
    print(f"输出：{result.output}")
    if result.error:
        print(f"错误：{result.error}")
    print(f"耗时：{result.duration_ms}ms")
    
    # 清理
    hands.cleanup()


if __name__ == "__main__":
    main()
