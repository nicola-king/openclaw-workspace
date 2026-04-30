# 重庆 18 定额配套文件下载指南

> **目标目录**: `/home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota/`  
> **文件大小**: 约 5.3GB  
> **创建时间**: 2026-04-10

---

## 📁 目录结构

```
data/
└── chongqing_18_quota/
    ├── README.md                 # 本说明文件
    ├── 重庆 2018 市政定额.pdf         # 待下载
    ├── 重庆 2018 市政定额解释.pdf       # 待下载
    ├── 重庆 2018 市政定额计算规则.pdf    # 待下载
    └── ...                       # 其他配套文件
```

---

## 📥 下载方式

### 方式 1: 百度网盘手动下载

1. **打开百度网盘**
   - 网址：https://pan.baidu.com/
   - 登录账号

2. **搜索文件**
   - 搜索关键词：`重庆 18 定额配套文件`
   - 或：`重庆 2018 市政定额`

3. **下载到本地**
   - 选择所有文件
   - 下载到：`/home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota/`

---

### 方式 2: 使用 bypy 命令行工具

```bash
# 1. 登录百度网盘
bypy info

# 2. 搜索文件
bypy search 重庆 18 定额
bypy search 重庆 2018 市政定额

# 3. 下载文件 (找到后)
cd /home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota
bypy download /apps/重庆 18 定额配套文件/
```

---

### 方式 3: 使用浏览器下载后移动

```bash
# 1. 在浏览器中下载到 ~/Downloads/
# 2. 移动到目标目录
mv ~/Downloads/重庆 18 定额配套文件/* \
   /home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota/
```

---

## 📋 预期文件列表

根据"重庆 18 定额配套文件"，预期包含以下内容：

### 定额主文件
- [ ] 重庆市市政工程计价定额 (2018 版).pdf
- [ ] 重庆市建设工程计价定额 (2018 版).pdf

### 配套文件
- [ ] 重庆 2018 市政定额解释.pdf
- [ ] 重庆 2018 市政定额计算规则.pdf
- [ ] 重庆 2018 市政定额费用标准.pdf
- [ ] 重庆 2018 市政定额材料价格.pdf

### 补充文件
- [ ] 重庆市建设工程工程量计算规则 (2018 版).pdf
- [ ] 重庆市建设工程费用定额 (2018 版).pdf
- [ ] 重庆造价信息 2026 年各期.pdf

---

## 🔧 下载后处理

### 1. 验证文件完整性

```bash
# 检查文件大小
ls -lh /home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota/

# 检查文件数量
ls /home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota/ | wc -l
```

### 2. 解压文件 (如果是压缩包)

```bash
cd /home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota

# 如果是 zip 文件
unzip 重庆 18 定额配套文件.zip

# 如果是 7z 文件
7z x 重庆 18 定额配套文件.7z

# 如果是 rar 文件
unrar x 重庆 18 定额配套文件.rar
```

### 3. 更新定额数据库

下载完成后，系统会自动：
- ✅ 读取定额 PDF 文件
- ✅ 提取定额数据
- ✅ 更新定额数据库
- ✅ 同步到造价计算器

---

## 📊 集成到系统

下载完成后，系统会自动集成：

### 1. 定额数据集成
```python
# 自动读取 PDF 中的定额数据
# 更新到 cost.py 的 QUOTAS 数据库
```

### 2. 材料价格集成
```python
# 读取材料价格 PDF
# 更新到 material_prices.json
```

### 3. 费用标准集成
```python
# 读取费用标准 PDF
# 更新到 cost.py 的费用配置
```

---

## 📞 常见问题

### Q1: 找不到文件怎么办？
**A**: 请确认百度网盘账号是否正确，或联系文件分享者重新分享。

### Q2: 下载速度慢怎么办？
**A**: 5.3GB 文件较大，建议使用百度网盘客户端下载，速度更快。

### Q3: 下载后如何使用？
**A**: 下载完成后，系统会自动读取并集成到造价计算系统中。

### Q4: 文件太大放不下怎么办？
**A**: 目标目录在工控机本地，5.3GB 应该可以放下。如果空间不足，请清理磁盘空间。

---

## 📝 下载进度

| 步骤 | 状态 | 说明 |
|------|------|------|
| 创建目标目录 | ✅ 完成 | `/data/chongqing_18_quota/` |
| 搜索百度网盘 | ✅ 完成 | 需要手动查找 |
| 下载文件 | ⏳ 待开始 | 约 5.3GB |
| 解压文件 | ⏳ 待开始 | 如果是压缩包 |
| 集成到系统 | ⏳ 待开始 | 自动处理 |

---

## 🎯 下一步

1. ⏳ 从百度网盘下载"重庆 18 定额配套文件"
2. ⏳ 保存到目标目录
3. ⏳ 系统自动集成
4. ⏳ 验证集成效果

---

*文档：太一 AGI · 市政工程造价 Skill*  
*创建时间：2026-04-10*  
*目标：下载并集成重庆 18 定额配套文件 (5.3GB)*
