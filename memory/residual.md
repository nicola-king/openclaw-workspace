# Residual Memory - 太一残差记忆

> 最后更新：2026-03-26 17:45 | 1-bit 纠错标记 | 状态：🟡 按需加载

---

## 使用说明

本文件存储**细节信息**和**边缘案例**，采用 1-bit 标记设计：
- `[✓]` = 已验证/已完成
- `[!]` = 需注意/有例外
- `[?]` = 待确认/有疑问
- `[→]` = 有依赖/需跟进

---

## 配置细节

### 飞书应用完整配置
| Bot | App ID | App Secret | 备注 |
|-----|--------|------------|------|
| 太一 | cli_a9086d6b5779dcc1 | tXHOop03ZHQynCRuEPkambASNori3KhZ | [✓] 已验证 |
| 知几 | cli_a90fc49a4b78dcd4 | JARQ374uVMVdnehV88T4IbcPQ2TLGyZl | [✓] 已验证 |
| 山木 | cli_a93298c9b0789cc6 | Sv6FCgMGTYyg1b33DvDEKdwI76GW5krI | [!] Gemini 需配置 |
| 素问 | cli_a932968a1338dcc7 | TrVWKrMIVVB0SfwF7AIhYR3dCwThSRLj | [✓] 已验证 |
| 罔两 | cli_a932999506789cb3 | m02XEFFlRYX6JL3oPDsdYgVdzNdpilpW | [✓] 已验证 |
| 庖丁 | cli_a9329934c7f85cb0 | P1WOIJddDHrA2fxI5XLowfvo8bSfnHWJ | [✓] 已验证 |

### 微信公众号开发配置
| 项目 | 配置 | 状态 |
|------|------|------|
| **AppID** | wx720a4c489fec9df3 | [✓] 已获取 |
| **AppSecret** | 🟡 待获取 | [→] 开发→基本配置 |
| **Token** | 待设置 | [→] 服务器配置 |
| **EncodingAESKey** | 待生成 | [→] 服务器配置 |

---

## 技术细节

### CAD 工具版本
| 工具 | 版本 | 安装命令 | 备注 |
|------|------|---------|------|
| LibreCAD | 2.2.0.2-1build3 | `apt install librecad` | [✓] 2D 图纸 |
| FreeCAD | 0.21.2 | `apt install freecad` | [✓] 3D 建模 |

### Clash 代理配置
| 项目 | 配置 |
|------|------|
| **端口** | 7890 |
| **协议** | HTTP/SOCKS5 |
| **systemd 服务** | /etc/systemd/system/clash.service |

---

## 边缘案例记录

### 会话压缩触发
- [!] context > 80K → 建议压缩
- [!] context > 100K → 强制压缩
- [✓] 压缩后写入今日 memory 文件

### Bot 委派边界
- [→] 知几：量化交易（置信度>90% 自动执行）
- [→] 素问：技术开发（需确认 API 变更）
- [!] 山木：内容创意（需人工审核敏感内容）
- [→] 罔两：数据分析（只读权限）
- [!] 庖丁：预算（>$100 需确认）

---

## 历史归档索引

| 日期 | 文件 | 关键事件 |
|------|------|---------|
| 2026-03-24 | memory/2026-03-24.md | 太一独立日，MEMORY.md 创建 |
| 2026-03-23 | memory/2026-03-23.md | 微信接入成功 |
| 2026-03-22 | memory/2026-03-22.md | 多 Bot 架构确立 |

---

## 待确认事项

- [?] Claude API 注册状态（TASK-004）
- [?] Discord 邀请链接获取（TASK-037）
- [?] 小红书发布排期（TASK-031）

---

*创建时间：2026-03-26 17:45 | TurboQuant Residual v1.0 | 按需加载*
