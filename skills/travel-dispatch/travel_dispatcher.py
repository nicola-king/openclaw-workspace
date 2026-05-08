#!/usr/bin/env python3
"""
travel-dispatcher v1.0.0
太一旅游探路者 · 自动调度引擎

职责:
  1. 解析用户自然语言旅行意图
  2. 自动分派到对应 Bot 的核心模块
  3. 单域直接派 / 跨域拆解并行
  4. 聚合结果 → 交付
"""

import sys, json, logging, re, os, subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

sys.path.insert(0, str(Path(__file__).parent))
from travel_formatter import TravelFormatter

logger = logging.getLogger("travel-dispatcher")

# ── 路径 ──
SKILL_DIR = Path(__file__).parent
DOMESTIC_DIR = SKILL_DIR.parent / "domestic-travel-agent"
INTL_DIR = SKILL_DIR.parent / "international-travel-agent"


# ════════════════════════════════════════════════════════
# 意图解析
# ════════════════════════════════════════════════════════

@dataclass
class TravelIntent:
    raw: str
    is_domestic: bool = True
    scenario: str = "short"     # short/deep/group
    mode: str = "selected"      # selected/daily/all
    city: str = ""
    city_en: str = ""
    days: int = 3
    budget: Optional[int] = None
    members: int = 1
    preferences: str = "综合"
    category: Optional[str] = None
    bots_needed: List[str] = field(default_factory=list)


class IntentParser:
    CITIES_CN = {"北京":"beijing","上海":"shanghai","成都":"chengdu","重庆":"chongqing",
                 "三亚":"sanya","杭州":"hangzhou","广州":"guangzhou","深圳":"shenzhen",
                 "西安":"xian","昆明":"kunming","大理":"dali","南京":"nanjing","厦门":"xiamen"}
    CITIES_INTL = {"东京":"tokyo","大阪":"osaka","曼谷":"bangkok","普吉":"phuket",
                   "首尔":"seoul","新加坡":"singapore","吉隆坡":"kuala_lumpur",
                   "纽约":"new_york","洛杉矶":"los_angeles","伦敦":"london","巴黎":"paris",
                   "罗马":"rome","悉尼":"sydney","奥克兰":"auckland"}

    BOT_MAP = {
        "知几": {"kw": ["数据","分析","评分","性价比","什么时候","对比","评分"], "role": "数据分析"},
        "山木": {"kw": ["规划","安排","行程","攻略","路线","计划","做"], "role": "业务执行"},
        "素问": {"kw": ["签证","文化","风俗","天气","安全","使领馆","法律","研究"], "role": "技术研究"},
        "罔两": {"kw": ["推荐","评价","好吃","好玩","博主","口碑","酒店","景点","餐厅"], "role": "市场情报"},
        "庖丁": {"kw": ["多少钱","预算","穷游","划算","成本","费用","花费"], "role": "财务管控"},
    }

    @classmethod
    def parse(cls, text: str) -> TravelIntent:
        t = text.lower()
        intent = TravelIntent(raw=text)

        # 国内/国际 — 先检查国际城市名和英文名
        for cn, en in cls.CITIES_INTL.items():
            if cn in text or en in t:
                intent.is_domestic = False
                intent.city = cn
                intent.city_en = en
                break
        if not intent.city:
            for cn, en in cls.CITIES_CN.items():
                if cn in text or en in t:
                    intent.city = cn
                    intent.city_en = en
                    break

        # 天数
        nums = re.findall(r'(\d+)\s*[天日]', text)
        if nums: intent.days = int(nums[0])

        # 场景
        if any(kw in t for kw in ["深度","沉浸","慢慢","7天","一周"]): intent.scenario = "deep"
        elif any(kw in t for kw in ["团体","团队","家庭","全家","团建"]): intent.scenario = "group"

        # 预算
        budgets = re.findall(r'(\d+)\s*[万千]?\s*[元块]', text)
        if budgets: intent.budget = int(budgets[0])

        # 模式
        if any(kw in t for kw in ["推荐","精华","必去","必吃"]): intent.mode = "selected"
        elif any(kw in t for kw in ["行程","攻略","规划","安排","路线"]): intent.mode = "daily"
        elif any(kw in t for kw in ["全部","所有","全量"]): intent.mode = "all"
        else: intent.mode = "selected"

        # 分类
        if any(kw in t for kw in ["酒店","住宿","住"]): intent.category = "hotels"
        elif any(kw in t for kw in ["吃","餐厅","餐馆","美食","饭店"]): intent.category = "restaurants"
        elif any(kw in t for kw in ["景点","玩","景区","打卡"]): intent.category = "attractions"

        # 偏好
        if any(kw in t for kw in ["历史","古迹"]): intent.preferences = "历史"
        elif any(kw in t for kw in ["自然","山水","户外"]): intent.preferences = "自然"
        elif any(kw in t for kw in ["美食","吃"]): intent.preferences = "美食"

        # Bot 路由
        bots = set()
        if intent.mode == "daily":
            bots.add("山木")
        for bot_name, spec in cls.BOT_MAP.items():
            if any(kw in t for kw in spec["kw"]):
                bots.add(bot_name)
        if not bots:
            if intent.mode == "daily":
                bots = {"山木", "素问"}
            else:
                bots = {"罔两", "知几"}
        intent.bots_needed = list(bots)
        return intent


# ════════════════════════════════════════════════════════
# 调度器
# ════════════════════════════════════════════════════════

