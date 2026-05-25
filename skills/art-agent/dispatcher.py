#!/usr/bin/env python3
"""
太一艺术 Agent 统一调度引擎 v3.0
===================================
智能自动化调度 + 自进化

职责:
  路由任意艺术/设计/视觉/品牌任务到正确模块
  自动生成调度拓扑
  每次执行后自进化学习
"""

import json, logging, inspect, sys, os, time, hashlib
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent / "modules" / "self-evolution"))

MODULES_DIR = Path(__file__).parent / "modules"

# ═══════════════════════════════════════════════════════════════
# 任务类型路由表
# ═══════════════════════════════════════════════════════════════

class TaskDomain(Enum):
    DESIGN = "design"           # 设计系统/UI/UX
    BRAND = "brand"             # 品牌风格 (Starbucks/Ruixing/Apple)
    VISUAL = "visual"           # 可视化 (图表/卡片/3D)
    CONTENT = "content"         # 内容创作 (排版/发布)
    FILTER = "filter"           # 美学过滤/评分
    NARRATIVE = "narrative"     # 视觉叙事
    WORKFLOW = "workflow"       # 工作流可视化
    EVOLVE = "evolve"           # 自进化
    RENDER = "render"           # 渲染引擎 (PDF/HTML)

ROUTING_TABLE = {
    "设计": TaskDomain.DESIGN, "design": TaskDomain.DESIGN, "ui": TaskDomain.DESIGN, "ux": TaskDomain.DESIGN,
    "品牌": TaskDomain.BRAND, "brand": TaskDomain.BRAND, "风格": TaskDomain.BRAND, "配色": TaskDomain.BRAND,
    "图表": TaskDomain.VISUAL, "chart": TaskDomain.VISUAL, "card": TaskDomain.VISUAL, "卡片": TaskDomain.VISUAL,
    "3d": TaskDomain.VISUAL, "可视化": TaskDomain.VISUAL,
    "排版": TaskDomain.CONTENT, "发布": TaskDomain.CONTENT, "内容": TaskDomain.CONTENT,
    "美学": TaskDomain.FILTER, "filter": TaskDomain.FILTER, "评分": TaskDomain.FILTER,
    "叙事": TaskDomain.NARRATIVE, "story": TaskDomain.NARRATIVE,
    "拓扑": TaskDomain.WORKFLOW, "topology": TaskDomain.WORKFLOW, "工作流": TaskDomain.WORKFLOW,
    "进化": TaskDomain.EVOLVE, "evolve": TaskDomain.EVOLVE, "学习": TaskDomain.EVOLVE,
    "渲染": TaskDomain.RENDER, "render": TaskDomain.RENDER, "pdf": TaskDomain.RENDER, "输出": TaskDomain.RENDER,
    "生成文档": TaskDomain.RENDER, "导出": TaskDomain.RENDER,}



# ═══════════════════════════════════════════════════════════════
# 智能品牌匹配器 — 根据内容自动选择品牌风格
# ═══════════════════════════════════════════════════════════════

