# 太一统管 GMGN × Polymarket 架构文档

> 版本：v1.0 | 创建：2026-03-27 21:18 | 太一主导 · 全 Bot 协同

---

## 🎯 系统架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    太一 (Taiyi) 统管层                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              决策引擎 (Decision Engine)              │   │
│  │  • 资金分配决策  • 风险控制  • 策略调度  • 收益统计  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────────┐                     ┌───────────────────┐
│    GMGN 线        │                     │  Polymarket 线    │
│  (链上交易)       │                     │  (预测市场)       │
├───────────────────┤                     ├───────────────────┤
│ 猎手·聪明钱       │                     │ 知几·气象套利     │
│ 天机·数据追踪     │                     │ 猎手·聪明钱跟随   │
│ 罔两·新币调研     │                     │ 罔两·事件调研     │
└───────────────────┘                     └───────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              ↓
                    ┌───────────────────┐
                    │   管家·用户管理    │
                    │   • 收益统计       │
                    │   • 报表生成       │
                    │   • 提现管理       │
                    └───────────────────┘
```

---

## 📊 Bot 职责详细分工

### 太一 (Taiyi) - 统管层

| 职责 | 说明 | 频率 |
|------|------|------|
| **资金分配** | GMGN 60% / Poly 40% 动态调整 | 每日 |
| **风险控制** | 监控止损/止盈/回撤 | 实时 |
| **策略调度** | 启用/禁用策略 | 按需 |
| **收益统计** | 汇总双平台收益 | 每日 |
| **最终决策** | 重大调整决策 | 按需 |

**核心代码**:
```python
class TaiyiController:
    def __init__(self):
        self.gmgn_allocation = 0.60  # 60%
        self.poly_allocation = 0.40  # 40%
        self.total_capital = 5000
    
    def rebalance(self):
        """再平衡逻辑"""
        gmgn_value = self.get_gmgn_value()
        poly_value = self.get_poly_value()
        total = gmgn_value + poly_value
        
        # 计算偏离度
        gmgn_ratio = gmgn_value / total
        deviation = abs(gmgn_ratio - self.gmgn_allocation)
        
        # 偏离>20% 触发再平衡
        if deviation > 0.20:
            self.execute_rebalance()
    
    def risk_check(self):
        """风险控制检查"""
        daily_loss = self.get_daily_loss()
        if daily_loss < -0.10:  # -10%
            self.emergency_stop()  # 紧急停止
```

---

### 猎手 (Hunter) - GMGN 线

| 职责 | 说明 | 频率 |
|------|------|------|
| **聪明钱筛选** | 筛选胜率>70% 钱包 | 每周 |
| **跟单配置** | GMGN 跟单参数设置 | 每周 |
| **信号推送** | 高置信度信号发现 | 实时 |
| **表现监控** | 钱包胜率/盈亏跟踪 | 每日 |

**核心代码**:
```python
class HunterGMGN:
    def __init__(self):
        self.wallets = []
        self.min_win_rate = 0.70
    
    def scan_smart_money(self):
        """扫描聪明钱"""
        wallets = gmgn_api.get_top_traders(limit=100)
        qualified = [w for w in wallets if w['win_rate'] > self.min_win_rate]
        return qualified[:10]  # 返回前 10 个
    
    def configure_copy_trading(self, wallets):
        """配置跟单"""
        for wallet in wallets:
            gmgn_api.set_copy_trading(
                address=wallet['address'],
                amount=wallet['allocation'],
                stop_loss=wallet['stop_loss'],
                take_profit=wallet['take_profit']
            )
```

---

### 天机 (Tianji) - 数据追踪

| 职责 | 说明 | 频率 |
|------|------|------|
| **数据采集** | Polymarket/GMGN 数据 | 实时 |
| **聪明钱监控** | 50+ 钱包交易追踪 | 实时 |
| **数据分析** | 胜率/回报/回撤计算 | 每日 |
| **报表生成** | 数据可视化报表 | 每周 |

**核心代码**:
```python
class TianjiSystem:
    def __init__(self):
        self.poly_api = PolymarketAPI()
        self.gmgn_api = GMGNAPI()
    
    def collect_data(self):
        """数据采集"""
        poly_data = self.poly_api.get_recent_trades()
        gmgn_data = self.gmgn_api.get_whale_trades()
        return {'polymarket': poly_data, 'gmgn': gmgn_data}
    
    def analyze_performance(self):
        """表现分析"""
        data = self.collect_data()
        stats = {
            'win_rate': self.calc_win_rate(data),
            'pnl': self.calc_pnl(data),
            'max_drawdown': self.calc_max_dd(data)
        }
        return stats
