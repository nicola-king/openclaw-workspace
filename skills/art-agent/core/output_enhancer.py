#!/usr/bin/env python3
"""
Output Enhancer v1.0.0
太一系统输出增强器 - 安全的美化处理器

原则：
- 只处理明确传入的文件路径
- 不自动扫描 workspace
- 提供 enhance(file_path) 接口供其他模块主动调用
- 替代之前危险的 scan-and-filter.sh
"""

import json
import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# 导入美学过滤器
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules', 'aesthetic-filter'))
from core import AestheticFilter, ContentType


class OutputEnhancer:
    """输出增强器 - 安全的美化处理器"""
    
    def __init__(self, config_path: str = None):
        """初始化增强器
        
        Args:
            config_path: 配置文件路径 (可选)
        """
        self.logger = self._setup_logger()
        self.filter = AestheticFilter(config_path or self._default_config_path())
        self.enhance_history: List[Dict[str, Any]] = []
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("output-enhancer")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _default_config_path(self) -> str:
        """默认配置文件路径"""
        return os.path.join(
            os.path.dirname(__file__),
            '..',
            'modules',
            'aesthetic-filter',
            'config.json'
        )
    
    def enhance(self, file_path: str, output_path: str = None, content_type: str = None) -> Dict[str, Any]:
        """增强单个文件
        
        Args:
            file_path: 输入文件路径
            output_path: 输出文件路径 (可选，默认覆盖原文件)
            content_type: 内容类型 (可选，自动检测)
            
        Returns:
            增强结果
        """
        start_time = datetime.now()
        
        # 验证文件路径
        path = Path(file_path)
        if not path.exists():
            return {
                "status": "error",
                "message": f"文件不存在：{file_path}"
            }
        
        self.logger.info(f"增强文件：{file_path}")
        
        # 读取文件
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确定内容类型
        ct = None
        if content_type:
            try:
                ct = ContentType(content_type)
            except ValueError:
                ct = None
        
        # 执行美学过滤
        result = self.filter.process(content, content_type=ct)
        
        # 确定输出路径
        out_path = output_path or file_path
        
        # 写入文件
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result["content"])
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 记录历史
        self.enhance_history.append({
            "timestamp": start_time.isoformat(),
            "input": file_path,
            "output": out_path,
            "quality": result.get("quality_level", "N/A"),
            "elapsed": elapsed
        })
        
        self.logger.info(f"增强完成：{file_path} → {out_path} (质量：{result.get('quality_level', 'N/A')})")
        
        return {
            "status": "success",
            "input_file": file_path,
            "output_file": out_path,
            "quality_level": result.get("quality_level", "N/A"),
            "changes": result.get("changes_count", 0),
            "elapsed": elapsed
        }
    
    def enhance_batch(self, file_paths: List[str], output_dir: str = None) -> Dict[str, Any]:
        """批量增强文件
        
        Args:
            file_paths: 文件路径列表
            output_dir: 输出目录 (可选，默认覆盖原文件)
            
        Returns:
            批量增强结果
        """
        start_time = datetime.now()
        
        self.logger.info(f"批量增强：{len(file_paths)} 个文件")
        
        results = []
        for file_path in file_paths:
            result = self.enhance(file_path, output_path=None)
            results.append(result)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 统计结果
        success_count = sum(1 for r in results if r.get("status") == "success")
        error_count = sum(1 for r in results if r.get("status") == "error")
        
        return {
            "status": "completed",
            "total": len(file_paths),
            "success": success_count,
            "error": error_count,
            "results": results,
            "elapsed": elapsed
        }
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取增强历史
        
        Args:
            limit: 返回数量限制
            
        Returns:
            增强历史列表
        """
        return self.enhance_history[-limit:]
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查
        
        Returns:
            健康状态
        """
        return {
            "status": "healthy",
            "module": "output-enhancer",
            "version": "1.0.0",
            "total_enhanced": len(self.enhance_history),
            "filter_health": self.filter.health_check()
        }
    
    @property
    def name(self) -> str:
        return "output-enhancer"
    
    @property
    def version(self) -> str:
        return "1.0.0"


# 便捷函数
def enhance(file_path: str, output_path: str = None, content_type: str = None) -> Dict[str, Any]:
    """增强单个文件 (便捷函数)
    
    Args:
        file_path: 输入文件路径
        output_path: 输出文件路径 (可选)
        content_type: 内容类型 (可选)
        
    Returns:
        增强结果
    """
    enhancer = OutputEnhancer()
    return enhancer.enhance(file_path, output_path, content_type)


def enhance_batch(file_paths: List[str], output_dir: str = None) -> Dict[str, Any]:
    """批量增强文件 (便捷函数)
    
    Args:
        file_paths: 文件路径列表
        output_dir: 输出目录 (可选)
        
    Returns:
        批量增强结果
    """
    enhancer = OutputEnhancer()
    return enhancer.enhance_batch(file_paths, output_dir)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="输出增强器")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--type", "-t", choices=["markdown", "code", "data", "report", "config"], help="内容类型")
    parser.add_argument("--batch", nargs="+", help="批量增强文件列表")
    parser.add_argument("--history", action="store_true", help="查看增强历史")
    parser.add_argument("--health", action="store_true", help="健康检查")
    
    args = parser.parse_args()
    
    enhancer = OutputEnhancer()
    
    if args.health:
        print(json.dumps(enhancer.health_check(), indent=2, ensure_ascii=False))
    elif args.batch:
        result = enhancer.enhance_batch(args.batch)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.history:
        history = enhancer.get_history()
        print(json.dumps(history, indent=2, ensure_ascii=False))
    elif args.input:
        result = enhancer.enhance(args.input, args.output, args.type)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(enhancer.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
