# Deprecated Files


> 这些文件已被模块化重构取代，保留仅用于向后兼容。  
> 新代码请使用 `src/` 下的模块。

| 旧文件 | 新位置 | 迁移说明 |
|--------|--------|----------|
| `taiyi_travel_agent.py` | `src/router.py` + `src/planner/` | 统一路由 + 规划模块 |
| `ground_services.py` | `src/ground/` | 地接服务模块 |
| `provider_cli.py` | `src/provider/cli.py` | 供应商管理模块 |
| `travel_info_distillation.py` | `src/distill/` | 信息蒸馏模块 |
| `self_evolving_travel_agent.py` | `src/evolve/` | 自进化引擎模块 |
| `travel_knowledge_learner.py` | `src/learn/` | 知识学习模块 |
| `destination_notices.py` | `src/destination/` | 目的地注意事项模块 |
| `dual_mode_strategy.py` | `src/dual_mode/` | 双模式策略模块 |

**迁移日期**: 2026-04-25  
**计划删除**: 2026-07-25（保留 3 个月兼容期）


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48