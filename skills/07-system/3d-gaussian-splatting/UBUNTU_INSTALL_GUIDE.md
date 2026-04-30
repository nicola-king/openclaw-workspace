# 🐧 Ubuntu 工控机 3D 高斯泼溅安装指南

> **版本**: v1.0  
> **创建**: 2026-04-18 09:55  
> **系统**: Ubuntu 20.04/22.04/24.04  
> **状态**: 🚀 立即安装

---

## 📦 系统要求

### 最低要求

| 要求 | 详情 |
|------|------|
| **系统** | Ubuntu 20.04+ |
| **CPU** | 4 核+ |
| **内存** | 8GB+ |
| **GPU** | NVIDIA GTX 1060+ (可选但推荐) |
| **存储** | 10GB+ 可用空间 |
| **网络** | WiFi/有线 (下载用) |

---

### 推荐配置

| 配置 | 详情 |
|------|------|
| **系统** | Ubuntu 22.04 LTS |
| **CPU** | 8 核+ (i7/Ryzen 7) |
| **内存** | 16GB+ |
| **GPU** | NVIDIA RTX 3060+ |
| **存储** | 50GB+ SSD |
| **CUDA** | 11.8+ (NVIDIA GPU) |

---

## 🔧 方案选择

### 方案 1: Brush (推荐) ⭐⭐⭐⭐⭐

**特点**:
```
✅ 跨平台支持
✅ 开源免费
✅ 本地处理
✅ 支持照片/视频
✅ 高质量输出
```

**适用**:
```
• 有 NVIDIA GPU
• 追求高质量
• 学习研究
• 批量处理
```

---

### 方案 2: LichtFeld Studio ⭐⭐⭐⭐⭐

**特点**:
```
✅ 桌面应用
✅ 图形界面
✅ 易于使用
✅ 本地 GPU 运行
✅ Python 插件支持
```

**适用**:
```
• 不想用命令行
• 需要图形界面
• 专业编辑需求
```

---

### 方案 3: 官方 3DGS ⭐⭐⭐⭐

**特点**:
```
✅ 官方实现
✅ 最权威
✅ 开源免费
✅ 需要编译
```

**适用**:
```
• 研究人员
• 开发者
• 需要最新功能
```

---

## 🚀 方案 1: Brush 安装 (推荐)

### Step 1: 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

---

### Step 2: 安装依赖

```bash
# 基础依赖
sudo apt install -y python3 python3-pip python3-venv

# Git
sudo apt install -y git

# FFmpeg (视频处理)
sudo apt install -y ffmpeg

# COLMAP 依赖
sudo apt install -y libeigen3-dev libboost-all-dev wget
```

---

### Step 3: 安装 NVIDIA 驱动 (如有 GPU)

```bash
# 检查 GPU
lspci | grep -i nvidia

# 安装驱动
sudo apt install -y nvidia-driver-535

# 安装 CUDA Toolkit
sudo apt install -y nvidia-cuda-toolkit

# 验证安装
nvidia-smi
nvcc --version
```

---

### Step 4: 克隆 Brush

```bash
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting

# 克隆 Brush
git clone https://github.com/ArthurBrussee/brush.git
cd brush
```

---

### Step 5: 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip
```

---

### Step 6: 安装 PyTorch

**NVIDIA GPU**:
```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**无 GPU (CPU 模式)**:
```bash
# CPU 版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

### Step 7: 安装 Brush 依赖

```bash
# 安装依赖
pip install -r requirements.txt

# 安装额外依赖
pip install opencv-python-headless pycolmap
```

---

### Step 8: 验证安装

```bash
# 测试 Brush
python brush.py --help

# 测试 CUDA (如有 GPU)
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

---

## 🎨 使用 Brush

### 照片重建

```bash
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting/brush

# 运行重建
python brush.py reconstruct \
  --input /path/to/photos \
  --output /path/to/output \
  --format ply
```

---

### 视频重建

```bash
# 先从视频提取帧
ffmpeg -i input.mp4 -vf fps=1 frames/frame_%04d.jpg

# 重建
python brush.py reconstruct \
  --input frames/ \
  --output output/ \
  --format ply
```

---

### 查看结果

```bash
# 使用 MeshLab 查看
meshlab output/reconstruction.ply

# 或使用在线查看器
# https://antimatter15.com/splat/
```

---

## 🚀 方案 2: LichtFeld Studio 安装

### Step 1: 下载

