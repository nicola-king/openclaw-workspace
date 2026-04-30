# VoxCPM 集成 - 语音克隆 TTS 引擎

> 状态：🟡 调研完成，待集成  
> 学习日期：2026-04-08  
> 来源：SAYELF 分享

---

## 📦 工具信息

| 项目 | 详情 |
|------|------|
| **名称** | VoxCPM / VoxCPM2 |
| **版本** | 2.0（最新版） |
| **开源** | [GitHub - OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM/) |
| **开发者** | 面壁智能 × 清华大学深圳国际研究生院 |
| **模型规模** | 0.5B 参数 |
| **榜单** | HuggingFace 全球模型趋势榜 #1 |

---

## 🎯 核心能力

**VoxCPM** 是新一代无分词器（Tokenizer-Free）TTS 系统：

- ✅ **零样本声音克隆** - 几秒音频复刻任何人声
- ✅ **连续空间建模** - 超越离散分词限制
- ✅ **上下文感知** - 情感/语调/风格自然
- ✅ **多语言支持** - 中英文混合
- ✅ **本地部署** - 完全开源，无 API 限制

### 三种模式

| 模式 | 说明 | 使用场景 |
|------|------|---------|
| **声音设计** | 无参考音频，从零创建 | 虚拟角色/通用语音 |
| **可控克隆** | 控制情绪/语速/风格 | 有情感朗读 |
| **终极克隆** | 最高保真度克隆 | 名人声音复刻 |

---

## 🔧 部署方式

### 方案 A：本地部署（推荐 P0）

```bash
# 环境要求
- Python 3.8+
- GPU: NVIDIA 8GB+ 显存
- CUDA 11.7+

# 安装
git clone https://github.com/OpenBMB/VoxCPM.git
cd VoxCPM
pip install -r requirements.txt

# 使用示例
python inference.py \
  --text "你好，这是测试文本" \
  --reference_audio "sample.wav" \
  --output "output.wav"
```

**优势**：
- ✅ 完全免费，无额度限制
- ✅ 隐私安全，本地运行
- ✅ 可定制微调

**劣势**：
- 🔴 需要 GPU 资源
- 🔴 首次部署需下载模型

---

### 方案 B：API 调用（备选）

```bash
# 如有官方/第三方 API 服务
curl -X POST "https://api.example.com/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好",
    "voice": "clone",
    "reference": "audio_url"
  }'
```

---

## 💡 太一集成场景

### 场景 1：研报语音播报（知几 + 太一）

```
金融研报 → 太一总结 → VoxCPM(SAYELF 声音) → 音频推送
```

**价值**：
- 通勤时听研报摘要
- 个性化声音（SAYELF 音色）
- 多语言播报（中英文混合）

### 场景 2：故事叙述（内容创作）

```
小说/故事 → VoxCPM(多角色声音) → 有声书
```

### 场景 3：视频配音（即梦 CLI 联动）

```
脚本 → 即梦生成视频 + VoxCPM 配音 → 完整视频
```

### 场景 4：Bot 语音差异化

| Bot | 声音设定 |
|-----|---------|
| 太一 | 沉稳男声（默认） |
| 知几 | 专业女声（金融分析师） |
| 山木 | 创意青年声 |
| 素问 | 学者声 |

---

## 📋 集成 Checklist

### P0 - 立即执行（今日）
- [x] ✅ 调研完成
- [ ] ⏳ 创建 Skill 框架
- [ ] ⏳ 编写使用文档
- [ ] ⏳ 本地部署测试

### P1 - 本周执行
- [ ] ⏳ 声音采样（录制 SAYELF 参考音频）
- [ ] ⏳ 声音克隆测试
- [ ] ⏳ 与现有 TTS 技能对比

### P2 - 按需执行
- [ ] ⏳ 多角色声音库
- [ ] ⏳ 批量音频生成
- [ ] ⏳ 性能优化

---

## 🔗 相关链接

- GitHub: https://github.com/OpenBMB/VoxCPM/
- HuggingFace: https://huggingface.co/OpenBMB/VoxCPM
- 清华大学新闻：https://www.tsinghua.edu.cn/info/1182/121508.htm
- 掘金教程：https://juejin.cn/post/7585727457473036288

---

*创建时间：2026-04-08 22:15*  
*创建人：太一 AGI*  
*状态：🟡 调研完成，待集成*
