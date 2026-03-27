# Syncthing 文件传输配置方案

> 太一→工作站单向同步 + 笔记本→工作站单向同步

---

## 📁 目录结构

### 太一 (工控机)

```
/home/nicola/.openclaw/workspace/
├── 📁 sync-to-workstation/        # 同步到工作站
│   ├── reports/                   # 报告
│   ├── skills/                    # 技能
│   ├── memory/                    # 记忆
│   └── jobs/                      # 待处理任务
├── 📁 sync-from-workstation/      # 从工作站接收
│   ├── results/                   # 工作成果
│   └── data/                      # 数据文件
└── 📁 local/                      # 本地不同步
    └── cache/
```

### 工作站 (家里 - 中心节点)

```
/home/nicola/syncthing-hub/
├── 📁 from-taiyi/                 # 从太一接收 (只读)
│   ├── reports/
│   ├── skills/
│   ├── memory/
│   └── jobs/                      # 待处理任务队列
├── 📁 from-laptop/                # 从笔记本接收 (只读)
│   ├── data/
│   └── requests/                  # 资料调取请求
├── 📁 to-taiyi/                   # 发送给太一 (只读)
│   ├── results/                   # 工作成果
│   └── data/                      # 数据文件
├── 📁 to-laptop/                  # 发送给笔记本 (只读)
│   ├── results/
│   └── data/
└── 📁 processing/                 # 处理中
    └── current Jobs/
```

### 笔记本 (办公室)

```
/home/nicola/laptop-sync/
├── 📁 sync-to-workstation/        # 同步到工作站
│   ├── data/                      # 数据文件
│   └── requests/                  # 调取请求
├── 📁 sync-from-workstation/      # 从工作站接收
│   ├── results/                   # 资料/成果
│   └── data/                      # 数据文件
└── 📁 local/                      # 本地不同步
```

---

## 🔧 Syncthing 配置

### 设备 ID

获取设备 ID:
```bash
# 在每个设备上执行
syncthing --device-id
# 或在 Web 界面：操作 → 显示 ID
```

### 文件夹共享配置

#### 太一 → 工作站 (单向)

| 配置项 | 太一端 | 工作站端 |
|--------|--------|---------|
| 文件夹 ID | `taiyi-to-workstation` | `from-taiyi` |
| 文件夹路径 | `~/.openclaw/workspace/sync-to-workstation/` | `~/syncthing-hub/from-taiyi/` |
| 共享设备 | 工作站 | 太一 |
| 权限 | 发送接收 | **仅接收** (只读) |
| 忽略权限 | ❌ | ✅ |
| 版本控制 | 简单文件版本控制 | 简单文件版本控制 |

#### 工作站 → 太一 (单向)

| 配置项 | 工作站端 | 太一端 |
|--------|---------|--------|
| 文件夹 ID | `workstation-to-taiyi` | `from-workstation` |
| 文件夹路径 | `~/syncthing-hub/to-taiyi/` | `~/.openclaw/workspace/sync-from-workstation/` |
| 共享设备 | 太一 | 工作站 |
| 权限 | 发送接收 | **仅接收** (只读) |
| 忽略权限 | ❌ | ✅ |

#### 笔记本 → 工作站 (单向)

| 配置项 | 笔记本端 | 工作站端 |
|--------|---------|--------|
| 文件夹 ID | `laptop-to-workstation` | `from-laptop` |
| 文件夹路径 | `~/laptop-sync/sync-to-workstation/` | `~/syncthing-hub/from-laptop/` |
| 共享设备 | 工作站 | 笔记本 |
| 权限 | 发送接收 | **仅接收** (只读) |

#### 工作站 → 笔记本 (单向)

| 配置项 | 工作站端 | 笔记本端 |
|--------|---------|--------|
| 文件夹 ID | `workstation-to-laptop` | `from-workstation` |
| 文件夹路径 | `~/syncthing-hub/to-laptop/` | `~/laptop-sync/sync-from-workstation/` |
| 共享设备 | 笔记本 | 工作站 |
| 权限 | 发送接收 | **仅接收** (只读) |

---

## 🚀 远程调用机制

### 太一 → 工作站 (任务调度)

**流程**:
```
1. 太一创建任务文件
   → sync-to-workstation/jobs/job-YYYYMMDD-HHMMSS.json

2. Syncthing 自动同步到工作站
   → from-taiyi/jobs/job-YYYYMMDD-HHMMSS.json

3. 工作站监控脚本检测到新任务
   → 执行任务

4. 任务完成写入结果
   → to-taiyi/results/result-YYYYMMDD-HHMMSS.json

5. Syncthing 同步回太一
   → from-workstation/results/result-YYYYMMDD-HHMMSS.json

6. 太一读取结果
```

