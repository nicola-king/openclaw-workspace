---
name: cad-convert
tier: 2
trigger: DWG/DXF/转换/格式
enabled: true
depends: []
---
# CAD 格式转换技能（DWG→DXF）

## 核心原则

**负熵法则：** 一站式解决文件格式问题

**简化优先：** 自动检测 + 自动转换

**零成本：** 免费工具优先

**搜索优先级：** GitHub 开源 > 全网搜索

---

## 支持格式

| 输入格式 | 输出格式 | 转换方式 |
|----------|----------|----------|
| **DWG** | DXF | ODA File Converter |
| **DXF** | DXF | 直接使用 |
| **其他** | DXF | 手动转换 |

---

## 转换流程

```
用户上传文件
    ↓
格式检测 (.dwg/.dxf)
    ↓
如 DWG → 自动调用转换
    ↓
DXF 解析计算
    ↓
生成报告
```

---

## ODA File Converter

### 下载安装

**官网：** https://www.opendesign.com/guestfiles/oda_file_converter

**步骤：**
1. 注册免费账号
2. 下载对应平台版本
3. 安装到 `/opt/ODAFileConverter/`

### 命令行使用

```bash
# 单个文件转换
ODAFileConverter /path/to/input.dwg /path/to/output.dxf

# 批量转换
for f in *.dwg; do
  ODAFileConverter "$f" "${f%.dwg}.dxf"
done
```

### 集成到太一

```python
import subprocess

def convert_dwg_to_dxf(dwg_path, dxf_path):
    """DWG→DXF 转换"""
    cmd = [
        '/opt/ODAFileConverter/ODAFileConverter',
        dwg_path,
        dxf_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0
```

---

## 备选方案

### 方案 B：libreDWG（开源库）

```bash
# 安装
pip install libredwg

# Python 使用
import libredwg
dwg = libredwg.read_file("input.dwg")
```

**优点：** 无需外部工具
**缺点：** 成熟度中等，文档少

### 方案 C：手动转换指南

**用户自行转换：**
1. 用 CAD 软件打开 DWG
2. 另存为 → 选择 DXF 格式
3. 上传 DXF 到太一

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 转换失败 | ODA 未安装 | 提示用户安装 |
| 格式不支持 | 非 DWG/DXF | 提示手动转换 |
| 文件损坏 | 文件问题 | 提示重新上传 |

---

## 快速参考

### 安装 ODA

```bash
# 下载
wget https://www.opendesign.com/.../ODAFileConverter.tar.gz
tar -xzf ODAFileConverter.tar.gz
sudo mv ODAFileConverter /opt/
```

### 转换命令

```bash
# 单个文件
/opt/ODAFileConverter/ODAFileConverter input.dwg output.dxf

# 批量转换
for f in *.dwg; do
  /opt/ODAFileConverter/ODAFileConverter "$f" "${f%.dwg}.dxf"
done
```

---

## 总结

**定位：** CAD 格式预处理技能

**价值：** 一站式解决格式问题

**审查：** L1（太一自主执行）

---
*版本：1.0 | 生效日期：2026-03-22 | 最后更新：12:35*
