# 🚨 Crontab 变更告警

> **检测时间**: 2026-04-28 00:00 | **负责 Bot**: 太一

## 告警内容

**发现新增禁用任务**: 2 个 (上次：1)

## 详细信息

- **备份文件**: /home/nicola/.openclaw/workspace/backups/crontab/crontab-20260428-000001.txt
- **差异报告**: /home/nicola/.openclaw/workspace/backups/crontab/diff-20260428-000001.txt
- **注释行总数**: 36 / 88

## 疑似禁用任务

```bash
# 更新时间：2026-04-24 20:47
#*/45 * * * * cd /home/nicola/.openclaw/workspace && /usr/bin/python3 scripts/check-bailian-quota.py >> logs/model-router.log 2>&1
```

## 处理建议

1. **立即审查**: 确认为何被禁用
2. **联系责任人**: 询问禁用原因
3. **恢复任务**: 如无正当理由，立即恢复
4. **记录原因**: 如确需禁用，走审批流程

## 审批流程

根据 `constitution/directives/CRON-PROTECTION.md`:
- 禁用任务必须经过太一审批
- 必须标注原因和恢复时间
- 超期自动恢复

---
*自动生成 | Crontab 保护机制 v1.0*
