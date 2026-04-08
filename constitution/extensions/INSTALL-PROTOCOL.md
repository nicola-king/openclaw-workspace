# INSTALL-PROTOCOL.md - 软件安装与部署协议

> 太一 AGI 系统软件安装标准流程 | 版本：**v2.0** | 创建：2026-03-26 | 更新：2026-03-29

---

## 🎯 核心原则

```
帮助，不表演 · 安全优先 · 可恢复 · 自动化 · 深度学习
```

---

## 📋 八层协议框架 (v2.0)

```
秩序流程:
  第 0 层：蒸馏 → 第 3 层：检测 → 第 1 层：比对 → 第 2 层：提炼 → 第 4 层：评估 → 第 5 层：修复 → 第 6 层：清理 → 第 7 层：安装

逻辑说明:
  蒸馏 (0) → 检测 (3) → 比对 (1) → 提炼 (2) → 评估 (4) → 修复 (5) → 清理 (6) → 安装 (7)
```

---

## 🧠 前置三层：学习融合 (新增 v2.0)

### 第 0 层：蒸馏 (Distillation)

**目标**: 对准备安装的软件进行蒸馏，提取核心信息

**执行清单**:
```markdown
1. 软件是什么？
   - 一句话概括核心功能
   - 解决什么问题
   - 目标用户是谁

2. 关键信息提取
   - 官方来源 (GitHub/官网)
   - 最新版本号
   - 安装方式 (apt/snap/source)
   - 依赖要求
   - 资源占用

3. 去除噪音
   - 删除营销表述
   - 删除夸张宣传
   - 保留数据/事实/参数
```

**输出格式**:
```markdown
### 软件蒸馏报告

**软件名称**: [名称]
**一句话概括**: [核心功能]
**官方来源**: [URL]
**最新版本**: [版本号]
**安装方式**: [apt/snap/source]
**依赖要求**: [依赖列表]
**资源占用**: [CPU/内存/磁盘]

**核心功能**:
1. [功能 1]
2. [功能 2]
3. [功能 3]
```

**自动化脚本**: `skills/suwen/distill.sh`

---

### 第 1 层：比对 (Comparison)

**目标**: 分析优劣势，决策是否采用

**执行清单**:
```markdown
1. 横向对比 (同类软件)
   - 功能对比
   - 性能对比
   - 成本对比
   - 社区活跃度对比

2. 纵向对比 (太一现状)
   - 太一是否有类似功能？
   - 太一现状如何？
   - 差距在哪里？
   - 是否需要引入？

3. 优劣势分析
   - 软件优势是什么？
   - 软件劣势是什么？
   - 太一优势是什么？
   - 太一劣势是什么？
```

**输出格式**:
```markdown
### 软件比对报告

**横向对比**:
| 维度 | 软件 A | 软件 B | 太一现有 |
|------|--------|--------|---------|
| 功能 | ... | ... | ... |
| 性能 | ... | ... | ... |
| 成本 | ... | ... | ... |
| 社区 | ... | ... | ... |

**纵向对比**:
| 维度 | 对方 | 太一 | 差距 |
|------|------|------|------|
| 功能 | ... | ... | ... |
| 性能 | ... | ... | ... |
| 成本 | ... | ... | ... |

**优劣势分析**:
- **软件优势**: [...]
- **软件劣势**: [...]
- **太一优势**: [...]
- **太一劣势**: [...]

**决策**: ✅ 采用 / 🟡 部分采用 / ❌ 放弃
```

**自动化脚本**: `skills/suwen/compare.sh`

---

### 第 2 层：提炼 (Refinement)

**目标**: 取其精华去其糟粕，只采用有价值部分

**执行清单**:
```markdown
1. 精华识别 (必须采用)
   - 哪些功能是核心需求？
   - 哪些特性不可替代？
   - 哪些配置必须保留？

2. 糟粕识别 (应该放弃)
   - 哪些功能是多余的？
   - 哪些配置有风险？
   - 哪些依赖不必要？

3. 改良方案 (适配太一)
   - 如何适配太一架构？
   - 如何优化配置？
   - 如何降低成本？
```

