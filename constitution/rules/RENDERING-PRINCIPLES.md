# 渲染原则（永久生效）

> 版本：v1.0 | 状态：✅ 常驻生效
> 创建：2026-05-08 | 缘由：PDF 生成本地化失败 → 修复 → 原则提炼

---

## 核心原则

**渲染的正确性 = 字体 × 引擎 × 内容类型的三角匹配，缺一不可。**

不因为"能生成 PDF"就生成 PDF。每次渲染前必须做匹配检查。

---

## 一、渲染引擎选择矩阵

| 内容类型 | 推荐引擎 | 理由 |
|---------|---------|------|
| 纯英文文档 | fpdf2 + Helvetica | 内置字体，零依赖，文件小 |
| 中文/多语言文档 (≤5页) | fpdf2 + NotoSansCJK Regular.ttc | 快速生成，控制方便 |
| **中文/多语言文档 (>5页 / 含表格)** | **WeasyPrint + HTML/CSS** | **渲染可靠，字体嵌入正确** |
| Markdown → PDF | pandoc (如有) 或 WeasyPrint | 结构转换可靠 |
| 图片/截图 | 直接截图工具 | 所见即所得 |
| 纯文本输出 | 直接回答/sessions_send | 零渲染成本 |

**教训 1：fpdf2 + .ttc 字体有隐形渲染坑**
- 虽然能生成文件且无报错，但某些字符可能渲染空白
- .ttc 格式被 fpdf2 解码后存在字符映射偏移风险
- 始终用 `pdftotext` 验证输出内容完整性

**教训 2：WeasyPrint 是中文 PDF 的首选**
- 直接使用系统字体文件的 TrueType 克隆
- HTML+CSS 渲染引擎成熟，字符覆盖完整
- 生成后同样需要 pdftotext 验证

---

## 二、PDF 生成标准流程

```
开始 → 确定内容类型 → 选择引擎
                        │
                        ├── fpdf2 方案
                        │   └── 检查字体兼容性（所有中文字符必须测试）
                        │   └── 用 pdftotext 验证每一页
                        │
                        └── WeasyPrint 方案
                            └── 用 HTML 模板生成结构
                            └── 用 pdftotext 验证关键字段
                            └── 检查文件大小是否合理（字体嵌入会增大）
```

### 质量门禁（必须全部通过）

1. **pdftotext 完整导出** — 所有文字可提取，无乱码
2. **关键字段检查** — 所有中文 Bot 名称/模块名出现在提取文本中
3. **页数合理** — 与内容量匹配，没有空白页
4. **文件大小合理** — WeasyPrint 嵌入字体会大 (300-500KB)，正常
5. **无警告/报错** — 零 stderr 输出

---

## 三、字体选择策略

| 字体文件 | 格式 | CJK | Latin | fpdf2 | WeasyPrint |
|---------|------|-----|-------|-------|-----------|
| Helvetica | 内置 | ✗ | ✓ | 原生 | 原生 |
| NotoSansCJK-*.ttc | .ttc | ✓ | ✓ | ⚠️ 有坑 | ✓ |
| DroidSansFallbackFull.ttf | .ttf | ✓ | ✗ | ✓ | ✓ |
| Ubuntu | .ttf | ✗ | ✓ | ✓ | ✓ |

**最佳组合（中文PDF）：WeasyPrint + NotoSansCJK .ttc**

---

## 四、CJK 文档渲染 10 条铁律

1. **不用 .ttc 字体配合 fpdf2** — 字符映射存在隐性偏移
2. **优先选择 WeasyPrint** — HTML+CSS 渲染中文最可靠
3. **如果必须用 fpdf2** — 只处理纯英文或简单表格，用内置 Helvetica
4. **生成后必须验证** — `pdftotext` 提取全文并检查所有中文关键词
5. **表格用纯 HTML** — WeasyPrint 的表比 fpdf2 的 cell API 更可靠
6. **字体文件必须引用绝对路径** — WeasyPrint 的 `file:///` 格式
7. **复杂文档 (多章节/表格/pre) 用 HTML 模板** — 可维护性强
8. **不依赖"没报错就正确"** — .ttc 坑证明了无声错误的存在
9. **页边距 20mm 是安全值** — 打印友好
10. **文件命名统一前缀** — `太一-*` 方便用户识别

---

## 五、渲染失败回退路径

```
WeasyPrint 失败
    │
    ├── 检查系统字体 → fc-list :lang=zh
    │   └── 无合适字体 → 安装 noto-cjk 包
    │
    ├── 检查 weasyprint 版本 → pip3 show weasyprint
    │
    ├── 降级到 fpdf2（仅限纯英文内容）
    │
    └── 终极回退 → 纯文本/代码块直接展示在会话栏
        不输出 PDF，直接给内容让用户自行处理
```

---

## 六、经验沉淀（这次事故的教训）

### 问题
fpdf2 + NotoSansCJK-*.ttc 组合：
- 生成文件无报错
- 但 `·` 中点字符渲染为 `?`/空格，部分中文排版异常
- 用户说"还是错的"时，信任用户的反馈，立即换引擎

### 根因
- fpdf2 对 .ttc (TrueType Collection) 的解码存在兼容性问题
- .ttc 是多字体容器，fpdf2 只读取其中第一个子字体
- NotoSansCJK-Regular.ttc 的第一个子字体是 **JP (日文)** 变体，非 SC (简体中文)
- 导致部分 CJK 字符映射偏移，特定字符渲染异常

### 修复
- 切换到 WeasyPrint + HTML/CSS 模板
- WeasyPrint 内部使用 Pango/Cairo，对 .ttc 的字体子集选择更准确
- 生成 6 页 PDF，388KB，无错误无警告
- `pdftotext` 验证所有关键字段完整

### 以后
- **中文 PDF 默认走 WeasyPrint**
- **生成后必须 pdftotext 验证**
- **.fpdf2 + .ttc 组合禁用（除非验证通过且无替代方案）**

---

*本文件是对 Constitution 的补充，优先级与 TOOL-DISCIPLINE.md 同级*
*写入时间：2026-05-08 | 下次审查：2026-08-08*
