# 多平台内容采集框架

**免费开源 · 可扩展 · 自动化**

---

## 📦 支持平台

| 平台 | 状态 | 采集器 |
|------|------|--------|
| **X (Twitter)** | ✅ 就绪 | `platforms/x_crawler.py` |
| **微信公众号** | ✅ 就绪 | `platforms/wechat_crawler.py` |
| **小红书** | 🟡 待配置 | `platforms/xiaohongshu_crawler.py` |
| **视频号** | 🔴 高风险 | 暂缓 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/crawlers
pip install -r requirements.txt
```

### 2. 配置目标

编辑 `config/targets.json`，添加要监控的账号/关键词。

### 3. 运行采集

```bash
# 采集所有平台
python main.py

# 采集指定平台
python main.py --platform x
python main.py --platform wechat

# 测试单个采集器
python -m platforms.x_crawler --test
```

### 4. 查看结果

采集结果输出到 `output/` 目录：
- `output/raw/` - 原始数据 (JSON)
- `output/processed/` - 处理后数据 (CSV/Markdown)
- `output/logs/` - 运行日志

---

## 📁 目录结构

```
crawlers/
├── main.py              # 主入口
├── requirements.txt     # 依赖
├── config/
│   └── targets.json     # 采集目标配置
├── core/
│   ├── base.py          # 采集器基类
│   ├── storage.py       # 数据存储
│   └── utils.py         # 工具函数
├── platforms/
│   ├── x_crawler.py     # X 采集器
│   ├── wechat_crawler.py # 公众号采集器
│   └── xiaohongshu_crawler.py # 小红书采集器
└── output/
    ├── raw/             # 原始数据
    ├── processed/       # 处理后数据
    └── logs/            # 日志
```

---

## ⚙️ 配置说明

### targets.json 格式

```json
{
  "x": {
    "accounts": ["@elonmusk", "@OpenAI"],
    "keywords": ["AI", "AGI", "Taiyi"],
    "hashtag": ["#TaiyiAGI"]
  },
  "wechat": {
    "accounts": ["AI 科技评论", "机器之心"],
    "keywords": ["大模型", "Agent"]
  },
  "xiaohongshu": {
    "keywords": ["AI 工具", "效率神器"]
  }
}
```

---

## 🔧 定时任务

采集器已集成 OpenClaw 定时任务，自动执行：

```bash
# 查看定时任务
openclaw cron list

# 手动触发
openclaw cron run crawler-daily
```

---

## 📊 数据用途

采集的数据可用于：
- 竞品监控
- 舆情分析
- 内容灵感
- 趋势追踪
- AI 训练数据

---

*最后更新：2026-03-25 | 版本：v1.0*
