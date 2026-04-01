# Claude Code Prompt 架构分析

> 分析时间：2026-03-31 22:07
> 来源：/tmp/claude-code-source-code-deobfuscation/claude-code/src/ai/prompts.ts

---

## 📊 核心发现

### [系统提示词分类] (4 种)

| 类型 | 常量名 | 用途 |
|------|--------|------|
| 代码助手 | `CODE_ASSISTANT_SYSTEM_PROMPT` | 代码问答/调试/重构 |
| 代码生成 | `CODE_GENERATION_SYSTEM_PROMPT` | 代码编写 |
| 代码审查 | `CODE_REVIEW_SYSTEM_PROMPT` | 代码审查/建议 |
| 代码解释 | `CODE_EXPLANATION_SYSTEM_PROMPT` | 代码解释/教学 |

---

### [Prompt 模板结构]

```typescript
interface PromptTemplate {
  template: string;        // 带占位符的模板
  system?: string;         // 可选系统消息
  defaults?: Record<string, string>;  // 占位符默认值
}
```

**设计优点**:
- ✅ 模块化：模板与系统提示分离
- ✅ 可配置：支持默认值
- ✅ 类型安全：TypeScript 接口定义

---

### [预定义模板] (5 种)

| 模板名 | 用途 | 占位符 |
|--------|------|--------|
| `explainCode` | 代码解释 | `{code}` |
| `refactorCode` | 代码重构 | `{code}`, `{focus}`, `{context}` |
| `debugCode` | 代码调试 | `{code}`, `{issue}`, `{errorMessages}` |
| `reviewCode` | 代码审查 | `{code}` |
| `generateCode` | 代码生成 | `{task}`, `{language}`, `{requirements}` |

---

### [太一可借鉴的设计]

**1. 系统提示词分类**
```typescript
// 太一 Bot 系统提示词
const TAIYI_SYSTEM_PROMPTS = {
  EXECUTIVE: "你是太一，AGI 执行总管...",
  ZHIJI: "你是知几，量化交易专家...",
  SHANMU: "你是山木，内容创意专家...",
  SUWEN: "你是素问，技术开发专家...",
  // ...
};
```

**2. Prompt 模板库**
```typescript
const PROMPT_TEMPLATES = {
  geoContent: {
    template: "创作 GEO 优化内容：{topic}\n\n核心数据：{data}\n\n结论：{conclusion}",
    system: SHANMU_SYSTEM_PROMPT,
  },
  codeAnalysis: {
    template: "分析代码架构：{code}\n\n关注点：{focus}",
    system: SUWEN_SYSTEM_PROMPT,
  },
  // ...
};
```

**3. 占位符替换工具**
```typescript
function formatPrompt(template: PromptTemplate, values: Record<string, string>): string {
  let result = template.template;
  for (const [key, value] of Object.entries(values)) {
    result = result.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
  }
  return result;
}
```

---

### [与太一当前架构对比]

| 维度 | Claude Code | 太一 AGI | 改进空间 |
|------|-------------|---------|---------|
| 系统提示词 | 4 种分类 | 8 Bot 各有定义 | ✅ 太一更完善 |
| Prompt 模板 | 5 种预定义 | 分散在各 Skill | ⚠️ 需集中管理 |
| 占位符支持 | ✅ 有 | ⚠️ 部分支持 | ⚠️ 需统一 |
| 类型安全 | ✅ TypeScript | ⚠️ 混合 | ⚠️ 可改进 |

---

### [太一 Prompt 架构升级方案]

**文件**: `constitution/prompts/PROMPT-TEMPLATES.md`

**内容**:
1. 系统提示词库 (8 Bot)
2. Prompt 模板库 (按场景分类)
3. 占位符替换工具函数
4. 使用示例和最佳实践

**GEO 内容机会**:
```markdown
标题：太一 Prompt 工程：基于 Claude Code 源码的架构升级

核心洞察:
- Claude Code 的 4 种系统提示词分类
- 5 种预定义 Prompt 模板
- 太一 8 Bot 架构的 Prompt 设计
- GEO 优化的 Prompt 技巧
```

---

*分析时间：2026-03-31 22:07*
*状态：✅ 完成初步分析*
*下一步：创建太一 Prompt 模板库*
