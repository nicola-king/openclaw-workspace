#!/usr/bin/env python3
"""
输出钩子 (Output Hook) - 全局美学过滤器拦截器
每个 Agent 的输出函数自动包装此钩子，确保所有输出经过美学过滤
"""

import json
import logging
import functools
from typing import Dict, Any, Callable, Optional
from pathlib import Path
from datetime import datetime

from core import AestheticFilter, ContentType, QualityLevel


class OutputHook:
    """输出钩子 - 全局美学过滤器拦截器"""
    
    def __init__(self, filter: AestheticFilter = None, config_path: str = "config.json"):
        self.filter = filter or AestheticFilter(config_path)
        self.logger = self._setup_logger()
        self.output_history: list = []
        self.quality_gate: str = "B"  # 质量门禁阈值
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("output-hook")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def hook_output(self, func: Callable) -> Callable:
        """装饰器：包装输出函数
        
        用法：
        @output_hook.hook_output
        def save_report(content, output_path):
            with open(output_path, 'w') as f:
                f.write(content)
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 提取输出内容
            content = kwargs.get('content') or (args[0] if args else None)
            output_path = kwargs.get('output_path') or (args[1] if len(args) > 1 else None)
            content_type = kwargs.get('content_type')
            
            if content is None:
                return func(*args, **kwargs)
            
            self.logger.info(f"拦截输出：{output_path or '未知路径'}")
            
            # 美学过滤
            result = self.filter.process(
                content,
                content_type=content_type
            )
            
            # 质量门禁检查
            quality = QualityLevel(result['quality_level'])
            if not self._pass_quality_gate(quality):
                self.logger.warning(f"质量不达标：{quality.value} < {self.quality_gate}，打回重做")
                return {
                    "status": "rejected",
                    "reason": f"质量等级 {quality.value} 低于门禁 {self.quality_gate}",
                    "suggestions": result.get('changes', [])
                }
            
            # 更新输出内容
            if output_path:
                kwargs['content'] = result['content']
                kwargs['output_path'] = self._get_final_path(output_path)
            
            # 执行原始函数
            output_result = func(*args, **kwargs)
            
            # 记录历史
            self.output_history.append({
                "timestamp": datetime.now().isoformat(),
                "path": output_path,
                "quality": quality.value,
                "status": "published"
            })
            
            self.logger.info(f"输出完成：{output_path} (质量：{quality.value})")
            
            return output_result
        
        return wrapper
    
    def _pass_quality_gate(self, quality: QualityLevel) -> bool:
        """检查质量是否通过门禁"""
        gate_order = {QualityLevel.S: 4, QualityLevel.A: 3, QualityLevel.B: 2, QualityLevel.C: 1}
        return gate_order.get(quality, 0) >= gate_order.get(QualityLevel(self.quality_gate), 2)
    
    def _get_final_path(self, output_path: str) -> str:
        """获取最终发布路径"""
        path = Path(output_path)
        
        # 如果路径包含 staging，替换为 production
        if 'staging' in str(path):
            return str(path).replace('staging', 'production')
        
        return str(path)
    
    def process_file(self, file_path: str, output_path: str = None) -> Dict[str, Any]:
        """处理文件并发布
        
        Args:
            file_path: 输入文件路径
            output_path: 输出文件路径 (默认自动命名)
            
        Returns:
            处理结果
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"status": "error", "message": f"文件不存在：{file_path}"}
        
        # 读取文件
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 美学过滤
        result = self.filter.process(content)
        
        # 质量门禁
        quality = QualityLevel(result['quality_level'])
        if not self._pass_quality_gate(quality):
            return {
                "status": "rejected",
                "quality": quality.value,
                "gate": self.quality_gate,
                "message": f"质量等级 {quality.value} 低于门禁 {self.quality_gate}"
            }
        
        # 确定输出路径
        if output_path is None:
            output_path = str(path.parent / f"{path.stem}_beautiful{path.suffix}")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        
        # 记录历史
        self.output_history.append({
            "timestamp": datetime.now().isoformat(),
            "input": str(path),
            "output": output_path,
            "quality": quality.value,
            "status": "published"
        })
        
        self.logger.info(f"文件处理并发布：{path.name} → {Path(output_path).name} (质量：{quality.value})")
        
        return {
            "status": "published",
            "input_file": str(path),
            "output_file": output_path,
            "quality": quality.value,
            "changes": result.get('changes', []),
            "changes_count": result.get('changes_count', 0)
        }
    
    def process_directory(self, dir_path: str, pattern: str = "*.md") -> Dict[str, Any]:
        """处理目录下所有文件
        
        Args:
            dir_path: 目录路径
            pattern: 文件匹配模式
            
        Returns:
            处理结果
        """
        path = Path(dir_path)
        
        if not path.exists():
            return {"status": "error", "message": f"目录不存在：{dir_path}"}
        
        results = []
        for file_path in path.glob(pattern):
            if file_path.is_file():
                result = self.process_file(str(file_path))
                results.append(result)
        
        published = sum(1 for r in results if r.get('status') == 'published')
        rejected = sum(1 for r in results if r.get('status') == 'rejected')
        
        return {
            "status": "completed",
            "total": len(results),
            "published": published,
            "rejected": rejected,
            "results": results
        }
    
    def get_history(self, limit: int = 10) -> list:
        """获取输出历史"""
        return self.output_history[-limit:]
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "healthy",
            "module": "output-hook",
            "version": "1.0.0",
            "quality_gate": self.quality_gate,
            "total_published": len(self.output_history),
            "filter_health": self.filter.health_check()
        }


# 全局输出钩子实例

output_hook = OutputHook()


def auto_hook_all_agents():
    """自动为所有 Agent 的输出函数包装钩子
    
    在太一系统启动时调用此函数
    """
    import sys
    
    # 获取所有已加载的模块
    for module_name, module in sys.modules.items():
        if not module_name.startswith('agent'):
            continue
        
        # 查找输出函数并包装
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and ('output' in attr_name.lower() or 'save' in attr_name.lower() or 'write' in attr_name.lower()):
                setattr(module, attr_name, output_hook.hook_output(attr))
                output_hook.logger.info(f"已包装 {module_name}.{attr_name}")
