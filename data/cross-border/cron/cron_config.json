{
  "tasks": {},
  "crontab": "# 太一全域跨境贸易 Agent - 定时任务配置\n# 生成时间：2026-05-04T08:00:12.241824\n\n# ========== 自媒体运营任务 ==========\n0 8 * * * cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 self_media_engine.py # 晨间新闻推送\n0 9 * * 1-5 cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 self_media_engine.py # 周度深度分析\n0 20 * * * cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 self_media_engine.py # 流量数据汇总\n0 18 * * 5 cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 self_media_engine.py # 转化漏斗分析\n0 22 * * 0 cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 self_evolution_engine.py # 自进化报告\n0 10 * * 1 cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 brand_building_engine.py # 品牌健康度报告\n0 11 * * 1 cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 private_traffic_engine.py # 私域运营报告\n0 3 * * * cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent && python3 backup.py # 数据备份\n\n# ========== 系统维护任务 ==========\n0 3 * * * find /tmp -type f -mtime +7 -delete # 清理 7 天前临时文件\n0 4 * * 0 cd /home/sayelf/.openclaw/workspace && git add -A && git commit -m '自动备份' # 每周备份",
  "status": {
    "status": "success",
    "file": "/home/sayelf/.openclaw/workspace/data/cross-border/cron/openclaw_cron",
    "task_count": 8,
    "message": "crontab 配置已保存到 /home/sayelf/.openclaw/workspace/data/cross-border/cron/openclaw_cron，请手动执行：crontab /home/sayelf/.openclaw/workspace/data/cross-border/cron/openclaw_cron"
  }
}