# 太一 GitHub 集成 (Taiyi GitHub Integration)

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **类别**: 集成/代码管理/协作
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 太一系统与 GitHub 的无缝集成

**适用场景**:
- 代码仓库管理
- Issue/PR 自动化处理
- 工作流触发与监控
- 代码审查辅助
- 版本发布管理
- 系统配置同步

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    太一系统 (Taiyi System)                │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 跨境贸易 │  │ 旅游探路 │  │ OSINT   │  │ TTS     │   │
│  │ Agent   │  │ Agent   │  │ Agent   │  │ Agent   │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │         │
│       └────────────┴────────────┴────────────┘         │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              GitHub 集成层                        │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 仓库管理  │  │ Issue/PR │  │ 工作流   │      │   │
│  │  │ Repo     │  │ Manager  │  │ Actions  │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 代码审查  │  │ 版本发布  │  │ 配置同步  │      │   │
│  │  │ Review   │  │ Release  │  │ Sync     │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              GitHub API / Git CLI                │   │
│  │                                                  │   │
│  │  REST API │ GraphQL │ Git Operations │ Webhooks │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 核心组件

### 1. 仓库管理 (Repository Manager)

**功能**: 管理 GitHub 仓库

**支持操作**:
| 操作 | 说明 | 使用场景 |
|------|------|---------|
| 创建仓库 | 新建代码仓库 | 新项目初始化 |
| 克隆仓库 | 下载代码到本地 | 开发环境搭建 |
| 提交代码 | git commit/push | 代码更新 |
| 分支管理 | 创建/合并分支 | 功能开发 |
| 代码同步 | 拉取最新代码 | 保持同步 |

### 2. Issue/PR 管理 (Issue & PR Manager)

**功能**: 自动化处理 Issue 和 Pull Request

**支持操作**:
| 操作 | 说明 | 使用场景 |
|------|------|---------|
| 创建 Issue | 提交问题/任务 | Bug 报告 |
| 关闭 Issue | 标记完成 | 问题解决 |
| 创建 PR | 提交代码审查 | 功能合并 |
| 审查 PR | 代码审查辅助 | 质量把控 |
| 合并 PR | 合并代码 | 发布功能 |

### 3. 工作流管理 (Actions Manager)

**功能**: 管理 GitHub Actions 工作流

**支持操作**:
| 操作 | 说明 | 使用场景 |
|------|------|---------|
| 触发工作流 | 手动/自动触发 | CI/CD |
| 查看状态 | 检查运行状态 | 监控 |
| 下载产物 | 获取构建产物 | 部署 |
| 配置工作流 | 创建/修改 YAML | 自动化 |

---

## 📡 系统内部信息集成

### 信息来源

太一 GitHub 集成采用系统内部信息:

```
系统内部信息
├── 代码状态
│   ├── 本地修改
│   ├── 提交历史
│   ├── 分支信息
│   └── 代码统计
├── 任务执行结果
│   ├── 测试结果
│   ├── 构建状态
│   ├── 部署记录
│   └── 性能指标
├── 系统配置
│   ├── 环境变量
│   ├── 配置文件
│   ├── 依赖清单
│   └── 版本信息
├── 文档生成
│   ├── API 文档
│   ├── 变更日志
│   ├── 使用说明
│   └── 架构图
└── 监控数据
    ├── 错误日志
    ├── 性能数据
    ├── 用户反馈
    └── 告警信息
```

---

## 🚀 使用方式

### 1. 配置 GitHub 认证

```yaml
# config/github.yaml
github:
  # 认证方式 (token/ssh)
  auth_type: "token"
  
  # Personal Access Token
  token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  
  # 或 SSH 配置
  ssh_key: "~/.ssh/id_rsa"
  
  # 默认仓库
  default_repo: "sayelf/taiyi-system"
  
  # 用户名
  username: "sayelf"
```

### 2. 仓库操作

