# 网络分流 · 智能切换技能

## 原则
1. 国内模型（百炼、DeepSeek、Kimi）→ 直连
2. 国外模型（Gemini、Claude、OpenAI）→ 代理
3. 代理在线 → Telegram + Feishu + WeChat 全开
4. 代理断线 → 自动切换到 Feishu + WeChat

## 常用命令
```bash
# 查看当前状态
bash ~/.openclaw/scripts/net-routing.sh status

# 立即探测并切换
bash ~/.openclaw/scripts/net-routing.sh probe

# 查看日志
tail -f /tmp/openclaw/net-routing.log

# 查看 timer 状态
systemctl --user status openclaw-net-routing.timer
```

## 自动探测
每 3 分钟自动探测一次，状态变化时自动切换并重启 Gateway。
