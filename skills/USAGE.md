# 技能使用手册

> **版本**: 2.0 | **更新**: 2026-04-07 08:45

---

## 🎯 技能调用方式

### 1. 直接导入

```python
from skills.browser_automation import BrowserAutomation
from skills.gmgn import GMGN
from skills.content_creator import ContentCreator
from skills.visual_designer import VisualDesigner

# 使用
ba = BrowserAutomation()
gmgn = GMGN()
cc = ContentCreator()
vd = VisualDesigner()
```

### 2. 智能路由

```python
from skills.smart_router import SmartRouter

router = SmartRouter()

# 自动选择技能
skill_name = router.route("帮我分析市场数据")
# 返回：'gmgn' 或 'trading'

# 执行
result = router.execute(skill_name, task_params)
```

### 3. 共享层

```python
from skills.shared import SharedDatabase, EventBus, Events

# 数据库
db = SharedDatabase.get_instance()
db.record_action('user_login', {'user': 'test'})

# 事件总线
event_bus = EventBus.get_instance()
event_bus.publish(Events.TASK_COMPLETED, {'task': 'analysis'})

# 缓存
cache = db.get_cache()
cache.set('key', 'value', ttl=3600)
```

---

## 📋 核心技能 API

### browser-automation

```python
from skills.browser_automation.core.browser_automation import BrowserAutomation

ba = BrowserAutomation(headless=True)
await ba.start()

# 导航
await ba.open('https://example.com')

# 交互
await ba.click('#button')
await ba.fill('#input', 'text')

# 截图
await ba.screenshot('output.png')

# 数据采集
content = await ba.get_text('.article')

await ba.close()
```

**平台适配器**:
```python
from skills.browser_automation.adapters.polymarket_adapter import PolymarketAdapter

adapter = PolymarketAdapter(ba)
await adapter.login()
await adapter.place_bet('market_id', 'outcome', amount)
```

### gmgn

```python
from skills.gmgn import GMGN

gmgn = GMGN(api_key='YOUR_API_KEY')
gmgn.set_chain('sol')  # sol | bsc | base | eth | ton

# 市场数据
trending = await gmgn.market.get_trending()
kline = await gmgn.market.get_kline('TOKEN_ADDRESS', '1h')

# 钱包组合
holdings = await gmgn.portfolio.get_holdings('WALLET_ADDRESS')
transactions = await gmgn.portfolio.get_transactions('WALLET_ADDRESS')

# 代币信息
info = await gmgn.token.get_info('TOKEN_ADDRESS')
security = await gmgn.token.get_security('TOKEN_ADDRESS')

# 链上追踪
smart_money = await gmgn.track.get_smart_money_trades()
kol_trades = await gmgn.track.get_kol_trades()

# ⚠️ 交易执行 (需要确认)
swap_result = await gmgn.swap.execute(
    from_token='SOL',
    to_token='TOKEN_ADDRESS',
    amount=1.0,
    slippage=0.5
)
```

### content-creator

```python
from skills.content_creator import ContentCreator

cc = ContentCreator()

# 排期
cc.scheduler.add_task(
    platform='xiaohongshu',
    content_type='note',
    scheduled_time='2026-04-07 21:00',
    content={'title': '...', 'body': '...'}
)

# 优化
titles = await cc.optimizer.generate_viral_titles('AI 工具')
seo_content = await cc.optimizer.geo_optimize('文章內容', keywords=['AI', '工具'])

# 发布
result = await cc.publisher.publish(
    platform='wechat',
    title='标题',
    content='内容',
    images=['image1.png', 'image2.png']
)

# 生成
article = await cc.generator.create_article(
    topic='AI 发展趋势',
    style='professional',
    length=2000
)
```

### visual-designer