```

---

### 知几 (Zhiji) - Polymarket 线

| 职责 | 说明 | 频率 |
|------|------|------|
| **气象套利** | 知几-E v5.0 执行 | 实时 |
| **置信度计算** | 贝叶斯更新 + 凯利公式 | 实时 |
| **下注执行** | Polymarket API 下单 | 实时 |
| **策略优化** | 参数调整优化 | 每周 |

**核心代码**:
```python
class ZhijiEPoly:
    def __init__(self):
        self.confidence_threshold = 0.96
        self.edge_threshold = 0.02
        self.kelly_multiplier = 0.25  # Quarter-Kelly
    
    def calculate_position(self, confidence, odds):
        """凯利公式计算仓位"""
        p = confidence
        q = 1 - p
        b = (1 / odds) - 1
        kelly = (b * p - q) / b
        return max(0, kelly * self.kelly_multiplier)
    
    def execute_bet(self, market, direction, amount):
        """执行下注"""
        polymarket_api.place_order(
            market=market,
            direction=direction,
            amount=amount
        )
```

---

### 罔两 (Wangliang) - 调研支持

| 职责 | 说明 | 频率 |
|------|------|------|
| **新币调研** | GMGN 新币分析 | 每日 |
| **事件调研** | Polymarket 事件分析 | 每日 |
| **竞品分析** | 市场趋势分析 | 每周 |
| **机会发现** | 套利机会识别 | 实时 |

**核心代码**:
```python
class WangliangResearch:
    def scan_new_coins(self):
        """扫描新币"""
        new_coins = gmgn_api.get_new_listings(hours=24)
        analyzed = []
        for coin in new_coins:
            risk = self.analyze_risk(coin)
            if risk['score'] > 70:  # 安全分>70
                analyzed.append(coin)
        return analyzed
    
    def scan_events(self):
        """扫描事件"""
        events = polymarket_api.get_trending_events()
        opportunities = []
        for event in events:
            arb = self.calc_arbitrage(event)
            if arb['edge'] > 0.05:  # 价差>5%
                opportunities.append(event)
        return opportunities
```

---

### 管家 (Steward) - 用户管理

| 职责 | 说明 | 频率 |
|------|------|------|
| **收益统计** | 双平台收益汇总 | 每日 |
| **报表生成** | 日报/周报/月报 | 定期 |
| **提现管理** | 盈利提现执行 | 每周 |
| **用户通知** | Telegram 推送通知 | 实时 |

**核心代码**:
```python
class StewardManager:
    def generate_daily_report(self):
        """生成日报"""
        gmgn_pnl = self.get_gmgn_pnl()
        poly_pnl = self.get_poly_pnl()
        total = gmgn_pnl + poly_pnl
        
        report = f"""
【双平台日报 · {today}】
GMGN: ${gmgn_pnl}
Polymarket: ${poly_pnl}
总计：${total}
        """
        return report
    
    def withdraw_profit(self, ratio=0.50):
        """提现盈利"""
        total_profit = self.get_total_profit()
        withdraw_amount = total_profit * ratio
        
        gmgn_api.withdraw(withdraw_amount * 0.60)
        poly_api.withdraw(withdraw_amount * 0.40)
```

---

## 🔧 具体实现步骤

### Step 1: 太一控制器部署

**文件**: `skills/taiyi/controller.py`

```python
#!/usr/bin/env python3
# 太一统管控制器

from skills.hunter.gmgn import HunterGMGN
from skills.zhiji.poly import ZhijiEPoly
from skills.wangliang.research import WangliangResearch
from skills.steward.manager import StewardManager

