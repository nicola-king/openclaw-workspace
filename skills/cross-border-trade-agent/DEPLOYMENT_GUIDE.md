# 全域跨境贸易 Agent v8.6 部署指南

> **版本**: v8.6  
> **更新时间**: 2026-04-19  
> **部署环境**: Ubuntu 24.04 / Python 3.12+

---

## 📋 系统要求

| 要求 | 最低配置 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Ubuntu 22.04 | Ubuntu 24.04 |
| Python | 3.10+ | 3.12+ |
| 内存 | 8GB | 16GB+ |
| 存储 | 50GB | 100GB+ |
| CPU | 4 核 | 8 核+ |

---

## 🚀 快速部署

### 1. 克隆仓库

```bash
cd /home/sayelf/.openclaw/workspace
git pull origin main
```

### 2. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 3. 配置 API 密钥

```bash
# 创建配置文件
cp config/api_keys.json.example config/api_keys.json

# 编辑配置
nano config/api_keys.json
```

### 4. 配置环境变量

```bash
# 编辑.env 文件
nano .env

# 添加以下内容
GOOGLE_API_KEY=your_google_api_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### 5. 安装定时任务

```bash
# 查看配置
cat data/cross-border/cron/openclaw_cron

# 安装
crontab data/cross-border/cron/openclaw_cron

# 验证
crontab -l
```

### 6. 启动服务

```bash
# 启动 OpenClaw Gateway
openclaw gateway start

# 检查状态
openclaw gateway status
```

---

## 📁 目录结构

```
/home/sayelf/.openclaw/workspace/
├── skills/01-trading/cross-border-trade-agent/
│   ├── 获客之王模块 (6 个)
│   ├── GEO 外贸模块 (7 个)
│   ├── 智能决策模块 (4 个)
│   ├── 交易支持模块 (4 个)
│   ├── 数据整合模块 (8 个)
│   ├── 外贸社媒模块 (11 个)
│   ├── B2B/B2C 平台模块 (2 个)
│   ├── 自媒体运营模块 (4 个)
│   └── P1/P2/P3 模块 (5 个)
├── data/cross-border/          # 数据目录
├── reports/cross-border/       # 报告目录
├── config/                     # 配置目录
└── logs/                       # 日志目录
```

---

## ⚙️ 配置说明

### API 密钥配置

**文件**: `config/api_keys.json`

```json
{
  "google": {
    "api_key": "your_google_api_key",
    "credentials": "/path/to/credentials.json"
  },
  "customs": {
    "api_key": "your_customs_api_key"
  },
  "amazon": {
    "client_id": "your_amazon_client_id",
    "client_secret": "your_amazon_client_secret"
  }
}
```

### 定时任务配置

**文件**: `data/cross-border/cron/openclaw_cron`

```bash
# 晨间新闻推送 (每日 08:00)
0 8 * * * cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 self_media_engine.py

# 流量数据汇总 (每日 20:00)
0 20 * * * cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 self_media_engine.py

# 自进化报告 (每周日 22:00)
0 22 * * 0 cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 self_evolution_engine.py
```

---

## 🔧 运维管理

### 查看日志

```bash
# 查看最新日志
tail -f logs/cross-border/*.log

# 查看错误日志
grep ERROR logs/cross-border/*.log
```

### 数据备份

```bash
# 手动备份
python3 scripts/backup.py

# 恢复备份
python3 scripts/restore.py --backup=2026-04-19
```

### 系统监控

```bash
# 查看 Gateway 状态
openclaw gateway status

# 查看定时任务状态
systemctl status cron

# 查看磁盘使用
df -h

# 查看内存使用
free -h
```

---

## 📊 验证部署

### 1. 模块测试

```bash
# 测试 B2B 模块
python3 skills/01-trading/cross-border-trade-agent/b2b_platform_module.py

# 测试 B2C 模块
python3 skills/01-trading/cross-border-trade-agent/b2c_platform_module.py

# 测试自媒体引擎
python3 skills/01-trading/cross-border-trade-agent/self_media_engine.py
```

### 2. API 测试

```bash
# 测试 Google Trends API
python3 skills/01-trading/cross-border-trade-agent/google_trends_integrator.py
```

### 3. 报告生成测试

```bash
# 生成测试报告
python3 skills/01-trading/cross-border-trade-agent/operation_report_generator.py
```

---

## ❓ 故障排查

### 问题 1: 模块导入失败

```bash
# 检查 Python 路径
echo $PYTHONPATH

# 添加路径
export PYTHONPATH=/home/sayelf/.openclaw/workspace:$PYTHONPATH
```

### 问题 2: API 密钥错误

```bash
# 检查配置文件
cat config/api_keys.json

# 检查环境变量
echo $GOOGLE_API_KEY
```

### 问题 3: 定时任务不执行

```bash
# 检查 cron 服务
systemctl status cron

# 重启 cron
sudo systemctl restart cron

# 查看 cron 日志
grep CRON /var/log/syslog
```

### 问题 4: 数据目录不存在

```bash
# 创建目录
mkdir -p data/cross-border/{b2b_platform,b2c_platform,self_media,private_traffic,brand_building,self_evolution,cron,trends,optimization}
```

---

## 📈 性能优化

### 1. 数据库优化

```bash
# 使用 SQLite 索引
sqlite3 data/cross-border/main.db "CREATE INDEX IF NOT EXISTS idx_date ON data(date);"
```

### 2. 缓存配置

```bash
# 启用 Redis 缓存
redis-server /etc/redis/redis.conf
```

### 3. 并发优化

```python
# 使用多线程
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_data, data_list)
```

---

## 🔐 安全建议

### 1. API 密钥保护

```bash
# 设置文件权限
chmod 600 config/api_keys.json

# 不要提交到 Git
echo "config/api_keys.json" >> .gitignore
```

### 2. 数据备份

```bash
# 每日备份
0 3 * * * python3 /home/sayelf/.openclaw/workspace/scripts/backup.py
```

### 3. 访问控制

```bash
# 限制目录访问
chmod 750 data/cross-border
```

---

## 📞 技术支持

### 文档

- 用户指南：`USER_GUIDE.md`
- API 参考：`API_REFERENCE.md`
- 集成测试：`INTEGRATION_TEST_REPORT.md`

### 日志位置

- 系统日志：`logs/`
- 模块日志：`logs/cross-border/`
- 定时任务日志：`/var/log/syslog`

### 联系方式

- GitHub: https://github.com/nicola-king
- 文档：`/home/sayelf/.openclaw/workspace/docs/`

---

*太一全域跨境贸易 Agent v8.6 · 部署指南 v1.0*  
*更新时间：2026-04-19 20:23*  
*部署状态：✅ Production Ready*
