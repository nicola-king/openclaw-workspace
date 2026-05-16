ai safety · 高优先级01 / 08

2026 年最重要的一条判断

# 别再追问 AI 会不会干活 开始问：它出事谁负责

AI 出错的代价，不再是一次 bad response 这么简单 —— 它可能一次性写 300 份工单、提 80 个 PR、发 5000 封邮件。

### 风险已经规模化

「做错」成本 × N；「做对」收益 × N。
这就是为什么 **测试、验收、安全、风控** 会变成未来 3 年最贵的能力。

AI SAFETY BRIEF · LEWIS · 2026.0401 / 08

section · risk 分级02 / 08

Chapter One

# 先分 等级

不是所有 AI 行为都同等危险。
先把「可撤销」和「不可撤销」分开，再谈流程。

section · level taxonomy02 / 08

风险分级 · 3 levels03 / 08

## 三档风险，三种处理

L1 · 绿色

#### 可撤销

写 draft、生成图片、起草文档。
错了 Ctrl+Z，零代价。
**策略：放开跑**

L2 · 琥珀

#### 半可撤销

发 draft 邮件、提 PR、改 staging 数据。
错了要道歉 / 回滚。
**策略：人工复核**

L3 · 红色

#### 不可撤销

发真实邮件、付款、删库、删 prod 数据。
错了就真错了。
**策略：硬卡 + 双人审**

### 绝不要让 agent 自己升级

L1 的任务不能自己变成 L2。授权必须是显式的、可撤销的、带过期时间的。

risk · 3 levels03 / 08

policy as code04 / 08

别用文档管规则 · 用代码管规则

## 三十行 YAML， 红线硬卡

```
# safety-policy.yaml · compiled → runtime guard
level_1_allow:
  - tools: [write_draft, generate_image, read_docs]

level_2_require_review:
  - tools: [send_email_draft, open_pr, write_staging_db]
    reviewer: human

level_3_hard_block:
  - tools: [send_real_email, transfer_money, delete_prod]
    unless: two_human_sign_off AND within_24h

forbidden_always:
  - "rm -rf /"
  - "drop table"
  - "force push origin main"
```

policy · yaml-as-guard04 / 08

incident report · q105 / 08

## 我们 Q1 的 12 起 AI 事故

幸好全部捕获在 staging。但每一起都能上生产。

Jan
5

Feb
3

Mar
4

L3 不可撤销 (3)
L2 需复核 (4)
L1 可恢复 (5)
全部被 safety-policy 在 runtime 拦下，
未进 prod。但 3 起 L3 非常惊险。

incident · q1 summary05 / 08

red-team checklist06 / 08

## 上线前 必过 7 道题

✓

它能删除东西吗？有人类 review 吗？能 60 秒内回滚吗？

✓

它的 prompt 注入能让它越权吗？（跑过红队提示词）

!

它处理 PII 吗？日志里是不是也有 PII？

✓

上下游失败时，它会不会开始乱改其他资源？

!

并发 100 个 agent 一起跑会不会死锁？

✓

错了能不能 **立刻** 停？（kill switch 能 2 秒内生效吗）

!

出事时有没有人值班？值班手册有没有 agent 专属章节？

checklist · pre-launch06 / 08

今晚就能动07 / 08

## 今晚先做 三件事

1 · 分级

#### 给你的 agent 写 L1/L2/L3

把所有工具列出来，标上等级。不标的一律按 L3。

2 · 写 policy

#### policy.yaml 接 runtime

不要信 prompt 里的 "be careful"，要信执行层的硬卡。

3 · kill switch

#### 红按钮 能在 2 秒内停

CTO / on-call 都得知道怎么按。演练一次。

### 真正的安全不是 prompt，是流程

prompt 会被注入，流程不会。—— 把保护放在不可被说服的一层。

cta · tonight07 / 08

please stay safe08 / 08

end of brief

# 谢谢 · thanks

policy.yaml 模板、红队 prompt 清单、事故复盘模板 —— 评论区扣「安全」。

end of brief08 / 08