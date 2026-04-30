# md2pdf Skill - Markdown 转 PDF

**版本**: v1.0
**创建**: 2026-03-26
**作者**: 太一

---

## 📦 功能

- ✅ Markdown 转 PDF
- ✅ 支持图片嵌入
- ✅ 支持中文
- ✅ 使用 Chrome headless 渲染

---

## 🔧 用法

### 基本用法
```bash
md2pdf.sh input.md
md2pdf.sh input.md output.pdf
```

### 示例
```bash
# 转换当前目录文件
./md2pdf.sh report.md

# 指定输出文件
./md2pdf.sh report.pdf

# 完整路径
~/.openclaw/workspace/skills/suwen/md2pdf.sh input.md output.pdf
```

---

## 📋 依赖

- Google Chrome（已安装）
- bash

---

## 🎯 使用场景

1. **旅游攻略** - Markdown 写攻略，一键生成 PDF
2. **报告文档** - 工作汇报、数据分析
3. **图文手册** - 支持图片的文档

---

## 📄 示例

```bash
# 生成三亚旅游攻略 PDF
./md2pdf.sh sanya-guide.md sanya-guide.pdf

# 输出
📄 转换中：sanya-guide.md -> sanya-guide.pdf
✅ PDF 已生成：sanya-guide.pdf (383K)
```

---

## 🔗 文件位置

**脚本**: `~/.openclaw/workspace/skills/suwen/md2pdf.sh`

---

*太一 | 素问技能*
