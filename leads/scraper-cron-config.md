# 买家数据抓取定时任务配置

**配置时间**: 2026-04-01T21:32:22+08:00
**执行频率**: 每日 06:00
**状态**: ✅ 已激活

---

## 📋 配置详情

| 项目 | 配置 |
|------|------|
| Cron 表达式 | `0 6 * * *` |
| 执行脚本 | `/tmp/daily-buyer-scraper.sh` |
| 虚拟环境 | `/home/nicola/github-scraper-venv` |
| 工作目录 | `/home/nicola/.openclaw/workspace` |
| 日志文件 | `/tmp/buyer-scraper.log` |

---

## 🔧 管理命令

### 查看当前任务
```bash
crontab -l
```

### 查看执行日志
```bash
tail -f /tmp/buyer-scraper.log
```

### 手动执行一次
```bash
bash /tmp/daily-buyer-scraper.sh
```

### 删除定时任务
```bash
crontab -l | grep -v "daily-buyer-scraper" | crontab -
```

### 禁用任务 (注释)
```bash
crontab -e
# 在行首添加 # 注释掉
```

---

## 📊 预期输出

每日 06:00 自动执行：
1. Alibaba 买家数据抓取 (5 关键词)
2. 数据解析 + 开发信生成
3. 输出到 `leads/` 目录

**预计耗时**: 2-3 分钟  
**预计数据量**: 10-20 条线索/天

---

## 🚨 故障排查

### 任务未执行
```bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog | tail -20
```

### 脚本执行失败
```bash
# 手动执行测试
bash /tmp/daily-buyer-scraper.sh

# 查看详细日志
cat /tmp/buyer-scraper.log
```

---

*配置生成：太一 AGI | 2026-04-01*
