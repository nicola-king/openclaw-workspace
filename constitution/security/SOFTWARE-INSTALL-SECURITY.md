# 软件安装安全评估流程

**版本**: v1.0  
**创建时间**: 2026-03-31 22:01  
**触发事件**: axios 投毒事件预警 (Cos 余弦 微博)  
**适用范围**: 所有 npm/pip/apt/npm 等包管理器安装的软件/依赖

---

## 🔐 安全评估流程 (5 步)

### 步骤 1: 安装前调研

**必须检查项**:
- [ ] **包来源**: 官方仓库 / 知名维护者 / 社区推荐
- [ ] **下载量**: npm downloads / PyPI stats / GitHub stars
- [ ] **维护状态**: 最近更新时间 (≤6 个月)
- [ ] **安全告警**: `npm audit`, `snyk test`, GitHub Security
- [ ] **依赖树**: 检查间接依赖是否有风险

**检查命令**:
```bash
# npm
npm view <package> | grep -E "license|maintainers|time"
npm audit --before-install

# PyPI
pip show <package>
pip-audit

# GitHub
gh repo view <owner/repo>
```

---

### 步骤 2: 风险评估矩阵

| 风险等级 | 标准 | 决策 |
|---------|------|------|
| 🟢 **低风险** | 官方包 + 高下载量 + 活跃维护 + 无告警 | ✅ 直接安装 |
| 🟡 **中风险** | 社区包 + 中等下载量 + 最近有更新 | ⚠️ 需审批后安装 |
| 🟠 **高风险** | 新包 (<1 年) + 低下载量 + 依赖复杂 | 🔴 需 SAYELF 审批 |
| 🔴 **极高风险** | 未知来源 + 无维护者信息 + 有安全告警 | ❌ 禁止安装 |

---

### 步骤 3: 安装时防护

**隔离措施**:
```bash
# 使用虚拟环境 (Python)
python -m venv .venv
source .venv/bin/activate

# 使用局部安装 (npm)
npm install --prefix ./node_modules-local

# 使用容器 (Docker)
docker run --rm -it node:20 bash
```

**权限限制**:
- ❌ 不使用 `sudo npm install -g`
- ❌ 不使用 `pip install --break-system-packages`
- ✅ 使用用户级安装或虚拟环境

---

### 步骤 4: 安装后验证

**必须执行**:
```bash
# 1. 检查实际安装版本
npm list <package>
pip show <package>

# 2. 扫描安全漏洞
npm audit
pip-audit

# 3. 检查恶意文件
find node_modules -name "*.js" -exec grep -l "child_process\|fs.writeFileSync\|process.env" {} \;

# 4. 检查异常网络连接
lsof -i -n -P | grep node

# 5. 检查系统文件访问
auditctl -w /etc -p wa
```

---

### 步骤 5: 持续监控

**定期任务**:
- [ ] **每周**: `npm audit` / `pip-audit`
- [ ] **每月**: 检查依赖更新
- [ ] **每季度**: 清理未使用依赖
- [ ] **事件驱动**: 安全事件爆发时立即排查

**自动化脚本**:
```bash
#!/bin/bash
# weekly-security-check.sh

echo "【1】npm audit"
npm audit --audit-level=high

echo "【2】检查异常文件"
find node_modules -name "*.js" -newer /tmp -exec grep -l "eval\|exec" {} \;

echo "【3】检查网络连接"
lsof -i -n -P | grep -E "node|python" | grep -v localhost

echo "✅ 安全检查完成"
```

---

## 🚨 安全事件响应

### 触发条件
- 安全研究员曝光投毒事件
- npm/PyPI 官方安全告警
- 系统出现异常行为 (CPU 占用/网络请求/文件修改)

### 响应流程
```
1. 立即停止相关服务
2. 隔离受感染环境
3. 排查依赖树
4. 清理恶意文件
5. 恢复安全版本
6. 更新安全策略
7. 记录事件报告
```

### 排查命令模板
```bash
# 检查恶意版本
npm list | grep -E "1\.14\.1|0\.30\.4"

# 查找恶意模块
find node_modules -name "plain-crypto-js"

# 查找 RAT 文件
find /tmp -name "*.py" -o -name "*.sh" | xargs grep -l "socket\|requests"

# 检查系统文件
ls -la ~/Library/Caches/com.apple.act.mond 2>/dev/null  # macOS
ls -la "%PROGRAMDATA%\wt.exe" 2>nul  # Windows
```

---

## 📋 安装审批清单

### P0 级软件 (核心依赖)
**审批人**: SAYELF  
**适用范围**: Polymarket SDK、量化交易、支付相关

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 包来源验证 | ☐ | 官方/知名维护者 |
| 安全审计 | ☐ | npm audit 通过 |
| 依赖审查 | ☐ | 无高风险间接依赖 |
| 隔离安装 | ☐ | 虚拟环境/容器 |
| 安装后验证 | ☐ | 版本 + 安全扫描 |

### P1 级软件 (工具类)
**审批人**: 太一 (自主决策)  
**适用范围**: 开发工具、文档生成、数据处理

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 下载量 >1000/月 | ☐ | 社区认可 |
| 最近 6 个月有更新 | ☐ | 活跃维护 |
| 无高危漏洞 | ☐ | CVE 检查 |
| 用户级安装 | ☐ | 不使用 sudo |

### P2 级软件 (实验性)
**审批人**: 太一 (需记录)  
**适用范围**: 测试工具、一次性脚本

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 容器隔离 | ☐ | Docker/venv |
| 网络限制 | ☐ | 防火墙规则 |
| 用完即删 | ☐ | 清理计划 |

---

## 📊 已安装软件清单

### 核心依赖 (P0)
| 软件 | 版本 | 安装时间 | 安全状态 |
|------|------|---------|---------|
| @polymarket/clob-client | 5.8.1 | 2026-03-27 | ✅ 安全 |
| ethers | 5.8.0 | 2026-03-27 | ✅ 安全 |

### 工具类 (P1)
| 软件 | 版本 | 安装时间 | 安全状态 |
|------|------|---------|---------|
| reportlab | 待安装 | - | 待评估 |
| python-docx | 待安装 | - | 待评估 |

---

## 🔒 安全红线

**绝对禁止**:
1. ❌ 安装来源不明的包
2. ❌ 使用 `sudo` 安装非必要包
3. ❌ 忽略 `npm audit` 高危告警
4. ❌ 在生产环境直接安装未测试包
5. ❌ 安装后不进行安全验证

**必须执行**:
1. ✅ 安装前调研 (5 分钟)
2. ✅ 使用虚拟环境/容器隔离
3. ✅ 安装后扫描漏洞
4. ✅ 定期更新依赖
5. ✅ 记录所有安装操作

---

## 📝 安装日志模板

```markdown
## [日期] 安装 [软件名]

**版本**: x.x.x  
**用途**: [一句话说明]  
**审批**: [SAYELF/太一]  

### 安装前检查
- [ ] 包来源验证：[结果]
- [ ] 安全审计：[npm audit 结果]
- [ ] 依赖审查：[间接依赖风险]

### 安装命令
```bash
[实际执行的命令]
```

### 安装后验证
- [ ] 版本确认：[实际版本]
- [ ] 漏洞扫描：[pip-audit/npm audit 结果]
- [ ] 功能测试：[是否正常]

### 备注
[其他需要记录的信息]
```

---

*创建时间：2026-03-31 22:01 | 太一 AGI | 安全等级：P0*
