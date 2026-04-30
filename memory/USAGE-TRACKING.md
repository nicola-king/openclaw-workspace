# 模型用量追踪

## 问题说明

OpenClaw 日志中 `usage` 字段全部为 0，这是设计行为（节省日志空间）。
实际用量需通过阿里云百炼控制台查看。

## 查看方式

### 方式 1：阿里云控制台（准确）
- URL: https://bailian.console.aliyun.com/
- 路径：用量统计 → API 调用明细
- 筛选：按模型 (qwen3.5-plus)、按日期

### 方式 2：阿里云 API（自动化）

```bash
# 需要配置阿里云 AccessKey
curl -X POST "https://bailian.cn-shanghai.aliyuncs.com/openapi/usage/query" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"startTime":"2026-03-23T00:00:00Z","endTime":"2026-03-23T23:59:59Z"}'
```

### 方式 3：本地估算（粗略）

```bash
# 统计 session 文件大小估算
du -sh /home/nicola/.openclaw/agents/taiyi/sessions/*.jsonl | sort -hr
```

## 定价参考 (qwen3.5-plus)

| 类型 | 价格 |
|------|------|
| 输入 | ¥0.004 / 1K tokens |
| 输出 | ¥0.012 / 1K tokens |
| 上下文缓存 | ¥0.001 / 1K tokens |

## 优化建议

1. **减少心跳频率** - 从 30m 改为 60m（如果不需要频繁检查）
2. **使用缓存** - 启用阿里云上下文缓存功能
3. **切换模型** - 简单任务用 qwen3-coder-plus（更便宜）
4. **压缩上下文** - 定期清理 session 日志

## 今日估算

根据 session 文件大小：
- 总会话文件：~20.5 MB
- 估算 tokens: ~500K-1M
- 估算成本：¥5-15/天

*最后更新：2026-03-23 17:11*
