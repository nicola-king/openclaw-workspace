~/hermes · zsh · 118x42 · 01:37:04

whoami --hermes

# HERMES AGENT / v0.9.2

一个号称能「自主跑完整软件工程任务」的命令行 agent。
真的好用？还是又一轮营销？—— 我连续跑了 72 小时，告诉你答案。

rust-core
mcp-native
72h-benchmark
honest-review

hermes-review · lewis · 202601 / 08

section · 01/04

cat chapter\_01.md

# // Setup

从 `brew install hermes` 到第一次 prompt —— 一共 4 分 22 秒。

section · setup02 / 08

benchmark · cold-start

## 开箱数据

cold start → first-successful-task 三次平均

install time

42s

单 binary，无 docker，无 python env。

first token

1.8s

接入 claude-opus-4-6，无预热。

first PR merged

4m22s

跑的是 fix-a-typo 级别的低难度任务。

// verdict +

冷启动是真的快

和 OpenClaw 的 docker + pip 流程比，快不止一个数量级。

// verdict -

MCP 服务器配置不够友好

env 变量需要手动塞进 ~/.hermes/env，文档几乎没写。

data · verified 3 runs03 / 08

trace · hermes run

hermes run "refactor auth module to use pkce"

### ↓ 真实 trace (节选)

```
# hermes v0.9.2 · session 42a1
[plan]    "分析 src/auth/*.ts → 找 oauth flow → 抽成 pkce"
[read]    src/auth/oauth.ts       // 214 lines
[read]    src/auth/token.ts       // 88 lines
[think]   "发现 implicit flow，改为 code+pkce，需新 state param"
[edit]    src/auth/oauth.ts       +43 -17
[edit]    src/auth/token.ts       +12 -4
[test]    pnpm vitest auth        PASS 18/18
[commit]  "feat(auth): migrate to oauth2 code+pkce"
[push]    origin feat/pkce-auth   ok

# 总耗时 3m 14s · 14k tokens · $0.21
```

trace · live04 / 08

benchmark · hermes vs openclaw

## 72 小时对比

同一组 48 个 GitHub issue，两个 agent 各跑一遍

100%
75%
50%
25%
0

82%
resolved

58%
one-shot

89%
test-pass

71%
pr-merged

60%
resolved

38%
one-shot

67%
test-pass

hermes 0.9.2

openclaw 2.1

benchmark · n=4805 / 08

tldr

echo $VERDICT

7.8/ 10

值得装，还不值得完全依赖。

+ strong points

• rust 本体冷启快
• trace 可读性极强
• diff 审核友好，commit message 也写得合格

- weak points

• plan 阶段偶尔跳步
• 超 50k LoC 仓库会 OOM
• MCP 配置需要手动塞 env

verdict · honest06 / 08

install

## 想自己跑一遍？

三条命令，不到 5 分钟就能看见它干第一件事。

```
# 1. install
$ brew install hermes-agent/tap/hermes

# 2. auth (先准备好 anthropic api key)
$ hermes auth login

# 3. first task
$ cd ~/your-repo && hermes run "add a CHANGELOG.md from git log"
```

brew-ready
opus-4.6
needs-api-key

try-it-now07 / 08

EOF

exit 0

# // thanks

完整 trace、48 个任务的 PR 列表、benchmark 脚本都在 github.com/lewis/hermes-review

session closed08 / 08