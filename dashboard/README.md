# TurboQuant 压缩率监控面板

实时追踪记忆文件压缩效率的可视化 Dashboard。

## 功能特性

- ✅ **实时压缩率**：显示当前 memory 文件的平均压缩率
- ✅ **7 日趋势图**：可视化展示过去 7 天的压缩率变化
- ✅ **异常告警**：压缩率 < 3x 时自动告警
- ✅ **离线可用**：纯 HTML/JS，无外部依赖
- ✅ **轻量级**：单文件，<20KB

## 使用方法

### 1. 打开面板

直接在浏览器中打开：
```bash
firefox /home/nicola/.openclaw/workspace/dashboard/compression-monitor.html
# 或
chromium /home/nicola/.openclaw/workspace/dashboard/compression-monitor.html
```

### 2. 更新数据

运行数据生成脚本：
```bash
bash /home/nicola/.openclaw/workspace/dashboard/generate-data.sh
```

然后在浏览器中点击「刷新数据」按钮。

### 3. 自动更新（可选）

添加 cron 任务每小时更新数据：
```bash
crontab -e
# 添加以下行：
0 * * * * bash /home/nicola/.openclaw/workspace/dashboard/generate-data.sh
```

## 数据结构

### compression-data.json

```json
{
  "generatedAt": "ISO8601 时间戳",
  "files": [
    {
      "name": "文件名.md",
      "size": 压缩后大小 (字节),
      "originalSize": 估算原始大小 (字节),
      "date": "日期",
      "path": "完整路径"
    }
  ],
  "history": [
    {"date": "MM-DD", "rate": 压缩率}
  ],
  "alerts": []
}
```

## 压缩率计算

```
压缩率 = 原始大小 / 压缩后大小
```

**目标范围：** 4-6x（TurboQuant 协议）
**告警阈值：** < 3x

## 文件说明

| 文件 | 用途 |
|------|------|
| `compression-monitor.html` | 主面板（可视化界面） |
| `compression-data.json` | 数据文件（由脚本生成） |
| `generate-data.sh` | 数据生成脚本 |
| `README.md` | 本文档 |

## 设计原则

- **极简黑客风**：黑白配色，monospace 字体
- **零依赖**：不依赖任何 CDN 或外部库
- **本地优先**：所有数据在本地，无需网络
- **实时性**：支持手动/自动刷新

## 扩展建议

1. **实时文件监控**：使用 inotify 监听文件变化自动触发更新
2. **历史数据持久化**：将每日数据保存为独立文件
3. **告警通知**：压缩率异常时发送 Telegram/微信通知
4. **对比分析**：core.md vs residual.md 压缩率对比

---

*版本：v1.0 | 创建时间：2026-03-26*