CONTENT_BRAND_MAP = {
    # 建筑/工程/工业 (优先级最高)
    "钢结构": "bmw", "steel structure": "bmw", "construction": "bmw",
    "engineering": "bmw", "预制": "bmw", "foldable house": "bmw",
    "建筑": "bmw", "施工": "bmw", "厂房": "bmw", "钢铁": "bmw",
    
    # 中东/能源/基建
    "中东": "hashicorp", "middle east": "hashicorp", "沙特": "hashicorp",
    "uae": "hashicorp", "迪拜": "hashicorp", "能源": "nvidia",
    "infrastructure": "ibm", "基建": "ibm",
    
    # 跨境贸易/金融/出口
    "跨境贸易": "binance", "export": "coinbase", "外贸": "binance",
    "trade": "binance", "投资": "binance", "financial": "binance",
    
    # 咖啡/餐饮/消费
    "咖啡馆": "starbucks", "coffee": "starbucks", "餐饮": "intercom",
    "restaurant": "intercom",
    
    # 科技/软件/AI
    "科技": "nvidia", "data": "clickhouse", "软件": "cursor",
    "ai": "cursor", "cloud": "hashicorp", "tech": "nvidia",
    
    # 设计/创意
    "设计": "figma", "creative": "framer", "品牌": "apple",
    "art": "apple", "艺术": "apple",
    
    # 旅游
    "travel": "airbnb", "酒店": "airbnb", "旅游": "airbnb",
    
    # 汽车/制造
    "汽车": "ferrari", "manufacturing": "bmw", "机械": "bugatti",
    
    # 教育
    "education": "notion", "学习": "claude", "知识": "mintlify",
    
    # 中国传统 / 东方美学 (chinese-traditional brand)
    "茶馆": "chinese-traditional", "中式茶馆": "chinese-traditional",
    "中式": "chinese-traditional", "东方美学": "chinese-traditional",
    "园林": "chinese-traditional", "宋": "chinese-traditional",
    "明": "chinese-traditional", "清": "chinese-traditional",
    "故宫": "chinese-traditional", "诗词": "chinese-traditional",
    "书法": "chinese-traditional", "水墨": "chinese-traditional",
    "国风": "chinese-traditional", "古风": "chinese-traditional",
    "华夏": "chinese-traditional", "传统色": "chinese-traditional",
    "中国风": "chinese-traditional", "汉服": "chinese-traditional",
    "国潮": "chinese-traditional", "瓷器": "chinese-traditional",
    "青花": "chinese-traditional", "红木": "chinese-traditional",
    "琴棋书画": "chinese-traditional", "竹": "chinese-traditional",
    "茶道": "chinese-traditional", "禅意": "chinese-traditional",
    "传统文化": "chinese-traditional", "老祖宗": "chinese-traditional",
    "故宫红": "chinese-traditional", "天青": "chinese-traditional",
    "孔雀蓝": "chinese-traditional", "海棠红": "chinese-traditional",
    "桃夭": "chinese-traditional", "瑾瑜": "chinese-traditional",
    "水龙吟": "chinese-traditional", "海天霞": "chinese-traditional",
    "黄不老": "chinese-traditional",

    # 生活/纪实/日常 (MUJI 风格最匹配)
    "日常": "muji", "生活": "muji", "纪实": "muji",
    "纪录片": "muji", "daily": "muji", "life": "muji",
    "story": "muji", "叙事": "muji", "烟火": "muji",
    "菜市场": "muji", "街头": "muji", "工作": "muji",
    "普通人": "muji", "平凡": "muji", "old man": "muji",
}

DEFAULT_BRAND = "muji"  # 默认回退  # 默认品牌 — 2026-05-10 从 binance 切到 MUJI

def smart_match_brand(task: str) -> str:
    """根据任务内容智能匹配品牌风格（长关键词优先）"""
    task_lower = task.lower()
    # 按关键词长度降序排列（更具体的关键词优先匹配）
    sorted_keywords = sorted(CONTENT_BRAND_MAP.items(), key=lambda x: -len(x[0]))
    for keyword, brand in sorted_keywords:
        if keyword in task_lower:
            return brand
    return DEFAULT_BRAND

# 注入到 ArtDispatcher

MODULE_MAP = {
    TaskDomain.DESIGN:    ("design-agent",     "DesignAgent",     "设计 Agent"),
    TaskDomain.BRAND:     ("brand-studio",     "BrandStudio",     "品牌工作室"),
    TaskDomain.VISUAL:    ("chart-generator",  "ChartGenerator",  "可视化引擎"),
    TaskDomain.CONTENT:   ("content-creator",  "ContentCreator",  "内容创作"),
    TaskDomain.FILTER:    ("aesthetic-filter", "AestheticFilter", "美学过滤器"),
    TaskDomain.NARRATIVE: ("visual-narrative", "VisualNarrative", "视觉叙事"),
    TaskDomain.WORKFLOW:  ("dispatch-viz",     "DispatchViz",     "调度拓扑"),
    TaskDomain.EVOLVE:    ("self-evolution",   "SelfEvolution",   "自进化"),
}

# ═══════════════════════════════════════════════════════════════
# 统一调度引擎
# ═══════════════════════════════════════════════════════════════

