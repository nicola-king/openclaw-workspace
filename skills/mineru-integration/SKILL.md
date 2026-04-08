# MinerU Skill - PDF 高精度解析

> 状态：🟡 框架创建中  
> 优先级：P0  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 需要解析 PDF 文档（尤其是含表格/公式的复杂文档）
- 金融研报/技术论文/学术文档提取
- PDF → Markdown/JSON 转换需求
- RAG 知识库文档预处理

---

## 能力

- ✅ PDF 表格精准提取
- ✅ 数学公式 LaTeX 识别
- ✅ 布局分析（文字/图片/表格分离）
- ✅ 多格式输出（Markdown/JSON）
- ✅ 中英文混合支持

---

## 配置

### API 模式（推荐）

```bash
MINERU_API_KEY=your_api_key
MINERU_API_URL=https://api.mineru.net/v1/parse
```

### 本地部署模式

```bash
MINERU_MODE=local
MINERU_MODEL_PATH=/path/to/model
```

---

## 使用方法

```bash
# API 调用
mineru-cli parse document.pdf --output output.md

# 本地部署
mineru-cli parse document.pdf --mode local
```

---

## 输出示例

```markdown
# 文档标题

## 表格

| 指标 | 2024 | 2025 |
|------|------|------|
| 营收 | 100 亿 | 120 亿 |

## 公式

$$ E = mc^2 $$
```

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ API Key 申请
- [ ] ⏳ 本地部署测试
- [ ] ⏳ 与知几-E 集成

---

*最后更新：2026-04-08 22:15*
