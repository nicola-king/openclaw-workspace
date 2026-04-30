# 🎭 agency-agents 项目蒸馏报告

> 分析时间：2026-04-16 | 项目地址：github.com/msitarzewski/agency-agents | 太一 AGI  distilled

---

## 一、项目核心信息

| 维度 | 详情 |
|------|------|
| **仓库名称** | `agency-agents` |
| **作者** | `msitarzewski` |
| **Agent 数量** | **226 个** (已确认) |
| **分类体系** | 11 个 Division (部门) |
| **支持工具** | 10+ 种 (Claude Code/OpenClaw/Cursor 等) |
| **许可证** | MIT |
| **核心特点** | 人格化 + 专业化 + 可交付成果 |

---

## 二、核心架构分析

### 2.1 Agent 分类体系（11 个 Division）

| Division | Agent 数量 | 职责域 | 代表 Agent |
|----------|-----------|--------|-----------|
| **Engineering** | ~30 | 工程技术 | Frontend Developer, Backend Architect, DevOps |
| **Design** | ~8 | 设计创意 | UI Designer, UX Researcher, Brand Guardian |
| **Paid Media** | ~7 | 付费媒体 | PPC Strategist, Search Query Analyst |
| **Sales** | ~9 | 销售 | Outbound Strategist, Deal Strategist |
| **Marketing** | ~28 | 市场营销 | Growth Hacker, TikTok Strategist, Xiaohongshu |
| **Product** | ~2 | 产品 | Sprint Prioritizer, Trend Researcher |
| **Support** | ~? | 客户支持 | - |
| **Strategy** | ~? | 战略规划 | - |
| **Specialized** | ~? | 专业技能 | Sales Outreach |
| **Game Development** | ~? | 游戏开发 | - |
| **Academic** | ~? | 学术研究 | - |
| **Finance** | ~? | 金融财务 | - |
| **Spatial Computing** | ~? | 空间计算 | - |
| **Testing** | ~? | 测试 | - |
| **Integrations** | ~? | 集成 | - |

---

### 2.2 单个 Agent 结构（标准模板）

```markdown
---
name: [Agent 名称]
description: [一句话描述]
color: [颜色标识]
emoji: [Emoji 图标]
vibe: [风格氛围描述]
---

# [Agent Name] Agent Personality

## 🧠 Identity & Memory (身份与记忆)
- **Role**: [角色定位]
- **Personality**: [性格特征]
- **Memory**: [记忆机制]
- **Experience**: [经验背景]

## 🎯 Core Mission (核心使命)
### 职责 1
- 具体任务描述
- 技术实现方式
- **Default requirement**: 默认要求

### 职责 2
- ...

## 🚨 Critical Rules (关键规则)
### 规则类别 1
- 必须遵守的规则 1
- 必须遵守的规则 2

### 规则类别 2
- ...

## 📋 Technical Deliverables (技术交付物)
### 示例 1
```[语言]
// 代码示例
```

### 示例 2
- 流程示例
- 输出模板

## ✅ Success Metrics (成功指标)
- 可量化的成功标准 1
- 可量化的成功标准 2

## 💬 Communication Style (沟通风格)
- 沟通偏好
- 语言风格
- 交互方式
```

---

## 三、核心优势分析

### 3.1 设计优势

| 优势 | 说明 | 太一借鉴点 |
|------|------|-----------|
| **人格化设计** | 每个 Agent 有独特性格/vibe | ✅ 太一 Bot 已有类似设计 |
| **交付物导向** | 提供代码示例/流程模板 | ✅ 可增强交付物模板库 |
| **成功指标** | 量化成功标准 | ⭐ 太一需补充 |
| **沟通风格** | 明确交互偏好 | ✅ 太一 Bot 已有定义 |
| **分类清晰** | 11 个 Division 职责明确 | ⭐ 可优化太一分类 |

### 3.2 技术优势

| 优势 | 实现方式 | 太一借鉴点 |
|------|---------|-----------|
| **多工具集成** | convert.sh + install.sh | ⭐⭐ 立即学习 |
| **安装脚本** | 支持 10+ 工具一键安装 | ⭐⭐ 立即学习 |
| **国际化支持** | i18n 目录 + 多语言 | ⭐ 可选增强 |
| **质量检查** | lint-agents.sh 检查 Agent 质量 | ⭐⭐ 立即学习 |
| **文档完善** | CONTRIBUTING + 示例 | ✅ 太一已有 |

### 3.3 生态优势

