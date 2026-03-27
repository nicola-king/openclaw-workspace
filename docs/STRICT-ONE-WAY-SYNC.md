# 严格单向同步配置说明

> 核心原则：工作站和笔记本不能主动向太一传输数据

---

## 🎯 核心原则

```
✅ 太一 → 工作站：允许 (备份/命令)
❌ 工作站 → 太一：禁止 (除非太一请求)
✅ 笔记本 → 工作站：允许 (数据/请求)
❌ 笔记本 → 太一：禁止 (必须通过工作站中转)
✅ 工作站 → 笔记本：允许 (共享所有数据)
❌ 工作站 → 太一：禁止 (除非太一触发)
```

---

## 📁 目录权限设计

### 太一端

```
~/.openclaw/workspace/
├── sync-to-workstation/        # 太一写入 ✅
│   ├── backup/                 # 备份数据
│   ├── commands/               # 命令文件
│   └── results/                # 接收结果 (只读) ⚠️
├── sync-from-workstation/      # 接收结果 (只读) ⚠️
│   ├── results/                # 任务执行结果
│   └── data/                   # 请求的数据
└── local/                      # 本地不同步
```

**权限**:
- `sync-to-workstation/`: 太一可写，工作站只读
- `sync-from-workstation/`: 太一只读，工作站可写

---

### 工作站端

```
/mnt/d/syncthing-hub/
├── from-taiyi/                 # 只读 ⚠️ (太一写入)
│   ├── backup/
│   └── commands/
├── to-taiyi/                   # 工作站可写 (仅结果)
│   ├── results/                # 任务结果
│   └── data/                   # 请求的数据
├── from-laptop/                # 只读 ⚠️ (笔记本写入)
│   ├── data/
│   └── requests/
├── to-laptop/                  # 工作站可写 (共享)
│   ├── all-data/
│   └── results/
└── shared/                     # SMB 共享 (笔记本访问)
    ├── public/
    ├── projects/
    └── archives/
```

**权限**:
- `from-taiyi/`: chmod 555 (只读)
- `from-laptop/`: chmod 555 (只读)
- `to-taiyi/`: chmod 755 (仅写入结果)
- `to-laptop/`: chmod 755 (可写入共享)
- `shared/`: chmod 755 (可写入共享)

---

### 笔记本端

```
~/laptop-sync/
├── sync-to-workstation/        # 笔记本写入 ✅
│   ├── data/                   # 数据文件
│   └── requests/               # 请求文件
├── sync-from-workstation/      # 接收结果 (只读) ⚠️
│   ├── results/                # 请求结果
│   └── data/                   # 数据文件
└── local/                      # 本地不同步
```

**权限**:
- `sync-to-workstation/`: 笔记本可写，工作站只读
- `sync-from-workstation/`: 笔记本只读，工作站可写

---

## 🔧 Syncthing 配置要点

### 关键设置

**发送端配置**:
```
文件夹属性 → 共享设备 → 目标设备
权限：发送接收 (Send & Receive)
```

**接收端配置**:
```
文件夹属性 → 共享设备 → 源设备
权限：仅接收 (Receive Only) ⚠️
```

### 具体配置

#### 太一 → 工作站 (单向)

**太一端**:
- 文件夹 ID: `taiyi-backup`
- 路径：`~/.openclaw/workspace/sync-to-workstation`
- 共享给：工作站
- 权限：发送接收

**工作站端**:
- 文件夹 ID: `from-taiyi`
- 路径：`/mnt/d/syncthing-hub/from-taiyi`
- 共享给：太一
- 权限：**仅接收 (Receive Only)** ⚠️

---

#### 工作站 → 太一 (单向 - 仅结果)

**工作站端**:
- 文件夹 ID: `workstation-results`
- 路径：`/mnt/d/syncthing-hub/to-taiyi`
- 共享给：太一
- 权限：发送接收

**太一端**:
- 文件夹 ID: `from-workstation`
- 路径：`~/.openclaw/workspace/sync-from-workstation`
- 共享给：工作站
- 权限：**仅接收 (Receive Only)** ⚠️

