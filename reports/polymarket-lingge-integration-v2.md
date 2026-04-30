# Polymarket LinggeTracer 集成方案 v2

> 版本：v2.0 (新 API Key)
> 执行：太一 AGI
> 时间：2026-03-30 12:24
> 截止：2026-03-30 23:59
> API Key: 019d2560-86f6-710d-ad87-57af5ad6b47e ✅

---

## 🎯 任务目标

集成 LinggeTracer 核心功能到知几-E 策略：
1. 大户钱包追踪
2. 交易行为分析
3. 隐藏 API 接入
4. 自动生成研报

---

## 📊 API 状态验证

### 新 API Key 测试

| 接口 | 状态 | 说明 |
|------|------|------|
| 账户接口 | ❌ 404 | 路径待确认 |
| 市场接口 | ✅ 200 | 可获取 50+ 市场 |
| API Key | ✅ 有效 | 2026-03-30 12:22 创建 |

### 可用功能

- ✅ 市场列表获取
- ✅ 公开数据访问
- 🔴 账户数据（需进一步调试）
- 🔴 下注功能（需钱包签名）

---

## 🔧 集成方案

### 1. 大户钱包追踪

```python
class WhaleTracker:
    """大户交易追踪器"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://gamma-api.polymarket.com"
        
        # 目标大户列表
        self.whales = [
            "0x2b45165959433831d9009716A15367421D6c97C9",  # SAYELFbot
            "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",  # SAYELF
            # 可添加更多大户地址
        ]
    
    def get_wallet_trades(self, wallet_address, limit=100):
        """获取钱包交易记录"""
        url = f"{self.base_url}/trades/{wallet_address}"
        params = {"limit": limit}
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()
    
    def analyze_wallet(self, wallet_address):
        """分析钱包行为"""
        trades = self.get_wallet_trades(wallet_address)
        
        analysis = {
            "total_trades": len(trades),
            "win_rate": self.calculate_win_rate(trades),
            "total_pnl": self.calculate_pnl(trades),
            "favorite_markets": self.get_favorite_markets(trades),
            "avg_position_size": self.get_avg_position(trades),
            "trading_frequency": self.get_frequency(trades),
        }
        
        return analysis
    
    def generate_report(self, wallet_address):
        """生成深度研报"""
        analysis = self.analyze_wallet(wallet_address)
        
        report = f"""
# 大户交易研报

**钱包地址**: {wallet_address}
**分析时间**: {datetime.now().isoformat()}

## 核心指标

| 指标 | 数值 |
|------|------|
| 总交易数 | {analysis['total_trades']} |
| 胜率 | {analysis['win_rate']:.1%} |
| 总盈亏 | ${analysis['total_pnl']:.2f} |
| 平均仓位 | ${analysis['avg_position_size']:.2f} |
| 交易频率 | {analysis['trading_frequency']} 笔/天 |

## 偏好市场

{self.format_markets(analysis['favorite_markets'])}

## 跟单建议

{self.generate_recommendations(analysis)}
        """
        
        return report
```

### 2. 市场数据采集（更新版）

```python
class PolymarketDataCollector:
    """数据采集器（使用新 API Key）"""
    
    def __init__(self):
        self.api_key = "019d2560-86f6-710d-ad87-57af5ad6b47e"
        self.db_path = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"
    
    def get_markets(self, category=None, limit=50):
        """获取市场列表"""
        url = "https://gamma-api.polymarket.com/events"
        params = {"limit": limit}
        if category:
            params["category"] = category
        
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    
    def get_market_details(self, market_id):
        """获取市场详情"""
        url = f"{self.base_url}/event/{market_id}"
        response = requests.get(url, timeout=30)
        return response.json()
    
    def collect_weather_markets(self):
        """采集气象市场"""
        keywords = ["temperature", "weather", "rain", "snow", "climate"]
        
        markets = self.get_markets(limit=200)
        weather_markets = []
        
        for market in markets:
            title = market.get("title", "").lower()
            if any(kw in title for kw in keywords):
                weather_markets.append(market)
        
        # 保存到数据库
        self.save_to_db(weather_markets)
        
        return weather_markets
    
    def save_to_db(self, markets):
        """保存到 SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for m in markets:
            cursor.execute("""
                INSERT OR REPLACE INTO market_odds
                (market_id, market_name, fetched_at)
                VALUES (?, ?, ?)
            """, (
                m.get("id"),
                m.get("title", "")[:200],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
```