**输出格式**:
```markdown
### 精华糟粕分析报告

**精华 (采用)**:
- [ ] [核心功能 1]
- [ ] [核心功能 2]
- [ ] [关键配置 1]

**糟粕 (放弃)**:
- [ ] [多余功能 1]
- [ ] [风险配置 1]
- [ ] [不必要依赖]

**改良 (适配太一)**:
- [ ] [功能 1] → [太一改良版]
- [ ] [配置 1] → [太一配置版]

**最终方案**:
[详细描述采用的功能、配置、优化方案]
```

**自动化脚本**: `skills/suwen/refine.sh`

---

## 🛠️ 执行五层：安装部署

### 第 3 层：检测 (Detection)

**目标**: 全面了解系统现状

**执行清单**:
```bash
# 1. 检查已安装版本
dpkg -l | grep <package>
snap list | grep <package>
which <command>

# 2. 检查服务状态
systemctl status <service>
systemctl --user status <service>

# 3. 检查进程
ps aux | grep <package> | grep -v grep

# 4. 检查端口占用
ss -tlnp | grep <port>
netstat -tlnp | grep <port>

# 5. 检查依赖
apt-cache depends <package>
ldd $(which <command>) 2>/dev/null

# 6. 检查磁盘空间
df -h /
df -h /home
```

**自动化脚本**: `skills/suwen/install-check.sh`

**输出**: JSON 格式系统状态报告

---

### 第 4 层：评估 (Assessment)

**目标**: 风险评估 + 方案选择

**评估矩阵**:

| 检测项 | 状态 | 风险 | 方案 |
|--------|------|------|------|
| 已安装 (同版本) | ✅ 运行 | 低 | 配置优化 |
| 已安装 (旧版本) | ⚠️ 运行 | 中 | 升级/兼容 |
| 已安装 (新版本) | ❌ 失败 | 高 | 降级/清理 |
| 多版本共存 | ⚠️ 冲突 | 高 | 删除冗余 |
| 未安装 | - | 低 | 新安装 |

**决策树**:
```
已安装？
├── 是 → 运行正常？
│   ├── 是 → 配置优化 (不重装)
│   └── 否 → 尝试修复
│       ├── 成功 → 验证
│       └── 失败 → 清理后重装
└── 否 → 新安装
    ├── 评估风险
    ├── 选择版本
    └── 执行安装
```

**风险评分**:
```
0-3 分：低风险 → 自动执行
4-6 分：中风险 → 用户确认
7-10 分：高风险 → 详细报告 + 用户决策
```

---

### 第 5 层：修复 (Repair)

**目标**: 优先修复现有安装

**修复优先级**:
```
P0: 服务配置修复 (systemd restart/reload)
P1: 权限修复 (chmod/chown)
P2: 依赖修复 (apt --fix-broken install)
P3: 配置重置 (mv config backup + restart)
P4: 彻底清理后重装
```

**修复命令库**:
```bash
# 服务修复
systemctl daemon-reload
systemctl restart <service>
systemctl reset-failed <service>

# 用户服务修复
systemctl --user daemon-reload
systemctl --user restart <service>
systemctl --user unmask <service>

# 权限修复
chmod 755 <binary>
chown root:root <binary>

# 依赖修复
sudo apt --fix-broken install
sudo apt install -f

# 配置重置
mv ~/.config/<app>/config.xml ~/.config/<app>/config.xml.backup
rm -rf ~/.local/state/<app>/*
```

**回滚机制**:
```bash
# 修复前自动备份
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r ~/.config/<app> "$BACKUP_DIR/" 2>/dev/null
cp /etc/systemd/system/<service>.service "$BACKUP_DIR/" 2>/dev/null

# 修复失败时回滚
if [ $? -ne 0 ]; then
    echo "修复失败，执行回滚..."
    cp -r "$BACKUP_DIR/<app>" ~/.config/ 2>/dev/null
    systemctl daemon-reload
fi
```

---

### 第 6 层：清理 (Cleanup)

**目标**: 标准化清理，确保可恢复

