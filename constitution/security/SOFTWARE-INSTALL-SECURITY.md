# 软件安装安全评估协议

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: SAYELF + 太一 AGI
> **类别**: 安全/宪法
> **状态**: ✅ 已激活

---

## 🎯 核心原则

**所有代码或软件新增必须经过6步安全评估流程**

---

## 📋 6步安全评估流程

### 步骤1: 系统查重

**目标**: 检查系统是否已有类似或相同功能

**检查清单**:
- [ ] 搜索现有skills目录 (`skills/*/`)
- [ ] 检查已有Agent功能
- [ ] 查看现有脚本和工具
- [ ] 确认无重复功能

**执行命令**:
```bash
# 搜索现有功能
find skills/ -type f -name "*.py" | xargs grep -l "关键词" 2>/dev/null

# 检查已有模块
ls skills/*/ | grep -i "关键词"
```

**决策标准**:
| 结果 | 行动 |
|------|------|
| 无重复 | 继续步骤2 |
| 有类似 | 评估是否需要升级替代 |
| 有相同 | 拒绝安装，使用现有 |

---

### 步骤2: 开源调研

**目标**: 在GitHub/Claude/Hermes/OpenAI等平台搜索最佳实践

**搜索平台**:
| 平台 | URL | 用途 |
|------|-----|------|
| GitHub | github.com/search | 开源项目搜索 |
| Claude Skills | claude.ai/skills | Claude官方技能 |
| OpenAI Codex | openai.com/codex | Codex工具 |
| Awesome Lists | awesome.re | 精选列表 |
| PyPI | pypi.org | Python包 |
| npm | npmjs.com | Node.js包 |

**搜索关键词**:
```
# 通用格式
"功能关键词" + "language:python" + "stars:>100"

# 示例
"web scraping" language:python stars:>1000
"text to speech" language:python stars:>500
"osint tool" language:python stars:>1000
```

**评估维度**:
| 维度 | 权重 | 标准 |
|------|------|------|
| Stars | 20% | >1000优先 |
| 活跃度 | 25% | 近3个月有提交 |
| 文档 | 20% | 有完整README |
| 测试 | 15% | 有测试覆盖 |
| 许可证 | 10% | MIT/Apache优先 |
| 依赖 | 10% | 依赖少优先 |

---

### 步骤3: 蒸馏提炼

**目标**: 从搜索结果中提炼精华，设计集成方案

**蒸馏流程**:
```
搜索结果
    ↓
筛选Top 3项目
    ↓
分析架构设计
    ↓
提取核心算法
    ↓
设计集成接口
    ↓
输出蒸馏报告
```

**蒸馏报告模板**:
```markdown
# 蒸馏报告: [功能名称]

## 候选项目
| 排名 | 项目 | Stars | 许可证 | 选择理由 |
|------|------|-------|--------|---------|
| 1 | xxx | 5000 | MIT | 架构清晰 |
| 2 | yyy | 3000 | Apache | 功能完整 |
| 3 | zzz | 1000 | GPL | 算法优秀 |

## 核心提炼
- **架构模式**: [描述]
- **关键算法**: [描述]
- **接口设计**: [描述]

## 集成方案
- **集成方式**: [直接引用/修改适配/重写]
- **依赖管理**: [说明]
- **风险评估**: [说明]
```

---

### 步骤4: 安全评估

**目标**: 对要集成的代码进行安全评估

**安全检查清单**:

#### 4.1 代码安全
- [ ] 无硬编码密钥
- [ ] 无恶意代码
- [ ] 无后门程序
- [ ] 无数据窃取行为
- [ ] 无未授权网络请求

#### 4.2 依赖安全
- [ ] 依赖包无已知漏洞
- [ ] 依赖包来源可信
- [ ] 依赖数量合理
- [ ] 无循环依赖

#### 4.3 运行安全
- [ ] 沙箱运行测试
- [ ] 资源限制测试
- [ ] 权限最小化
- [ ] 网络隔离测试

**安全评估命令**:
```bash
# 检查硬编码密钥
grep -r "api_key\|password\|secret\|token" --include="*.py" . 2>/dev/null | grep -v "example\|test"

# 检查网络请求
grep -r "requests\.\|urllib\|socket" --include="*.py" . 2>/dev/null

# 检查文件操作
grep -r "open(\|os\.system\|subprocess" --include="*.py" . 2>/dev/null

# 依赖安全扫描
pip install safety
safety check -r requirements.txt
```

---

### 步骤5: 可靠性验证

**目标**: 确保不影响本系统，安全可靠可信