**限制**:
- 太一不在此目录创建文件
- 只接收工作站返回的结果

---

#### 笔记本 → 工作站 (单向)

**笔记本端**:
- 文件夹 ID: `laptop-data`
- 路径：`~/laptop-sync/sync-to-workstation`
- 共享给：工作站
- 权限：发送接收

**工作站端**:
- 文件夹 ID: `from-laptop`
- 路径：`/mnt/d/syncthing-hub/from-laptop`
- 共享给：笔记本
- 权限：**仅接收 (Receive Only)** ⚠️

---

#### 工作站 → 笔记本 (单向 - 共享)

**工作站端**:
- 文件夹 ID: `workstation-to-laptop`
- 路径：`/mnt/d/syncthing-hub/to-laptop`
- 共享给：笔记本
- 权限：发送接收

**笔记本端**:
- 文件夹 ID: `from-workstation`
- 路径：`~/laptop-sync/sync-from-workstation`
- 共享给：工作站
- 权限：**仅接收 (Receive Only)** ⚠️

---

## 🚫 防止主动传输机制

### 1. 文件系统权限

```bash
# 工作站端设置
chmod 555 /mnt/d/syncthing-hub/from-taiyi      # 只读
chmod 555 /mnt/d/syncthing-hub/from-laptop     # 只读
```

### 2. Syncthing 只读模式

```
Syncthing Web 界面 → 文件夹 → 共享设备 → 权限
选择 "Receive Only" (仅接收)
```

### 3. 监控脚本检测

```python
# 检测异常写入
if detect_write_to_readonly_folder():
    log_alert("⚠️ 检测到向只读文件夹写入！")
    send_telegram_alert()
```

### 4. 定期审计

```bash
# 每周检查权限
find /mnt/d/syncthing-hub/from-* -type f -mtime -7
# 如有新文件，说明权限配置有误
```

---

## ✅ 数据触发流程

### 太一请求工作站数据

```
1. 太一创建请求文件
   → sync-to-workstation/requests/request-001.json

2. Syncthing 同步到工作站
   → from-taiyi/requests/request-001.json

3. 工作站监控脚本检测到请求
   → 准备数据

4. 数据写入发送目录
   → to-taiyi/data/files.zip

5. Syncthing 同步回太一
   → sync-from-workstation/data/files.zip

6. 太一读取数据
```

**关键**: 只有太一主动请求，工作站才返回数据！

---

### 笔记本请求工作站数据

```
1. 笔记本创建请求文件
   → sync-to-workstation/requests/request-001.json

2. Syncthing 同步到工作站
   → from-laptop/requests/request-001.json

3. 工作站监控脚本检测到请求
   → 准备数据

4. 数据写入共享目录
   → to-laptop/results/files.zip

5. Syncthing 同步回笔记本
   → sync-from-workstation/results/files.zip

6. 笔记本读取数据
```

**关键**: 笔记本通过工作站获取数据，不直接访问太一！

---

## 📊 验证清单

- [ ] `from-taiyi/` 权限 555 (只读)
- [ ] `from-laptop/` 权限 555 (只读)
- [ ] Syncthing 接收端设置为 "Receive Only"
- [ ] 工作站无法主动写入太一目录
- [ ] 笔记本无法主动写入太一目录
- [ ] 太一请求时，工作站可返回结果
- [ ] 笔记本请求时，工作站可提供数据

---

## 🚨 异常处理

### 场景 1: 工作站误写入太一目录

```bash
# 检测
ls -la /mnt/d/syncthing-hub/from-taiyi/
# 如有新文件，说明权限有误

# 修复
chmod 555 /mnt/d/syncthing-hub/from-taiyi
# Syncthing 会标记为 "Out of Sync"
```

### 场景 2: Syncthing 权限错误

```
Syncthing Web 界面 → 文件夹 → 覆盖更改
选择 "Revert Local Changes"
```

---

*创建时间：2026-03-26 | 太一 AGI | 版本：v1.0*
