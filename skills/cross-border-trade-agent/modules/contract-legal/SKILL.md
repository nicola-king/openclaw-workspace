# contract-legal Skill

## 描述
合同与法律支持引擎：合同生成·法律审查·条款库·合规框架

## 蒸馏来源
- 跨境贸易合同模板：折叠房屋出口合同
- 太一系统：宪法级合规要求
- 合规引擎：法规框架
- 金融情报：交易安全条款

## 独立运行
```bash
python core.py --task generate --type "sales" --product "折叠房屋" --buyer "Aus Modular Homes"
```

## 依赖
- cross-border-core: ^10.0.0
- compliance-engine: ^10.0.0

## 核心能力

### 1. 合同生成
- 销售合同模板
- 采购合同模板
- 代理协议模板
- NDA 模板

### 2. 法律审查
- 条款合规检查
- 风险条款识别
- 管辖法律建议
- 争议解决机制

### 3. 条款库
- 国际贸易术语 (Incoterms 2020)
- 标准条款库
- 行业特定条款
- 多语言条款

### 4. 合规框架
- 出口管制检查
- 制裁名单筛查
- 反贿赂条款
- 数据保护条款

## API

### 输入
```json
{
  "task": "generate",
  "type": "sales",
  "product": "折叠房屋",
  "buyer": "Aus Modular Homes",
  "amount": 50000,
  "currency": "AUD",
  "incoterm": "CIF"
}
```

### 输出
```json
{
  "status": "success",
  "contract_id": "CT-2026-001",
  "contract_type": "sales",
  "template": "international_sales",
  "clauses": [...],
  "risk_clauses": [],
  "compliance_check": {...},
  "generated_contract": "..."
}
```

## 配置
```json
{
  "contract": {
    "enabled": true,
    "default_template": "international_sales",
    "language": "bilingual"
  },
  "legal": {
    "jurisdiction_preference": "neutral",
    "arbitration": "SIAC",
    "governing_law": "CISG"
  },
  "compliance": {
    "export_control": true,
    "sanction_check": true,
    "anti_bribery": true
  }
}
```

## 使用示例
```python
from core import ContractLegal

cl = ContractLegal(config_path="config.json")

# 生成合同
contract = cl.generate(
    type="sales",
    product="折叠房屋",
    buyer="Aus Modular Homes",
    amount=50000,
    currency="AUD",
    incoterm="CIF"
)

# 法律审查
review = cl.legal_review(
    contract_text="...",
    jurisdiction="Australia"
)

# 条款查询
clause = cl.lookup_clause(
    topic="payment_terms",
    incoterm="CIF"
)
```