class TaiyiController:
    def __init__(self):
        self.hunter = HunterGMGN()
        self.zhiji = ZhijiEPoly()
        self.wangliang = WangliangResearch()
        self.steward = StewardManager()
        
        self.gmgn_allocation = 0.60
        self.poly_allocation = 0.40
        self.total_capital = 5000
    
    def start(self):
        """启动统管系统"""
        print("🚀 太一统管系统启动...")
        
        # 初始化各 Bot
        self.hunter.init()
        self.zhiji.init()
        self.wangliang.init()
        self.steward.init()
        
        # 启动监控循环
        while True:
            self.monitor_loop()
            time.sleep(60)  # 每分钟检查
    
    def monitor_loop(self):
        """监控循环"""
        # 风险控制
        self.risk_check()
        
        # 再平衡检查
        self.rebalance_check()
        
        # 收益统计
        self.steward.update_stats()
```

**部署命令**:
```bash
cd ~/.openclaw/workspace/skills/taiyi
python3 controller.py &
```

---

### Step 2: GMGN 线配置

**文件**: `skills/hunter/gmgn_config.yaml`

```yaml
gmgn:
  enabled: true
  api_key: "待配置"
  api_secret: "待配置"
  
  # 聪明钱跟单
  copy_trading:
    enabled: true
    wallets:
      - address: "ColdMath"
        allocation: 0.20  # 20%
        stop_loss: -0.15
        take_profit: 1.50
      - address: "majorexploiter"
        allocation: 0.20
        stop_loss: -0.15
        take_profit: 1.50
      # ... 共 10 钱包
  
  # 新币狙击
  sniper:
    enabled: true
    amount: 1.0  # SOL
    gas_priority: "high"
    slippage: 0.20
    anti_mev: true
  
  # 条件单
  condition_order:
    enabled: true
    buy_conditions:
      - market_cap < 500000
      - liquidity > 1000000
    sell_conditions:
      - 2x: sell 50%
      - 5x: sell 30%
      - 10x: sell 100%
```

**部署命令**:
```bash
cd ~/.openclaw/workspace/skills/hunter
python3 gmgn_bot.py &
```

---

### Step 3: Polymarket 线配置

**文件**: `skills/zhiji/poly_config.yaml`

```yaml
polymarket:
  enabled: true
  wallet: "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf"
  
  # 气象套利
  weather_arbitrage:
    enabled: true
    confidence_threshold: 0.96
    edge_threshold: 0.02
    kelly_multiplier: 0.25  # Quarter-Kelly
    max_position: 0.25  # 25%
  
  # 聪明钱跟随
  whale_following:
    enabled: true
    wallets:
      - name: "ColdMath"
        allocation: 0.20
      - name: "majorexploiter"
        allocation: 0.15
  
  # 事件套利
  event_arbitrage:
    enabled: true
    min_edge: 0.05  # 5% 价差
    max_position: 0.10  # 10%
```

**部署命令**:
```bash
cd ~/.openclaw/workspace/skills/zhiji
python3 poly_bot.py &
```

---

### Step 4: 管家报表系统

**文件**: `skills/steward/report.py`

```python
#!/usr/bin/env python3
# 管家报表系统

class ReportGenerator:
    def generate_daily(self):
        """日报"""
        gmgn_pnl = self.get_gmgn_pnl()
        poly_pnl = self.get_poly_pnl()
        
        report = f"""
【双平台日报 · {datetime.now().strftime('%Y-%m-%d')}】

┌────────────┬───────┬───────┬─────────┐
│ 平台       │ 本金  │ 盈亏  │ 回报率  │
├────────────┼───────┼───────┼─────────┤
│ GMGN       │ $3000 │ ${gmgn_pnl}  │ {gmgn_pnl/30:.1f}% │
│ Polymarket │ $2000 │ ${poly_pnl}  │ {poly_pnl/20:.1f}% │
└────────────┴───────┴───────┴─────────┘

总计：${gmgn_pnl + poly_pnl}
        """
        return report
    
    def generate_weekly(self):
        """周报"""
        # 类似日报，汇总 7 天数据
        pass
    
    def generate_monthly(self):
        """月报"""
        # 汇总 30 天数据
        pass