class ArtDispatcher:
    """
    太一艺术 Agent 调度核心
    自动路由 + 拓扑生成 + 自进化闭环
    """
    
    def __init__(self, log_dir: str = None):
        self.logger = self._setup_logger()
        self.modules_loaded = {}
        self.dispatch_history = []
        self.evolution_agent = None
        self.dispatch_viz = None
        
        # 加载自进化（先加载，用于 Learn）
        self._load_evolve()
        
    def _setup_logger(self):
        logger = logging.getLogger("TaiyiArtDispatch")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter(
                '%(asctime)s - ArtDispatch - %(levelname)s - %(message)s'
            ))
            logger.addHandler(h)
        return logger
    
    def _load_module(self, domain: TaskDomain):
        """懒加载模块"""
        if domain in self.modules_loaded:
            return self.modules_loaded[domain]
        
        mod_name, cls_name, desc = MODULE_MAP[domain]
        mod_path = MODULES_DIR / mod_name / "core.py"
        
        if not mod_path.exists():
            self.logger.warning(f"模块 {mod_name} 不存在, 返回 stub")
            return None
        
        spec = importlib.util.spec_from_file_location(mod_name, str(mod_path))
        mod = importlib.util.module_from_spec(spec)
        # 加入模块所在目录到 sys.path，确保子依赖可解析
        mod_dir = str(mod_path.parent)
        if mod_dir not in sys.path:
            sys.path.insert(0, mod_dir)
        spec.loader.exec_module(mod)
        
        cls = getattr(mod, cls_name, None)
        if cls:
            instance = cls()
            self.modules_loaded[domain] = instance
            self.logger.info(f"  ✅ 加载 {desc} ({cls_name})")
            return instance
        return None
    
    def _load_evolve(self):
        """加载自进化模块"""
        try:
            ev_path = MODULES_DIR / "self-evolution" / "core.py"
            if ev_path.exists():
                spec = importlib.util.spec_from_file_location("evolution", str(ev_path))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.evolution_agent = mod.SelfEvolution()
                self.logger.info("  ✅ 自进化引擎已加载")
        except Exception as e:
            self.logger.warning(f"自进化加载失败: {e}")
    
    def _load_dispatch_viz(self):
        """加载调度拓扑模块"""
        try:
            dv_path = MODULES_DIR / "dispatch-viz" / "core.py"
            if dv_path.exists():
                spec = importlib.util.spec_from_file_location("dispatch_viz", str(dv_path))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
        except: pass
        return None
    
    def resolve_domain(self, task: str) -> TaskDomain:
        """智能识别任务类型"""
        task_lower = task.lower()
        # 优先精确匹配
        for keyword, domain in ROUTING_TABLE.items():
            if keyword in task_lower:
                return domain
        # 模糊匹配: 根据内容判断
        if any(w in task_lower for w in ["星巴克", "瑞幸", "apple", "starbucks", "ruixing", "品牌"]):
            return TaskDomain.BRAND
        if any(w in task_lower for w in ["报告", "排版", "pdf", "格式"]):
            return TaskDomain.FILTER
        if any(w in task_lower for w in ["流程", "架构", "拓扑"]):
            return TaskDomain.WORKFLOW
        return TaskDomain.FILTER  # 默认美学过滤
    
    def dispatch(self, task: str, params: Dict = None) -> Dict:
        """
        统一调度入口
        task: 任务描述 (如 "用星巴克风格美化这个报告")
        params: 输入参数
        """
        t0 = time.time()
        params = params or {}
        
        domain = self.resolve_domain(task)
        module = self._load_module(domain)
        
        result = {"status": "error", "domain": domain.name, "task": task}
        
        if module:
            self.logger.info(f"🎯 路由: {task[:40]}... → {MODULE_MAP[domain][2]}")
            try:
                if hasattr(module, 'execute'):
                    module_result = module.execute(task=task, **params)
                elif hasattr(module, 'process'):
                    module_result = module.process(**params)
                else:
                    module_result = {"status": "ok", "data": "module loaded"}
                
                result = {
                    "status": "success",
                    "domain": domain.name,
                    "module": MODULE_MAP[domain][1],
                    "result": module_result,
                    "duration_ms": round((time.time() - t0) * 1000),
                }
                self.logger.info(f"  ✅ 完成 ({result['duration_ms']}ms)")
            except Exception as e:
                result["error"] = str(e)
                self.logger.error(f"  ❌ 执行失败: {e}")
        else:
            result["error"] = f"模块 {domain.name} 未加载"
            self.logger.warning(f"  ⚠️ 无可用模块: {domain.name}")
        
        # ═══ 记录调度历史 ═══
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task[:80],
            "domain": domain.name,
            "module": MODULE_MAP[domain][1],
            "duration_ms": result.get("duration_ms", 0),
            "status": result["status"],
        }
        self.dispatch_history.append(record)
        
        # ═══ 生成调度拓扑 ═══
        viz_mod = self._load_dispatch_viz()
        if viz_mod and hasattr(viz_mod, 'generate_topology'):
            try:
                viz_mod.generate_topology(
                    domain="art-agent",
                    active_bots=[MODULE_MAP[domain][1]],
                    task_description=task[:60],
                    metadata={"domain": domain.name, "status": result["status"]}
                )
            except: pass
        
        # ═══ 自进化学习 & 反馈闭环 ═══
        if self.evolution_agent:
            try:
                # 1. 记录本次调度
                self.evolution_agent.execute(
                    task="learn",
                    dispatch_record=record
                )
                # 2. 查询历史模式，优化下次路由
                scene = self._extract_scene(task)
                emotion = self._extract_emotion(task)
                if scene or emotion:
                    recommendation = self.evolution_agent.get_recommendation(
                        scene=scene or 'generic',
                        emotion=emotion or 'neutral'
                    )
                    if recommendation.get('recommended'):
                        self.logger.info(
                            f"  🧠 自进化推荐: {recommendation.get('masters',[])} "
                            f"(置信度{recommendation['confidence']}%)"
                        )
                        result['evolution_recommendation'] = recommendation
            except Exception as e:
                self.logger.warning(f"  ⚠️ 自进化异常: {e}")
        
        # ═══ 智能品牌匹配 ═══
        brand = self.smart_match_brand(task)
        self.logger.info(f"  🏷️ 匹配品牌风格: {brand}")
        result["matched_brand"] = brand
        
        return result
    
    def record_feedback(self, dispatch_id: str, feedback: str) -> Dict:
        """
        记录用户反馈，驱动自进化
        feedback: 'accept' | 'reject' | 'adjust'
        """
        if not self.evolution_agent:
            return {"status": "error", "message": "自进化系统未加载"}
        try:
            self.evolution_agent.record_dispatch({
                'input': dispatch_id,
                'feedback': feedback,
            })
            self.logger.info(f"  📝 反馈记录: {feedback}")
            return {"status": "ok", "feedback": feedback}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _extract_scene(self, task: str) -> str:
        """从任务描述中提取场景关键词"""
        scenes = ['coast', 'river', 'forest', 'mountain', 'desert', 
                  'city', 'lake', 'valley', 'highland', 'plain',
                  '海边', '海岸', '森林', '山地', '城市', '湖畔', 
                  '溪谷', '高原', '平原', '沙漠', '茶室', '庭院']
        for s in scenes:
            if s in task.lower():
                return {'海边': 'coast', '海岸': 'coast', '森林': 'forest', 
                        '山地': 'mountain', '城市': 'city', '湖畔': 'lake',
                        '溪谷': 'valley', '高原': 'highland', '平原': 'plain',
                        '沙漠': 'desert', '茶室': 'tea-house', '庭院': 'garden'
                       }.get(s, s)
        return ''
    
    def _extract_emotion(self, task: str) -> str:
        """从任务描述中提取情绪关键词"""
        emotions = ['焦虑', '疲惫', '独处', '冥想', '放松', '社交', '奢华',
                    '治愈', '宁静', '禅意', '放松', '疗愈']
        for e in emotions:
            if e in task:
                return {'焦虑': 'anxiety', '疲惫': 'tired', '独处': 'isolated',
                        '冥想': 'meditation', '放松': 'calm', '社交': 'social',
                        '奢华': 'luxury', '治愈': 'healing', '宁静': 'calm',
                        '禅意': 'zen', '疗愈': 'healing'}.get(e, e)
        return ''
    
    def get_stats(self) -> Dict:
        """获取调度统计"""
        total = len(self.dispatch_history)
        success = sum(1 for r in self.dispatch_history if r["status"] == "success")
        domains = {}
        for r in self.dispatch_history:
            d = r["domain"]
            domains[d] = domains.get(d, 0) + 1
        
        return {
            "total_dispatch": total,
            "success_rate": f"{success/total*100:.1f}%" if total else "0%",
            "domains": domains,
            "history": self.dispatch_history[-20:] if self.dispatch_history else [],
        }


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════


