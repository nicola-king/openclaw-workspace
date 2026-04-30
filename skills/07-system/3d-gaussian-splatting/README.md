# 🎨 3D 高斯泼溅 (Brush) 集成技能

> **版本**: v1.0  
> **创建**: 2026-04-18 09:43  
> **项目**: https://github.com/ArthurBrussee/brush  
> **状态**:  准备安装

---

## 📦 安装步骤

### 1. 系统要求

```
✅ 操作系统：Windows/macOS/Linux
✅ GPU: NVIDIA/AMD/Intel (支持 Vulkan)
✅ 内存：8GB+ (推荐 16GB)
✅ 存储：10GB+ 可用空间
✅ Python: 3.8+
```

---

### 2. 安装 Brush

#### macOS 安装

```bash
# 使用 Homebrew
brew install brush

# 或从 GitHub 下载
git clone https://github.com/ArthurBrussee/brush.git
cd brush
pip install -r requirements.txt
```

---

#### Windows 安装

```powershell
# 下载安装包
# https://github.com/ArthurBrussee/brush/releases

# 或使用 winget
winget install ArthurBrussee.brush
```

---

#### Linux 安装

```bash
# 从 GitHub 克隆
git clone https://github.com/ArthurBrussee/brush.git
cd brush

# 安装依赖
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# 运行
python brush.py
```

---

## 📸 使用流程

### Step 1: 拍照/视频

**拍照要求**:
```
• 数量：20-100 张
• 角度：环绕 360°
• 重叠：60-80%
• 光线：均匀
• 分辨率：1080p+
```

**视频要求**:
```
• 时长：30 秒 -2 分钟
• 分辨率：1080p/4K
• 帧率：30-60 FPS
• 运动：缓慢环绕
```

---

### Step 2: 导入 Brush

```
1. 打开 Brush 应用
2. 点击"New Project"
3. 选择照片/视频文件夹
4. 点击"Import"
```

---

### Step 3: 3D 重建

```
1. 点击"Reconstruct"
2. 等待处理 (5-30 分钟)
3. 自动完成 COLMAP + 3DGS
```

---

### Step 4: 预览/编辑

```
• 实时 3D 预览
• 调整参数
• 编辑场景
• 优化质量
```

---

### Step 5: 导出

```
支持格式:
• .ply (3D 高斯)
• .obj (网格)
• .mp4 (视频)
• 交互式网页
```

---

## 🔧 太一集成技能

### Skill 配置

```json
{
  "name": "3d-gaussian-splatting",
  "version": "1.0",
  "description": "3D 高斯泼溅重建技能",
  "input": {
    "type": "photos_or_video",
    "min_photos": 20,
    "max_photos": 200,
    "video_max_duration": 120
  },
  "output": {
    "format": ["ply", "obj", "mp4", "html"],
    "processing_time": "5-30 minutes"
  }
}
```

---

### 使用示例

```bash
# 命令行使用
python3 skills/07-system/3d-gaussian-splatting/brush_skill.py \
  --input /path/to/photos \
  --output /path/to/output \
  --format ply
```

---

## 📊 处理时间

| 照片数量 | 处理时间 | 输出大小 |
|----------|----------|----------|
| 20-50 张 | 5-10 分钟 | 50-200MB |
| 50-100 张 | 10-20 分钟 | 200-500MB |
| 100-200 张 | 20-30 分钟 | 500MB-1GB |
| 视频 1 分钟 | 15-25 分钟 | 300-600MB |

---

## 💰 成本

```
✅ 软件：免费开源
✅ 硬件：已有设备
✅ 云端：无需
✅ 总计：$0
```

---

## 🎯 应用场景

### 1. 房地产展示

```
• 房屋 3D 漫游
• 虚拟看房
• 室内设计和
```

### 2. 电商产品展示

```
• 产品 3D 展示
• 360°查看
• 虚拟试用
```

### 3. 旅游纪念

```
• 景点 3D 记录
• 旅行回忆
• 分享体验
```

### 4. 文物数字化

```
• 文物 3D 存档
• 虚拟博物馆
• 教育展示
```

---

## 🔗 相关链接

| 资源 | 链接 |
|------|------|
| **GitHub** | https://github.com/ArthurBrussee/brush |
| **官方 3DGS** | https://github.com/graphdeco-inria/gaussian-splatting |
| **Mobile-GS** | https://github.com/xiaobiaodu/Mobile-GS |
| **LichtFeld** | https://lichtfeld.io/ |
| **教程** | https://www.youtube.com/results?search_query=3d+gaussian+splatting |

---

## 🎊 总结

### 优势

```
✅ 免费开源
✅ 手机拍照即可
✅ 实时渲染
✅ 高质量输出
✅ 跨平台支持
✅ 易于使用
```

---

### 下一步

```
1. ✅ 选择安装方案
2. ⏳ 安装 Brush
3. ⏳ 准备照片/视频
4. ⏳ 3D 重建
5. ⏳ 预览/导出
```

---

*太一 AGI · 3D 高斯泼溅技能 v1.0 · 2026-04-18 09:43*

**🎨 3D 高斯泼溅技能已创建！准备安装 Brush！**
