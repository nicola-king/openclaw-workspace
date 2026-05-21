---
name: opencliz
description: Zig CLI Hub — 把任何网站/工具转为标准化 CLI，AI Agent 自动发现调用
version: 0.1.0
author: zouyee/opencliz
tags: [cli, tools, agent, runtime]
---

# OpenCLI-Z — 太一集成

Zig 原生实现的 CLI Hub。把任何网站/本地工具封装成统一的 CLI 接口。

## 用法

```bash
# 列出可用的 CLI 工具
opencliz list

# 运行某个工具
opencliz run <tool-name> [args...]

# 查看工具文档
opencliz help <tool-name>
```

## 集成路径

`~/.local/bin/opencliz` — 已安装，太一 Agent 可调用的高性能 CLI 运行时。

配置文件: `~/.opencli/config.yaml`
插件目录: `~/.opencli/plugins/`