```python
from skills.github_integration import GitHubIntegration

# 初始化
github = GitHubIntegration()

# 克隆仓库
github.clone_repo("https://github.com/sayelf/taiyi-system.git")

# 提交代码
github.commit(
    message="[更新] 添加新功能",
    files=["skills/new_feature.py"]
)

# 推送代码
github.push(branch="main")

# 创建分支
github.create_branch("feature/new-skill")
```

### 3. Issue/PR 操作

```python
# 创建 Issue
issue = github.create_issue(
    title="[Bug] 系统启动失败",
    body="描述问题...",
    labels=["bug", "high-priority"]
)

# 创建 PR
pr = github.create_pull_request(
    title="[功能] 添加飞书集成",
    body="实现飞书消息推送...",
    head="feature/feishu",
    base="main"
)

# 审查 PR
review = github.review_pull_request(
    pr_number=42,
    comment="代码审查通过 ✅"
)
```

### 4. 工作流操作

```python
# 触发工作流
github.trigger_workflow(
    workflow_id="deploy.yml",
    inputs={"environment": "production"}
)

# 查看工作流状态
status = github.get_workflow_status("deploy.yml")
print(f"状态: {status}")
```

---

## 📊 消息模板

### 代码提交通知

```markdown
## 📝 代码提交

**仓库**: sayelf/taiyi-system
**分支**: main
**提交者**: 太一 AGI
**时间**: 2026-05-04 10:30:00

### 变更内容
- 新增: skills/feishu-integration/
- 修改: constitution/CONST-ROUTER.md
- 删除: 无

### 统计
- 新增文件: 5
- 修改文件: 2
- 删除文件: 0
- 代码行数: +1,234 -56
```

### PR 审查通知

```markdown
## 🔍 PR 审查

**标题**: [功能] 添加飞书集成
**作者**: 太一 AGI
**状态**: ✅ 已通过

### 审查结果
- 代码质量: ✅ 通过
- 测试覆盖: ✅ 通过
- 文档完整: ✅ 通过

### 建议
无
```

---

## 🔒 安全与权限

### 认证管理

| 级别 | 权限 | 使用场景 |
|------|------|---------|
| 读取 | 只读访问 | 代码查看 |
| 写入 | 代码提交 | 日常开发 |
| 管理 | 仓库管理 | 管理员 |

### 敏感信息保护

```python
# 环境变量存储 Token
import os

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN 未设置")
```

---

## 🧪 测试

```bash
# 测试仓库操作
python3 skills/github-integration/test_repo.py

# 测试 Issue/PR
python3 skills/github-integration/test_issue_pr.py

# 测试工作流
python3 skills/github-integration/test_workflow.py
```

---

## 📁 文件结构

```
skills/github-integration/
├── SKILL.md                          # 技能说明
├── github_integration.py             # 核心集成类
├── repo_manager.py                   # 仓库管理
├── issue_pr_manager.py               # Issue/PR管理
├── actions_manager.py                # 工作流管理
├── config.yaml                       # 配置文件
├── test_repo.py                      # 仓库测试
├── test_issue_pr.py                  # Issue/PR测试
└── test_workflow.py                  # 工作流测试
```

---

## 🔄 与现有系统集成

### 已集成
- ✅ 跨境贸易Agent - 代码版本管理
- ✅ 旅游探路者 - 文档同步
- ✅ 系统配置 - 配置文件同步

### 待集成
- 🟡 CI/CD 流水线
- 🟡 自动化测试
- 🟡 文档生成

---

## 🎯 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| GitHub Pages | P1 | 静态网站托管 |
| GitHub Packages | P1 | 包管理 |
| GitHub Codespaces | P2 | 云端开发 |
| GitHub Copilot | P2 | AI 编程辅助 |
| GitHub Projects | P2 | 项目管理 |

---

*太一 AGI · GitHub 集成技能 v1.0*
*创建时间: 2026-05-04*
*核心能力: 系统内部代码管理 → GitHub 平台同步*