**任务文件格式**:
```json
{
  "job_id": "job-20260326-223000",
  "type": "data_processing",
  "input_files": ["data/file1.csv", "data/file2.csv"],
  "command": "python3 process.py",
  "priority": "high",
  "created_at": "2026-03-26T22:30:00Z",
  "timeout": 3600
}
```

**工作站监控脚本**:
```python
#!/usr/bin/env python3
# ~/syncthing-hub/scripts/job-monitor.py

import os
import json
import subprocess
from pathlib import Path

JOBS_DIR = Path("~/syncthing-hub/from-taiyi/jobs").expanduser()
RESULTS_DIR = Path("~/syncthing-hub/to-taiyi/results").expanduser()
PROCESSING_DIR = Path("~/syncthing-hub/processing").expanduser()

def process_job(job_file):
    with open(job_file) as f:
        job = json.load(f)
    
    # 移动到处理中
    processing_file = PROCESSING_DIR / job_file.name
    job_file.rename(processing_file)
    
    try:
        # 执行任务
        result = subprocess.run(
            job['command'],
            shell=True,
            capture_output=True,
            timeout=job.get('timeout', 3600)
        )
        
        # 写入结果
        result_file = RESULTS_DIR / f"result-{job['job_id']}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'job_id': job['job_id'],
                'status': 'completed',
                'return_code': result.returncode,
                'stdout': result.stdout.decode(),
                'stderr': result.stderr.decode()
            }, f, indent=2)
        
    except Exception as e:
        # 写入错误
        result_file = RESULTS_DIR / f"result-{job['job_id']}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'job_id': job['job_id'],
                'status': 'failed',
                'error': str(e)
            }, f, indent=2)
    
    # 清理
    processing_file.unlink()

if __name__ == '__main__':
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        for job_file in JOBS_DIR.glob('job-*.json'):
            process_job(job_file)
        time.sleep(10)  # 每 10 秒检查一次
```

---

### 笔记本 → 工作站 (资料调取)

**流程**:
```
1. 笔记本创建调取请求
   → sync-to-workstation/requests/request-YYYYMMDD-HHMMSS.json

2. Syncthing 同步到工作站
   → from-laptop/requests/request-YYYYMMDD-HHMMSS.json

3. 工作站监控脚本检测到请求
   → 准备资料

4. 资料写入发送目录
   → to-laptop/data/files.zip

5. Syncthing 同步到笔记本
   → sync-from-workstation/data/files.zip
```

**请求文件格式**:
```json
{
  "request_id": "req-20260326-223000",
  "type": "data_retrieval",
  "files": ["reports/report1.pdf", "data/dataset.csv"],
  "priority": "normal",
  "created_at": "2026-03-26T22:30:00Z"
}
```

---

## 📊 监控仪表板

创建监控脚本:
```bash
# ~/.openclaw/workspace/skills/suwen/syncthing-monitor.sh
```

功能:
- 同步状态检查
- 任务队列监控
- 传输速度统计
- 错误告警

---

## 🔐 安全配置

### 防火墙规则

```bash
# 允许 Syncthing 端口
sudo ufw allow 22000/tcp  # 文件传输
sudo ufw allow 22000/udp  # 发现协议
sudo ufw allow 8384/tcp   # Web 界面 (仅本地)
```

### 设备认证

- 每个设备有唯一 Device ID
- 首次连接需要手动确认
- 所有传输端到端加密

### 访问控制

- Web 界面绑定 127.0.0.1
- 启用 HTTPS
- 设置强密码

---

## 📋 实施步骤

### Day 1: 安装配置

- [ ] 太一安装 Syncthing
- [ ] 工作站安装 Syncthing
- [ ] 笔记本安装 Syncthing
- [ ] 创建目录结构
- [ ] 配置文件夹共享

### Day 2: 远程调用

- [ ] 太一→工作站任务调度脚本
- [ ] 工作站→太一结果返回脚本
- [ ] 笔记本→工作站资料调取脚本
- [ ] 监控仪表板

### Day 3: 测试优化

- [ ] 端到端测试
- [ ] 性能优化
- [ ] 错误处理
- [ ] 文档完善

---

## 📞 故障排查

### 问题 1：同步慢

**解决**:
```
1. 检查网络连接
2. 增加带宽限制
3. 减少同时传输文件数
```

### 问题 2：文件冲突

**解决**:
```
1. 启用版本控制
2. 检查文件锁
3. 避免同时修改
```

### 问题 3：设备离线

**解决**:
```
1. 检查 Tailscale 连接
2. 重启 Syncthing 服务
3. 检查防火墙
```

---

*创建时间：2026-03-26 | 太一 AGI*