```bash
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting

# 下载最新版本
wget https://github.com/lichtfeld-io/lichtfeld/releases/latest/download/LichtFeld-Linux.AppImage

# 赋予执行权限
chmod +x LichtFeld-Linux.AppImage
```

---

### Step 2: 运行

```bash
# 直接运行
./LichtFeld-Linux.AppImage
```

---

### Step 3: 使用

```
1. 打开 LichtFeld
2. 导入照片/视频
3. 点击"Reconstruct"
4. 等待处理
5. 查看/编辑
6. 导出
```

---

## 🚀 方案 3: 官方 3DGS 安装

### Step 1: 克隆仓库

```bash
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting

git clone https://github.com/graphdeco-inria/gaussian-splatting.git
cd gaussian-splatting
```

---

### Step 2: 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 安装子模块
git submodule update --init --recursive

# 安装依赖
pip install -r requirements.txt
```

---

### Step 3: 编译 CUDA 扩展

```bash
# 需要 NVIDIA GPU 和 CUDA
cd submodules/diff-gaussian-rasterization
pip install .

cd ../simple-knn
pip install .
```

---

### Step 4: 训练

```bash
python train.py -s /path/to/images
```

---

## 🔧 Ubuntu 优化

### GPU 性能优化

```bash
# 设置高性能模式
sudo nvidia-smi -pm 1
sudo nvidia-smi --power-limit=300

# 监控 GPU
watch -n 1 nvidia-smi
```

---

### 内存优化

```bash
# 增加 swap (如内存不足)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### 存储优化

```bash
# 清理缓存
sudo apt autoremove
sudo apt clean

# 监控磁盘
df -h
du -sh /home/nicola/.openclaw/workspace/3d-gaussian-splatting/*
```

---

## 📊 性能预期

### 处理时间对比

| 配置 | 照片数 | 时间 |
|------|--------|------|
| **RTX 3060** | 50 张 | 5-10 分钟 |
| **RTX 3060** | 100 张 | 10-20 分钟 |
| **RTX 3080** | 50 张 | 3-7 分钟 |
| **RTX 3080** | 100 张 | 7-15 分钟 |
| **CPU 模式** | 50 张 | 30-60 分钟 |
| **CPU 模式** | 100 张 | 60-120 分钟 |

---

## 💾 输出格式

### 支持格式

| 格式 | 用途 | 大小 |
|------|------|------|
| **.ply** | 3D 高斯 | 50-500MB |
| **.obj** | 网格 | 10-100MB |
| **.mp4** | 漫游视频 | 10-50MB |
| **.html** | 网页展示 | 1-5MB |

---

## 🎯 测试流程

### 快速测试

```bash
# 1. 准备测试照片
mkdir -p /home/nicola/.openclaw/workspace/3d-gaussian-splatting/test/photos

# 2. 复制手机照片到该目录

# 3. 运行测试
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting/brush
python brush.py reconstruct \
  --input ../test/photos \
  --output ../test/output \
  --format ply

# 4. 查看结果
ls -lh ../test/output/
```

---

## 🔍 故障排查

### 问题 1: CUDA 不可用

**现象**: `CUDA not available`  
**解决**:
```bash
# 检查 NVIDIA 驱动
nvidia-smi

# 重新安装 PyTorch CUDA 版本
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

### 问题 2: 内存不足

**现象**: `Killed` 或 `OOM`  
**解决**:
```bash
# 增加 swap
sudo fallocate -l 16G /swapfile
sudo swapon /swapfile

# 减少照片数量
# 或使用更低分辨率
```

---

### 问题 3: 依赖冲突

**现象**: `ImportError`  
**解决**:
```bash
# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎊 总结

### 推荐方案

```
🏆 Brush - 最佳选择
   • 开源免费
   • 高质量
   • 本地处理
   • 易于使用

💻 LichtFeld - 图形界面
   • 桌面应用
   • 易于使用
   • 专业编辑

🔬 官方 3DGS - 研究用途
   • 官方实现
   • 最新功能
   • 需要编译
```

---

### 立即开始

```bash
# 1. 安装依赖
sudo apt update && sudo apt install -y python3-pip git ffmpeg

# 2. 克隆 Brush
cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting
git clone https://github.com/ArthurBrussee/brush.git

# 3. 安装
cd brush
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# 4. 测试
python brush.py --help
```

---

*太一 AGI · Ubuntu 3D 高斯安装指南 v1.0 · 2026-04-18 09:55*

**🐧 Ubuntu 工控机完全支持！立即安装 Brush！**
