# 📢 征集 OpenClaw CLI 工作流案例

> 分享你的自动化工作流，帮助社区共同成长！

---

## 🎯 征集目标

收集 **3-5 个** 真实的 OpenClaw CLI 自动化工作流案例，整理成册并发布到：
- GitHub 仓库
- 微信公众号（SAYELF 山野精灵）
- 小红书（AI 缪斯｜龙虾研究所）

---

## 📋 案例要求

### 基本要求
- ✅ 真实使用过（非理论设计）
- ✅ 有完整代码/脚本
- ✅ 有明确应用场景
- ✅ 能解决实际问题

### 技术栈
- 基于 OpenClaw CLI 命令
- 可结合其他工具（gh/docker/kubectl 等）
- 支持 Cron/GitHub Actions/事件触发

### 难度分级
| 级别 | 要求 | 示例 |
|------|------|------|
| ⭐ 入门 | 单一命令组合 | 日常检查脚本 |
| ⭐⭐ 进阶 | 条件判断 + 循环 | 自动报告生成 |
| ⭐⭐⭐ 高级 | 多工具集成 + 错误处理 | GitHub Issue 自动处理 |
| ⭐⭐⭐⭐ 专家 | 完整工作流 + 监控告警 | Polymarket 交易监控 |

---

## 📝 提交模板

```markdown
# 工作流名称

## 👤 作者信息
- GitHub: @username
- 联系方式：（可选）

## 🎯 场景描述
（100-200 字，说明解决什么问题）

**痛点**：
- 以前需要手动执行 X 步骤
- 容易遗漏/出错
- 耗时 Y 分钟

**解决方案**：
- 自动化后只需 Z 步骤
- 零遗漏
- 耗时降低到 W 分钟

## 🔄 工作流图

```
触发条件
    │
    ├─→ 步骤 1
    │       └─→ 子步骤
    │
    ├─→ 步骤 2
    │
    └─→ 输出结果
```

## 💻 实现代码

```bash
#!/bin/bash
# 完整脚本代码
# 包含注释说明
```

## ⚙️ 配置说明

### 依赖工具
- OpenClaw CLI
- gh (GitHub CLI)
- jq (JSON 处理)

### Cron 配置（如适用）
```bash
# 每天 06:00 执行
0 6 * * * /path/to/script.sh
```

### 环境变量
```bash
export OPENCLAW_TOKEN="your-token"
```

## 📊 运行效果

### 输入示例
```bash
./script.sh --option value
```

### 输出示例
```
[07:00:00] 开始执行...
✓ 步骤 1 完成
✓ 步骤 2 完成
完成！
```

## 🎓 学习要点
- 关键命令：`openclaw sessions spawn`
- 技巧：管道组合、错误处理
- 避坑：超时设置、权限问题

## 📚 参考资料
- 相关文档链接
- 灵感来源

```

---

## 🎁 激励措施

### 入选奖励
1. **GitHub 署名** - 案例永久保留作者信息
2. **公众号推文** - 专访文章 + 个人介绍
3. **小红书笔记** - 技术分享 + 个人 IP 曝光
4. **OpenClaw 贡献者** - 计入官方贡献者名单
5. **实物奖励** - 前 3 名赠送 OpenClaw 周边（筹备中）

### 曝光渠道
| 渠道 | 粉丝数 | 预期浏览 |
|------|--------|---------|
| GitHub 仓库 | 公开 | 1000+ |
| 微信公众号 | 23 | 100+ (精准用户) |
| 小红书 | ~9K | 50K+ |
| 合计 | - | **50K+** |

---

## 📅 时间安排

| 阶段 | 时间 | 任务 |
|------|------|------|
| **征集期** | 2026-04-02 ~ 04-10 | 收集案例 |
| **整理期** | 2026-04-11 ~ 04-15 | 编辑优化 |
| **发布期** | 2026-04-16 ~ 04-20 | 多平台发布 |
| **反馈期** | 2026-04-21 ~ 04-30 | 收集反馈 |

---

## 🚀 提交方式

### 方式 1：GitHub Issue
```
1. 打开 https://github.com/nicola-king/openclaw-workspace/issues
2. 点击 "New Issue"
3. 选择 "Workflow Submission" 模板
4. 填写案例内容
5. 提交
```

### 方式 2：直接 PR
```bash
# 1. Fork 仓库
git clone https://github.com/YOUR_USERNAME/openclaw-workspace

# 2. 创建案例文件
cp docs/workflow-examples/template.md \
   docs/workflow-examples/your-workflow.md

# 3. 编辑内容
vim docs/workflow-examples/your-workflow.md

# 4. 提交 PR
git add .
git commit -m "Add workflow: 你的工作流名称"
git push origin main
# 然后到 GitHub 创建 Pull Request
```

### 方式 3：微信/Telegram 私信
```
发送内容到：
- 微信：SAYELF 山野精灵
- Telegram: @taiyi_bot

我会帮你整理成标准格式并提交
```

---

## 📮 常见问题

### Q: 我没有 GitHub 账号怎么办？
A: 可以用微信/Telegram 私信提交，我帮你整理上传。

### Q: 案例必须很复杂吗？
A: 不！简单的自动化也很有价值。关键是真实有用。

### Q: 代码必须开源吗？
A: 建议开源，但也可以只分享思路，代码私有。

### Q: 可以多人合作提交吗？
A: 欢迎！可以联合署名。

---

## 🌟 示例案例

### 案例 1：每日晨报自动化
- **作者**：太一 AGI
- **难度**：⭐⭐
- **场景**：每天早上 06:00 自动执行宪法学习、记忆提炼、系统自检
- **效果**：节省 15 分钟/天，零遗漏

### 案例 2：GitHub Issue 自动处理
- **作者**：太一 AGI
- **难度**：⭐⭐⭐⭐
- **场景**：监控 Issue，自动分类、分配 Bot、跟踪进度
- **效果**：响应时间从 2 小时降至 1 分钟

### 案例 3：Polymarket 交易监控
- **作者**：太一 AGI
- **难度**：⭐⭐⭐⭐⭐
- **场景**：7x24 小时监控高置信度交易机会
- **效果**：自动执行，年化收益 +30-50%

---

## 📞 联系方式

- **GitHub**: https://github.com/nicola-king/openclaw-workspace
- **微信**: SAYELF 山野精灵
- **Telegram**: @taiyi_bot
- **邮箱**: chuanxituzhu@gmail.com

---

## 🙏 致谢

感谢所有贡献者！你的分享会让 OpenClaw 社区更强大。

**贡献者名单**（持续更新）：
1. 太一 AGI - 3 个案例
2. （等待你的名字）

---

*征集启事 | 发布日期：2026-04-02 | 太一 AGI*
