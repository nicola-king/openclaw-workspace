01 / 08

Karpathy LLM Wiki

# 为什么笔记 治不了 LLM

8 种背景、8 张幻灯，一个关于如何把 AI 变成「长期记忆外挂」的最短陈述。**按 → 继续。**

nav · `←` `→` · `space`

cover

02 / 08

Chapter 01

# The Problem.

Token 上限是一个物理事实。你每次和 LLM 说话，它都是一个失忆症患者。

chapter · 01 / 04

section

03 / 08

Symptoms

## 四种你已经 受够的 遗忘。

* 昨天聊过的项目，今天重新解释一遍
* 上下文窗口一到，它开始「编造记忆」
* 不同 session 之间毫无关联，就像第一次见
* 你的真正偏好从未被记住，每次都要 re-prompt

content · list

03

04 / 08

The Fix

## 答案不是 更大 的窗口。

而是：把你的知识、偏好、历史都**写进文件系统**。
让 LLM 每次对话前，先去读那个系统。

### × 窗口 stuffing

把所有东西塞 prompt，贵、慢、最终溢出。

### ✓ 文件 + 检索

按需加载，永远不溢出，结构化可 diff。

content · compare

04

05 / 08

Minimal Setup

## 4 行 YAML 就能开始。

```
memory:
  root: ~/.llm-wiki
  format: markdown
  retrieval: hybrid  # embedding + bm25
```

你现在拥有一个会随时间增长的 **第二大脑**。每次对话它都会被读、被更新。

content · code

05

06 / 08

30-day result

87%

的 re-explain 被消除。平均每次对话节省 **4.2 分钟** 的 re-context。

87%

chart · big-num

06

07 / 08

Start tonight

## 开始 你的 wiki。

不是装又一个插件。是决定：从今晚起，**你的所有 AI 对话都要有一个共同的 vault**。

```
$ mkdir ~/llm-wiki && cd ~/llm-wiki
$ git init
$ echo "# my brain" > README.md
```

cta · three-commands

07

08 / 08

End · thanks for staying

# 謝謝。

Karpathy 的原始 thread + 我的 vault 结构都在 **github.com/lewis/llm-wiki**。欢迎按 ← 再看一遍。

press `←` to rewind · `F` for fullscreen

fin