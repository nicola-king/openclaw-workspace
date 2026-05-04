# compliance-engine Skill

## 描述
合规与清关自动化引擎：法规追踪·合规检查·清关自动化·关税计算

## 蒸馏来源
- 宪法层：负熵法则（合规即效率）
- 海关数据：全球 9 大海关机构
- 行业规范：ISO/CE/FDA 等认证标准
- 太一系统：反封号策略→合规操作规范

## 独立运行
```bash
python core.py --task compliance --product "折叠房屋" --market "澳大利亚"
```

## 依赖
- cross-border-core: ^10.0.0
- data-integrator: ^10.0.0

## 核心能力

### 1. 法规追踪
- 目标市场法规实时更新
- 法规变更预警
- 合规差距分析

### 2. 合规检查
- 产品认证要求 (CE/FDA/ISO)
- 标签/包装合规
- 环保/安全标准

### 3. 清关自动化
- HS 编码自动匹配
- 关税计算
- 清关文件生成
- 报关行推荐

### 4. 合规报告
- 合规状态仪表板
- 风险等级评估
- 改进建议

## API

### 输入
```json
{
  "task": "compliance",
  "product": "折叠房屋",
  "market": "澳大利亚",
  "hs_code": "9406.00"
}
```

### 输出
```json
{
  "status": "success",
  "compliance_score": 85,
  "regulations": [...],
  "certifications_required": ["CE", "ISO9001"],
  "tariff_rate": 5.0,
  "clearance_docs": ["商业发票", "装箱单", "原产地证"],
  "risks": ["需澳大利亚建筑标准认证"],
  "recommendations": ["优先获取 CE 认证"]
}
```

## 配置
```json
{
  "compliance": {
    "enabled": true,
    "auto_update": true,
    "update_interval": 86400
  },
  "clearance": {
    "enabled": true,
    "auto_hs_code": true,
    "doc_template": "standard"
  },
  "alert": {
    "regulation_change": true,
    "compliance_risk": true,
    "certification_expiry": true
  }
}
```

## 使用示例
```python
from core import ComplianceEngine

engine = ComplianceEngine(config_path="config.json")

# 合规检查
result = engine.check(
    product="折叠房屋",
    market="澳大利亚",
    hs_code="9406.00"
)

# 清关文件生成
docs = engine.generate_clearance_docs(
    shipment_id="SH-2026-001",
    destination="Sydney"
)

# 法规追踪
updates = engine.track_regulations(
    market="Australia",
    category="construction"
)
```
