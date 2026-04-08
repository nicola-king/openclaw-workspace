---
skill: ssh-control
version: 1.0.0
author: 太一
created: 2026-03-10
updated: 2026-04-04
status: stable
triggers: ['SSH', '远程控制', '系统状态', '运维操作', 'ssh', 'remote', 'system status']
permissions: ['exec', 'file_read']
max_context_tokens: 3000
priority: 2
description: SSH 远程控制本机或其他设备
tags: ['ssh', 'remote', 'ops']
config: {'default_host': 'nicola@192.168.2.242', 'require_confirmation': True}
category: tools
---



# SSH 控制技能

## 目标主机
- 本机：nicola@192.168.2.242（免密已配置）

## 使用方式
- 太一：远程查看系统状态
- 素问：执行技术运维操作

## 安全规则
- 破坏性操作需向太一确认
- 不执行删除系统文件的命令
