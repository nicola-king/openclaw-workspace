## 2026-05-22 22:00 数据归档

### 已检查
- **workspace 根目录**：无临时文件（*.tmp/*.temp/*.swp）需要清理
- **temp/**：目录不存在，无需处理
- **data/**（4.1M）：活跃状态，跨境贸易/Token 监控数据均正常
- **reports/**（96K）：无新增过期报告
- **notes/**（7.5M）：含今日新增文件（outreach-queue 稿件、OERV 内容、合规指南），活跃中无需归档
- **e2e_results/**：系统结果已更新，留作参考

### 已清理
- 无临时文件残留
- `.bak` 文件 2 个（skills/ 下备份，保留）

### 当前状态
- 磁盘：128G/1.8T（8%）— 健康
- Workspace 总大小：30G（skills/ 占 7.4G，.git/ 占 237M）
- `.last-archive` 已更新

## 2026-05-15 22:00 数据归档

### 已清理
- `/tmp/buyer_intel_api.pid` — stale PID
- `/tmp/oerv_dispatch.pid` — stale PID
- `/tmp/tmpzmzw5mao.html` — orphan temp
- `/tmp/jiti/` — old cache (>7d)
- `/tmp/org.chromium.*` — old temps (>1d)

### 保留（活跃中、无 workspace 副本）
- `/tmp/cross-border-evening-20260515.md`
- `/tmp/competitor-monitor-20260515.md`
- `/tmp/geo-report-20260515.md`

### 数据目录概览
| 目录 | 大小 | 备注 |
|------|------|------|
| workspace | 23G | voice-pro/ (22G, 模型文件) |
| data | 3.5M | 搜索缓存/自动化扫描 |
| reports | 92K | 7 份报告 |
| logs | 136K | 运行日志 |
| memory | 428K | 记忆文件 |

### 无需归档
- `data/search-automation/` — sweep 结果已组织，可保留
- `data/shared-search-cache/` — 搜索缓存，正常
- `notes/outreach-queue/` — 5/15 待处理外联任务
- `reports/` — 报告已就位
- `voice-pro/model/` — 18G 语音模型，已知项目

---

## 2026-05-16 22:00 数据归档

### 已清理
- `workspace/=1.20.0` — 空文件，疑似 artifact
- `data/inbound_purchase_contract.md` — 0 字节空文件
- `skills/feishu-integration/webhook.pid` — stale PID (8042, 进程不存在)
- `skills/feishu-integration/ngrok.pid` — stale PID (8212, 进程不存在)
- `ngrok.pid` — stale PID (8138, 进程不存在)
- `/tmp/openclaw/openclaw-2026-05-15.log` — 昨日日志，压缩归档至 logs/
- `agents/shoucang/sessions/...jsonl.lock` — stale session lock

### 已归档
- `logs/openclaw-2026-05-15.log.gz` (54K, 压缩比 ~18:1)

### 数据目录概览
| 目录 | 大小 | 变化 |
|------|------|------|
| workspace | 25G | +2G (voice-pro 模型缓存增长) |
| data | 3.5M | 不变 |
| reports | 92K | 不变 |
| logs | 1.1M | +54K (昨日日志压缩) |
| memory | 428K | 今日记忆 8.5K |

### 磁盘状态
- 总量 1.8T，已用 99G (6%)，空间充裕
- `/tmp` OpenClaw 日志 2.1M (今日日志仍在增长)

### 无需归档
- `data/shared-search-stats.json` vs `.md` — JSON 最新 (总请求 283)，MD 是旧版 (273)，保留 JSON，MD 留作历史参考
- `data/.archive/202605/` — 已有月归档机制正常运行
- `memory/2026-05-16.md` (8.5K) — 今日活跃记忆
- `reports/` — 7 份报告已归档完毕

---

## 2026-05-17 22:00 数据归档

### 已清理
- `/tmp/.org.chromium.Chromium.*` — 143 个过期临时文件 (>1d)
- `data/shared-search-cache/` — 26 个过期缓存文件 (>7d)
- `data/search-automation/` — 2 个过期 sweep 文件 (>7d)

### 保留（活跃中）
- `/tmp/cross-border-evening-20260517.md` (10K, 18:00 生成)
- `/tmp/competitor-monitor-20260517.md` (1.5K, 18:00 生成)
- `/tmp/geo-report-20260517.md` (9.9K, 14:00 生成)
- `reports/` — 7 份报告，稳定
- `notes/` — 6.9M 笔记文件，重庆项目资料活跃

### 数据目录概览
| 目录 | 大小 | 变化 |
|------|------|------|
| workspace | 25G | voice-pro 已知 (23G) |
| data | 1.2M | -2.3M (清洗缓存) |
| reports | 92K | 不变 |
| logs | 1.1M | 不变 |
| memory | 428K | 不变 |

### 磁盘状态
- 总量 1.8T，已用 107G (7%)，空间充裕
- 今日无新增报告，无 PID 残留，系统健康

### 2026-05-19
- **tmp/**: 清理 `cron-cross-border-api-keepalive.log` (75B)
- **data/**: shared-search-cache 9 文件 (今日活跃，保留)，cross-border/ (776K) 活跃
- **notes/**: `__deprecated/` 1 个遗留文件，其他笔记正常
- **logs/**: health.log 9.2K，无日志需归档
- **磁盘**: 1.8T/107G (7%)，空间充裕
- **PID/锁文件**: 无残留

## 2026-05-20 22:00 - 每日归档
- 归档 competitor 报告: 2026-05-11 ~ 2026-05-13 (6 文件移至 data/.archive/competitors/202605/)
- 清理 .cache/scraper/: 644K
---

## 2026-05-21 22:00 数据归档

### 已清理
- `__pycache__` 缓存目录 (skills/: ~264K)
- core dump 文件 (skills/, 3 个)

### 已检查
- `data/` (4.1M): 跨境贸易数据、token 监控日志 — 活跃数据，无需归档
- `reports/` (92K): 无新增过期文件
- `.git/` (262M): 含 4202 个松散对象；`git gc --aggressive` 因 OOM 终止，待手工处理
- 临时文件: 无残留 *.tmp/*.temp/*.swp 文件

### 当前状态
- workspace 总大小: 30G
- 无过期报告需归档
- 所有数据文件均为活跃状态

## 2026-05-21 22:00 数据归档

### 重大升级
- **OpenOCR 安装** → 图片文字识别管线 (0.2s/张，CPU)
- **AnySearch 集成** → 统一搜索后端，替代 DuckDuckGo
- **Taiyi Search 统一搜索引擎** → 蒸馏合并 3 个旧搜索 skill 为 1 个
- **废弃 3 个旧 skill**：search-agent, shared-search-agent, anysearch-skill

### 系统配置
- tools.media → openocr-understand.sh（自动识别图片）
- taiyi-search → 已挂载 7 个 Agent
- 系统搜索启用 → provider=anysearch
- VLM 管线已取消（tools.media 和热保 cron 均移除）

### 基础设施
- ollama v0.24.0 @ systemd（3个模型，14.9GB）
- openocr-python @ ~/.venvs/vlm/
- anysearch-skill @ skills/anysearch-skill/
- taiyi-search @ skills/taiyi-search/
=== 2026-05-25 22:00 数据归档 ===
- tmp/: 24 个临时文件 (May 20-21) 移至 data/archive/tmp-files-202605/
- 剩余 2 个文件 (烘箱方案, May 22) 保留在 tmp/
- 磁盘使用: 131G/1.8T (8%)
---

=== 2026-05-26 22:00 数据归档 ===
- 所有目录检查通过，无新增临时文件
- tmp/: 2 文件 (烘箱方案, 与上次一致) — 保留
- reports/: 12 文件正常
- data/: 正常
- 磁盘使用: 131G/1.8T (8%) — 健康
- 超30天旧文件: 无
- 措施: 无需要归档的项目
---

## 2026-05-27 22:00 归档
- 归档 workspace 日志文件: weixin-listener.log, heartbeat.log, cron-health.log → data/archive/tmp-logs-202605/
- 归档 tmp/ 中未修改文件 → data/archive/tmp-files-202605/
