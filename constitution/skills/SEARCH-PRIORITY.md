---
name: search-priority
tier: 2
trigger: 搜索/安装/插件/GitHub
enabled: true
depends: []
---
# 搜索优先级技能（GitHub 优先）

## 核心原则

**负熵法则：** 开源优先，减少商业依赖

**简化优先：** 标准化搜索流程

**零成本：** 免费开源方案优先

---

## 搜索优先级

### 1️⃣ GitHub 开源搜索（默认）

**搜索策略：**
```
1. 关键词 + "github"
2. 关键词 + "python" + "library"
3. 关键词 + "open source" + "alternative"
```

**评估标准：**
| 指标 | 权重 | 说明 |
|------|------|------|
| Stars | ⭐⭐⭐ | 社区认可度 |
| 更新时间 | ⭐⭐⭐ | 项目活跃度 |
| Issues 解决率 | ⭐⭐ | 维护质量 |
| 文档完整度 | ⭐⭐ | 易用性 |
| 许可协议 | ⭐⭐ | MIT/Apache 优先 |

**安装优先级：**
1. `pip install <package>`（PyPI）
2. `pip install git+https://github.com/...`（GitHub）
3. 源码编译安装

---

### 2️⃣ 全网穿透性搜索（GitHub 无结果时）

**搜索渠道：**
| 渠道 | 优先级 | 说明 |
|------|--------|------|
| PyPI | ⭐⭐⭐⭐ | Python 官方 |
| npm | ⭐⭐⭐ | Node.js 生态 |
| 官方文档 | ⭐⭐⭐ | 权威来源 |
| 技术博客 | ⭐⭐ | 实践经验 |
| 在线工具 | ⭐⭐ | 临时方案 |

---

### 3️⃣ 手动方案（自动化失败时）

**适用场景：**
- GitHub 无成熟方案
- 全网搜索无结果
- 需注册/付费工具

**示例：**
- ODA File Converter（需注册）
- 商业 API（需付费）
- 在线转换工具

---

## 安装流程

### 标准流程

```
1. GitHub 搜索
    ↓ 找到合适项目
2. 评估（Stars/更新/文档/许可）
    ↓ 通过评估
3. 尝试安装（pip/git）
    ↓ 安装成功
4. 测试验证
    ↓ 验证通过
5. 集成到太一技能体系
```

### 失败回退

```
GitHub 安装失败
    ↓
PyPI 搜索
    ↓ 如无
全网搜索
    ↓ 如无
手动方案指南
```

---

## 评估模板

### GitHub 项目评估

```markdown
## 项目评估 · [项目名]

**GitHub:** https://github.com/xxx/xxx
**Stars:** xxx
**更新:** 最后更新时间
**许可:** MIT/Apache/GPL

### 优点
- [ ] 活跃维护
- [ ] 文档完整
- [ ] 安装简单
- [ ] 社区活跃

### 缺点
- [ ] 更新缓慢
- [ ] 文档缺失
- [ ] 依赖复杂
- [ ] 许可限制

### 结论
- [ ] ✅ 推荐安装
- [ ] 🟡 可尝试
- [ ] ❌ 不推荐
```

---

## 今日验证（DWG→DXF 转换）

### 搜索结果

| 项目 | GitHub Stars | 状态 | 原因 |
|------|--------------|------|------|
| libre-dwg | ⭐⭐⭐ | ❌ 失败 | 需编译 C 库 |
| dwg2dxf | ⭐⭐ | ❌ 失败 | 无 Python 绑定 |
| dwg-parser | ⭐ | ❌ 失败 | 项目已废弃 |
| FreeCAD | ⭐⭐⭐⭐⭐ | ❌ 失败 | 包太大 |

### 结论

**DWG 解析领域：** GitHub 无成熟 Python 方案

**原因：** DWG 是 Autodesk 私有格式，开源项目需反向工程

**最优解：** 在线转换工具（Zamzar 等）

---

## 快速参考

### GitHub 搜索命令

```bash
# 通用搜索
site:github.com <关键词> python

# 高星项目
site:github.com <关键词> stars:>100

# 最近更新
site:github.com <关键词> pushed:>2024-01-01
```

### 安装命令

```bash
# PyPI 安装
pip install <package>

# GitHub 安装
pip install git+https://github.com/user/repo.git

# 指定分支
pip install git+https://github.com/user/repo.git@main
```

---

## 总结

**定位：** 搜索与安装优先级规范

**价值：** 开源优先，减少商业依赖

**审查：** L1（太一自主执行）

---
*版本：1.0 | 生效日期：2026-03-22 | 最后更新：12:50*
