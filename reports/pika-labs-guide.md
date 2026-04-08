# 🎬 Pika Labs 快速使用指南

> 创建时间：2026-04-06 09:29  
> 用途：让重庆涂鸦图片动起来  
> 状态：✅ 免费可用，无需 API Key

---

## 🚀 快速开始（5 分钟）

### 步骤 1: 加入 Pika Discord

**官方邀请链接**: https://discord.gg/pika

1. 点击链接
2. 登录 Discord（没有账号需注册）
3. 接受邀请加入 Pika 服务器

### 步骤 2: 找到生成频道

加入后，在左侧频道列表找到：
- `#create` - 主生成频道
- `#create-1`, `#create-2` - 备用频道

### 步骤 3: 发送指令

在频道中输入：

```
/create
```

会弹出指令菜单，选择 **`/animate`** (图生视频)

---

## 📸 图生视频参数

### 基础用法

```
/animate
image: [上传你的涂鸦图片]
prompt: 金鱼游动，霓虹灯闪烁，赛博朋克风格
motion: 3  (运动强度 1-10)
camera: zoom_in  (镜头效果)
```

### 完整参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `image` | 上传图片 | 必选 |
| `prompt` | 动作描述 | 必选 |
| `motion` | 运动强度 (1-10) | 3-5 |
| `camera` | 镜头效果 | zoom_in/pan_left/pan_right |
| `aspect_ratio` | 画面比例 | 16:9 / 9:16 / 1:1 |
| `fps` | 帧率 | 24 |

---

## 🎨 针对涂鸦图片的提示词

### 中文提示词
```
金鱼尾巴摆动，霓虹灯光闪烁，
粒子效果飘动，赛博朋克风格，
动态模糊，电影感，高饱和度
```

### 英文提示词 (推荐)
```
Golden fish tail moving, neon lights flickering,
particle effects floating, cyberpunk style,
motion blur, cinematic, vibrant colors,
street art coming to life
```

### 镜头效果建议
- `zoom_in` - 缓慢放大 (聚焦金鱼)
- `pan_left` - 从左到右扫过
- `pan_right` - 从右到左扫过

---

## 📊 预期效果

| 指标 | 数值 |
|------|------|
| **视频时长** | 3-4 秒 |
| **分辨率** | 720p-1080p |
| **帧率** | 24fps |
| **生成时间** | 1-3 分钟 |
| **免费配额** | 约 100-200 次/天 |

---

## 💡 进阶技巧

### 1. 局部动画
```
/animate
image: [涂鸦图片]
prompt: only the golden fish moves, rest is static
motion: 2
```

### 2. 多重效果
```
prompt: fish swimming + lights flickering + particles floating
motion: 4
camera: zoom_in
```

### 3. 风格强化
```
prompt: cyberpunk style, neon glow, dynamic lighting,
        cinematic quality, highly detailed
```

---

## 🎯 完整操作流程

```
1. Discord → 加入 Pika 服务器
2. 进入 #create 频道
3. 输入 /animate
4. 上传涂鸦图片
5. 输入提示词
6. 等待 1-3 分钟
7. 下载视频
```

---

## 📝 示例指令 (复制即用)

### 示例 1: 金鱼游动
```
/create animate
image: [上传涂鸦.jpg]
prompt: golden fish swimming, tail moving gently, 
        neon lights flickering, cyberpunk atmosphere
motion: 3
camera: zoom_in
```

### 示例 2: 全景动态
```
/create animate
image: [上传涂鸦.jpg]
prompt: entire mural coming to life, lights blinking,
        particles floating, dynamic street art
motion: 4
camera: pan_left
```

### 示例 3: 电影感
```
/create animate
image: [上传涂鸦.jpg]
prompt: cinematic motion, golden fish breathing,
        neon reflections, moody lighting
motion: 2
camera: zoom_in
aspect_ratio: 16:9
```

---

## ⚠️  注意事项

### ✅ 推荐
- 使用英文提示词 (效果更好)
- 运动强度从 3 开始测试
- 首次生成用小图测试
- 保存满意的提示词

### ❌ 避免
- 运动强度过高 (>7 会失真)
- 提示词过于复杂
- 期望过长视频 (最长 4 秒)
- 在公共频道发敏感内容

---

## 🔗 相关链接

- **Pika 官网**: https://pika.art
- **Discord 邀请**: https://discord.gg/pika
- **官方文档**: https://docs.pika.art
- **教程视频**: https://www.bilibili.com/video/BV1KMNtzJEBf

---

## 🎉 生成后

**如果效果满意**:
1. 下载视频
2. 可以分享到社交媒体
3. 记录提示词供下次使用

**如果效果不满意**:
1. 调整 motion 参数 (降低/提高)
2. 修改提示词
3. 尝试不同 camera 效果
4. 重新生成 (免费配额充足)

---

*指南创建：太一 AGI | 2026-04-06 09:29*  
*状态：✅ 立即可用，无需等待*
