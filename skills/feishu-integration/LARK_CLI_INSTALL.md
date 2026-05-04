# 飞书 Lark CLI 安装记录

> **时间**: 2026-05-04
> **版本**: lark-cli v1.0.23
> **状态**: ✅ 已安装，等待身份绑定

---

## 安装步骤

### 步骤1: 安装 CLI ✅

```bash
npm install -g @larksuite/cli
```

**结果**: ✅ 成功
- 安装路径: `/home/sayelf/.npm-global/lib/node_modules/@larksuite/cli/`
- 版本: 1.0.23

### 步骤2: 安装 CLI Skills ✅

```bash
npx -y skills add https://open.feishu.cn --skill -y
```

**结果**: ✅ 成功
- 安装路径: `~/.openclaw/workspace/.agents/skills/`
- 技能数: 20+ 个

### 已安装技能列表

| 技能 | 功能 |
|------|------|
| lark-approval | 审批 |
| lark-attendance | 考勤 |
| lark-base | 多维表格 |
| lark-calendar | 日历 |
| lark-contact | 通讯录 |
| lark-doc | 文档 |
| lark-drive | 云盘 |
| lark-event | 活动 |
| lark-im | 即时消息 |
| lark-mail | 邮件 |
| lark-markdown | Markdown |
| lark-minutes | 会议记录 |
| lark-openapi-explorer | API 探索 |
| lark-sheets | 表格 |
| lark-skill-maker | 技能制作 |
| lark-slides | 幻灯片 |
| lark-task | 任务 |
| lark-vc | 视频会议 |
| lark-whiteboard | 白板 |
| lark-wiki | 知识库 |
| lark-workflow-meeting-summary | 会议总结 |
| lark-workflow-standup-report | 日报 |

---

## 环境配置

### PATH 设置

```bash
export PATH="/home/sayelf/.npm-global/lib/node_modules/@larksuite/cli/bin:$PATH"
```

### 验证安装

```bash
lark-cli --version
# 输出: lark-cli version 1.0.23
```

---

## 下一步: 身份绑定

**请选择身份模式：**

| 模式 | 说明 | 命令 |
|------|------|------|
| **bot-only** | Bot 身份，适合群聊/通知 | `lark-cli config bind --identity bot-only` |
| **user-default** | 用户身份，访问个人数据 | `lark-cli config bind --identity user-default` |

**⚠️ 警告**: 如果选择 user 模式，不要将此 Bot 分享给他人或添加到群聊 — 它可以访问你的个人飞书数据。

---

## 使用示例

### 查看日历
```bash
lark-cli calendar +agenda
```

### 搜索用户
```bash
lark-cli contact +search-user --query "用户名"
```

### 发送消息
```bash
lark-cli im +send --user_id "用户ID" --content "消息内容"
```

### 查看帮助
```bash
lark-cli --help
lark-cli calendar --help
```

---

## 文档参考

- [飞书 CLI 官方文档](https://open.feishu.cn/document/mcp_open_tools/feishu-cli/set-up-lark-cli-for-ai-agents-in-openclaw_hermes.md)
- [飞书开放平台](https://open.feishu.cn/)

---

*太一 AGI · 飞书 CLI 安装记录*
