# 太一 AGI Skill SDK

> **版本**: 1.0.0  
> **创建时间**: 2026-04-10  
> **灵感**: OpenClaw v2026.4.9 Plugin SDK Exports

---

## 📦 安装

```bash
# 无需安装 - SDK 内置于 workspace
import sdk from '/home/nicola/.openclaw/workspace/skills/sdk/index.js';
```

---

## 🚀 快速开始

### 创建新 Skill

```javascript
import { BaseSkill } from '/home/nicola/.openclaw/workspace/skills/sdk/index.js';

class MySkill extends BaseSkill {
    constructor() {
        super({
            name: 'my-skill',
            version: '1.0.0',
            description: '我的 Skill 描述',
            author: '太一 AGI'
        });
    }

    async execute(input) {
        // 实现 Skill 逻辑
        return { result: 'success', data: input };
    }
}

const skill = new MySkill();
await skill.init();
const result = await skill.execute({ key: 'value' });
```

---

## 📚 API 文档

### 基础类 (BaseSkill)

#### 构造函数

```javascript
new BaseSkill(config)
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config.name | string | 否 | Skill 名称 |
| config.version | string | 否 | 版本号 |
| config.description | string | 否 | 描述 |
| config.author | string | 否 | 作者 |

#### 方法

```javascript
// 初始化
await skill.init();

// 执行
const result = await skill.execute(input);

// 验证
const valid = skill.validate(input);

// 获取信息
const info = skill.getInfo();
```

---

### 记忆工具 (memory)

#### parseDailyNote

```javascript
import { parseDailyNote } from 'taiyi-sdk';

const result = parseDailyNote('2026-04-10');
// 返回：{ date, decisions[], tasks[], insights[], emergence[] }
```

#### extractDecisions

```javascript
import { extractDecisions } from 'taiyi-sdk';

const decisions = extractDecisions(content);
// 返回：string[]
```

#### extractTasks

```javascript
import { extractTasks } from 'taiyi-sdk';

const tasks = extractTasks(content);
// 返回：string[]
```

#### extractInsights

```javascript
import { extractInsights } from 'taiyi-sdk';

const insights = extractInsights(content);
// 返回：string[]
```

---

### 配置工具 (config)

#### loadProviderConfig

```javascript
import { loadProviderConfig } from 'taiyi-sdk';

const qwen = loadProviderConfig('qwen');
// 返回：{ base_provider, env_prefix, variants[] }
```

#### loadProviderAliases

```javascript
import { loadProviderAliases } from 'taiyi-sdk';

const aliases = loadProviderAliases();
// 返回：{ qwen, google, openai, ... }
```

#### resolveModel

```javascript
import { resolveModel } from 'taiyi-sdk';

const codeModel = resolveModel('qwen', 'code');
// 返回："qwen3-coder-plus"

const visualModel = resolveModel('openai', 'visual');
// 返回："gpt-4o"
```

---

### 美学工具 (aesthetic)

#### scoreAesthetic

```javascript
import { scoreAesthetic } from 'taiyi-sdk';

const score = scoreAesthetic(content, { strict: true });
// 返回：{ score, dimensions, feedback }
```

#### generateDesignCard

```javascript
import { generateDesignCard } from 'taiyi-sdk';

const card = generateDesignCard({
    title: '设计卡片',
    eastern: 'japan',
    western: 'apple',
    content: '内容'
});
// 返回：Markdown 卡片字符串
```

#### applyDesignPrinciples

```javascript
import { applyDesignPrinciples } from 'taiyi-sdk';

const beautified = applyDesignPrinciples(content, {
    apple: 0.80,
    eastern: 0.15,
    chinese: 0.05
});
// 返回：美化后的内容
```

---

## 📝 示例

### 示例 1: 创建记忆分析 Skill

```javascript
import { BaseSkill, parseDailyNote } from 'taiyi-sdk';

class MemoryAnalyzer extends BaseSkill {
    constructor() {
        super({
            name: 'memory-analyzer',
            description: '记忆分析 Skill'
        });
    }

    async execute(input) {
        const { date } = input;
        const data = parseDailyNote(date);
        
        return {
            summary: {
                decisions: data.decisions.length,
                tasks: data.tasks.length,
                insights: data.insights.length,
                emergence: data.emergence.length
            },
            data
        };
    }
}
```

### 示例 2: 创建模型路由 Skill

```javascript
import { BaseSkill, resolveModel } from 'taiyi-sdk';

class ModelRouter extends BaseSkill {
    constructor() {
        super({
            name: 'model-router',
            description: '模型路由 Skill'
        });
    }

    async execute(input) {
        const { taskType } = input;
        
        const model = {
            code: resolveModel('qwen', 'code'),
            visual: resolveModel('openai', 'visual'),
            long_text: resolveModel('google', 'long_text')
        }[taskType];
        
        return { model, provider: taskType };
    }
}
```

### 示例 3: 创建美学评分 Skill

```javascript
import { BaseSkill, scoreAesthetic, generateDesignCard } from 'taiyi-sdk';

class AestheticScorer extends BaseSkill {
    constructor() {
        super({
            name: 'aesthetic-scorer',
            description: '美学评分 Skill'
        });
    }

    async execute(input) {
        const { content } = input;
        const score = scoreAesthetic(content);
        const card = generateDesignCard({ title: '美学报告' });
        
        return { score, card };
    }
}
```

---

## 🎯 最佳实践

### ✅ 推荐

- 继承 BaseSkill 类
- 实现 execute() 方法
- 使用 SDK 工具函数
- 遵循美学原则
- 编写文档

### ❌ 避免

- 直接操作文件系统
- 重复实现工具函数
- 忽略错误处理
- 无文档发布

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-10 | 初始版本 |

---

## 🙏 致谢

- 灵感来源：OpenClaw v2026.4.9 Plugin SDK Exports

---

*文档：太一 AGI Skill SDK*  
*创建时间：2026-04-10 13:45*