# 注入智能品牌匹配到 ArtDispatcher
ArtDispatcher.smart_match_brand = staticmethod(smart_match_brand)
if __name__ == "__main__":
    dispatcher = ArtDispatcher()
    print("\n" + "="*50)
    print("🎨 太一艺术 Agent 统一调度引擎 v3.0")
    print("="*50)
    
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        print(f"\n📋 任务: {task}")
        result = dispatcher.dispatch(task)
        print(f"📊 状态: {result['status']}")
        print(f"🎯 路由: {result['domain']} → {result.get('module','?')}")
        if 'duration_ms' in result:
            print(f"⏱ 耗时: {result['duration_ms']}ms")
    else:
        # 演示模式
        test_tasks = [
            "用星巴克风格美化咖啡店选址报告",
            "生成图表展示3个选址的对比数据",
            "设计品牌配色方案 北欧风格",
            "生成工作流拓扑图",
        ]
        for task in test_tasks:
            print(f"\n📋 {task}")
            r = dispatcher.dispatch(task)
            print(f"   → {r['domain']} | {r['status']} | {r.get('duration_ms',0)}ms")
        
        print("\n📊 调度统计:")
        stats = dispatcher.get_stats()
        print(f"   总调度: {stats['total_dispatch']}")
        print(f"   成功率: {stats['success_rate']}")
        print(f"   域分布: {stats['domains']}")