**清理标准**:
```bash
# 1. 停止服务
systemctl stop <service>
systemctl --user stop <service>
pkill -9 <process>

# 2. 备份配置 (可恢复)
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r ~/.config/<app> "$BACKUP_DIR/" 2>/dev/null
cp -r /etc/<app> "$BACKUP_DIR/" 2>/dev/null
cp -r /var/lib/<app> "$BACKUP_DIR/" 2>/dev/null

# 3. 删除包
sudo apt remove --purge <package>
sudo snap remove <package>

# 4. 清理残留
rm -rf ~/.config/<app> 2>/dev/null
rm -rf ~/.local/state/<app> 2>/dev/null
rm -rf /var/lib/<app> 2>/dev/null
rm -rf /etc/<app> 2>/dev/null

# 5. 清理 systemd
rm /etc/systemd/system/<service>.service 2>/dev/null
rm ~/.config/systemd/user/<service>.service 2>/dev/null
systemctl daemon-reload
systemctl --user daemon-reload
```

**清理验证**:
```bash
# 确认无残留
dpkg -l | grep <package>
snap list | grep <package>
find / -name "<app>" -type f 2>/dev/null | head -5
```

---

### 第 7 层：安装 (Installation)

**目标**: 安全安装 + 自动化测试

**安装流程**:
```bash
# 1. 安全评估
# 检查包来源
apt-cache policy <package>
# 检查签名
apt-get install --print-uris <package> | grep gpg

# 2. 选择安装源
# 优先：官方仓库
# 其次：官方 PPA
# 再次：snap/flatpak
# 最后：源码编译

# 3. 执行安装
sudo apt update
sudo apt install -y <package>

# 4. 配置服务
systemctl enable <service>
systemctl start <service>

# 5. 防火墙配置
sudo ufw allow <port>/tcp
sudo ufw allow <port>/udp
```

**自动化测试**:
```bash
# 1. 服务状态测试
systemctl is-active <service>
if [ $? -ne 0 ]; then
    echo "❌ 服务启动失败"
    exit 1
fi

# 2. 端口监听测试
ss -tlnp | grep <port>
if [ $? -ne 0 ]; then
    echo "❌ 端口未监听"
    exit 1
fi

# 3. Web 访问测试
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>
if [ $? -ne 0 ]; then
    echo "❌ Web 访问失败"
    exit 1
fi

# 4. 资源占用测试
ps aux | grep <process> | awk '{print $3,$4}'
# CPU < 10%, 内存 < 20%

# 5. 功能测试
# 根据具体软件定义
```

**安全基线**:
```
✅ 仅监听必要端口
✅ 默认绑定 127.0.0.1
✅ 防火墙规则配置
✅ 无 root 权限运行 (如可能)
✅ 日志记录启用
✅ 自动更新启用
```

---

## 🔧 自动化脚本框架

### distill.sh (蒸馏)

```bash
#!/bin/bash
# 软件蒸馏脚本

SOFTWARE=$1
OUTPUT="distill-report-$(date +%Y%m%d-%H%M%S).md"

echo "# 软件蒸馏报告" > $OUTPUT
echo "" >> $OUTPUT
echo "**软件名称**: $SOFTWARE" >> $OUTPUT
echo "**蒸馏时间**: $(date)" >> $OUTPUT
echo "" >> $OUTPUT

# 获取基本信息
echo "## 核心信息" >> $OUTPUT
echo "- **官方来源**: [待补充]" >> $OUTPUT
echo "- **最新版本**: [待补充]" >> $OUTPUT
echo "- **安装方式**: [待补充]" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 核心功能" >> $OUTPUT
echo "1. [功能 1]" >> $OUTPUT
echo "2. [功能 2]" >> $OUTPUT
echo "3. [功能 3]" >> $OUTPUT
echo "" >> $OUTPUT

echo "✅ 蒸馏报告已生成：$OUTPUT"
```

### compare.sh (比对)

```bash
#!/bin/bash
# 软件比对脚本

SOFTWARE=$1
OUTPUT="compare-report-$(date +%Y%m%d-%H%M%S).md"

echo "# 软件比对报告" > $OUTPUT
echo "" >> $OUTPUT
echo "**软件名称**: $SOFTWARE" >> $OUTPUT
echo "**比对时间**: $(date)" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 横向对比" >> $OUTPUT
echo "| 维度 | 软件 A | 软件 B | 太一现有 |" >> $OUTPUT
echo "|------|--------|--------|---------|" >> $OUTPUT
echo "| 功能 | ... | ... | ... |" >> $OUTPUT
echo "| 性能 | ... | ... | ... |" >> $OUTPUT
echo "| 成本 | ... | ... | ... |" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 决策" >> $OUTPUT
echo "- [ ] ✅ 采用" >> $OUTPUT
echo "- [ ] 🟡 部分采用" >> $OUTPUT
echo "- [ ] ❌ 放弃" >> $OUTPUT
echo "" >> $OUTPUT

echo "✅ 比对报告已生成：$OUTPUT"
```

