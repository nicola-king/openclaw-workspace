# 真实数据验证 (Real Data Verifier) Skill

## 描述
真实数据验证：公司验证/电话验证/邮箱验证/官网验证

## 独立运行
```bash
python core.py --task company --name "Aus Modular Homes"
```

## 依赖
- cross-border-core: ^9.0.0
- data-integrator: ^9.0.0

## API

### 输入
```json
{
  "task": "company",
  "name": "Aus Modular Homes",
  "website": "https://www.ausmodularhomes.com.au"
}
```

### 输出
```json
{
  "status": "success",
  "verified": true,
  "company": {...}
}
```

## 配置
```json
{
  "company": {
    "enabled": true,
    "sources": ["website", "linkedin", "registry"]
  },
  "phone": {
    "enabled": true,
    "format_check": true,
    "country_code": true
  },
  "email": {
    "enabled": true,
    "format_check": true,
    "mx_record": true
  },
  "website": {
    "enabled": true,
    "status_check": true,
    "content_check": true
  }
}
```

## 使用示例
```python
from core import RealDataVerifier

agent = RealDataVerifier(config_path="config.json")
result = agent.execute(task="company", name="Aus Modular Homes")
print(result)
```
