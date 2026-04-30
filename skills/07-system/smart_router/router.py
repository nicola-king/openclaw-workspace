#!/usr/bin/env python3
"""
Smart Router - 智能路由引擎
根据任务类型/成本/延迟自动调度模型和技能
"""

import json
import yaml
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class TaskType(str, Enum):
    CODE = "code"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    MATH = "math"
    CHAT = "chat"
    RESEARCH = "research"
    DATA = "data"


class Priority(str, Enum):
    P0 = "P0"  # 关键任务，立即执行
    P1 = "P1"  # 重要任务
    P2 = "P2"  # 常规任务
    P3 = "P3"  # 后台任务


class CostTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LatencyTier(str, Enum):
    FAST = "fast"
    NORMAL = "normal"
    SLOW = "slow"


@dataclass
class ModelConfig:
    model_id: str
    cost_per_1k_tokens: float
    max_context: int
    avg_latency_ms: int
    capabilities: List[str]
    enabled: bool = True


@dataclass
class SkillMetadata:
    skill_id: str
    category: str
    cost_tier: str
    latency_tier: str
    capabilities: List[str]
    enabled: bool = True


@dataclass
class RoutingDecision:
    model: str
    reason: str
    estimated_cost: float
    estimated_latency_ms: int
    fallback_model: Optional[str] = None


@dataclass
class Task:
    type: str
    priority: str
    context_size: int = 0
    budget_limit: float = 0.0
    latency_sensitive: bool = False
    metadata: Dict[str, Any] = None


