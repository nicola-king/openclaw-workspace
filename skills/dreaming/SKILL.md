# Dreaming Skill - 自动记忆整理系统

> 状态：✅ 已启用  
> 优先级：P0（已运行）  
> 创建日期：2026-04-08

---

## 触发条件

**自动触发**：每天凌晨 3 点

**手动触发**：
- 需要整理记忆时
- context 接近上限时
- 需要提炼长期记忆时

---

## 能力

- ✅ 三阶段处理（Light → REM → Deep）
- ✅ 自动输出 DREAMS.md
- ✅ 自动更新 MEMORY.md
- ✅ 记忆关联增强
- ✅ 模式识别
- ✅ 记忆压缩

---

## 配置

```bash
DREAMING_SCHEDULE="0 3 * * *"  # 每天凌晨 3 点
DREAMING_OUTPUT_DIR=./memory/
DREAMING_AUTO_UPDATE_MEMORY=true
DREAMING_RETENTION_DAYS=30
```

---

## 使用方法

```bash
# 自动运行（Crontab）
0 3 * * * openclaw dream

# 手动触发
openclaw dream --force

# 查看梦境
cat memory/DREAMS.md

# 查看记忆更新
git diff memory/MEMORY.md
```

---

## 输出

| 文件 | 内容 | 说明 |
|------|------|------|
| DREAMS.md | 梦境日记 | 原始整理记录 |
| MEMORY.md | 长期记忆 | 自动更新 |
| memory/YYYY-MM-DD.md | 日记忆 | 自动归档 |

---

## 状态

- [x] ✅ 调研完成
- [x] ✅ SAYELF 已启用（21:42）
- [ ] ⏳ 验证首次运行
- [ ] ⏳ 查看梦境输出

---

*最后更新：2026-04-08 22:30*
