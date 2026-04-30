# 多平台推送模块 (push)



> **名称**: taiyi-travel-push  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 多平台推送——Telegram/微信


## 🎯 职责域



**核心功能**: Telegram 推送、微信推送

**适用场景**:
- 行程规划结果推送到 Telegram
- 行程规划结果推送到微信
- 实时通知


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `telegram.py` | Telegram 推送 |
| `wechat.py` | 微信推送 |


## 🚀 使用方式



```python
from src.push.telegram import TelegramPush
from src.push.wechat import WeChatPush

tg = TelegramPush(bot_token="xxx", chat_id="xxx")
tg.send("您的东京行程已生成")

wx = WeChatPush()
wx.send("您的东京行程已生成")
```


## 🔌 依赖



- `requests`


## 📦 发布



```bash
clawhub publish taiyi-travel-push
```


*太一旅行探路者 · 多平台推送模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48