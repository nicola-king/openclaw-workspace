# DESIGN.md Skill - AI 设计系统

> 状态：🟡 框架创建中  
> 优先级：P2  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 新前端项目启动
- 需要统一 UI 设计规范
- AI 生成 UI 需要风格指导
- 品牌一致性检查

---

## 能力

- ✅ DESIGN.md 模板生成
- ✅ AGENTS.md 编码规范
- ✅ 55+ 大厂设计语言参考
- ✅ AI 可读格式
- ✅ 无需 Figma/JSON

---

## 配置

```bash
DESIGN_MD_TEMPLATE=default  # default/apple/google/material/ant
DESIGN_MD_OUTPUT_PATH=./src/DESIGN.md
AGENTS_MD_OUTPUT_PATH=./src/AGENTS.md
```

---

## 使用方法

```bash
# 创建设计规范
design-md create --template default --output ./src/

# 应用设计语言
design-md apply --language apple --project ./my-app/

# 检查一致性
design-md check --project ./my-app/
```

---

## 模板示例

### 太一极简黑客风

```markdown
# DESIGN.md - 太一 AGI

## 色彩
- 主色：#000000（黑）
- 辅色：#FFFFFF（白）
- 强调：#00FF00（终端绿）

## 字体
- 代码：JetBrains Mono
- 标题：Inter Bold
- 正文：Inter Regular

## 风格
- 极简主义
- 高对比度
- 无多余装饰
```

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ 创建模板库
- [ ] ⏳ 应用到 Bot Dashboard
- [ ] ⏳ 收集 55+ 设计语言

---

*最后更新：2026-04-08 22:15*
