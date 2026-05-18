# rtk-ai/rtk 蒸馏笔记

> 蒸馏时间：2026-05-19 00:39 | 来源：rtk-ai/rtk (GitHub)
> ★ 49.6K | MIT | Rust | v0.35+

---

## 项目画像

CLI 代理，拦截 AI 工具与 Shell 之间的命令输出，压缩后送入 LLM 上下文。

## 核心指标

- 2,927 条命令实测：89.2% 噪音去除
- 输入 11.6M → 输出 1.4M tokens
- 支持 100+ 命令，13 个 AI 工具
- 单 Rust 二进制，零依赖，<10ms 延迟

## 精华吸收

1. **四种过滤策略**：Smart Filtering / Grouping / Truncation / Deduplication
2. **测试输出91.8%压缩**：262 tests → 20行摘要
3. **自钩子模式**：透明重写，无感集成
4. **rtk gain 仪表盘**：量化 token 节省
5. **Git 命令 80%**、find 78%、grep 49% 节省
6. **DevOps 扩展**：AWS 25个子命令、Docker、K8s、GH CLI

## 融入位置

- `constitution/directives/RTK-TOKEN-EFFICIENCY.md` — 重写更新

## 不采用

- RTK 二进制本身（太一通过 OpenClaw exec，不直接对接 Shell）
- ICM / Vox（上下文管理/语音模块，与现有冲突）
