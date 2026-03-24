# CAD 工具安装指南 (免费开源)

**状态：** 🟡 待安装
**预计时间：** 30 分钟
**成本：** $0

---

## 方案选择

| 工具 | 用途 | 推荐 |
|------|------|------|
| **LibreCAD** | 2D 图纸查看/编辑 | ✅ 首选 |
| **FreeCAD** | 3D 建模 | ✅ 备选 |
| **ODA File Converter** | DWG→DXF 批量转换 | ✅ 必需 |

---

## 安装命令 (Ubuntu/Debian)

### 1. LibreCAD (2D)
```bash
sudo apt update
sudo apt install -y librecad
```

### 2. FreeCAD (3D)
```bash
sudo apt install -y freecad
```

### 3. ODA File Converter
```bash
# 下载
cd /tmp
wget https://www.opendesign.com/sites/default/files/2023-12/ODAFileConverter_24_12_0_Ubuntu22_64bit_2024-12-11.tar.xz

# 解压
tar -xf ODAFileConverter_*.tar.xz
cd ODAFileConverter_*

# 安装依赖
sudo apt install -y libxcb-cursor0

# 运行
./ODAFileConverter
```

---

## 验证安装

```bash
# LibreCAD
librecad --version

# FreeCAD
freecad --version

# ODA
ls -la /tmp/ODAFileConverter_*/ODAFileConverter
```

---

## 自动化转换脚本

```bash
#!/bin/bash
# dwg-to-dxf.sh
INPUT_DIR="$1"
OUTPUT_DIR="$2"

for dwg in "$INPUT_DIR"/*.dwg; do
    filename=$(basename "$dwg" .dwg)
    /tmp/ODAFileConverter_*/ODAFileConverter "$dwg" "$OUTPUT_DIR/$filename.dxf"
done
```

---

## 下一步

执行以下命令安装：
```bash
sudo apt update && sudo apt install -y librecad freecad
```

然后下载 ODA File Converter。
