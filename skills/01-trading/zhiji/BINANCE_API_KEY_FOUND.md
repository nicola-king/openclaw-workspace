# 币安 API Key 配置位置

> **查找时间**: 2026-04-22 22:20  
> **状态**: ✅ 已找到测试用 API Key

---

## 📍 API Key 位置

### 1. 测试用 API Key (硬编码)

**文件**: `scripts/binance-test-trade.py`

```python
api_key = os.getenv("BINANCE_API_KEY", "cMtuxE7spOseD2wQJJVpCdqur54tNmKvlFdyEHjL9n1bPyttqjVDjeGC5VlzqQTy")
```

**API Key**: `cMtuxE7spOseD2wQJJVpCdqur54tNmKvlFdyEHjL9n1bPyttqjVDjeGC5VlzqQTy`

**注意**: 这是测试用 API Key，可能已过期或无效

---

### 2. 环境变量配置

**文件**: `/home/nicola/.openclaw/.env`

**当前状态**: ❌ 未配置币安 API Key

**需要添加**:
```bash
# 币安 API 配置
BINANCE_API_KEY=你的_API_Key
BINANCE_API_SECRET=你的_Secret_Key
```

---

### 3. 测试网配置模板

**文件**: `skills/01-trading/zhiji/binance-trading/.env.binance-testnet.template`

**内容**:
```bash
# 币安测试网 API 配置
BINANCE_TESTNET_API_KEY=你的测试网_API_Key
BINANCE_TESTNET_API_SECRET=你的测试网_API_Secret
```

---

## 🔧 配置方法

### 方法 1: 添加到.env 文件 (推荐)

```bash
# 编辑.env 文件
nano /home/nicola/.openclaw/.env

# 添加
BINANCE_API_KEY=你的_API_Key
BINANCE_API_SECRET=你的_Secret_Key

# 保存
```

### 方法 2: 使用环境变量

```bash
# 临时设置
export BINANCE_API_KEY=你的_API_Key
export BINANCE_API_SECRET=你的_Secret_Key

# 永久设置 (添加到~/.bashrc)
echo "export BINANCE_API_KEY=你的_API_Key" >> ~/.bashrc
echo "export BINANCE_API_SECRET=你的_Secret_Key" >> ~/.bashrc
source ~/.bashrc
```

### 方法 3: 在脚本中硬编码 (不推荐)

```python
# 在交易脚本中添加
api_key = "你的_API_Key"
api_secret = "你的_API_Secret"
```

---

## 📋 获取 API Key 步骤

### 1. 访问币安 API 管理

```
https://www.binance.com/cn/my/settings/api-management
```

### 2. 创建 API Key

```
1. 点击"创建 API"
2. 填写 API 名称 (如：太一交易)
3. 完成安全验证
4. 复制 API Key 和 Secret Key
```

### 3. 配置权限

```
✅ 启用现货交易
✅ 启用读取权限
❌ 禁用提现
✅ IP 白名单：103.151.172.28
```

### 4. 添加到系统

```bash
# 编辑.env 文件
nano /home/nicola/.openclaw/.env

# 添加
BINANCE_API_KEY=你的_API_Key
BINANCE_API_SECRET=你的_Secret_Key

# 保存并重启交易系统
```

---

## ⚠️ 安全提示

### API Key 安全

| 建议 | 说明 |
|------|------|
| **不要分享** | API Key = 密码 |
| **限制 IP** | 添加 IP 白名单 |
| **禁用提现** | 只启用交易权限 |
| **定期更换** | 每 90 天更换一次 |

### 当前找到的 API Key

```
cMtuxE7spOseD2wQJJVpCdqur54tNmKvlFdyEHjL9n1bPyttqjVDjeGC5VlzqQTy

状态：⚠️ 可能是测试用/已过期
建议：在币安后台创建新的 API Key
```

---

## 📊 系统内 API 相关文件

| 文件 | 状态 | 说明 |
|------|------|------|
| **.env** | ⚠️ 未配置 | 主配置文件 |
| **binance-test-trade.py** | ✅ 硬编码 | 测试用 API Key |
| **binance-test.py** | ⚠️ 需配置 | 从环境变量读取 |
| **zhiji_auto_evolution_trader.py** | ⚠️ 需配置 | 从.env 读取 |
| **binance_24h_auto_trader.py** | ⚠️ 需配置 | 从.env 读取 |

---

## ✅ 下一步操作

### 立即执行

```
1. 访问币安 API 管理
2. 创建新的 API Key
3. 配置到.env 文件
4. 重启交易系统
5. 验证余额查询
```

### 验证命令

```bash
# 测试 API 连接
python3 /home/nicola/.openclaw/workspace/scripts/test_binance_api.py

# 查看余额
tail -f /home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log | grep "余额"
```

---

*币安 API Key 配置位置*  
*查找时间：2026-04-22 22:20*  
*状态：✅ 已找到测试 Key，需要配置正式 Key*
