# MemPalace 集成指南 (更新)

> **版本**: 3.1.0  
> **更新时间**: 2026-04-10 21:05  
> **状态**: ⚠️ API 需调整

---

## 📊 安装状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **安装** | ✅ 成功 | v3.1.0 |
| **依赖** | ✅ 正常 | chromadb 等 |
| **API** | ⚠️ 调整 | 非预期 API |
| **CLI** | ✅ 可用 | 命令行工具 |

---

## 🔍 API 分析

**实际导出的模块**:
```python
from mempalace import (
    cli,        # 命令行接口
    config,     # 配置管理
    logging,    # 日志系统
    main,       # 主函数
    version     # 版本信息
)
```

**不是预期的**:
```python
❌ MemPalace 类
❌ MemoryPalace 类
❌ remember() 方法
❌ search() 方法
```

---

## 🔧 使用方式 (CLI)

### 方式 1: 命令行使用

```bash
# 查看帮助
mempalace --help

# 初始化记忆宫殿
mempalace init

# 添加记忆
mempalace add "太一是硅基生命" --category identity

# 搜索记忆
mempalace search "硅基生命"
```

### 方式 2: Python 调用 CLI

```python
import subprocess

# 添加记忆
subprocess.run(["mempalace", "add", "太一是硅基生命", "--category", "identity"])

# 搜索记忆
result = subprocess.run(["mempalace", "search", "硅基生命"], capture_output=True)
print(result.stdout)
```

---

## 🎯 太一集成方案 (更新)

### 方案 A: CLI 封装

```python
# skills/mempalace-integration/mempalace_wrapper.py

import subprocess
import json

class MemPalaceWrapper:
    """MemPalace CLI 封装"""
    
    def __init__(self):
        self.cmd = "mempalace"
    
    def remember(self, text: str, category: str = ""):
        """存储记忆"""
        cmd = [self.cmd, "add", text]
        if category:
            cmd.extend(["--category", category])
        subprocess.run(cmd)
    
    def search(self, query: str):
        """检索记忆"""
        result = subprocess.run(
            [self.cmd, "search", query],
            capture_output=True,
            text=True
        )
        return result.stdout
```

### 方案 B: 直接集成 chromadb

```python
# MemPalace 底层使用 chromadb
# 太一可直接使用 chromadb

import chromadb

client = chromadb.Client()
collection = client.create_collection("taiyi_memory")

# 添加记忆
collection.add(
    documents=["太一是硅基生命"],
    metadatas=[{"category": "identity"}],
    ids=["1"]
)

# 检索记忆
results = collection.query(query_texts=["硅基生命"])
```

---

## 📋 集成状态

| 功能 | 状态 | 说明 |
|------|------|------|
| MemPalace 安装 | ✅ 完成 | v3.1.0 |
| CLI 工具 | ✅ 可用 | 命令行接口 |
| Python API | ⚠️ 调整 | 非预期 API |
| CLI 封装 | ⏳ 待执行 | 包装 CLI |
| chromadb 直用 | ⏳ 待执行 | 底层集成 |
| 太一集成 | ⏳ 待执行 | 混合架构 |

---

## 🚀 下一步

- [x] ✅ 安装 MemPalace
- [x] ✅ 功能测试
- [x] ✅ API 分析
- [ ] CLI 封装实现
- [ ] chromadb 直接集成
- [ ] 太一记忆系统集成

---

*集成指南：太一 AGI*  
*更新时间：2026-04-10 21:05*  
*状态：⚠️ API 需调整/CLI 可用*
