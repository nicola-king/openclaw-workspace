# Polymarket 环境变量配置

> 配置时间：2026-04-02 10:53  
> 状态：✅ 已配置

---

## 🔑 API 凭证（2026-04-02 更新）

```bash
# Polymarket CLOB API 凭证
export POLYMARKET_API_KEY="019d4c16-9ffe-79e9-b2be-368220456a98"
export POLYMARKET_API_SECRET="F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw="
export POLYMARKET_API_PASSPHRASE="985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265"
export POLYMARKET_WALLET_ADDRESS="0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5"
export POLYMARKET_CHAIN_ID="137"
export POLYMARKET_CLOB_URL="https://clob.polymarket.com"
export POLYMARKET_RELAYER_URL="https://relayer-v2.polymarket.com"
```

---

## 📁 配置文件位置

### 1. 知几-E 配置文件
```
~/.taiyi/zhiji/polymarket.json
```

**内容**：
```json
{
  "polymarket": {
    "api_key": "019d4c16-9ffe-79e9-b2be-368220456a98",
    "api_secret": "F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw=",
    "api_passphrase": "985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265",
    "wallet_address": "0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5",
    "chain_id": 137,
    "clob_url": "https://clob.polymarket.com",
    "relayer_url": "https://relayer-v2.polymarket.com",
    "status": "active"
  }
}
```

### 2. Shell 环境变量（推荐）
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export POLYMARKET_API_KEY="019d4c16-9ffe-79e9-b2be-368220456a98"' >> ~/.bashrc
echo 'export POLYMARKET_API_SECRET="F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw="' >> ~/.bashrc
echo 'export POLYMARKET_API_PASSPHRASE="985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265"' >> ~/.bashrc
source ~/.bashrc
```

### 3. .env 文件（项目级）
```bash
# 创建 /home/nicola/.openclaw/workspace/.env
cat > /home/nicola/.openclaw/workspace/.env << 'EOF'
POLYMARKET_API_KEY=019d4c16-9ffe-79e9-b2be-368220456a98
POLYMARKET_API_SECRET=F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw=
POLYMARKET_API_PASSPHRASE=985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265
POLYMARKET_WALLET_ADDRESS=0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5
POLYMARKET_CHAIN_ID=137
EOF
```

---

## 🔒 安全提醒

1. **不要提交到 Git**：
   ```bash
   # .gitignore 已包含
   .env
   *.json  # 包含敏感信息的配置文件
   ```

2. **文件权限**：
   ```bash
   chmod 600 ~/.taiyi/zhiji/polymarket.json
   chmod 600 /home/nicola/.openclaw/workspace/.env
   ```

3. **不要分享**：
   - API Secret 和 Passphrase 等同于密码
   - 泄露后需在 Polymarket 后台撤销并重新生成

---

## ✅ 验证配置

```bash
# 检查环境变量
echo $POLYMARKET_API_KEY
echo $POLYMARKET_API_SECRET
echo $POLYMARKET_API_PASSPHRASE

# 应输出：
# 019d4c16-9ffe-79e9-b2be-368220456a98
# F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw=
# 985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265
```

---

## 🚀 使用示例

### Python 脚本
```python
import os
from py_clob_client.client import ClobClient

client = ClobClient(
    host=os.getenv('POLYMARKET_CLOB_URL'),
    key=os.getenv('POLYMARKET_API_KEY'),
    secret=os.getenv('POLYMARKET_API_SECRET'),
    passphrase=os.getenv('POLYMARKET_API_PASSPHRASE'),
    chain_id=int(os.getenv('POLYMARKET_CHAIN_ID'))
)
```

### Bash 脚本
```bash
#!/bin/bash
source /home/nicola/.openclaw/workspace/.env

echo "API Key: $POLYMARKET_API_KEY"
echo "Wallet: $POLYMARKET_WALLET_ADDRESS"
```

---

*创建时间：2026-04-02 10:53 | 太一 AGI | 已配置*
