# 📦 太一 Agent 交付物模板库

> 版本：v1.0 | 借鉴 agency-agents | 更新：2026-04-16

---

## 一、代码交付物模板

### 1.1 Python 模块模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[模块名称]

功能描述：[一句话描述模块功能]

作者：太一 AGI
创建：[日期]
版本：v1.0
"""

import logging
from typing import Dict, List, Optional

# 日志配置
logger = logging.getLogger(__name__)

# 配置
CONFIG = {
    "timeout": 30,
    "retry": 3,
}


class [ClassName]:
    """[类名] - [类功能描述]"""
    
    def __init__(self, config: Dict = None):
        """
        初始化
        
        参数:
            config: 配置参数
        """
        self.config = config or CONFIG
        logger.info(f"[ClassName] 初始化完成")
    
    async def execute(self, **kwargs) -> Dict:
        """
        执行核心功能
        
        参数:
            **kwargs: 动态参数
        
        返回:
            Dict: 执行结果
        """
        try:
            # 实现逻辑
            result = await self._process(**kwargs)
            return result
        except Exception as e:
            logger.error(f"执行失败：{e}")
            raise
    
    async def _process(self, **kwargs) -> Dict:
        """内部处理方法"""
        # 实现细节
        pass


# 使用示例
if __name__ == "__main__":
    agent = [ClassName]()
    result = agent.execute(param="value")
    print(result)
```

### 1.2 API 接口模板

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="[API 名称]")


class [RequestModel](BaseModel):
    """请求模型"""
    param1: str
    param2: Optional[int] = None


class [ResponseModel](BaseModel):
    """响应模型"""
    success: bool
    data: Dict
    message: str


@app.post("/api/[endpoint]", response_model=[ResponseModel])
async def [endpoint](request: [RequestModel]):
    """
    [接口描述]
    
    - **param1**: 参数 1 描述
    - **param2**: 参数 2 描述
    
    返回:
        - success: 是否成功
        - data: 返回数据
        - message: 消息
    """
    try:
        # 业务逻辑
        result = await process(request)
        
        return [ResponseModel](
            success=True,
            data=result,
            message="操作成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 1.3 配置文件模板 (YAML)

```yaml
# config.yaml - [模块名称] 配置

# 基础配置
base:
  name: "[模块名称]"
  version: "1.0.0"
  environment: "production"  # development/staging/production

# 服务配置
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 30

# 数据库配置
database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  name: "database_name"
  user: "user"
  password: "${DB_PASSWORD}"  # 使用环境变量

# 日志配置
logging:
  level: "INFO"  # DEBUG/INFO/WARNING/ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/app.log"
  max_size: "10MB"
  backup_count: 5

# 功能开关
features:
  feature_a: true
  feature_b: false
  feature_c:
    enabled: true
    threshold: 0.8
```

---

## 二、文档交付物模板

### 2.1 技术设计文档

```markdown
# [项目名称] 技术设计文档

> 版本：v1.0 | 日期：2026-04-16 | 作者：太一 AGI

---

## 一、概述

### 1.1 项目背景
[描述项目背景和目标]

### 1.2 设计目标
- 目标 1
- 目标 2
- 目标 3

### 1.3 范围
**包含**:
- 功能 1
- 功能 2

**不包含**:
- 非功能 1
- 非功能 2

---

## 二、架构设计

### 2.1 系统架构图
```
┌─────────────┐
│   用户层    │
└──────┬──────┘
       │
┌──────▼──────┐
│   应用层    │
└────────────┘
       │
┌──────▼──────┐
│   数据层    │
└─────────────┘
```

### 2.2 技术选型
| 层次 | 技术 | 理由 |
|------|------|------|
| 前端 | React/Vue | 生态成熟 |
| 后端 | Python/FastAPI | 性能优秀 |
| 数据库 | PostgreSQL | 稳定可靠 |

---

## 三、模块设计

### 3.1 模块 A
**职责**: [模块职责]

**接口**:
```python
def function_a(param1: str) -> Dict:
    """函数描述"""
    pass
```

**依赖**:
- 依赖 1
- 依赖 2

---

## 四、数据设计

### 4.1 数据模型
```sql
CREATE TABLE [table_name] (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.2 数据流
```
用户输入 → 验证 → 处理 → 存储 → 返回
```

---

## 五、安全设计

### 5.1 认证授权
- JWT Token 认证
- RBAC 权限控制

### 5.2 数据安全
- 敏感数据加密
- SQL 注入防护
- XSS 防护

---

## 六、部署方案

### 6.1 环境要求
- Python 3.12+
- PostgreSQL 14+
- Redis 6+

### 6.2 部署步骤
1. 安装依赖
2. 配置环境变量
3. 数据库迁移
4. 启动服务

---

## 七、监控与运维

### 7.1 监控指标
- CPU 使用率
- 内存使用率
- 请求延迟
- 错误率

### 7.2 告警策略
- CPU>80% 告警
- 错误率>1% 告警
```

### 2.2 API 文档模板

```markdown
# [API 名称] 接口文档

> 版本：v1.0 | 基础 URL: `https://api.example.com/v1`

---

## 认证

所有接口需要在 Header 中携带 Token:
```
Authorization: Bearer <your_token>
```

---

## 接口列表

### 1. [接口名称]

**请求**:
```http
POST /api/[endpoint]
Content-Type: application/json

{
  "param1": "value1",
  "param2": 123
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "example"
  },
  "message": "操作成功"
}
```

**错误码**:
| 码 | 说明 |
|----|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 500 | 服务器错误 |

---

## SDK 使用示例

### Python
```python
from sdk import Client

client = Client(api_key="your_key")
result = client.[method](param="value")
```

### JavaScript
```javascript
const client = new Client({ apiKey: 'your_key' });
const result = await client.[method]({ param: 'value' });
```
```

---

## 三、报告交付物模板

### 3.1 日报模板

```markdown
# 工作日报 · [日期]

> 报告人：[Agent 名称] | 部门：[部门]

---

## 一、今日完成

| 任务 | 状态 | 耗时 | 成果 |
|------|------|------|------|
| 任务 1 | ✅ | 2h | 完成内容 |
| 任务 2 | ✅ | 3h | 完成内容 |
| 任务 3 | 🟡 | 1h | 进行中 |

---

## 二、关键指标

| 指标 | 目标 | 实际 | 达成率 |
|------|------|------|--------|
| 指标 1 | 100 | 95 | 95% |
| 指标 2 | 50 | 55 | 110% |

---

## 三、问题与风险

### 问题
1. **问题描述**: [描述]
   **影响**: [影响]
   **解决方案**: [方案]

### 风险
1. **风险描述**: [描述]
   **概率**: 高/中/低
   **应对**: [应对措施]

---

## 四、明日计划

- [ ] 任务 1
- [ ] 任务 2
- [ ] 任务 3

---

## 五、需要支持

- [需要协调的资源/帮助]
```

### 3.2 周报模板

```markdown
# 工作周报 · 第 [X] 周 (YYYY-MM-DD)

> 报告人：[Agent 名称] | 部门：[部门]

---

## 一、本周摘要

**核心成果**:
- 成果 1
- 成果 2
- 成果 3

**关键指标**:
| 指标 | 本周 | 上周 | 环比 |
|------|------|------|------|
| 指标 1 | 100 | 90 | +11% |
| 指标 2 | 50 | 55 | -9% |

---

## 二、工作详情

### 2.1 已完成
| 任务 | 优先级 | 状态 | 成果 |
|------|--------|------|------|
| 任务 1 | P0 | ✅ | 详细描述 |
| 任务 2 | P1 | ✅ | 详细描述 |

### 2.2 进行中
| 任务 | 优先级 | 进度 | 预计完成 |
|------|--------|------|---------|
| 任务 3 | P0 | 70% | 周三 |
| 任务 4 | P1 | 30% | 周五 |

### 2.3 未开始
| 任务 | 优先级 | 计划开始 | 备注 |
|------|--------|---------|------|
| 任务 5 | P2 | 下周 | 等待依赖 |

---

## 三、问题与风险

### 已解决问题
1. **问题**: [描述]
   **解决**: [方案]
   **时间**: [耗时]

### 待解决问题
1. **问题**: [描述]
   **影响**: [影响]
   **需要**: [需要的支持]

### 风险预警
| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 风险 1 | 中 | 高 | 应对措施 |

---

## 四、下周计划

### P0 任务
- [ ] 任务 1
- [ ] 任务 2

### P1 任务
- [ ] 任务 3
- [ ] 任务 4

### P2 任务
- [ ] 任务 5

---

## 五、思考与建议

[本周的思考、优化建议、创新想法等]
```

---

## 四、交付物质量检查清单

### 4.1 代码检查

- [ ] 代码符合 PEP8 规范
- [ ] 有完整的文档字符串
- [ ] 有单元测试覆盖
- [ ] 有使用示例
- [ ] 错误处理完善
- [ ] 日志记录完整
- [ ] 配置可外部化

### 4.2 文档检查

- [ ] 结构清晰完整
- [ ] 语言准确简洁
- [ ] 有图表辅助说明
- [ ] 有版本记录
- [ ] 有联系方式
- [ ] 格式统一规范

### 4.3 报告检查

- [ ] 数据准确无误
- [ ] 分析深入有洞察
- [ ] 建议具体可执行
- [ ] 格式美观易读
- [ ] 按时提交

---

*太一 AGI · Agent 交付物模板库 · 2026-04-16*