| 优势 | 说明 | 太一现状 |
|------|------|---------|
| **工具覆盖** | Claude Code/Cursor/OpenClaw 等 10+ | 主要 OpenClaw |
| **社区贡献** | 43 PRs + 36 Issues | 太一需增强 |
| **GitHub 曝光** | 小红书推广 + 社区传播 | 太一需学习 |
| **商业化** | GitHub Sponsor | 太一可考虑 |

---

## 四、关键代码分析

### 4.1 安装脚本核心逻辑

```bash
# install.sh 核心功能

# 1. 多工具支持
install_claude_code() {
  mkdir -p ~/.claude/agents
  cp engineering/*.md ~/.claude/agents/
  ok "Installed to Claude Code"
}

install_openclaw() {
  mkdir -p ~/.openclaw/agency-agents
  cp -r . ~/.openclaw/agency-agents/
  ok "Installed to OpenClaw"
}

# 2. 交互式选择
interactive_select() {
  tools=("claude-code" "copilot" "openclaw" "cursor" "all")
  # 使用 select 菜单
}

# 3. 并行安装
parallel_install() {
  for tool in "${selected_tools[@]}"; do
    install_$tool &
  done
  wait
}
```

### 4.2 转换脚本核心逻辑

```bash
# convert.sh 核心功能

# 1. 为不同工具生成适配文件
convert_for_claude_code() {
  # 生成 .md 格式
}

convert_for_cursor() {
  # 生成 .mdc 格式
}

convert_for_openclaw() {
  # 生成 SKILL.md 格式
}

# 2. Frontmatter 处理
process_frontmatter() {
  # 解析 YAML frontmatter
  # 转换为目标工具格式
}
```

### 4.3 Agent 质量检查

```bash
# lint-agents.sh 核心功能

# 1. 检查必要字段
check_required_fields() {
  # name/description/vibe 必须存在
}

# 2. 检查代码示例
check_code_examples() {
  # 至少有 1 个代码块
}

# 3. 检查可读性
check_readability() {
  # 标题层级/列表格式/链接有效性
}
```

---

## 五、太一系统对比分析

### 5.1 Agent 数量对比

| 系统 | Agent 数量 | 分类数 | 覆盖领域 |
|------|-----------|--------|---------|
| **agency-agents** | 226 | 11 | 工程/设计/市场/销售/产品 |
| **太一系统** | 60+ | 7 | 交易/内容/系统/监控/成本 |

**差距**：太一 Agent 数量少 166 个，但垂直领域更深

### 5.2 设计对比

| 维度 | agency-agents | 太一系统 | 优劣 |
|------|--------------|---------|------|
| **人格化** | ✅ 强 (vibe/emoji) | ✅ 强 (SOUL.md) | 平手 |
| **交付物** | ✅ 代码示例丰富 | ✅ 有但较少 | 太一需增强 |
| **成功指标** | ✅ 量化明确 | ❌ 较少 | 太一需补充 |
| **多工具** | ✅ 10+ 工具 | ❌ 主要 OpenClaw | 太一需扩展 |
| **自进化** | ❌ 无 | ✅ 有 | 太一领先 |
| **协作机制** | ❌ 无 | ✅ 多 Bot 协作 | 太一领先 |
| **宪法约束** | ❌ 无 | ✅ 有 | 太一领先 |

### 5.3 工程化对比

| 维度 | agency-agents | 太一系统 | 优劣 |
|------|--------------|---------|------|
| **安装脚本** | ✅ 完善 | ❌ 无 | 太一需学习 |
| **质量检查** | ✅ lint 脚本 | ❌ 无 | 太一需学习 |
| **转换工具** | ✅ convert.sh | ❌ 无 | 太一需学习 |
| **文档** | ✅ 完善 | ✅ 完善 | 平手 |
| **社区** | ✅ 活跃 | ⚠️ 发展中 | 太一需增强 |

---

## 六、立即融合清单

### 6.1 P0 级（本周内完成）

| 任务 | 说明 | 优先级 |
|------|------|--------|
| **1. 安装脚本** | 创建 `install.sh` 支持多工具部署 | P0 |
| **2. 质量检查** | 创建 `lint-agents.sh` 检查 Agent 质量 | P0 |
| **3. 成功指标** | 为现有 60+ Agent 补充成功指标 | P0 |
| **4. 交付物模板** | 增强 Agent 的代码示例/模板库 | P0 |

### 6.2 P1 级（本月内完成）