class SmartRouter:
    """智能路由引擎"""
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.environ.get('OPENCLAW_WORKSPACE', 
                                                                '/home/nicola/.openclaw/workspace')
        self.skills_dir = Path(self.workspace_root) / 'skills'
        self.router_dir = Path(self.workspace_root) / 'skills' / 'smart-router'
        self.state_dir = Path('/tmp/smart-router')
        
        # 确保状态目录存在
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.models = self._load_models()
        self.skills = self._load_skills()
        
        # 路由策略
        self.routing_matrix = self._init_routing_matrix()
        
        # 指标
        self.metrics = {
            'total_requests': 0,
            'model_distribution': {},
            'cost_savings': 0.0,
            'last_updated': datetime.now().isoformat()
        }
    
    def _load_models(self) -> Dict[str, ModelConfig]:
        """加载模型配置"""
        models_file = self.router_dir / 'models.yaml'
        
        default_models = {
            'qwen3-coder-plus': ModelConfig(
                model_id='qwen3-coder-plus',
                cost_per_1k_tokens=0.004,
                max_context=256000,
                avg_latency_ms=3000,
                capabilities=['code', 'analysis', 'math']
            ),
            'qwen3.5-plus': ModelConfig(
                model_id='qwen3.5-plus',
                cost_per_1k_tokens=0.002,
                max_context=131072,
                avg_latency_ms=2000,
                capabilities=['code', 'writing', 'analysis', 'creative', 'math', 'chat']
            ),
            'qwen3-turbo': ModelConfig(
                model_id='qwen3-turbo',
                cost_per_1k_tokens=0.0005,
                max_context=32000,
                avg_latency_ms=500,
                capabilities=['chat', 'writing', 'creative']
            ),
            'gemini-2.5-pro': ModelConfig(
                model_id='gemini-2.5-pro',
                cost_per_1k_tokens=0.003,
                max_context=2000000,
                avg_latency_ms=4000,
                capabilities=['analysis', 'research', 'data', 'writing']
            )
        }
        
        if models_file.exists():
            try:
                with open(models_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    for model_id, config in data.get('models', {}).items():
                        if model_id in default_models:
                            # 更新默认配置
                            for key, value in config.items():
                                if hasattr(default_models[model_id], key):
                                    setattr(default_models[model_id], key, value)
                        else:
                            # 添加新模型
                            default_models[model_id] = ModelConfig(**config)
            except Exception as e:
                self._log_error(f"加载模型配置失败：{e}")
        
        return default_models
    
    def _load_skills(self) -> Dict[str, SkillMetadata]:
        """加载技能注册表"""
        registry_file = self.router_dir / 'registry.yaml'
        
        if registry_file.exists():
            try:
                with open(registry_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    skills = {}
                    for skill_id, metadata in data.get('skills', {}).items():
                        skills[skill_id] = SkillMetadata(
                            skill_id=skill_id,
                            **metadata
                        )
                    return skills
            except Exception as e:
                self._log_error(f"加载技能注册表失败：{e}")
        
        return {}
    
    def _init_routing_matrix(self) -> Dict[str, Dict[str, str]]:
        """初始化路由策略矩阵"""
        return {
            TaskType.CODE: {
                Priority.P0: 'qwen3-coder-plus',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3.5-plus',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.WRITING: {
                Priority.P0: 'qwen3.5-plus',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3-turbo',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.ANALYSIS: {
                Priority.P0: 'qwen3.5-plus',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3-turbo',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.CREATIVE: {
                Priority.P0: 'qwen3.5-plus',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3-turbo',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.MATH: {
                Priority.P0: 'qwen3.5-plus',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3-turbo',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.CHAT: {
                Priority.P0: 'qwen3-turbo',
                Priority.P1: 'qwen3-turbo',
                Priority.P2: 'qwen3-turbo',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.RESEARCH: {
                Priority.P0: 'gemini-2.5-pro',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3.5-plus',
                Priority.P3: 'qwen3-turbo'
            },
            TaskType.DATA: {
                Priority.P0: 'gemini-2.5-pro',
                Priority.P1: 'qwen3.5-plus',
                Priority.P2: 'qwen3.5-plus',
                Priority.P3: 'qwen3-turbo'
            }
        }
    
    def route(self, task: Dict[str, Any]) -> RoutingDecision:
        """
        路由决策
        
        Args:
            task: 任务描述
                - type: 任务类型 (code|writing|analysis|creative|math|chat|research|data)
                - priority: 优先级 (P0|P1|P2|P3)
                - context_size: 上下文大小 (tokens)
                - budget_limit: 预算限制 (USD)
                - latency_sensitive: 是否延迟敏感
        
        Returns:
            RoutingDecision: 路由决策
        """
        self.metrics['total_requests'] += 1
        
        # 解析任务
        task_obj = Task(
            type=task.get('type', 'chat'),
            priority=task.get('priority', 'P2'),
            context_size=task.get('context_size', 0),
            budget_limit=task.get('budget_limit', 0.0),
            latency_sensitive=task.get('latency_sensitive', False),
            metadata=task.get('metadata', {})
        )
        
        # 基础路由决策
        model_id = self._get_base_model(task_obj)
        reason_parts = []
        
        # 应用优化规则
        model_id, reason = self._apply_cost_optimization(model_id, task_obj)
        if reason:
            reason_parts.append(reason)
        
        model_id, reason = self._apply_latency_optimization(model_id, task_obj)
        if reason:
            reason_parts.append(reason)
        
        model_id, reason = self._apply_context_optimization(model_id, task_obj)
        if reason:
            reason_parts.append(reason)
        
        model_id, reason = self._apply_budget_optimization(model_id, task_obj)
        if reason:
            reason_parts.append(reason)
        
        # 计算估算
        model_config = self.models.get(model_id, self.models['qwen3.5-plus'])
        estimated_cost = (task_obj.context_size / 1000) * model_config.cost_per_1k_tokens
        estimated_latency = model_config.avg_latency_ms
        
        # 确定回退模型
        fallback_model = self._get_fallback_model(model_id)
        
        decision = RoutingDecision(
            model=model_id,
            reason=' | '.join(reason_parts) if reason_parts else 'default_routing',
            estimated_cost=round(estimated_cost, 6),
            estimated_latency_ms=estimated_latency,
            fallback_model=fallback_model
        )
        
        # 更新指标
        self._update_metrics(model_id, estimated_cost)
        
        # 记录决策
        self._log_routing(task_obj, decision)
        
        return decision
    
    def _get_base_model(self, task: Task) -> str:
        """获取基础路由模型"""
        task_type = task.type.lower()
        priority = task.priority.upper()
        
        if task_type in self.routing_matrix:
            return self.routing_matrix[task_type].get(priority, 'qwen3.5-plus')
        
        return 'qwen3.5-plus'
    
    def _apply_cost_optimization(self, model_id: str, task: Task) -> tuple:
        """应用成本优化规则"""
        reason = None
        
        # P1/P2 任务优先使用便宜模型
        if task.priority in ['P1', 'P2'] and model_id in ['qwen3.5-plus', 'qwen3-coder-plus']:
            if not task.latency_sensitive:
                model_id = 'qwen3-turbo'
                reason = 'cost_optimization(P1/P2)'
        
        return model_id, reason
    
    def _apply_latency_optimization(self, model_id: str, task: Task) -> tuple:
        """应用延迟优化规则"""
        reason = None
        
        # P0 或延迟敏感任务使用更快模型
        if task.priority == 'P0' or task.latency_sensitive:
            if model_id == 'qwen3-turbo':
                # qwen3-turbo 已经是最快的，不需要调整
                pass
            elif self.models.get(model_id, ModelConfig('', 0, 0, 9999, [])).avg_latency_ms > 3000:
                model_id = 'qwen3.5-plus'
                reason = 'latency_optimization(P0/sensitive)'
        
        return model_id, reason
    
    def _apply_context_optimization(self, model_id: str, task: Task) -> tuple:
        """应用上下文优化规则"""
        reason = None
        
        # 上下文超过 80K 时强制使用大上下文模型
        if task.context_size > 80000:
            model_config = self.models.get(model_id)
            if model_config and model_config.max_context < task.context_size:
                model_id = 'qwen3.5-plus'  # 131K 上下文
                reason = f'context_overflow({task.context_size}>80K)'
        
        return model_id, reason
    
    def _apply_budget_optimization(self, model_id: str, task: Task) -> tuple:
        """应用预算优化规则"""
        reason = None
        
        if task.budget_limit > 0:
            model_config = self.models.get(model_id)
            if model_config:
                estimated_cost = (task.context_size / 1000) * model_config.cost_per_1k_tokens
                if estimated_cost > task.budget_limit:
                    # 降级到更便宜的模型
                    model_id = 'qwen3-turbo'
                    reason = f'budget_limit({task.budget_limit})'
        
        return model_id, reason
    
    def _get_fallback_model(self, model_id: str) -> str:
        """获取回退模型"""
        # 模型不可用时的回退策略
        fallback_map = {
            'qwen3-coder-plus': 'qwen3.5-plus',
            'qwen3.5-plus': 'qwen3-turbo',
            'qwen3-turbo': 'qwen3.5-plus',
            'gemini-2.5-pro': 'qwen3.5-plus'
        }
        return fallback_map.get(model_id, 'qwen3.5-plus')
    
    def register_skill(self, skill_id: str, metadata: Dict[str, Any]) -> bool:
        """
        注册技能
        
        Args:
            skill_id: 技能 ID
            metadata: 技能元数据
        
        Returns:
            bool: 是否成功
        """
        try:
            skill = SkillMetadata(
                skill_id=skill_id,
                category=metadata.get('category', 'other'),
                cost_tier=metadata.get('cost_tier', 'medium'),
                latency_tier=metadata.get('latency_tier', 'normal'),
                capabilities=metadata.get('capabilities', []),
                enabled=True
            )
            self.skills[skill_id] = skill
            self._save_skills()
            return True
        except Exception as e:
            self._log_error(f"注册技能失败：{e}")
            return False
    
    def discover_skills(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        发现技能
        
        Args:
            filters: 过滤条件
        
        Returns:
            List[Dict]: 匹配的技能列表
        """
        results = []
        
        for skill_id, skill in self.skills.items():
            if not skill.enabled:
                continue
            
            # 应用过滤
            if filters:
                if 'category' in filters and skill.category != filters['category']:
                    continue
                if 'cost_tier' in filters and skill.cost_tier != filters['cost_tier']:
                    continue
                if 'latency_tier' in filters and skill.latency_tier != filters['latency_tier']:
                    continue
            
            results.append({
                'skill_id': skill.skill_id,
                'category': skill.category,
                'cost_tier': skill.cost_tier,
                'latency_tier': skill.latency_tier,
                'capabilities': skill.capabilities
            })
        
        return results
    
    def get_model_config(self, model_id: str) -> Optional[Dict[str, Any]]:
        """获取模型配置"""
        model = self.models.get(model_id)
        if model:
            return asdict(model)
        return None
    
    def list_models(self) -> List[Dict[str, Any]]:
        """列出所有可用模型"""
        return [
            {
                'model_id': m.model_id,
                'cost_per_1k_tokens': m.cost_per_1k_tokens,
                'max_context': m.max_context,
                'avg_latency_ms': m.avg_latency_ms,
                'capabilities': m.capabilities,
                'enabled': m.enabled
            }
            for m in self.models.values()
            if m.enabled
        ]
    
    def _save_skills(self):
        """保存技能注册表"""
        registry_file = self.router_dir / 'registry.yaml'
        
        data = {
            'version': '1.0.0',
            'updated': datetime.now().isoformat(),
            'skills': {
                skill_id: {
                    'category': skill.category,
                    'cost_tier': skill.cost_tier,
                    'latency_tier': skill.latency_tier,
                    'capabilities': skill.capabilities,
                    'enabled': skill.enabled
                }
                for skill_id, skill in self.skills.items()
            }
        }
        
        with open(registry_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    def _update_metrics(self, model_id: str, cost: float):
        """更新指标"""
        # 更新模型分布
        if model_id not in self.metrics['model_distribution']:
            self.metrics['model_distribution'][model_id] = 0
        self.metrics['model_distribution'][model_id] += 1
        
        # 计算成本节省（相比默认使用 qwen3.5-plus）
        default_cost = (0.002 * self.metrics['total_requests'])  # 假设平均 1K tokens
        self.metrics['cost_savings'] = max(0, default_cost - cost)
        
        self.metrics['last_updated'] = datetime.now().isoformat()
        
        # 保存指标
        metrics_file = self.state_dir / 'metrics.json'
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2)
    
    def _log_routing(self, task: Task, decision: RoutingDecision):
        """记录路由决策"""
        log_file = self.state_dir / 'routing.log'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task': {
                'type': task.type,
                'priority': task.priority,
                'context_size': task.context_size
            },
            'decision': asdict(decision)
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def _log_error(self, message: str):
        """记录错误"""
        error_file = self.state_dir / 'errors.log'
        
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
    
    def get_status(self) -> Dict[str, Any]:
        """获取路由器状态"""
        return {
            'status': 'active',
            'total_requests': self.metrics['total_requests'],
            'registered_skills': len(self.skills),
            'available_models': len([m for m in self.models.values() if m.enabled]),
            'model_distribution': self.metrics['model_distribution'],
            'cost_savings': round(self.metrics['cost_savings'], 6),
            'last_updated': self.metrics['last_updated']
        }


# CLI 入口
if __name__ == '__main__':
    import sys
    
    router = SmartRouter()
    
    if len(sys.argv) < 2:
        print("用法：python router.py <command> [args]")
        print("命令:")
        print("  route <json>     - 路由决策")
        print("  status           - 获取状态")
        print("  list-models      - 列出模型")
        print("  list-skills      - 列出技能")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'route':
        if len(sys.argv) < 3:
            print("错误：需要提供任务 JSON")
            sys.exit(1)
        task_json = json.loads(sys.argv[2])
        decision = router.route(task_json)
        print(json.dumps(asdict(decision), indent=2))
    
    elif command == 'status':
        status = router.get_status()
        print(json.dumps(status, indent=2))
    
    elif command == 'list-models':
        models = router.list_models()
        print(json.dumps(models, indent=2))
    
    elif command == 'list-skills':
        skills = router.discover_skills()
        print(json.dumps(skills, indent=2))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
