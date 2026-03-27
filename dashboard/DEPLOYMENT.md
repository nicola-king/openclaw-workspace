# TurboQuant 压缩率监控面板 - 部署文档

## ✅ 部署状态

| 项目 | 状态 | 说明 |
|------|------|------|
| 面板服务 | ✅ 运行中 | Python HTTP Server (端口 8888) |
| 数据更新 | ✅ 已配置 | 每小时整点自动生成 |
| 告警通知 | ✅ 已配置 | 每小时 30 分检查 (压缩率<3x) |
| 访问 URL | ✅ 可用 | http://192.168.2.242:8888/compression-monitor.html |

---

## 📋 访问方式

### 本地访问
```
http://localhost:8888/compression-monitor.html
```

### 内网访问（推荐）
```
http://192.168.2.242:8888/compression-monitor.html
```

### 移动端访问
在同一 WiFi 网络下，使用手机浏览器访问上述内网 URL

---

## 🚀 部署架构

```
┌─────────────────────────────────────────────────────┐
│                   监控面板系统                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐    ┌──────────────┐              │
│  │  数据生成    │    │  告警检查     │              │
│  │  (每小时)    │───▶│  (每小时)    │              │
│  │ generate-    │    │ compression- │              │
│  │ data.sh      │    │ alert.sh     │              │
│  └──────┬───────┘    └──────┬───────┘              │
│         │                   │                       │
│         ▼                   ▼                       │
│  ┌──────────────┐    ┌──────────────┐              │
│  │  数据文件    │    │  通知渠道     │              │
│  │  compression-│    │  • 微信       │              │
│  │  data.json   │    │  • Telegram   │              │
│  └──────┬───────┘    └──────────────┘              │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │  监控面板    │                                   │
│  │  compression-│                                   │
│  │  monitor.    │                                   │
│  │  html        │                                   │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │  HTTP Server │                                   │
│  │  (端口 8888) │                                   │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │  用户浏览器  │                                   │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
/home/nicola/.openclaw/workspace/dashboard/
├── compression-monitor.html    # 主面板（可视化界面）
├── compression-data.json       # 数据文件（每小时更新）
├── generate-data.sh            # 数据生成脚本
├── compression-alert.sh        # 告警通知脚本
├── turboquant-dashboard.service # systemd 服务配置（备用）
└── DEPLOYMENT.md               # 本部署文档
```

---

## ⚙️ 配置说明

### 1. 数据生成（每小时整点）

**Cron 任务：**
```bash
0 * * * * bash /home/nicola/.openclaw/workspace/dashboard/generate-data.sh >/dev/null 2>&1
```

**功能：**
- 扫描 `memory/` 目录下所有 `.md` 文件
- 计算每个文件的压缩率（原始大小 / 压缩后大小）
- 生成 7 日趋势数据
- 输出到 `compression-data.json`

### 2. 告警检查（每小时 30 分）

**Cron 任务：**
```bash
30 * * * * bash /home/nicola/.openclaw/workspace/dashboard/compression-alert.sh >> logs/compression-alert.log 2>&1
```

**功能：**
- 读取 `compression-data.json`
- 检测压缩率 < 3x 的文件
- 发送微信通知（通过素问 Bot）
- 发送 Telegram 通知（通过知几 Bot）

**告警阈值：** 压缩率 < 3.0x

### 3. HTTP 服务（常驻）

**启动命令：**
```bash
cd /home/nicola/.openclaw/workspace/dashboard
nohup python3 -m http.server 8888 > logs/dashboard-server.log 2>&1 &
```

**进程管理：**
```bash
# 查看状态
ps aux | grep "http.server 8888"

# 重启服务
pkill -f "http.server 8888"
cd /home/nicola/.openclaw/workspace/dashboard && nohup python3 -m http.server 8888 > logs/dashboard-server.log 2>&1 &

# 查看日志
tail -f logs/dashboard-server.log
```

---

