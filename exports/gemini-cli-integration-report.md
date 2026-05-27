# Gemini CLI 集成太一系统 — 调研与方案报告

> 生成日期：2026-05-27 | 调研范围：GitHub + 官方文档

---

## 一、概述

在 GitHub 搜索 Gemini CLI 优秀项目，评估后集成到太一系统，实现智能自动化识别与调用。

---

## 二、候选项目评估

### 2.1 主选：google-gemini/gemini-cli（Google 官方）

| 项目 | 数据 |
|------|------|
| **仓库** | https://github.com/google-gemini/gemini-cli |
| **说明** | Google 官方开源 AI Agent，把 Gemini 能力带入终端 |
| **安装** | `npm install -g @google/gemini-cli` 或 `brew install gemini-cli` |
| **认证** | Google 账号免费（60次/分钟，1000次/天）+ API Key 付费 |
| **模型** | Gemini 3 系列，100万 token 上下文窗口 |
| **许可** | Apache 2.0 开源 |

**核心能力：**
- ✅ 终端交互式 AI Agent
- ✅ Google 搜索联网（内置 grounding）
- ✅ 文件操作、Shell 命令、网页抓取
- ✅ MCP 协议支持（可扩展自定义工具）
- ✅ 对话 checkpointing（保存恢复）
- ✅ 无头模式（headless，适合脚本自动化）
- ✅ 自定义上下文文件（GEMINI.md）
- ✅ GitHub Action 集成（PR 审核 / Issue 分类）

### 2.2 生态项目备选

| 项目 | 说明 | 集成价值 |
|------|------|---------|
| MCP 服务器扩展 | 官方 MCP 支持，可对接 Imagen/Veo 媒体生成 | 中（可后续扩展）|
| GitHub Action | 自动 PR Review / Issue Triage | 高（可直接配置）|
| 多 Agent 编排工具 | 同时管理 Claude Code / Codex / Gemini CLI | 低（已有太一调度）|

**结论：** 官方 google-gemini/gemini-cli 是唯一选择，功能最全、维护最活跃、生态最成熟。

---

## 三、集成方案

### 3.1 安装

当前系统已安装 Gemini CLI v0.43.0 ✅

### 3.2 认证配置

两种方式：

**方式 A：Google 账号免费认证（推荐起步）**
```bash
# 首次运行自动打开浏览器登录 Google 账号
gemini
# 免费额度：60次/分钟，1000次/天
# 支持 Gemini 3 Flash/Pro，百万上下文
```

**方式 B：API Key（生产环境）**
```bash
export GEMINI_API_KEY="你的API密钥"
gemini
# 从 https://aistudio.google.com/apikey 获取
```

### 3.3 智能调度架构

#### 太一自动调用判断逻辑

```
用户请求
  → 太一分析任务类型
    → 需要联网搜索 + 代码/文件操作？
      → 调用 Gemini CLI（headless 模式）
    → 需要多模型交叉验证？
      → 太一自处理（DeepSeek）+ Gemini CLI 验证
    → 标准问答/分析？
      → 太一直接处理（不动用 Gemini CLI，节省 token）
```

#### 调用场景矩阵

| 场景 | 触发条件 | 调用方式 |
|------|---------|---------|
| 联网搜索验证 | 需要实时信息（股价/新闻/天气） | `gemini -p "提问"` |
| 代码分析 | 需要大上下文代码理解 | `gemini --include-directories ./src -p "..."` |
| 跨模型验证 | 复杂决策需多角度分析 | 太一先推理 → gemini 交叉验证 |
| 文件批量操作 | 需批量处理/转换文件 | gemini headless 模式 |
| 自动 PR 审核 | GitHub PR 需审核 | GitHub Action 自动触发 |

### 3.4 集成方式：Skill 封装

封装为 OpenClaw Skill：

```
skills/gemini-cli/
├── SKILL.md            # 技能定义（触发规则 + 调用方法）
├── scripts/
│   ├── gemini-cli.sh   # CLI 包装脚本
│   └── auto-route.py   # 智能路由逻辑
└── config/
    └── settings.json   # 认证 + 配置
```

SKILL.md 核心触发规则：
- 用户请求涉及实时数据/联网搜索 → 自动调 gemini -p
- 用户请求需百万级上下文分析 → gemini --include-directories
- 复杂决策需交叉验证 → 太一推理后调 gemini 验证
- 手动触发：`/gemini <prompt>` 直接调用 Gemini CLI

---

## 四、实施计划

| 阶段 | 内容 | 预估 |
|------|------|------|
| P0 | ✅ npm 安装已完成（v0.43.0） | 已完成 |
| P1 | 配置 Google 账号认证 + 基础测试 | 5分钟 |
| P2 | 封装 gemini-cli.sh 包装脚本（headless 模式） | 15分钟 |
| P3 | 创建 SKILL.md 定义触发规则 | 10分钟 |
| P4 | 编写 auto-route.py 智能调度 | 30分钟 |
| P5 | 测试各场景调用 | 15分钟 |

---

## 五、注意事项

| 风险 | 缓解措施 |
|------|---------|
| API 配额限制 | 先用免费 Google 账号（1000次/天），后续按需升级 |
| 并发调用冲突 | 封装队列锁，避免与太一主推理同时调用 |
| 响应延迟 | headless 模式设置超时，超时回退到太一处理 |
| Google 账号过期 | 配置自动续期检查 + 通知 SAYELF |

---

## 六、推荐策略

**已完成（P0）：**
1. ✅ `npm install -g @google/gemini-cli` → v0.43.0
2. 下一步：配置 Google 账号认证

**今日内完成（P1-P3）：**
3. 配置认证 + 基础调用验证
4. 创建 Skill 封装（SKILL.md + 包装脚本）
5. 配置智能路由规则

**后续扩展：**
6. 配置 GitHub Action 实现自动 PR 审核
7. 开发自定义 MCP Server 对接太一数据源
8. 与跨境贸易 Agent 联动（Gemini 做多模态分析）

---

**核心结论：** google-gemini/gemini-cli 是官方开源项目，成熟度极高，npm 一键安装，免费额度充足。与太一集成后，可大幅增强联网搜索、大上下文分析、多模型交叉验证能力。建议立即完成认证配置并启用。
