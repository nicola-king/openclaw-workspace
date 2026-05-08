---
name: ui-tars
description: GUI 桌面自动化工具 — 通过自然语言操控电脑桌面（基于 ByteDance UI-TARS）
version: 0.1.0
requires:
  bins:
    - ui-tars
---

# UI-TARS — GUI Desktop Automation

基于 ByteDance UI-TARS Desktop（30K🌟）的桌面操控技能。

## 使用

```bash
ui-tars start --target nut-js --query "你的指令" --output json
```

## 输出

最后一行 `{"event":"done",...}` 含：
- `status` — end/error/call_user
- `summary` — 操作过程
- `screenshotPath` — 最终截图

详见：https://github.com/bytedance/UI-TARS-desktop

## 配置

创建 `~/.ui-tars-cli.json`（OpenAI 兼容格式）：
```json
{
  "baseURL": "https://ark.cn-beijing.volces.com/api/v3",
  "apiKey": "<火山引擎 API Key>",
  "model": "doubao-seed-2-0-pro-260215",
  "useResponsesApi": true
}
```
