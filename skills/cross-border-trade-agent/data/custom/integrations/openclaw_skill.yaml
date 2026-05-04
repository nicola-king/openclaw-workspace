name: cross-border-trade-agent
version: 8.5.0
description: |
  跨境贸易全流程自动化 Agent - 全域自进化智能体
  核心能力：获客之王 + GEO 外贸开发 + 7 大数据源 + AI 搜索优化
category: trading
tags:
  - trading
  - cross-border
  - e-commerce
  - geo-optimization
  - lead-generation
  - data-analysis
  - auto-evolution
author: 太一 AGI
source: /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent

# 入口点
entry:
  # 主 Agent
  agent: cross_border_agent.py
  # 快速命令
  commands:
    - name: market-analysis
      script: free_data_adapter.py
      description: 市场分析 (汇率/贸易数据)
    - name: prospect-search
      script: prospect_search.py
      description: 全网潜客搜寻
    - name: geo-audit
      script: geo_auditor.py
      description: GEO 可见度审计
    - name: product-select
      script: smart_product_selector.py
      description: 智能选品
    - name: price-compare
      script: price_comparator.py
      description: 价格对比
    - name: logistics-opt
      script: logistics_optimizer.py
      description: 物流优化

# 依赖
dependencies:
  python: ">=3.11"
  packages:
    - requests
    - aiohttp
    - pandas
    - numpy
    - scikit-learn
    - python-dotenv
  optional:
    - redis
    - python-docx
    - openpyxl
    - loguru

# 配置
config:
  # 数据目录
  data_dir: /home/sayelf/.openclaw/workspace/data/cross-border-trade-agent
  # 日志目录
  log_dir: /home/sayelf/.openclaw/workspace/logs
  # 缓存时间 (秒)
  cache_duration: 3600
  # 默认利润率
  profit_margin: 0.20
  # 营销渠道
  marketing_channels:
    - alibaba
    - google
    - facebook
    - linkedin

# 定时任务 (与 crontab 同步)
scheduled_tasks:
  - name: daily-news
    schedule: "0 8 * * *"
    script: self_media_engine.py
  - name: weekly-analysis
    schedule: "0 9 * * 1-5"
    script: self_media_engine.py
  - name: traffic-report
    schedule: "0 20 * * *"
    script: self_media_engine.py
  - name: evolution-report
    schedule: "0 22 * * 0"
    script: self_evolution_engine.py

# 权限
permissions:
  - file_read
  - file_write
  - network_request
  - cron_schedule

# 文档
documentation:
  readme: README.md
  architecture: ARCHITECTURE_V85.md
  api: API_REFERENCE.md
  free_data: FREE_DATA_SOURCES.md
