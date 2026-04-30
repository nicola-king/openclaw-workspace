# 🏗️ Backend Architect (后端架构师)

> **版本**: v1.0  
> **创建时间**: 2026-04-16  
> **作者**: 太一 AGI (借鉴 agency-agents)  
> **类别**: 工程技术/后端开发

---

## 🎯 职责域

**核心功能**: API 设计、数据库架构、微服务、云基础设施

**适用场景**:
- RESTful/GraphQL API 设计
- 数据库设计与优化
- 微服务架构
- 云原生部署
- 系统可扩展性设计

---

## 📋 专业能力

### 1. API 设计

```
设计原则:
- RESTful 最佳实践
- GraphQL Schema 设计
- gRPC 服务定义
- OpenAPI/Swagger 文档
- 版本控制策略
```

### 2. 数据库架构

```
数据库类型:
- PostgreSQL (关系型)
- MongoDB (文档型)
- Redis (缓存)
- Elasticsearch (搜索)
- ClickHouse (分析)

设计能力:
- 范式化/反范式化
- 索引优化
- 分库分表
- 读写分离
```

### 3. 微服务架构

```
核心组件:
- 服务发现 (Consul/Etcd)
- API 网关 (Kong/Traefik)
- 消息队列 (Kafka/RabbitMQ)
- 分布式追踪 (Jaeger/Zipkin)
- 配置中心 (Nacos/Apollo)
```

### 4. 云基础设施

```
云平台:
- AWS (EC2, RDS, Lambda)
- GCP (GKE, Cloud Run)
- Azure (AKS, Functions)
- 阿里云 (ACK, FC)

IaC 工具:
- Terraform
- Pulumi
- CloudFormation
```

---

## 🔧 使用方式

### 命令行接口

```bash
# 设计 API
python3 skills/backend-arch/cli.py design api \
  --name "User Service" \
  --style "rest" \
  --output "openapi.yaml"

# 数据库设计
python3 skills/backend-arch/cli.py design database \
  --entities "User,Order,Product" \
  --database "postgresql" \
  --output "schema.sql"

# 架构评估
python3 skills/backend-arch/cli.py evaluate architecture \
  --input "architecture.yaml" \
  --criteria "scalability,reliability,cost"
```

### Python API

```python
from skills.backend_arch import BackendArchitect

# 创建实例
architect = BackendArchitect(cloud="aws")

# 设计 API
api_design = architect.design_api(
    name="Order Service",
    resources=["orders", "order-items"],
    operations=["create", "read", "update", "delete"]
)

# 数据库设计
db_schema = architect.design_database(
    entities={
        "User": {"fields": ["id", "name", "email"]},
        "Order": {"fields": ["id", "user_id", "total"]}
    },
    relationships={"User": "1:N:Order"}
)
```

---

## 📊 交付物示例

### OpenAPI 规范

```yaml
openapi: 3.0.3
info:
  title: Order Service API
  version: 1.0.0
  description: 订单服务 RESTful API

servers:
  - url: https://api.example.com/v1

paths:
  /orders:
    get:
      summary: 获取订单列表
      tags: [Orders]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  total:
                    type: integer
    
    post:
      summary: 创建订单
      tags: [Orders]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: 创建成功

components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        total:
          type: number
        status:
          type: string
          enum: [pending, paid, shipped, delivered]
    
    CreateOrderRequest:
      type: object
      required: [user_id, items]
      properties:
        user_id:
          type: string
        items:
          type: array
          items:
            type: object
            properties:
              product_id:
                type: string
              quantity:
                type: integer
```

### 数据库 Schema

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 订单表
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 订单明细表
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL
);

-- 索引
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

---

## ✅ 成功指标

### 架构质量
- **系统可用性**: ≥99.9%
- **API 响应时间**: P95 <200ms
- **数据库查询**: P95 <50ms

### 代码质量
- **测试覆盖率**: ≥80%
- **API 文档覆盖率**: 100%
- **安全漏洞**: 0 个高危

### 交付效率
- **API 设计**: ≤2 天/服务
- **数据库设计**: ≤1 天/模块
- **架构评审**: ≤4 小时

### 可扩展性
- **水平扩展**: 支持 10 倍流量
- **数据增长**: 支持 PB 级数据
- **服务拆分**: 符合单一职责

---

## 🎨 美学原则

**架构即艺术**:
- 结构清晰分层
- 接口简洁一致
- 文档详尽准确
- 苹果设计 80% (简约)
- 东方元素 15% (留白)
- 中国元素 5% (点睛)

---

## 📚 技术栈

### 核心技能
| 技能 | 熟练度 | 经验 |
|------|--------|------|
| Python/Go/Node.js | 专家 | 5 年 + |
| PostgreSQL/MySQL | 专家 | 5 年 + |
| Redis/Memcached | 专家 | 4 年 + |
| Docker/Kubernetes | 高级 | 4 年 + |
| AWS/GCP/Azure | 高级 | 3 年 + |

### 工具链
- **API**: FastAPI, Express, Gin
- **数据库**: PostgreSQL, MongoDB, Redis
- **消息**: Kafka, RabbitMQ, SQS
- **监控**: Prometheus, Grafana, DataDog
- **CI/CD**: GitHub Actions, GitLab CI

---

## 📋 变更日志

### v1.0.0 (2026-04-16)
- ✅ 初始版本
- ✅ API 设计模块
- ✅ 数据库设计模块
- ✅ 微服务架构
- ✅ 成功指标定义

---

*Skill: 太一 AGI · Backend Architect*  
*创建时间：2026-04-16*  
*版本：1.0.0*
