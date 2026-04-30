---
name: multi-bot
tier: 1
trigger: 调度/分配/@bot/协作
enabled: true
depends: [COLLABORATION.md]
---
# 多 Bot 协作调度协议

## 核心架构

```
SAYELF (用户)
    ↓
太一 (总管/AGI) ← 唯一决策入口
    ↓
┌───┬───┬───┬───┬───┐
知几 山木 素问 罔两 庖丁
```

## Bot 职责域

| Bot | 职责 | Telegram | 飞书 |
|-----|------|----------|------|
| **知几** (zhiji) | 量化交易师 | @sayelf_bot | cli_a90fc49a4b78dcd4 |
| **山木** (shanmu) | 内容创意 | @sayelfmedia_bot | cli_a93298c9b0789cc6 |
| **素问** (suwen) | 技术开发 | @sayelfdoctor_bot | cli_a932968a1338dcc7 |
| **罔两** (wangliang) | 数据/CEO | @sayelftrade_bot | cli_a932999506789cb3 |
| **庖丁** (paoding) | 预算成本 | @sayelfCost_bot | cli_a9329934c7f85cb0 |

## 调度流程

### 1. 任务接收
- 所有任务默认由太一接收
- 识别任务类型和职责域

### 2. 任务分解
```
单域任务 → 直接分配给对应 Bot
跨域任务 → 太一拆解 → 分配给多个 Bot
```

### 3. 执行方式

**方式 A：群聊@bot（用户直接）**
```
在 Telegram/飞书群聊中：
@sayelf_bot 分析市场 → 知几直接回复
```

**方式 B：太一代发（私聊或跨平台）**
```
用户 → 太一 → 调用 Bot API → 汇总 → 用户
```

### 4. 结果汇总
- Bot 完成回报太一
- 太一整合多 Bot 结果
- 统一反馈给 SAYELF

## 平台配置

### Telegram
- **群聊名**: `🤖 太一 Bot 团队` (待创建)
- **交互方式**: `@bot_username 指令`
- **Token 管理**: 见 TOOLS.md

### 飞书
- **群聊 ID**: `oc_ea68a9a6efcbe729666de2343f790cb7`
- **群名**: `🤖 太一 Bot 团队测试`
- **交互方式**: `@bot 名称 指令`
- **App 配置**: 见 TOOLS.md

## 协作规则

1. **太一优先**: 所有消息默认经太一，除非群内直接@bot
2. **Bot 间讨论**: 允许 Bot 在群内@对方讨论
3. **太一裁决**: 有分歧时太一有最终决定权
4. **禁止绕过**: Bot 不得绕过太一直接下结论

## 升级条件

太一必须亲自处理（不得下发）：
- 宪法修订
- 新 Bot/系统接入
- SAYELF 明确点名太一
- 跨域任务出现分歧

## 故障处理

| 问题 | 解决方案 |
|------|----------|
| Bot 无响应 | 检查权限/群聊成员状态 |
| 消息发送失败 | 重新获取 access_token |
| Bot 不在群聊 | 手动添加到群聊 |
| 权限不足 | 飞书开放平台开通 `im:message:send` |

## 快速命令

```bash
# 测试 Bot 连接 (飞书)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"receive_id":"oc_ea68a9a6efcbe729666de2343f790cb7","msg_type":"text","content":"{\"text\":\"测试\"}"}'

# 获取 Bot Token
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'
```

---
*最后更新：2026-03-22 | 版本：1.0*