**验证清单**:
- [ ] 不影响现有功能
- [ ] 不冲突现有配置
- [ ] 资源占用合理
- [ ] 错误处理完善
- [ ] 可回滚方案

**测试流程**:
```bash
# 1. 备份现有配置
cp -r .openclaw/workspace .openclaw/workspace.backup

# 2. 隔离测试
python3 -m venv venv-test
source venv-test/bin/activate
pip install -r requirements.txt

# 3. 功能测试
python3 test_new_feature.py

# 4. 回归测试
python3 test_existing_features.py

# 5. 性能测试
python3 benchmark.py
```

---

### 步骤6: 系统集成

**目标**: 将新功能集成到太一系统

**集成规范**:

#### 6.1 目录结构
```
skills/
├── [new-skill]/
│   ├── SKILL.md              # 技能说明 (必须)
│   ├── __init__.py           # 包入口
│   ├── [main_module].py      # 主模块
│   ├── config.yaml           # 配置文件
│   ├── test_[module].py      # 测试文件
│   └── README.md             # 使用说明
```

#### 6.2 命名规范
- 技能名: 小写+连字符 (如 `feishu-integration`)
- 模块名: 小写+下划线 (如 `feishu_integration.py`)
- 类名: 大驼峰 (如 `FeishuIntegration`)
- 常量: 大写+下划线

#### 6.3 文档要求
- SKILL.md: 技能职责、使用方式、架构图
- README.md: 快速开始、示例代码
- 注释: 中文注释，说明设计意图

#### 6.4 集成检查
- [ ] 注册到 OpenClaw Gateway
- [ ] 添加到 TAIYI_SYSTEM_SKILLS.md
- [ ] 更新 AGENTS.md
- [ ] 记录到 memory/YYYY-MM-DD.md
- [ ] Git 提交并推送

---

## 🔒 安全红线

### 绝对禁止
- ❌ 安装来源不明的软件
- ❌ 执行未审查的脚本
- ❌ 使用硬编码的密钥
- ❌ 绕过系统安全机制
- ❌ 未经评估直接安装

### 必须遵守
- ✅ 所有软件必须经过6步评估
- ✅ 优先使用官方源/可信源
- ✅ 保持最小权限原则
- ✅ 记录所有安装操作
- ✅ 保留回滚方案

---

## 📊 评估记录

| 日期 | 软件/功能 | 评估人 | 步骤 | 结果 | 备注 |
|------|----------|--------|------|------|------|
| 2026-05-04 | MOSS-TTS-Nano | 太一 | 6步 | ✅通过 | ONNX CPU版本 |
| 2026-05-04 | Maigret | 太一 | 6步 | ✅通过 | OSINT工具 |
| 2026-05-04 | 反爬工具包 | 太一 | 6步 | ✅通过 | Crawl4AI融合 |

---

## 🚀 快速执行

### 一键评估脚本

```bash
#!/bin/bash
# software-eval.sh

echo "🚀 太一软件安全评估"
echo "==================="

# 步骤1: 系统查重
echo ""
echo "📋 步骤1: 系统查重"
find skills/ -type d -name "*$1*" 2>/dev/null && echo "⚠️ 发现类似技能" || echo "✅ 无重复"

# 步骤2: GitHub搜索
echo ""
echo "📋 步骤2: GitHub搜索"
echo "请手动搜索: https://github.com/search?q=$1&type=repositories"

# 步骤3: 蒸馏提炼
echo ""
echo "📋 步骤3: 蒸馏提炼"
echo "请编写蒸馏报告: skills/$1/DISTILLATION.md"

# 步骤4: 安全评估
echo ""
echo "📋 步骤4: 安全评估"
grep -r "api_key\|password\|secret" --include="*.py" skills/$1/ 2>/dev/null && echo "⚠️ 发现敏感信息" || echo "✅ 无敏感信息"

# 步骤5: 可靠性验证
echo ""
echo "📋 步骤5: 可靠性验证"
echo "请执行测试: python3 skills/$1/test_*.py"

# 步骤6: 系统集成
echo ""
echo "📋 步骤6: 系统集成"
echo "请完成集成并提交Git"

echo ""
echo "✅ 评估完成"
```

---

## 📚 参考文档

- [OpenClaw Security Guide](https://docs.openclaw.ai/security)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
- [GitHub Security Advisories](https://github.com/advisories)

---

*太一 AGI · 软件安装安全评估协议 v1.0*
*创建时间: 2026-05-04*
*核心原则: 6步评估 · 安全可靠 · 最小权限*