```

**部署命令**:
```bash
cd ~/.openclaw/workspace/skills/steward
python3 report.py --schedule daily &
```

---

## 📊 数据流架构

```
┌─────────────────┐
│  外部数据源      │
│  • GMGN API     │
│  • Poly API     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  天机数据采集    │
│  • 实时爬取      │
│  • 数据清洗      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  太一决策引擎    │
│  • 数据分析      │
│  • 策略决策      │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌──────┐  ┌──────┐
│GMGN  │  │ Poly │
│执行  │  │ 执行 │
└──────┘  └──────┘
    │         │
    └────┬────┘
         │
         ↓
┌─────────────────┐
│  管家报表系统    │
│  • 收益统计      │
│  • 通知推送      │
└─────────────────┘
```

---

## 🚀 完整部署脚本

**文件**: `scripts/deploy-dual-platform.sh`

```bash
#!/bin/bash
# 双平台系统部署脚本

echo "🚀 太一统管双平台系统部署..."

# 1. 启动太一控制器
echo "📊 启动太一控制器..."
cd ~/.openclaw/workspace/skills/taiyi
nohup python3 controller.py > /tmp/taiyi.log 2>&1 &

# 2. 启动 GMGN 线
echo "🎯 启动 GMGN 线..."
cd ~/.openclaw/workspace/skills/hunter
nohup python3 gmgn_bot.py > /tmp/gmgn.log 2>&1 &

# 3. 启动 Polymarket 线
echo "🎲 启动 Polymarket 线..."
cd ~/.openclaw/workspace/skills/zhiji
nohup python3 poly_bot.py > /tmp/poly.log 2>&1 &

# 4. 启动管家报表
echo "📝 启动管家报表..."
cd ~/.openclaw/workspace/skills/steward
nohup python3 report.py --schedule daily > /tmp/steward.log 2>&1 &

# 5. 检查状态
sleep 5
echo ""
echo "✅ 部署完成！检查状态..."
ps aux | grep -E "(controller|gmgn_bot|poly_bot|report)" | grep -v grep

echo ""
echo "📊 系统已启动！"
echo "  太一控制器：http://localhost:8000"
echo "  GMGN 日志：/tmp/gmgn.log"
echo "  Polymarket 日志：/tmp/poly.log"
echo "  管家报表：/tmp/steward.log"
```

**执行部署**:
```bash
chmod +x /home/nicola/.openclaw/workspace/scripts/deploy-dual-platform.sh
bash /home/nicola/.openclaw/workspace/scripts/deploy-dual-platform.sh
```

---

## 📋 执行清单

### Day 1 (今日)

**部署阶段**:
- [ ] 创建太一控制器 (`skills/taiyi/controller.py`)
- [ ] 配置 GMGN 线 (`skills/hunter/gmgn_config.yaml`)
- [ ] 配置 Polymarket 线 (`skills/zhiji/poly_config.yaml`)
- [ ] 运行部署脚本 (`scripts/deploy-dual-platform.sh`)
- [ ] 测试小额交易 (GMGN $10 + Poly $10)

### Day 2-3

**监控阶段**:
- [ ] 检查各 Bot 运行状态
- [ ] 确认数据流正常
- [ ] 确认收益统计准确
- [ ] 调整异常参数

### Week 1

**优化阶段**:
- [ ] 生成第 1 份周报
- [ ] 分析收益数据
- [ ] 优化策略参数
- [ ] 提现 50% 利润 (如盈利>50%)

---

## 📞 Bot 通信协议

**太一 → 猎手**:
```json
{
  "command": "update_wallets",
  "wallets": [
    {"address": "ColdMath", "allocation": 0.20}
  ]
}
```

**猎手 → 太一**:
```json
{
  "status": "success",
  "pnl": 150,
  "win_rate": 0.78
}
```

**太一 → 知几**:
```json
{
  "command": "place_bet",
  "market": "BTC_100K_2026",
  "direction": "YES",
  "amount": 100
}
```

**知几 → 太一**:
```json
{
  "status": "filled",
  "price": 0.52,
  "shares": 192
}
```

---

*版本：v1.0 | 创建时间：2026-03-27 21:18*
*状态：✅ 待部署*
