# MinerU Skill - PDF 高精度解析

> 状态：🟡 部署中（开源免费，本地部署）  
> 优先级：P0  
> 创建日期：2026-04-08
> 更新：2026-04-08 22:52 - 确认开源免费，无需 API Key

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
- ✅ 109 种语言 OCR
- ✅ VLM+OCR 双引擎

---

## 配置

### 本地部署模式（推荐 ✅）

```bash
MINERU_MODE=local
MINERU_MODEL_PATH=~/.mineru/models
MINERU_GPU=auto  # auto/true/false
```

**优势**：
- ✅ 100% 免费，无需 API Key
- ✅ 隐私安全（本地运行）
- ✅ 无调用限制
- ✅ 可离线使用

---

## 使用方法

```bash
# 安装
pip install mineru

# 基础使用
mineru parse document.pdf --output output.md

# GPU 加速
mineru parse document.pdf --gpu --output output.md

# 批量处理
mineru batch parse ./pdfs/ --output ./markdowns/

# 表格提取
mineru parse document.pdf --extract-tables --output output.md

# 公式提取
mineru parse document.pdf --extract-formulas --output output.md
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
- [x] ✅ 确认开源免费（2026-04-08 22:52）
- [ ] ⏳ Git 克隆中（/tmp/mineru）
- [ ] ⏳ Pip 安装
- [ ] ⏳ 模型下载
- [ ] ⏳ 样本测试
- [ ] ⏳ 与知几-E 集成

---

## 相关链接

- GitHub: https://github.com/opendatalab/MinerU (39K Stars)
- 官网：https://opendatalab.github.io/MinerU/
- 文档：https://opendatalab.github.io/MinerU/zh/usage/

---

*最后更新：2026-04-08 22:52*
