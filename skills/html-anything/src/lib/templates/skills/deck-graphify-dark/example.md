01 / 08

Tech Sharing · 纯干货

# 手把手用 Graphify 搭建个人知识图谱

一行命令 · 全多模态 · 诚实审计 —— 把任何文件夹变成可导航的知识网络。

↑ 背景就是 Graphify 真实跑出来的知识图谱

02 / 08

Part 01

# Why Graph?

folder → tree → graph，人类认知的下一步

03 / 08

Feature Map

## 一个工具，四件事

📂

#### Folder Ingest

递归扫描任意路径，支持 md / pdf / 代码 / 图片

🧠

#### Entity Extract

用 LLM 抽概念、人物、事件、关系

🕸️

#### Force Graph

D3 力导向，点击即跳转原文

🔍

#### Audit Trail

每条边都能追溯到 source span

它不是「又一个 RAG」—— 它是 把检索结果画出来，让你一眼就知道信息长什么样。

04 / 08

One command

## 从 0 到图谱，大概 90 秒

$ graphify ~/notes --out ./graph

```
# graphify.config.yaml
ingest:
  paths: [~/notes, ~/code/docs]
  include: ["*.md", "*.pdf", "*.py"]

extract:
  model: claude-opus-4-6
  schema: [concept, person, event, relation]

render:
  engine: d3-force
  audit: true     # 每条边带 source span
```

05 / 08

Efficiency Race

## 没有知识库 vs 有知识库

没有
知识库

🛵

反复喂信息…整理…又忘了…

有
知识库

🏎️

AI 自己找 → 确认 → 干活!

5×

速度提升

-80%

重复喂信息

∞

记忆持久化

06 / 08

Pipeline

## 端到端 4 步走

📂

Scan

递归读文件

→

🔬

Extract

LLM 抽实体

→

🕸️

Build

构图 + 去重

→

🎨

Render

D3 交互图

每一步都有 audit log：你永远知道某个节点为什么存在、它来自哪个文件的哪一行。

07 / 08

Try it tonight

## Graphify your folders

$ npm i -g @lewis/graphify

$ graphify ~/obsidian-vault

#knowledge-graph
#open-source
#claude-agent
#obsidian
#d3-force

08 / 08

Thanks.

github.com/lewis/graphify · 欢迎 star / issue / PR