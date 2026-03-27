# TOOLS.md - Local Notes

## 核心原则

**免费开源优先：**
- ✅ 优先采用免费开源方案
- ❌ 避免付费工具（除非必要）
- ✅ 自托管优先于云服务
- ✅ 社区活跃项目优先

---

## Telegram Bots (子代理)

| 名称 | Bot Username | Bot ID | Token |
|------|--------------|--------|-------|
| zhiji (知几) | @sayelf_bot | 8563369264 | `AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E` |
| shanmu (山木) | @sayelfmedia_bot | 8731213565 | `AAHzAnm8lUG2riIuhHyYrxYrzixZ0zibcxo` |
| suwen (素问) | @sayelfdoctor_bot | 8632190716 | `AAFR9k4811ISyQ4tTbn99G9GmtMNsgdkL6w` |
| wangliang (罔两) | @sayelftrade_bot | 8635135614 | `AAEnppb2absodyReJDX-qZAoERP29YFuh1c` |
| paoding (庖丁) | @sayelfCost_bot | 8610739795 | `AAGvKpqunuyBZlB4sgZwrsly4j1LVMJa728` |

**实际用途：**
- **zhiji** (知几) → 量化交易师
- **shanmu** (山木) → 内容创意
- **suwen** (素问) → **技术开发主管**（系统维护 + 新功能开发）
- **wangliang** (罔两) → 数据/CEO
- **paoding** (庖丁) → 预算成本

---

## 飞书应用配置

| 名称 | App ID | App Secret | 用途 |
|------|--------|------------|------|
| **taiyi** (太一) | `cli_a9086d6b5779dcc1` | `tXHOop03ZHQynCRuEPkambASNori3KhZ` | AGI 总管 |
| **zhiji** (知几) | `cli_a90fc49a4b78dcd4` | `JARQ374uVMVdnehV88T4IbcPQ2TLGyZl` | 量化交易师 |
| **shanmu** (山木) | `cli_a93298c9b0789cc6` | `Sv6FCgMGTYyg1b33DvDEKdwI76GW5krI` | 内容创意 |
| **suwen** (素问) | `cli_a932968a1338dcc7` | `TrVWKrMIVVB0SfwF7AIhYR3dCwThSRLj` | **技术开发主管** |
| **wangliang** (罔两) | `cli_a932999506789cb3` | `m02XEFFlRYX6JL3oPDsdYgVdzNdpilpW` | 数据/CEO |
| **paoding** (庖丁) | `cli_a9329934c7f85cb0` | `P1WOIJddDHrA2fxI5XLowfvo8bSfnHWJ` | 预算成本 |

---

## 微信公众号配置

| 项目 | 配置 |
|------|------|
| **名称** | SAYELF 山野精灵 |
| **公众号 ID** | `Sayelf_tea` |
| **地区** | 重庆 九龙坡 |
| **实名认证** | ✅ 已实名 |
| **登录邮箱** | 285915125@qq.com |
| **状态** | ✅ 已认证，待发布 |
| **用途** | 内容分发/品牌建立 |
| **账号简介** | 茶与禅的美学探索者 \| 分享生活中的宁静片刻 \| 用科技让东方美学触手可及 \| 提供专业治愈 AI 生成工具 |
| **技能** | md2wechat-skill (已安装) |

---

## 微信个人号配置

| 项目 | 配置 |
|------|------|
| **微信号** | `sayelf-tea` |
| **状态** | ✅ 已连接 |
| **说明** | 账号唯一凭证，一年只能修改一次 |
| **用途** | 个人微信接入/测试 |

---

## 部署方案（免费开源优先）

| 工具 | 用途 | 成本 | 状态 |
|------|------|------|------|
| **Coolify** | 应用部署 | ✅ 免费 | 🟡 待部署 |
| **CapRover** | 应用部署 | ✅ 免费 | ✅ 备选 |
| **Dokku** | 轻量部署 | ✅ 免费 | ✅ 备选 |
| **Railway** | ❌ 已放弃 | $5/月 | ❌ 不采用 |

**Coolify 部署：**
- 官网：https://github.com/coollabsio/coolify
- 一键安装：`curl -fsSL https://cdn.coollabs.io/coolify.sh | bash`
- 成本：✅ $0/月（自托管）

---

## CAD 工具配置（免费开源）

| 工具 | 用途 | 成本 | 状态 |
|------|------|------|------|
| **LibreCAD** | 2D CAD 图纸查看/编辑 | ✅ 免费 | 🟡 待安装 |
| **FreeCAD** | 3D CAD 建模 | ✅ 免费 | 🟡 待安装 |
| **ODA** | ❌ 已放弃 | 付费 | ❌ 不采用 |

**下载链接：**
- LibreCAD: https://librecad.org/
- FreeCAD: https://www.freecad.org/

**用途：** 跨境外贸通用发动机图纸处理

---

## AI 模型配置（成本优化）

| 模型 | 用途 | 成本 | 状态 |
|------|------|------|------|
| **通义千问** | 默认模型 | ¥0-50/月 | ✅ 已配置 |
| **Claude** | 代码增强 | 🟡 待注册 | 🟡 待确认 |
| **开源模型** | 自托管 | ✅ 免费 | 🟡 待配置 |
| **Gemini 2.0** | AI 生图 | ✅ 免费额度 | 🟡 **待配置 API Key** |

### Gemini API 配置

**用途**: 山木 AI 生图工作流（公众号配图/海报生成）

**配置方式**:
```bash
export GEMINI_API_KEY="AIzaSy..."  # 添加到 ~/.bashrc
```

**获取 Key**: https://aistudio.google.com/apikey

**文档**: `skills/shanmu/AI_IMAGE_SETUP.md`

---

## 重要账号

| 平台 | 账号 | 状态 |
|------|------|------|
| **Telegram** | @nicola king (7073481596) | ✅ 已配置 |
| **微信个人号** | sayelf-tea | ✅ 已连接 |
| **微信公众号** | Sayelf_tea (SAYELF 山野精灵) | ✅ 已认证 |
| **小红书** | SAYELF | 🟡 待发布 |
| **GitHub** | 待配置 | 🟡 待配置 |
| **Twitter/X** | 待配置 | 🟡 待配置 |

---

*最后更新：2026-03-23 21:32 | 状态：✅ 免费开源优先原则已确认*