### refine.sh (提炼)

```bash
#!/bin/bash
# 软件提炼脚本

SOFTWARE=$1
OUTPUT="refine-report-$(date +%Y%m%d-%H%M%S).md"

echo "# 精华糟粕分析报告" > $OUTPUT
echo "" >> $OUTPUT
echo "**软件名称**: $SOFTWARE" >> $OUTPUT
echo "**提炼时间**: $(date)" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 精华 (采用)" >> $OUTPUT
echo "- [ ] [核心功能 1]" >> $OUTPUT
echo "- [ ] [核心功能 2]" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 糟粕 (放弃)" >> $OUTPUT
echo "- [ ] [多余功能 1]" >> $OUTPUT
echo "- [ ] [风险配置 1]" >> $OUTPUT
echo "" >> $OUTPUT

echo "## 改良 (适配太一)" >> $OUTPUT
echo "- [ ] [功能 1] → [太一改良版]" >> $OUTPUT
echo "" >> $OUTPUT

echo "✅ 提炼报告已生成：$OUTPUT"
```

### install-check.sh (检测)

```bash
#!/bin/bash
# 软件安装前检测脚本

PACKAGE=$1

echo "{"
echo "  \"package\": \"$PACKAGE\","
echo "  \"installed\": {"
dpkg -l | grep $PACKAGE && echo "    \"apt\": true," || echo "    \"apt\": false,"
snap list | grep $PACKAGE && echo "    \"snap\": true" || echo "    \"snap\": false"
echo "  },"
echo "  \"service\": {"
systemctl is-active $PACKAGE && echo "    \"system\": \"active\"," || echo "    \"system\": \"inactive\","
systemctl --user is-active $PACKAGE && echo "    \"user\": \"active\"" || echo "    \"user\": \"inactive\""
echo "  }"
echo "}"
```

### install-repair.sh (修复)

```bash
#!/bin/bash
# 软件修复脚本

PACKAGE=$1
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"

echo "【修复】$PACKAGE"

# 备份
mkdir -p "$BACKUP_DIR"
cp -r ~/.config/$PACKAGE "$BACKUP_DIR/" 2>/dev/null

# 修复步骤
echo "1. 重置服务..."
systemctl --user reset-failed $PACKAGE

echo "2. 解除 mask..."
systemctl --user unmask $PACKAGE 2>/dev/null

echo "3. 重新加载..."
systemctl --user daemon-reload

echo "4. 启动服务..."
systemctl --user start $PACKAGE

# 验证
sleep 5
if systemctl --user is-active $PACKAGE > /dev/null 2>&1; then
    echo "✅ 修复成功"
else
    echo "❌ 修复失败，回滚..."
    cp -r "$BACKUP_DIR/$PACKAGE" ~/.config/ 2>/dev/null
    exit 1
fi
```

### install-clean.sh (清理)

```bash
#!/bin/bash
# 软件彻底清理脚本

PACKAGE=$1
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"

echo "【清理】$PACKAGE"

# 停止服务
systemctl stop $PACKAGE 2>/dev/null
systemctl --user stop $PACKAGE 2>/dev/null
pkill -9 $PACKAGE 2>/dev/null

# 备份
mkdir -p "$BACKUP_DIR"
cp -r ~/.config/$PACKAGE "$BACKUP_DIR/" 2>/dev/null
cp -r /etc/$PACKAGE "$BACKUP_DIR/" 2>/dev/null

# 删除包
apt remove --purge -y $PACKAGE 2>/dev/null
snap remove $PACKAGE 2>/dev/null

# 清理残留
rm -rf ~/.config/$PACKAGE 2>/dev/null
rm -rf ~/.local/state/$PACKAGE 2>/dev/null
rm -rf /var/lib/$PACKAGE 2>/dev/null

# 清理 systemd
rm /etc/systemd/system/$PACKAGE.service 2>/dev/null
rm ~/.config/systemd/user/$PACKAGE.service 2>/dev/null
systemctl daemon-reload
systemctl --user daemon-reload

echo "✅ 清理完成"
echo "备份位置：$BACKUP_DIR"
```

