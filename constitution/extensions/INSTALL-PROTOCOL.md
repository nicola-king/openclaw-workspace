# INSTALL-PROTOCOL.md - 软件安装与部署协议

> 太一 AGI 系统软件安装标准流程 | 版本：v1.0 | 创建：2026-03-26

---

## 🎯 核心原则

```
帮助，不表演 · 安全优先 · 可恢复 · 自动化
```

---

## 📋 五层协议框架

### 第一层：检测 (Detection)

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

### 第二层：评估 (Assessment)

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

### 第三层：修复 (Repair)

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

### 第四层：清理 (Cleanup)

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

### 第五层：安装 (Installation)

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

## 🧪 测试用例库

### 服务测试
```bash
test_service_active() {
    systemctl is-active $1
    return $?
}

test_port_listening() {
    ss -tlnp | grep -q $1
    return $?
}

test_web_accessible() {
    curl -s -o /dev/null -w "%{http_code}" $1 | grep -q "200"
    return $?
}

test_resource_usage() {
    MEM=$(ps aux | grep $1 | grep -v grep | awk '{print $4}' | cut -d. -f1)
    [ $MEM -lt 20 ]
    return $?
}
```

---

## 📞 故障恢复

### 回滚流程
```bash
# 1. 停止当前服务
systemctl stop $PACKAGE

# 2. 恢复配置
cp -r /opt/backup/<timestamp>/$PACKAGE ~/.config/

# 3. 恢复服务
cp /opt/backup/<timestamp>/$PACKAGE.service /etc/systemd/system/
systemctl daemon-reload

# 4. 启动服务
systemctl start $PACKAGE

# 5. 验证
systemctl is-active $PACKAGE
```

### 紧急恢复
```bash
# 系统无法启动时
# 1. 进入 recovery mode
# 2. mount -o remount,rw /
# 3. 恢复备份
# 4. reboot
```

---

## 📈 持续改进

### 每次安装后记录
```markdown
## 安装记录 <日期>

**软件**: <名称>
**版本**: <版本号>
**安装源**: <apt/snap/source>
**风险评分**: <0-10>
**遇到的问题**: <描述>
**解决方案**: <描述>
**测试用例**: <通过的测试>
**改进建议**: <下次优化>
```

### 每月回顾
- 统计安装成功率
- 分析失败原因
- 优化修复流程
- 更新测试用例

---

*版本：v1.0 | 创建时间：2026-03-26 | 太一 AGI*
