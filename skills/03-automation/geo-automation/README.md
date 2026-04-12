# GEO 自动化工作流

> 零成本启动 | 完全开源 | 基于 OpenClaw 生态

---

## 🚀 快速使用

### 手动触发
```bash
# 通过 OpenClaw 消息触发
发送："生成 GEO 内容"

# 或直接运行脚本
python3 /home/nicola/.openclaw/workspace/scripts/geo-question-generator.py
python3 /home/nicola/.openclaw/workspace/scripts/geo-content-generator.py
python3 /home/nicola/.openclaw/workspace/scripts/geo-publisher.py
```

### 自动执行
```bash
# Cron 定时任务（已配置）
0 10 * * *  # 每天 10:00 生成问题
0 14 * * *  # 每天 14:00 生成发布文件
```

---

## 📦 输出目录

| 目录 | 内容 |
|------|------|
| `geo-questions/` | 问题库（90 个问题） |
| `geo-content/` | 生成内容（30 篇） |
| `geo-published/` | 多平台发布文件 |

---

## 📊 已安装 Skills

| Skill | 用途 | 状态 |
|-------|------|------|
| geo-seo-optimizer | GEO+SEO 优化 | ✅ |
| content-scheduler | 内容定时发布 | ✅ |
| social-publisher | 多平台发布 | ✅ |
| portfolio-tracker | 投资组合追踪 | ✅ |
| social-media-scheduler | 社交媒体调度 | ✅ |

---

## 🔗 相关文档

- 完整文档：`/home/nicola/.openclaw/workspace/geo-workflow/README.md`
- 脚本目录：`/home/nicola/.openclaw/workspace/scripts/geo-*.py`

---

*最后更新：2026-04-05 00:05*