```python
from skills.visual_designer import VisualDesigner

vd = VisualDesigner()

# 图表
chart_path = await vd.charts.create_bar_chart(
    data={'A': 10, 'B': 20, 'C': 15},
    title='销售数据',
    output='chart.png'
)

# 信息卡片
card_path = await vd.cards.create_info_card(
    content='重要信息',
    style='magazine',  # magazine | minimal | tech
    output='card.png'
)

# 艺术生成
ascii_art = await vd.art.text_to_ascii('Hello', font='standard')
image = await vd.art.generate_image('prompt', style='artistic')
```

### cli-toolkit

```python
from skills.cli_toolkit import CLIToolkit

cli = CLIToolkit()

# AWS
await cli.aws.run_command('s3 ls')
await cli.aws.deploy_stack('stack-name', 'template.yaml')

# Docker
await cli.docker.run_container('nginx:latest', ports={'80': '8080'})
await cli.docker.build_image('./', 'myimage:latest')

# Kubernetes
await cli.k8s.deploy('deployment.yaml')
await cli.k8s.get_pods('default')

# Git
await cli.git.commit('feat: add new feature')
await cli.git.push('origin', 'main')
```

### monitoring

```python
from skills.monitoring import Monitoring

monitor = Monitoring()

# API 监控
status = await monitor.check_api('https://api.example.com/health')

# 自检
report = await monitor.self_check()

# 告警
await monitor.send_alert(
    level='critical',
    message='Service down',
    channel='slack'
)
```

### trading

```python
from skills.trading import Trading

trading = Trading()

# 币安
await trading.binance.set_api_key('KEY', 'SECRET')
balance = await trading.binance.get_balance()
order = await trading.binance.place_order('BTCUSDT', 'BUY', 0.001, price=50000)

# Polymarket
await trading.polymarket.login()
position = await trading.polymarket.get_position('market_id')
```

---

## 🔌 与 Bot 集成

### 太一 (总管)

```python
# 太一自动路由任务
from skills.smart_router import SmartRouter

router = SmartRouter()
result = router.route_and_execute(user_request)
```

### 知几 (交易)

```python
from skills.gmgn import GMGN
from skills.trading import Trading
from skills.zhiji import Zhiji

gmgn = GMGN()
trading = Trading()
zhiji = Zhiji()

# 策略执行
signal = await zhiji.generate_signal('BTCUSDT')
if signal.action == 'BUY':
    await trading.binance.place_order(
        symbol='BTCUSDT',
        side='BUY',
        quantity=signal.quantity
    )
```

### 山木 (内容)

```python
from skills.content_creator import ContentCreator
from skills.visual_designer import VisualDesigner
from skills.shanmu import Shanmu

cc = ContentCreator()
vd = VisualDesigner()
shanmu = Shanmu()

# 内容创作流程
content = await shanmu.generate_content('AI 工具推荐')
card = await vd.cards.create_info_card(content.summary)
await cc.publisher.publish('xiaohongshu', content.title, content.body, [card])
```

### 素问 (技术)

```python
from skills.browser_automation import BrowserAutomation
from skills.cli_toolkit import CLIToolkit
from skills.suwen import Suwen

ba = BrowserAutomation()
cli = CLIToolkit()
suwen = Suwen()

# 技术任务
code = await suwen.generate_code('Python web scraper')
await cli.git.commit(f'feat: {code.description}')
```

---

## 🧠 智能路由示例

### 关键词路由

```python
from skills.smart_router import SmartRouter

router = SmartRouter()

# 浏览器相关
task1 = "帮我截图这个网页 https://example.com"
skill1 = router.route(task1)  # → browser-automation

# 交易相关
task2 = "查询 SOL 链上热门代币"
skill2 = router.route(task2)  # → gmgn

# 内容相关
task3 = "写一篇小红书笔记关于 AI 工具"
skill3 = router.route(task3)  # → content-creator

# 视觉相关
task4 = "生成一个柱状图展示销售数据"
skill4 = router.route(task4)  # → visual-designer
```

### 多技能协作

