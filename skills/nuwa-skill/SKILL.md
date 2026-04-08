# 女娲 Skill - 思维蒸馏引擎

> 状态：🟡 框架创建中  
> 优先级：P0  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 需要名人思维框架分析问题
- 重大决策需要多视角
- 学习新知识需要费曼技巧
- 投资策略需要芒格思维
- 创新问题需要马斯克第一性原理

---

## 能力

- ✅ 6 个并行调研 Agent
- ✅ 40+ 信息源覆盖
- ✅ 三重验证机制
- ✅ 六层蒸馏架构
- ✅ 多顾问会议模式

---

## 配置

```bash
NUWA_SKILL_PATH=alchaincyf/nuwa-skill
NUWA_OUTPUT_DIR=./skills/distilled/
NUWA_MAX_SOURCES=40
NUWA_PARALLEL_AGENTS=6
```

---

## 使用方法

```bash
# 安装
npx skills add alchaincyf/nuwa-skill

# 蒸馏新人物
nuwa distill "Elon Musk" --output skills/elon-musk/

# 调用思维
nuwa ask "elon-musk" "如何用第一性原理分析这个问题？"

# 多顾问会议
nuwa meeting "elon-musk,munger,feynman" --topic "创业决策"
```

---

## 已蒸馏人物

| 人物 | 领域 | 核心思维 |
|------|------|---------|
| Steve Jobs | 产品/设计 | 极简主义 |
| Elon Musk | 工程/创新 | 第一性原理 |
| Charlie Munger | 投资 | 逆向思考 |
| Feynman | 学习/物理 | 简单解释 |
| Naval | 创业/投资 | 杠杆思维 |
| Taleb | 风险 | 反脆弱 |
| 张雪峰 | 教育 | 实用主义 |

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ 安装 Skill
- [ ] ⏳ 测试现有案例
- [ ] ⏳ 蒸馏 SAYELF 框架

---

*最后更新：2026-04-08 22:30*