| 任务 | 说明 | 优先级 |
|------|------|--------|
| **5. 转换工具** | 创建 `convert.sh` 生成多工具格式 | P1 |
| **6. 分类优化** | 借鉴 11 Division 优化太一分 | P1 |
| **7. 新增 Agent** | 补充缺失领域 (游戏/学术/金融等) | P1 |
| **8. GitHub 推广** | 学习小红书推广策略 | P1 |

### 6.3 P2 级（下季度完成）

| 任务 | 说明 | 优先级 |
|------|------|--------|
| **9. 国际化** | i18n 支持 (中英双语) | P2 |
| **10. 商业化** | GitHub Sponsor 配置 | P2 |
| **11. 社区运营** | Issues/PRs 激励机制 | P2 |
| **12. 生态建设** | 支持更多 AI 工具 | P2 |

---

## 七、可复用的 Agent 设计

### 7.1 太一缺失的 Agent（建议新增）

| Agent | 职责域 | 优先级 |
|------|--------|--------|
| **Technical Writer** | 技术文档撰写 | P1 |
| **Code Reviewer** | 代码审查 | P1 |
| **SRE** | 站点可靠性工程 | P1 |
| **UX Researcher** | 用户研究 | P2 |
| **Growth Hacker** | 增长黑客 | P1 |
| **SEO Specialist** | SEO 优化 | P1 |
| **TikTok Strategist** | TikTok 运营 | P2 |
| **Podcast Strategist** | 播客策略 | P2 |

### 7.2 可直接借鉴的 Agent 模板

**示例：Frontend Developer**
```markdown
---
name: Frontend Developer
description: 前端开发专家，专注于 React/Vue/Angular 和性能优化
emoji: 🖥️
vibe: 注重细节、性能导向、用户中心、技术精确
---

## 🎯 核心使命

### 编辑器集成工程
- 构建编辑器扩展（navigation commands）
- 实现 WebSocket/RPC 桥接
- 确保<150ms 延迟

### 现代 Web 应用开发
- 响应式设计 + 可访问性
- 性能优化（Core Web Vitals）
- PWA + 离线支持

### 代码质量
- 单元测试 + 集成测试
- TypeScript + 现代工具链
- CI/CD 集成

## ✅ 成功指标
- Lighthouse 分数≥90
- Core Web Vitals 全绿
- 测试覆盖率≥80%
```

---

## 八、融合实施计划

### 8.1 第 1 周：基础设施建设

```bash
# Day 1-2: 创建 install.sh
- 支持 OpenClaw/Claude Code/Cursor
- 交互式选择
- 并行安装

# Day 3-4: 创建 lint-agents.sh
- 检查必要字段
- 检查代码示例
- 检查可读性

# Day 5-7: 补充成功指标
- 为 60+ Agent 添加成功指标
- 为 60+ Agent 增强交付物模板
```

### 8.2 第 2-4 周：Agent 扩充

```
Week 2: Engineering Division (新增 10 个)
Week 3: Marketing Division (新增 15 个)
Week 4: Design + Support (新增 10 个)
```

### 8.3 第 2-3 月：生态建设

```
Month 2: 多工具集成 + 转换工具
Month 3: 社区运营 + GitHub 推广
```

---

## 九、太一独特优势（保持并增强）

| 优势 | 说明 | 如何增强 |
|------|------|---------|
| **自进化系统** | 能力涌现 + 自动创建 | ✅ 继续强化 |
| **多 Bot 协作** | 辩论投票 + 太一裁决 | ✅ 继续强化 |
| **宪法约束** | 负熵法则 + 价值基石 | ✅ 继续强化 |
| **TurboQuant 记忆** | 4 层记忆架构 | ✅ 继续强化 |
| **中文优化** | 深度中文支持 | ✅ 继续强化 |

---

## 十、行动总结

### 立即执行（今天）

1. ✅ 创建 `install.sh` 脚本框架
2. ✅ 创建 `lint-agents.sh` 脚本框架
3. ✅ 为 3 个核心 Agent 补充成功指标

### 本周完成

1. ✅ 完成 install.sh 支持 OpenClaw
2. ✅ 完成 lint-agents.sh 基础功能
3. ✅ 为 60+ Agent 补充成功指标

### 本月完成

1. ✅ 新增 35 个 Agent（Engineering/Marketing）
2. ✅ 完成 convert.sh 转换工具
3. ✅ GitHub 推广策略实施

---

*太一 AGI · agency-agents 蒸馏报告 · 2026-04-16*  
* distilled from github.com/msitarzewski/agency-agents*
