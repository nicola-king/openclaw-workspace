#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采集器基类 - 定义通用接口
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from loguru import logger


class BaseCrawler(ABC):
    """采集器基类"""
    
    def __init__(self, platform: str, output_dir: str = "output"):
        self.platform = platform
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        
    @abstractmethod
    async def fetch(self, target: str, **kwargs) -> List[Dict[str, Any]]:
        """
        采集单个目标
        
        Args:
            target: 采集目标（账号/关键词/URL）
            **kwargs: 额外参数
            
        Returns:
            采集结果列表
        """
        pass
    
    @abstractmethod
    async def fetch_batch(self, targets: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        批量采集
        
        Args:
            targets: 采集目标列表
            **kwargs: 额外参数
            
        Returns:
            采集结果列表
        """
        pass
    
    def save_raw(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> Path:
        """保存原始数据"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.platform}_{timestamp}.jsonl"
        
        output_path = self.output_dir / "raw" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
        self.logger.info(f"保存原始数据：{output_path}")
        return output_path
    
    def save_processed(self, data: List[Dict[str, Any]], format: str = "csv") -> Path:
        """保存处理后的数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "csv":
            import pandas as pd
            filename = f"{self.platform}_{timestamp}.csv"
            output_path = self.output_dir / "processed" / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(data).to_csv(output_path, index=False, encoding="utf-8-sig")
        elif format == "json":
            filename = f"{self.platform}_{timestamp}.json"
            output_path = self.output_dir / "processed" / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"不支持的格式：{format}")
        
        self.logger.info(f"保存处理数据：{output_path}")
        return output_path
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置"""
        required_fields = ["platform", "targets"]
        for field in required_fields:
            if field not in config:
                self.logger.error(f"缺少必需字段：{field}")
                return False
        return True
    
    async def run(self, targets: List[str], save: bool = True) -> Dict[str, Any]:
        """
        执行采集任务
        
        Args:
            targets: 采集目标列表
            save: 是否保存结果
            
        Returns:
            执行结果统计
        """
        self.logger.info(f"开始采集 {self.platform}，目标数：{len(targets)}")
        
        results = await self.fetch_batch(targets)
        
        if save and results:
            self.save_raw(results)
            self.save_processed(results)
        
        stats = {
            "platform": self.platform,
            "targets": len(targets),
            "results": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"采集完成：{stats}")
        return stats
