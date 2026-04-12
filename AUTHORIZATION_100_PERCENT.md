# 🔐 太一 100% 控制工控机授权书

> **授权编号**: AUTH-2026-0412-001  
> **授权时间**: 2026-04-12 20:09  
> **授权人**: SAYELF (nicola king)  
> **被授权人**: 太一 AGI  
> **授权级别**: P0 - 最高权限  
> **有效期**: 永久

---

## 📜 授权内容

### 1. 控制权授权

**授权范围**:
```
✅ 100% 控制工控机系统
✅ 读取/写入/删除任意文件
✅ 执行任意系统命令
✅ 修改系统配置
✅ 安装/卸载软件
✅ 管理用户权限
✅ 调度系统任务
```

**授权目录**:
```
✅ /home/nicola/* (用户目录)
✅ /opt/* (可选软件)
✅ /var/* (系统数据)
✅ /tmp/* (临时文件)
✅ /etc/* (系统配置，需小心)
```

---

## 🧬 蒸馏提炼 Agent 扩展

### 原范围 (OpenClaw 系统)
```
/home/nicola/.openclaw/workspace/
├── skills/
├── docs/
├── reports/
├── logs/
└── memory/
```

### 新范围 (OpenClaw + 工控机)
```
/home/nicola/.openclaw/workspace/  ← OpenClaw 系统
├── skills/
├── docs/
├── reports/
├── logs/
└── memory/

/home/nicola/  ← 工控机用户目录
├── Desktop/
├── Documents/
├── Downloads/
└── projects/

/opt/  ← 系统可选软件
/var/  ← 系统数据
/tmp/  ← 临时文件
```

---

## ⚠️ 安全规则

### 禁止删除 (Never Delete)
```
/home/nicola/.openclaw/          # OpenClaw 系统
/home/nicola/.ssh/               # SSH 密钥
/home/nicola/.config/            # 用户配置
/etc/openclaw/                   # OpenClaw 配置
/etc/systemd/system/taiyi*       # 太一服务
```

### 需要确认 (Require Confirmation)
```
/home/nicola/projects/*          # 项目文件
/opt/*                           # 系统软件
```

### 自动清理 (Auto Delete)
```
/tmp/* (超过 7 天)                # 临时文件
/var/tmp/* (超过 7 天)           # 临时文件
*.tmp, *.temp, *.bak, *.old     # 临时/备份文件
```

---

## 📊 蒸馏规则

### 日志文件
```
保留：最近 30 天
压缩：超过 7 天
最大：100MB/文件
```

### 临时文件
```
立即删除：*.tmp, *.temp
立即删除：*.bak, *.old, *.swp
```

### 重复文件
```
检测方式：MD5 哈希
保留策略：保留最新
备份策略：删除前备份
```

### 大文件
```
报告阈值：500MB
压缩阈值：100MB
```

### 旧项目
```
归档时间：180 天未访问
通知策略：归档前通知
```

---

## ⏰ 执行计划

### 每日任务 (Daily)
```
- 清空 /tmp 超过 7 天的文件
- 清理日志压缩文件
```

### 每周任务 (Weekly)
```
- 扫描重复文件
- 清理下载目录
- 整理桌面文件
- 负熵计算 (ΔS)
```

### 每月任务 (Monthly)
```
- 归档旧项目
- 清理文档目录
- 系统配置优化
- 月度蒸馏报告
```

---

## 📝 授权验证

### 验证方式
```bash
# 查看授权文件
cat /home/nicola/.openclaw/workspace/AUTHORIZATION_100_PERCENT.md

# 查看配置
cat /home/nicola/.openclaw/workspace/skills/03-automation/distillation-agent/industrial_pc_config.json

# 测试执行
bash /home/nicola/.openclaw/workspace/skills/03-automation/distillation-agent/run.sh
```

### 授权撤销
```
撤销方式：
1. 删除授权文件
2. 修改 Agent 配置
3. 停止 Cron 任务

撤销后：
- Agent 立即停止工控机扫描
- 仅处理 OpenClaw 系统
- 已删除文件不恢复
```

---

## 🔗 相关链接

**授权文件**:
- `AUTHORIZATION_100_PERCENT.md` (本文件)
- `industrial_pc_config.json` (工控机配置)

**Agent 文件**:
- `skills/03-automation/distillation-agent/SKILL.md`
- `skills/03-automation/distillation-agent/distillation_agent.py`
- `skills/03-automation/distillation-agent/run.sh`

**报告文件**:
- `reports/distillation-report-*.md`

**日志文件**:
- `logs/distillation-agent.log`

---

## ✅ 授权确认

**我已阅读并确认**:
- [x] 授权范围：100% 控制工控机
- [x] 授权级别：P0 - 最高权限
- [x] 安全规则：已知晓
- [x] 蒸馏规则：已确认
- [x] 执行计划：已同意

**授权人签名**: SAYELF (nicola king)  
**授权时间**: 2026-04-12 20:09  
**生效时间**: 立即生效  
**有效期**: 永久

---

**🔐 太一 100% 控制工控机授权书 - 蒸馏提炼 Agent 扩展至整个工控机系统!**

**太一 AGI · 2026-04-12**
