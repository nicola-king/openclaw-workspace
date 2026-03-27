# 🚀 快速开始指南

## ✅ 安装完成

多平台内容采集框架已成功安装并测试通过！

---

## 📋 下一步

### 1. 配置采集目标

编辑 `config/targets.json`：

```json
{
  "x": {
    "enabled": true,
    "accounts": ["@OpenAI", "@AnthropicAI"],
    "keywords": ["AGI", "AI Agent"],
    "hashtags": ["#TaiyiAGI"]
  }
}
```

### 2. 手动测试

```bash
cd ~/.openclaw/workspace/crawlers

# 测试采集器
bash run.sh test

# 采集 X 平台
bash run.sh x

# 采集所有启用的平台
bash run.sh all
```

### 3. 添加定时任务（可选）

```bash
openclaw cron add config/openclaw-cron.json
```

这将设置**每天上午 9 点**自动采集。

---

## 📊 查看结果

采集结果保存在：

```
~/.openclaw/workspace/crawlers/output/
├── raw/          # 原始 JSON 数据
├── processed/    # 处理后的 CSV/JSON
├── logs/         # 运行日志
└── reports/      # 汇总报告
```

---

## 🔧 常用命令

| 命令 | 说明 |
|------|------|
| `bash run.sh test` | 测试采集器 |
| `bash run.sh x` | 采集 X 平台 |
| `bash run.sh all` | 采集所有平台 |
| `bash run.sh daily` | 执行每日任务 |
| `openclaw cron list` | 查看定时任务 |
| `openclaw cron remove crawler-daily` | 删除定时任务 |

---

## ⚙️ 配置说明

### X (Twitter) 采集

- ✅ **免登录** - 使用 Playwright 模拟浏览器
- ✅ **支持** - 账号/关键词/话题
- 🟡 **限制** - 频繁请求可能触发验证码

### 微信公众号采集

- 🟡 **需要 Cookie** - 首次使用需手动获取
- 🟡 **有效期** - Cookie 约 24 小时
- 📖 **配置指南** - `python3 platforms/wechat_crawler.py --setup`

### 小红书采集

- 🔴 **待开发** - 需要 MediaCrawler + Cookie
- 🟡 **高风险** - 平台反爬严格

---

## 💡 使用建议

1. **先测试** - 用小数据量测试配置
2. **合理频率** - 避免频繁请求触发风控
3. **定期更新** - Cookie 需要定期刷新
4. **合法合规** - 仅采集公开数据

---

## 🆘 遇到问题？

### 采集不到数据

- 检查网络连接
- 增加等待时间（`wait_for_timeout`）
- 尝试显示浏览器模式：`--no-headless`

### 触发验证码

- 降低采集频率
- 增加请求间隔
- 使用代理 IP（可选）

### Cookie 失效

- 重新登录微信公众号后台
- 复制新的 Cookie 到配置文件

---

*框架版本：v1.0 | 最后更新：2026-03-25*
