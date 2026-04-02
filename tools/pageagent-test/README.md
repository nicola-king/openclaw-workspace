# PageAgent 集成测试

阿里开源的纯前端 GUI Agent，用自然语言操控网页。

## 安装

```bash
npm install page-agent
```

## 快速开始

```javascript
const { PageAgent } = require('page-agent');

const agent = new PageAgent({
  model: {
    provider: 'openai',
    apiKey: process.env.OPENAI_API_KEY,
    model: 'gpt-4o'
  }
});

// 用自然语言操控网页
await agent.navigate('https://example.com');
await agent.act('点击登录按钮');
await agent.act('在用户名输入框输入 "admin"');
```

## 测试

```bash
node test.js
```

## 环境变量

```bash
export OPENAI_API_KEY="sk-..."
# 或使用其他模型
export ANTHROPIC_API_KEY="sk-..."
export GOOGLE_API_KEY="..."
```

## 支持的操作

| 操作 | 示例 |
|------|------|
| 导航 | `agent.navigate('https://...')` |
| 点击 | `agent.act('点击登录按钮')` |
| 输入 | `agent.act('输入 "hello"')` |
| 观察 | `agent.observe()` |
| 滚动 | `agent.act('向下滚动页面')` |
| 截图 | `agent.screenshot()` |

## 兼容模型

- OpenAI (GPT-4o, GPT-4 Turbo)
- Anthropic (Claude 3.5/3.7)
- Google (Gemini 2.5 Pro)
- Ollama (本地模型)

## 项目结构

```
pageagent-test/
  ├── package.json       # npm 配置
  ├── test.js           # 测试脚本
  ├── skill.js          # OpenClaw Skill 封装
  └── README.md         # 本文档
```

## GitHub

- 仓库：https://github.com/alibaba/page-agent
- Stars: 9.6K+
- 文档：https://alibaba.github.io/page-agent/

---

*太一 AGI 实验室 · 2026-04-02*