## 🔔 告警通知配置

### 微信通知
- **Bot:** 素问 (@sayelfdoctor_bot)
- **渠道:** openclaw-weixin
- **触发条件:** 任意文件压缩率 < 3x

### Telegram 通知
- **Bot:** 知几 (@sayelf_bot)
- **用户:** Nicola (7073481596)
- **触发条件:** 任意文件压缩率 < 3x

### 告警消息格式
```
🚨 TurboQuant 压缩率告警

发现 X 个文件压缩率异常 (<3x)

• `2026-03-26.md`: 2.5x (5.8 KB)
• `core.md`: 2.8x (2.4 KB)

请检查：/home/nicola/.openclaw/workspace/memory/
```

---

## 📊 面板功能

### 实时指标
- **实时压缩率**: 当前会话平均压缩率
- **7 日平均**: 过去 7 天趋势
- **总文件数**: memory 目录文件总数
- **告警状态**: 当前告警数量

### 可视化图表
- 7 日压缩率趋势图（柱状图）
- 颜色编码：
  - 🟢 绿色：4-6x（正常）
  - 🔴 红色：<3x（告警）
  - ⚪ 白色：3-4x 或 >6x（观察）

### 文件详情
- 文件名
- 大小（KB）
- 压缩率
- 状态指示器

### 自动刷新
- 页面加载时自动获取数据
- 每 5 分钟自动刷新
- 手动刷新按钮

---

## 🛠️ 运维操作

### 手动更新数据
```bash
bash /home/nicola/.openclaw/workspace/dashboard/generate-data.sh
```

### 手动触发告警检查
```bash
bash /home/nicola/.openclaw/workspace/dashboard/compression-alert.sh
```

### 查看告警日志
```bash
tail -f /home/nicola/.openclaw/workspace/logs/compression-alert.log
```

### 查看服务日志
```bash
tail -f /home/nicola/.openclaw/workspace/logs/dashboard-server.log
```

### 重启 HTTP 服务
```bash
pkill -f "http.server 8888"
cd /home/nicola/.openclaw/workspace/dashboard
nohup python3 -m http.server 8888 > /home/nicola/.openclaw/workspace/logs/dashboard-server.log 2>&1 &
```

---

## 🔒 安全说明

### 数据边界
- ✅ 所有数据在本地处理
- ✅ 不上传到外部服务器
- ✅ 仅内网可访问
- ✅ 不暴露敏感信息（仅文件大小和压缩率）

### 访问控制
- 当前：内网 IP 访问（192.168.2.242）
- 建议：如需外网访问，配置 Nginx 反向代理 + 基本认证

### 未来迁移方案
如需迁移到 Coolify/Docker：
```bash
# Dockerfile 示例
FROM python:3.12-slim
WORKDIR /app
COPY dashboard/ /app/
EXPOSE 8888
CMD ["python3", "-m", "http.server", "8888"]
```

---

## 📈 验收标准

- [x] **面板可公开访问**
  - URL: http://192.168.2.242:8888/compression-monitor.html
  - 本地/内网均可访问

- [x] **数据自动更新**
  - Cron 任务：每小时整点
  - 脚本：generate-data.sh

- [x] **告警通知配置**
  - 微信通知：已配置
  - Telegram 通知：已配置
  - 触发条件：压缩率 < 3x

---

## 🎯 下一步优化建议

1. **Nginx 反向代理**（可选）
   - 配置 HTTPS
   - 添加基本认证
   - 限制访问 IP

2. **历史数据持久化**
   - 每日数据归档
   - 长期趋势分析

3. **实时文件监控**
   - 使用 inotify 监听文件变化
   - 实时触发数据更新

4. **压缩率对比分析**
   - core.md vs residual.md
   - 按文件类型分类统计

---

**部署时间:** 2026-03-26 19:09  
**部署人员:** 素问 (技术开发主管)  
**版本:** v1.0  
**状态:** ✅ 生产就绪
