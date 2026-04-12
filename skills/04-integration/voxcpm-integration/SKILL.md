# VoxCPM Skill - 语音克隆 TTS

> 状态：🟡 框架创建中  
> 优先级：P0  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 需要 TTS 语音生成
- 声音克隆需求（复刻特定人声）
- 有声书/故事叙述
- 视频配音
- Bot 语音差异化

---

## 能力

- ✅ 零样本声音克隆（几秒音频）
- ✅ 连续空间建模（高保真）
- ✅ 上下文感知（情感/语调）
- ✅ 多语言支持（中英文混合）
- ✅ 本地部署（无额度限制）

---

## 配置

```bash
VOXCPM_MODE=local
VOXCPM_MODEL_PATH=/path/to/voxcpm-model
VOXCPM_REFERENCE_AUDIO=/path/to/reference.wav
VOXCPM_VOICE_PROFILE=sayelf  # 或其他预设
```

---

## 使用方法

```bash
# 文本转语音
voxcpm-cli generate --text "你好" --output output.wav

# 声音克隆
voxcpm-cli clone --reference sayelf.wav --text "你好" --output cloned.wav

# 多角色生成
voxcpm-cli multi --roles taiyi,zhiji,shanmu --script script.txt
```

---

## 声音预设

| Bot | 声音设定 | 参考音频 |
|-----|---------|---------|
| 太一 | 沉稳男声 | TBD |
| 知几 | 专业女声 | TBD |
| 山木 | 创意青年 | TBD |
| 素问 | 学者声 | TBD |

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ 本地部署
- [ ] ⏳ 声音采样
- [ ] ⏳ 与即梦 CLI 联动

---

*最后更新：2026-04-08 22:15*
