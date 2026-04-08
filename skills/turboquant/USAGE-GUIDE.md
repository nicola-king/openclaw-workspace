# TurboQuant v2.0 知几-E 集成使用指南

> 快速开始 · 2026-03-26

---

## 🚀 快速开始

### 1. 生成测试数据（可选）

```bash
cd /home/nicola/.openclaw/workspace/skills/turboquant
python3 test/meteorological_data_generator.py
```

### 2. 运行集成测试

```bash
python3 zhiji_integration.py
```

### 3. 查看压缩报告

```bash
cat INTEGRATION-REPORT.md
```

---

## 📦 核心组件

### TurboQuantJSONCompressor

**位置：** `skills/turboquant/json_compressor.py`

**用途：** 结构化数据无损压缩

**示例：**
```python
from json_compressor import TurboQuantJSONCompressor

compressor = TurboQuantJSONCompressor(lossless=True)

# 压缩
compressed = compressor.compress(data)

# 解压
original = compressor.decompress(compressed)

# 验证
match, _ = compressor.verify_integrity(original, compressed)
```

---

### ZhijiTurboQuantIntegration

**位置：** `skills/turboquant/zhiji_integration.py`

**用途：** 知几-E 数据压缩集成

**示例：**
```python
from zhiji_integration import ZhijiTurboQuantIntegration

integrator = ZhijiTurboQuantIntegration()

# 压缩存储
stats = integrator.compress_data(data, 'output.json')

# 智能保存（>10KB 自动压缩）
integrator.save_data(data, 'output.json')

# 智能加载（自动检测压缩）
data, is_compressed = integrator.load_data('output.json')
```

---

### ZhijiStrategyWithCompression

**位置：** `skills/turboquant/zhiji_integration.py`

**用途：** 知几-E 策略引擎压缩增强

**示例：**
```python
from zhiji_integration import ZhijiStrategyWithCompression

strategy = ZhijiStrategyWithCompression()

# 保存气象数据（压缩）
stats = strategy.save_meteorological_data(
    weather_data, 
    '~/.taiyi/zhiji/data/weather.json',
    compress=True
)

# 加载气象数据（自动解压）
weather = strategy.load_meteorological_data(
    '~/.taiyi/zhiji/data/weather.json'
)
```

---

## 📊 性能指标

| 指标 | 189 条 | 1000 条 |
|------|-------|--------|
| **压缩比** | 5.36x | 11.50x |
| **压缩时间** | 31.51 ms | 23.94 ms |
| **解压时间** | 1.09 ms | 2.39 ms |
| **压缩速度** | 6,000 行/秒 | 41,769 行/秒 |
| **解压速度** | 173,394 行/秒 | 418,301 行/秒 |

---

## 🎯 使用场景

### ✅ 推荐使用

1. **磁盘 I/O 受限**
   - 嵌入式设备
   - SD 卡存储
   - 减少写入次数

2. **网络传输**
   - 远程数据同步
   - API 响应压缩
   - 节省带宽 81%

3. **长期归档**
   - 历史数据存储
   - 日志压缩
   - 节省 81% 空间

4. **大数据集**
   - >1000 条记录
   - 压缩率>10x
   - 性能最优

---

### 🟡 谨慎使用

1. **纯内存加载**
   - 小额外开销（1-2ms）
   - 适合预加载场景

2. **超小数据集**
   - <100 条记录
   - 压缩收益不明显

---

## 🔧 配置选项

### 环境变量

```bash
export TURBOQUANT_DATA_DIR=~/.taiyi/zhiji/data
export TURBOQUANT_AUTO_COMPRESS=true
export TURBOQUANT_MIN_SIZE=10240  # 10KB
```

### 初始化参数

```python
integrator = ZhijiTurboQuantIntegration(
    data_dir="~/.taiyi/zhiji/data",  # 数据目录
    auto_compress=True,               # 自动压缩
    min_size_for_compression=10240    # 最小压缩尺寸
)
```

---

## 📁 文件结构

```
skills/turboquant/
├── json_compressor.py          # JSON 压缩器 v2.0
├── zhiji_integration.py        # 知几-E 集成模块
├── compressor_v2.py            # 对话压缩器 v2.0（旧）
├── test/
│   ├── meteorological_data_generator.py  # 数据生成器
│   ├── meteorological_data_189.json      # 189 条测试数据
│   ├── meteorological_compressed.json    # 压缩后数据
│   └── meteorological_strategy.json      # 策略引擎测试
└── INTEGRATION-REPORT.md       # 集成报告
```

---

## 🧪 测试命令

### 运行完整测试

```bash
cd /home/nicola/.openclaw/workspace/skills/turboquant
python3 zhiji_integration.py
```

### 运行压缩器测试

```bash
python3 json_compressor.py
```

### 生成测试数据

```bash
python3 test/meteorological_data_generator.py
```

---

## 🐛 故障排除

### 问题 1: 压缩失败

**症状：** `ValueError: 未知格式`

**解决：** 检查数据格式是否为 List[dict]

```python
# 正确
data = [{'field': 'value'}, ...]

# 错误
data = {'field': 'value'}  # 必须是列表
```

---

### 问题 2: 解压后数据不匹配

**症状：** `verify_integrity` 返回 False

**解决：** 确保使用 `lossless=True`

```python
compressor = TurboQuantJSONCompressor(lossless=True)
```

---

### 问题 3: 性能不如预期

**症状：** 压缩率低

**解决：** 
1. 检查数据量（>1000 条效果最佳）
2. 检查数据冗余度（重复值越多压缩率越高）
3. 考虑使用列式存储预处理

---

## 📞 支持

- **文档位置：** `skills/turboquant/INTEGRATION-REPORT.md`
- **负责人：** 素问（技术开发主管）
- **汇报对象：** 太一（AGI 总管）

---

*版本：v2.0 | 状态：✅ 交付 | 最后更新：2026-03-26*