class TravelDispatcher:
    def __init__(self):
        self.parser = IntentParser()
        self.dispatch_history = []

    def dispatch(self, text: str, params: dict = None) -> Dict[str, Any]:
        t0 = __import__("time").time()
        intent = self.parser.parse(text)
        params = params or {}

        # 参数覆盖
        for k in ["city", "days", "mode", "budget", "preferences"]:
            if k in params:
                setattr(intent, k, params[k])

        if not intent.city:
            return {"status": "error", "error": "未识别到目的地城市",
                    "suggestion": "请告诉我你想去的城市，比如「北京」「东京」"}

        logger.info(f"🎯 {intent.raw[:40]}... → {intent.city} {intent.days}d mode={intent.mode} Bot={intent.bots_needed}")

        # 通过子进程调用 router 获取数据
        result = self._call_router(intent)

        # 格式化输出（人话）
        formatted = TravelFormatter.format_full(result)
        result["formatted"] = formatted

        result["_dispatch"] = {
            "bots_involved": intent.bots_needed,
            "duration_ms": round((__import__("time").time() - t0) * 1000),
            "intent": {
                "city": intent.city, "days": intent.days,
                "mode": intent.mode, "scenario": intent.scenario,
                "category": intent.category,
            }
        }

        record = {"timestamp": datetime.now().isoformat(), "raw": intent.raw[:60],
                  "mode": intent.mode, "bots": intent.bots_needed,
                  "duration_ms": result["_dispatch"]["duration_ms"]}
        self.dispatch_history.append(record)

        return result

    def _call_router(self, intent: TravelIntent) -> Dict[str, Any]:
        """通过子进程调用三层路由（国内/国际自动识别）"""
        if intent.is_domestic:
            router_script = str(DOMESTIC_DIR / "core" / "travel_router.py")
        else:
            router_script = str(INTL_DIR / "core" / "travel_router.py")

        if not os.path.exists(router_script):
            return self._mock_data(intent)

        # 构建查询参数，通过 CLI 传入
        cmd = [
            sys.executable, router_script,
            "--mode", intent.mode,
            "--city", intent.city_en or intent.city,
            "--days", str(intent.days),
        ]
        if intent.budget:
            cmd += ["--budget", str(intent.budget)]
        if intent.category:
            cmd += ["--category", intent.category]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
        except Exception as e:
            logger.warning(f"router 调用失败: {e}")

        return self._mock_data(intent)

    def _mock_data(self, intent: TravelIntent) -> Dict[str, Any]:
        """降级：返回 mock 数据"""
        city = intent.city
        city_en = intent.city_en or city
        days = intent.days
        tip_zh = "确认签证有效期" if not intent.is_domestic else "带好身份证"
        tip_extra = "购买旅行保险" if not intent.is_domestic else "提前预订门票"

        if intent.mode == "daily":
            itinerary = []
            for d in range(1, days + 1):
                itinerary.append({
                    "day": d,
                    "date": (datetime.now() + timedelta(days=d - 1)).strftime("%Y-%m-%d"),
                    "schedule": [
                        {"time": "09:00-12:00", "activity": f"{city}上午景点", "cost": 60},
                        {"time": "12:00-13:30", "activity": "午餐", "cost": 80},
                        {"time": "14:00-17:00", "activity": f"{city}下午景点", "cost": 50},
                        {"time": "18:30-20:00", "activity": "晚餐", "cost": 100},
                    ],
                    "daily_budget": round((intent.budget or 3000) / days, 2),
                })
            return {"mode": "daily", "city": city, "days": days, "itinerary": itinerary,
                    "total_budget": intent.budget or 3000,
                    "tips": [tip_zh, tip_extra]}
        else:
            return {"mode": intent.mode, "city": city, "sections": [
                {"label": "精选景点", "items": [
                    {"name": f"{city}景点1", "rating": 4.8, "price": "免费"},
                    {"name": f"{city}景点2", "rating": 4.7, "price": "50元"},
                ], "count": 2},
                {"label": "必吃餐厅", "items": [
                    {"name": f"{city}必吃1", "rating": 4.6, "price": "人均100"},
                ], "count": 1},
            ], "total": 3}

    def get_stats(self) -> Dict[str, Any]:
        return {"total_dispatch": len(self.dispatch_history),
                "history": self.dispatch_history[-20:]}


# ════════════════════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dispatcher = TravelDispatcher()

    print("\n" + "=" * 50)
    print("🧭 太一旅游探路者 · 自动调度引擎")
    print("=" * 50)

    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        print(f"\n📋 任务: {task}")
        result = dispatcher.dispatch(task)
        d = result.get("_dispatch", {})
        print(f"  模式: {d.get('intent',{}).get('mode','?')}")
        print(f"  Bot: {d.get('bots_involved',[])}")
        print(f"  耗时: {d.get('duration_ms',0)}ms")
        print(f"  结果: {json.dumps(result, indent=2, ensure_ascii=False)[:300]}...")
    else:
        test_tasks = [
            "去成都玩3天",
            "东京7天深度游要多少钱",
            "北京有什么好吃的推荐",
            "全家去三亚玩5天",
            "曼谷签证怎么办",
        ]
        for task in test_tasks:
            r = dispatcher.dispatch(task)
            d = r.get("_dispatch", {})
            print(f"  {task[:20]:20s} → "
                  f"城市={d['intent']['city']} "
                  f"mode={d['intent']['mode']} "
                  f"Bot={','.join(d['bots_involved']):10s} "
                  f"{d['duration_ms']}ms")

        print(f"\n📊 调度统计: {dispatcher.get_stats()['total_dispatch']} 次")
