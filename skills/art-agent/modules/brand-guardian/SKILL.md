# 🛡️ Brand Guardian - 品牌守护者

> **版本**: 1.0.0  
> **创建时间**: 2026-04-25  
> **作者**: 太一 AGI  
> **定位**: 太一系统品牌一致性守护者

---

## 🎯 核心使命

守护太一系统品牌一致性，确保所有输出符合品牌规范。

### 品牌元素

| 元素 | 规范 | 说明 |
|------|------|------|
| **色彩** | 太一标准色 | 主色/强调色/语义色 |
| **字体** | Noto Serif CJK | 宋体风格 |
| **风格** | 极简黑客风 | 简洁/清晰/专业 |
| **签名** | 太一美学印章 | 品牌标识 |

---

## 📦 模块功能

### 品牌检查

```python
from brand_guardian import BrandGuardian

guardian = BrandGuardian()
result = guardian.check(content)
print(f"品牌一致性：{result['score']}/100")
```

### 风格统一

```python
unified = guardian.unify(content, style="taiyi-standard")
```

---

## 🚀 使用方式

### 1. 独立运行

```bash
python core.py --input report.md --check
```

### 2. 太一系统集成

```python
from brand_guardian import BrandGuardian

guardian = BrandGuardian()
result = guardian.check(report_content)
```

---

## 📋 自进化

- **版本**: 1.0.0
- **进化日志**: `memory/evolution/brand-guardian.json`
- **反馈收集**: 品牌一致性评分 → 规范优化

---

*太一 Brand Guardian v1.0 · 品牌守护者*  
*创建时间：2026-04-25*
