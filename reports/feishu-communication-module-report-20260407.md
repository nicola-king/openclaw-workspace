# 飞书通讯模块配置报告

**生成时间**: 2026-04-07 13:35  
**查询**: 通讯模块中飞书配置  
**状态**: ✅ 已激活

---

## 📊 飞书应用配置（6 Bot）

| Bot | App ID | App Secret | 状态 |
|-----|--------|------------|------|
| **太一** | cli_a9086d6b5779dcc1 | tXHOop03ZHQynCRuEPkambASNori3KhZ | ✅ |
| **知几** | cli_a90fc49a4b78dcd4 | JARQ374uVMVdnehV88T4IbcPQ2TLGyZl | ✅ |
| **山木** | cli_a93298c9b0789cc6 | Sv6FCgMGTYyg1b33DvDEKdwI76GW5krI | ✅ |
| **素问** | cli_a932968a1338dcc7 | TrVWKrMIVVB0SfwF7AIhYR3dCwThSRLj | ✅ |
| **罔两** | cli_a932999506789cb3 | m02XEFFlRYX6JL3oPDsdYgVdzNdpilpW | ✅ |
| **庖丁** | cli_a9329934c7f85cb0 | P1WOIJddDHrA2fxI5XLowfvo8bSfnHWJ | ✅ |

**配置文件**: `/home/nicola/.openclaw/workspace-taiyi/config/feishu.json`

---

## 🔧 openclaw.json 配置

### 插件启用状态

```json
{
  "plugins": {
    "allow": [
      "openclaw-weixin",
      "feishu",
      "telegram"
    ],
    "load": {
      "paths": [
        "/home/nicola/.npm-global/lib/node_modules/openclaw/dist/extensions/telegram"
      ]
    }
  }
}
```

**状态**: ✅ 飞书插件已启用

---

### Bot 路由配置

**太一 Bot**:
```json
{
  "agentId": "taiyi",
  "match": {
    "channel": "feishu",
    "accountId": "taiyi"
  }
}
```

**知几 Bot**:
```json
{
  "agentId": "zhiji",
  "match": {
    "channel": "telegram",
    "accountId": "zhiji"
  },
  {
    "channel": "feishu",
    "accountId": "zhiji"
  }
}
```

**山木 Bot**:
```json
{
  "agentId": "shanmu",
  "match": {
    "channel": "telegram",
    "accountId": "shanmu"
  },
  {
    "channel": "feishu",
    "accountId": "shanmu"
  }
}
```

**素问 Bot**:
```json
{
  "agentId": "suwen",
  "match": {
    "channel": "telegram",
    "accountId": "suwen"
  },
  {
    "channel": "feishu",
    "accountId": "suwen"
  }
}
```

**罔两 Bot**:
```json
{
  "agentId": "wangliang",
  "match": {
    "channel": "telegram",
    "accountId": "wangliang"
  },
  {
    "channel": "feishu",
    "accountId": "wangliang"
  }
}
```

**庖丁 Bot**:
```json
{
  "agentId": "paoding",
  "match": {
    "channel": "feishu",
    "accountId": "paoding"
  }
}
```

---

## 🛠️ 飞书技能（skills/feishu/）

**文件位置**: `/home/nicola/.openclaw/workspace/skills/feishu/SKILL.md`

**已接入工具**:
- `feishu_doc` - 文档读写
- `feishu_chat` - 消息发送
- `feishu_wiki` - 知识库
- `feishu_drive` - 云盘
- `feishu_bitable` - 多维表格

**用户配置**:
```json
{
  "user_id": "ou_73a52625b0df639c12a8ffb0ceeeeb83",
  "default_app": "docx"
}
```

**触发词**: `['飞书', '文档', '多维表格', '知识库', 'feishu', 'lark', 'doc', 'bitable']`

---

## 📋 飞书工具能力

### feishu_doc（文档操作）

**动作**:
- `read` - 读取文档内容
- `write` - 写入文档内容
- `append` - 追加内容
- `insert` - 插入内容块
- `create` - 创建新文档
- `list_blocks` - 列出文档块
- `get_block` - 获取文档块
- `update_block` - 更新文档块
- `delete_block` - 删除文档块
- `create_table` - 创建表格
- `write_table_cells` - 写入表格单元格
- `insert_table_row` - 插入表格行
- `insert_table_column` - 插入表格列
- `delete_table_rows` - 删除表格行
- `delete_table_columns` - 删除表格列
- `merge_table_cells` - 合并表格单元格
- `upload_image` - 上传图片
- `upload_file` - 上传文件
- `color_text` - 文字着色

---

### feishu_chat（消息操作）

**动作**:
- `members` - 获取群成员
- `info` - 获取群信息
- `member_info` - 获取成员信息

---

### feishu_wiki（知识库操作）

**动作**:
- `spaces` - 获取知识空间
- `nodes` - 获取节点
- `get` - 获取节点内容
- `search` - 搜索知识库
- `create` - 创建节点
- `move` - 移动节点
- `rename` - 重命名节点

---

### feishu_drive（云盘操作）

**动作**:
- `list` - 列出文件/文件夹
- `info` - 获取文件信息
- `create_folder` - 创建文件夹
- `move` - 移动文件/文件夹
- `delete` - 删除文件/文件夹
- `list_comments` - 列出评论
- `list_comment_replies` - 列出评论回复
- `add_comment` - 添加评论
- `reply_comment` - 回复评论

---

### feishu_bitable（多维表格操作）

**动作**:
- `get_meta` - 获取应用元数据
- `list_fields` - 列出字段
- `list_records` - 列出记录
- `get_record` - 获取单条记录
- `create_record` - 创建记录
- `update_record` - 更新记录
- `create_app` - 创建应用
- `create_field` - 创建字段

---

## 🎯 三层智能自动化架构

根据 `TOOLS.md` 记录：

```
【大模型智能自动化】AI 决策/推理/进化 → 本地处理
【网关智能自动化】请求路由/负载均衡 → 智能分发
【通讯智能自动化】多平台消息收发 → 微信/飞书→国内，Telegram→代理
```

**三 Skills 架构**:
- 各自独立：职责分离，互不干扰
- 互联互通：共享数据，协同工作
- 智能路由：根据平台/内容/负载自动选择路径

---

## 📊 配置统计

| 项目 | 数量 | 状态 |
|------|------|------|
| **飞书应用** | 6 个 | ✅ 已配置 |
| **Bot 路由** | 6 Bot | ✅ 已注册 |
| **工具能力** | 5 大类/40+ 动作 | ✅ 可用 |
| **触发词** | 8 个 | ✅ 已配置 |
| **用户 ID** | 1 个 | ✅ ou_73a52625b0df639c12a8ffb0ceeeeb83 |

---

## 🔗 相关文件位置

| 文件 | 路径 |
|------|------|
| **主配置** | `/home/nicola/.openclaw/openclaw.json` |
| **飞书配置** | `/home/nicola/.openclaw/workspace-taiyi/config/feishu.json` |
| **技能文档** | `/home/nicola/.openclaw/workspace/skills/feishu/SKILL.md` |
| **工具记录** | `/home/nicola/.openclaw/workspace/TOOLS.md` |
| **记忆记录** | `/home/nicola/.openclaw/workspace/MEMORY.md` |

---

## 📝 Git 提交

**文档**: `reports/feishu-communication-module-report-20260407.md`  
**Git 提交**: 待提交

---

**报告状态**: ✅ 已完成  
**生成时间**: 2026-04-07 13:35  
**维护者**: 太一 AGI

---

*飞书通讯模块 = 6 Bot 应用 + 5 大类工具 + 40+ 动作*