### 3. 知几-E 策略集成

```python
class ZhijiEWithLingge:
    """知几-E + LinggeTracer 增强版"""
    
    def __init__(self):
        self.whale_tracker = WhaleTracker(API_KEY)
        self.data_collector = PolymarketDataCollector()
        self.base_strategy = ZhijiE_v21()
    
    def enhanced_signal(self, market_id):
        """增强版交易信号"""
        # 基础信号
        base_signal = self.base_strategy.generate_signal(market_id)
        
        # 大户行为分析
        whale_activity = self.analyze_whale_activity(market_id)
        
        # 融合信号
        if base_signal and whale_activity['whale_buying']:
            base_signal['confidence'] *= 1.1  # 大户买入，提升置信度
        
        return base_signal
    
    def analyze_whale_activity(self, market_id):
        """分析大户在该市场的活动"""
        activity = {
            'whale_buying': False,
            'whale_selling': False,
            'net_whale_flow': 0,
        }
        
        # 获取大户交易
        for whale in self.whale_tracker.whales:
            trades = self.whale_tracker.get_wallet_trades(whale)
            
            for trade in trades:
                if trade.get('market_id') == market_id:
                    if trade.get('side') == 'BUY':
                        activity['whale_buying'] = True
                        activity['net_whale_flow'] += trade.get('size', 0)
                    else:
                        activity['whale_selling'] = True
                        activity['net_whale_flow'] -= trade.get('size', 0)
        
        return activity
```

---

## 📁 交付文件

### 核心脚本

```
scripts/
├── polymarket-whale-tracker.py     # 大户追踪
├── polymarket-data-collector-v2.py # 数据采集 v2
├── polymarket-report-generator.py  # 研报生成
└── zhiji-e-lingge-integration.py   # 知几-E 集成
```

### 配置文件

```
config/
├── polymarket-api.json             # API 配置（新 Key）
├── whale-list.json                 # 大户地址列表
└── report-templates.yaml           # 研报模板
```

### 数据目录

```
polymarket-data/
├── polymarket.db                   # SQLite 数据库
├── whale-scans/                    # 大户扫描记录
└── reports/                        # 生成的研报
```

---

## 🚀 执行步骤

### 步骤 1: 更新 API 配置（已完成 ✅）

```bash
# API Key 已保存到：
# - /home/nicola/.taiyi/accounts/polymarket.json
# - /home/nicola/.openclaw/.env.polymarket
```

### 步骤 2: 创建大户追踪脚本（5 分钟）

```bash
cat > scripts/polymarket-whale-tracker.py << 'EOF'
# （上述代码）
EOF
```

### 步骤 3: 测试数据采集（5 分钟）

```bash
python3 scripts/polymarket-data-collector-v2.py
```

### 步骤 4: 生成首份研报（2 分钟）

```bash
python3 scripts/polymarket-report-generator.py \
  --wallet 0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf \
  --output reports/whale-analysis-sayelf.md
```

---

## 📊 验收标准

| 功能 | 验收标准 | 状态 |
|------|---------|------|
| API 连接 | 新 Key 验证通过 | ✅ |
| 市场采集 | 获取≥10 个气象市场 | 🟡 |
| 大户追踪 | 获取交易记录 | 🟡 |
| 研报生成 | 自动生成 Markdown 报告 | 🟡 |
| 策略集成 | 知几-E 融合大户信号 | 🟡 |

---

## 🎯 下一步行动

### P0（今日完成）
- [ ] 测试新 API Key 完整功能
- [ ] 创建大户追踪脚本
- [ ] 生成首份大户研报

### P1（本周完成）
- [ ] 集成到知几-E 策略
- [ ] 实盘测试（充值后）
- [ ] 监控调优

---

## 📞 快速命令

```bash
# 测试 API 连接
python3 scripts/polymarket-test-api.py

# 采集市场数据
python3 scripts/polymarket-data-collector-v2.py

# 追踪大户钱包
python3 scripts/polymarket-whale-tracker.py --wallet <address>

# 生成研报
python3 scripts/polymarket-report-generator.py --wallet <address>
```

---

*版本：v2.0 (新 API Key)*
*创建：2026-03-30 12:24*
*太一 AGI · Polymarket LinggeTracer 集成方案*
