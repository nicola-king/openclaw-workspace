# MinerU 集成 - PDF 高精度解析引擎

> 状态：🟡 调研完成，待集成  
> 学习日期：2026-04-08  
> 来源：SAYELF 分享

---

## 📦 工具信息

| 项目 | 详情 |
|------|------|
| **名称** | MinerU |
| **版本** | 3.0.0 (2026/03/29 更新) |
| **开源** | [GitHub - opendatalab/MinerU](https://github.com/opendatalab/MinerU) |
| **官网** | [mineru.net](https://mineru.net/) |
| **开发者** | 上海人工智能实验室 / OpenDataLab |

---

## 🎯 核心能力

**MinerU** 是一站式 PDF 文档解析工具，专为 LLM、RAG、Agent 工作流设计：

- ✅ **表格解析** - 精准提取复杂表格结构
- ✅ **公式识别** - LaTeX 格式数学公式
- ✅ **布局分析** - 文字/图片/表格智能分离
- ✅ **多格式输出** - Markdown / JSON / 结构化数据
- ✅ **多语言支持** - 中英文混合文档

---

## 🔧 部署方式

### 方案 A：在线 API（推荐 P0）

```bash
# 无需部署，直接调用 API
curl -X POST "https://api.mineru.net/v1/parse" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf"
```

**优势**：
- ✅ 零部署成本
- ✅ 最新模型自动更新
- ✅ 按量付费

**劣势**：
- 🔴 需要网络
- 🔴 有 API 调用成本

---

### 方案 B：本地部署（推荐 P1）

```bash
# 环境要求
- Python 3.8+
- GPU: 8GB+ 显存（推荐）
- CPU: 8 核+
- 内存：16GB+

# 安装
pip install mineru

# 使用
mineru parse document.pdf --output output/
```

**优势**：
- ✅ 本地运行，隐私安全
- ✅ 无 API 调用限制
- ✅ 可定制模型

**劣势**：
- 🔴 需要 GPU 资源
- 🔴 部署复杂度较高

---

## 💡 太一集成场景

### 场景 1：金融研报解析（知几-E）

```
PDF 研报 → MinerU → Markdown → 太一分析 → 交易信号
```

**价值**：
- 提取研报中的财务数据表格
- 识别公式和模型
- 结构化存储到向量数据库

### 场景 2：技术文档处理（素问）

```
PDF 论文 → MinerU → Markdown → 知识库 → RAG 问答
```

### 场景 3：内容创作素材（山木）

```
PDF 资料 → MinerU → 结构化内容 → 文案生成
```

---

## 📋 集成 Checklist

### P0 - 立即执行（今日）
- [x] ✅ 调研完成
- [ ] ⏳ 创建 Skill 框架
- [ ] ⏳ 编写使用文档
- [ ] ⏳ API Key 申请（如需）

### P1 - 本周执行
- [ ] ⏳ 本地部署测试
- [ ] ⏳ 与知几-E 集成
- [ ] ⏳ 创建测试用例

### P2 - 按需执行
- [ ] ⏳ 批量处理脚本
- [ ] ⏳ 性能优化

---

## 🔗 相关链接

- GitHub: https://github.com/opendatalab/MinerU
- 官网：https://mineru.net/
- 文档：https://opendatalab.github.io/MinerU/zh/usage/
- 知乎教程：https://zhuanlan.zhihu.com/p/1985647683768177611

---

*创建时间：2026-04-08 22:15*  
*创建人：太一 AGI*  
*状态：🟡 调研完成，待集成*