```python
# 复杂任务自动拆解
task = "分析 Polymarket 市场并生成报告发布到微信公众号"

# 太一自动拆解:
# 1. browser-automation: 访问 Polymarket 获取数据
# 2. gmgn: 分析市场趋势
# 3. shanmu-reporter: 生成研报
# 4. visual-designer: 创建图表
# 5. content-creator: 发布到微信

result = await router.execute_complex(task)
```

### 模型路由

```python
from skills.smart_model_router import SmartModelRouter

model_router = SmartModelRouter()

# 根据任务类型选择模型
task1 = "写一首诗"
model1 = model_router.route(task1)  # → qwen3.5-plus

task2 = "分析 100 页 PDF 文档"
model2 = model_router.route(task2)  # → gemini-2.5-pro

task3 = "修复这个 Python bug"
model3 = model_router.route(task3)  # → qwen3-coder-plus
```

---

## 📊 共享层 API 文档

### SharedDatabase

```python
from skills.shared import SharedDatabase

db = SharedDatabase.get_instance()

# 记录动作
db.record_action(
    action_type='user_login',
    data={'user_id': '123', 'ip': '192.168.1.1'},
    timestamp=None  # 默认当前时间
)

# 查询动作
actions = db.query_actions(
    action_type='user_login',
    start_time='2026-04-01',
    end_time='2026-04-07'
)

# 缓存操作
cache = db.get_cache()
cache.set('key', 'value', ttl=3600)  # TTL 秒
value = cache.get('key')
cache.delete('key')

# 配置管理
config = db.get_config('gmgn')
db.set_config('gmgn', {'api_key': 'xxx'})
```

### EventBus

```python
from skills.shared import EventBus, Events

event_bus = EventBus.get_instance()

# 发布事件
event_bus.publish(
    event_type=Events.TASK_COMPLETED,
    data={'task_id': '123', 'result': 'success'}
)

# 订阅事件
def on_task_completed(event):
    print(f"Task {event.data['task_id']} completed")

event_bus.subscribe(Events.TASK_COMPLETED, on_task_completed)

# 取消订阅
event_bus.unsubscribe(Events.TASK_COMPLETED, on_task_completed)
```

### Events 枚举

```python
from skills.shared import Events

# 系统事件
Events.SYSTEM_STARTUP
Events.SYSTEM_SHUTDOWN
Events.CONFIG_CHANGED

# 任务事件
Events.TASK_CREATED
Events.TASK_STARTED
Events.TASK_COMPLETED
Events.TASK_FAILED

# Bot 事件
Events.BOT_ONLINE
Events.BOT_OFFLINE
Events.BOT_MESSAGE_RECEIVED

# 技能事件
Events.SKILL_ACTIVATED
Events.SKILL_DEACTIVATED
Events.SKILL_ERROR
```

---

## ⚠️ 安全注意事项

### 金融操作

- ✅ GMGN swap 需要用户确认
- ✅ Trading 操作需要用户确认
- ✅ 设置滑点限制 (默认 0.5%)
- ✅ 设置单笔最大金额
- ✅ 启用交易前安全检查

### 发布操作

- ✅ 内容发布前审核
- ✅ 敏感词检查
- ✅ 平台速率限制遵守
- ✅ 发布前预览确认

### 系统操作

- ✅ CLI 写操作需要确认
- ✅ 删除操作需要确认
- ✅ 备份优先原则
- ✅ 危险命令拦截

---

## 🧪 测试

```bash
# 运行所有测试
cd /home/nicola/.openclaw/workspace
python3 -m pytest skills/tests/ -v

# 单个技能测试
python3 -m pytest skills/browser_automation/tests/ -v
python3 -m pytest skills/gmgn/tests/ -v

# 覆盖率
python3 -m pytest skills/tests/ --cov=skills --cov-report=html
```

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| **调用延迟** | <100ms | ~80ms |
| **路由命中率** | >95% | ~92% |
| **测试覆盖率** | >80% | ~65% |
| **技能可用性** | >99% | ~98% |

---

*维护：太一 AGI | 技能使用手册 v2.0*