### install-safe.sh (安全安装)

```bash
#!/bin/bash
# 安全安装脚本

PACKAGE=$1
PORT=$2

echo "【安全安装】$PACKAGE"

# 1. 检测
./install-check.sh $PACKAGE

# 2. 评估
# (读取检测结果，决策)

# 3. 修复或清理
# (根据评估结果)

# 4. 安装
echo "执行安装..."
apt update
apt install -y $PACKAGE

# 5. 配置
echo "配置服务..."
systemctl enable $PACKAGE
systemctl start $PACKAGE

# 6. 防火墙
if [ ! -z "$PORT" ]; then
    ufw allow $PORT/tcp
    ufw allow $PORT/udp
fi

# 7. 测试
echo "运行测试..."
sleep 5
systemctl is-active $PACKAGE
ss -tlnp | grep $PORT
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT

echo "✅ 安装完成"
```

---

## 📊 风险评估矩阵

| 风险因素 | 分值 | 说明 |
|---------|------|------|
| 官方仓库 | 0 | 最低风险 |
| 官方 PPA | 1 | 低风险 |
| 第三方源 | 5 | 中风险 |
| 源码编译 | 7 | 高风险 |
| 需要 root | +2 | 权限风险 |
| 开放端口 | +2 | 网络风险 |
| 无签名 | +3 | 验证风险 |

**决策**:
- 0-3 分：自动执行
- 4-6 分：用户确认
- 7+ 分：详细报告 + 用户决策

---

## 📈 完整流程图 (v2.0 秩序调整)

```
软件安装请求
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 0 层：蒸馏 → 提取核心信息                             │
│ (这是什么软件？核心功能？依赖要求？)                     │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 3 层：检测 → 系统现状                                 │
│ (已安装？服务状态？端口占用？依赖？)                     │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 1 层：比对 → 分析优劣势                               │
│ (横向对比同类软件，纵向对比太一现状)                     │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 2 层：提炼 → 取其精华去其糟粕                         │
│ (哪些采用？哪些放弃？如何改良适配太一？)                 │
└─────────────────────────────────────────────────────────┘
    ↓ 决策：采用/放弃
    ↓ (采用)
┌─────────────────────────────────────────────────────────┐
│ 第 4 层：评估 → 风险决策                                 │
│ (风险评分 0-10，决策自动执行/用户确认/详细报告)          │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 5 层：修复 → 优先修复                                 │
│ (P0-P4 优先级，尝试修复现有安装)                         │
└─────────────────────────────────────────────────────────┘
    ↓ (修复失败)
┌─────────────────────────────────────────────────────────┐
│ 第 6 层：清理 → 标准化清理                               │
│ (停止服务→备份→删除→清理残留→验证)                      │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ 第 7 层：安装 → 安全安装 + 测试                          │
│ (安全评估→选择源→执行安装→配置→测试)                     │
└─────────────────────────────────────────────────────────┘
    ↓
安装完成 + 测试报告
```

---

## 📝 安装记录模板

```markdown
## 安装记录 <日期>

**软件**: <名称>
**版本**: <版本号>
**安装源**: <apt/snap/source>

### 学习融合
- **蒸馏**: ✅ 完成
- **比对**: ✅ 完成
- **提炼**: ✅ 完成

### 安装部署
- **检测**: ✅ 完成
- **评估**: 风险评分 <0-10>
- **修复**: ✅/❌
- **清理**: ✅/❌
- **安装**: ✅ 完成

**遇到的问题**: <描述>
**解决方案**: <描述>
**测试用例**: <通过的测试>
**改进建议**: <下次优化>
```

---

## 🔗 相关文件

- `LEARNING-METHOD.md` - 深度学习方法 (8 步法)
- `DISTILLATION-PROTOCOL.md` - 蒸馏协议
- `TASK-EXECUTION.md` - 任务执行流程

---

*版本：v2.0 | 创建时间：2026-03-26 | 更新：2026-03-29 | 太一 AGI*

*「学习融合 + 安装部署 = 八层协议框架」*
