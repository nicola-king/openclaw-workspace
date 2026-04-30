# ✅ 百度网盘已连接

> 连接时间：2026-04-10 16:30  
> 状态：✅ 已授权

---

## 📊 网盘信息

| 项目 | 数值 |
|------|------|
| **总容量** | 2.007 TB |
| **已使用** | 925.866 GB |
| **可用空间** | ~1.1 TB |
| **使用率** | 45% |

---

## 🔐 授权状态

| 项目 | 状态 |
|------|------|
| **访问令牌** | ✅ 有效 |
| **刷新令牌** | ✅ 有效 |
| **配置文件** | `~/.bypy.json` |

---

## 📁 目录结构

已创建：
```
/apps/
└── taiyi/
    └── workspace/
```

---

## 🤖 自动化配置

### 工作区备份

**手动备份**：
```bash
bypy upload /home/nicola/.openclaw/workspace /apps/taiyi/workspace
```

**定时备份** (已配置)：
```bash
# 每天凌晨 2 点自动备份
0 2 * * * bypy upload /home/nicola/.openclaw/workspace /apps/taiyi/workspace
```

### 配置文件同步

```bash
# 同步配置
bypy sync /home/nicola/.openclaw/workspace-taiyi/config /apps/taiyi/config
```

### 报告归档

```bash
# 自动归档日报/周报
bypy upload /home/nicola/.openclaw/workspace/reports /apps/taiyi/reports
```

---

## 📋 常用命令

| 命令 | 功能 |
|------|------|
| `bypy info` | 查看账号信息 |
| `bypy quota` | 查看配额 |
| `bypy list` | 列出文件 |
| `bypy upload 本地 远程` | 上传 |
| `bypy download 远程 本地` | 下载 |
| `bypy mkdir /路径` | 创建目录 |
| `bypy remove 文件` | 删除 |
| `bypy search 关键词` | 搜索 |

---

## 📁 文件位置

| 项目 | 路径 |
|------|------|
| 配置文件 | `~/.bypy.json` |
| 数据目录 | `~/.bypy` |
| 使用文档 | `docs/baidu-netdisk-connected.md` |

---

## ✅ 集成完成

太一现在可以：
- ✅ 自动备份工作区文件
- ✅ 同步配置文件
- ✅ 归档报告文档
- ✅ 远程文件管理
- ✅ 灾难恢复

---

*太一 AGI 自主配置完成 | 2026-04-10 16:30*
