# CLI Toolkit CLI 工具集

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P1

---

## 📋 概述

CLI 工具集整合了常用命令行工具的 Python 封装，提供云资源管理、DevOps 自动化和系统工具的统一接口。

---

## 🏗️ 架构

```
cli-toolkit/
├── __init__.py              # 主入口，CLIToolkit 类
├── SKILL.md                 # 技能定义
├── cloud/                   # 云资源模块
│   ├── aws_cli.py           # AWS CLI 封装
│   ├── gcp_cli.py           # GCP CLI 封装
│   └── azure_cli.py         # Azure CLI 封装
├── devops/                  # DevOps 模块
│   ├── docker_ctl.py        # Docker 控制
│   ├── k8s_deploy.py        # K8s 部署
│   └── terraform_apply.py   # Terraform 执行
└── wrappers/                # 工具封装
    ├── git_wrapper.py       # Git 操作
    └── npm_wrapper.py       # NPM 操作
```

---

## 🚀 快速开始

### 初始化

```python
from skills.cli_toolkit import CLIToolkit

cli = CLIToolkit()
```

### 云资源管理

#### AWS

```python
# 列出 EC2 实例
instances = cli.cloud.aws.list_instances()

# 启动实例
cli.cloud.aws.start_instance('i-1234567890abcdef0')

# 创建 S3 bucket
cli.cloud.aws.create_bucket('my-bucket')

# 上传文件
cli.cloud.aws.upload_file('file.txt', 'my-bucket', 'path/file.txt')
```

#### GCP

```python
# 列出 VM 实例
instances = cli.cloud.gcp.list_instances()

# 创建存储桶
cli.cloud.gcp.create_bucket('my-bucket')

# 部署 Cloud Run
cli.cloud.gcp.deploy_cloud_run('service-name', 'image:tag')
```

#### Azure

```python
# 列出 VM
vms = cli.cloud.azure.list_vms()

# 创建资源组
cli.cloud.azure.create_resource_group('my-rg')

# 部署应用
cli.cloud.azure.deploy_app('app-name', 'resource-group')
```

### DevOps 自动化

#### Docker

```python
# 构建镜像
cli.devops.docker.build('my-image', './')

# 运行容器
cli.devops.docker.run('my-image', ports={'8080': '80'})

# 停止容器
cli.devops.docker.stop('container-id')

# 清理
cli.devops.docker.prune()
```

#### Kubernetes

```python
# 部署应用
cli.devops.k8s.deploy(
    name='my-app',
    image='my-image:tag',
    replicas=3,
    namespace='production'
)

# 扩缩容
cli.devops.k8s.scale('my-app', replicas=5)

# 查看日志
logs = cli.devops.k8s.logs('my-app-pod-xxx')

# 回滚
cli.devops.k8s.rollback('my-app')
```

#### Terraform

```python
# 初始化
cli.devops.terraform.init('./infra')

# 规划
plan = cli.devops.terraform.plan('./infra')

# 应用（需要确认）
cli.devops.terraform.apply('./infra', auto_approve=False)

# 销毁
cli.devops.terraform.destroy('./infra')
```

### Git 操作

```python
# 克隆仓库
cli.git.clone('https://github.com/user/repo.git')

# 提交更改
cli.git.commit('feat: add new feature')

# 推送
cli.git.push()

# 创建分支
cli.git.create_branch('feature/new-feature')

# 合并
cli.git.merge('main')
```

### NPM 操作

```python
# 安装包
cli.npm.install('package-name')

# 开发依赖
cli.npm.install_dev('jest')

# 运行脚本
cli.npm.run('build')

# 审计
audit_result = cli.npm.audit()
```

---

## ⚠️ 安全注意事项

### 云资源

- ✅ 使用 IAM 角色而非 Access Key
- ✅ 最小权限原则
- ✅ 操作前确认
- ✅ 审计日志

### DevOps

- ✅ 生产环境需要确认
- ✅ 回滚方案准备
- ✅ 备份优先
- ✅ 灰度发布

### Git

- ✅ 推送前 review
- ✅ 保护分支
- ✅ 签名提交
- ✅ CI 检查

---

## 🔧 配置

### 云配置

```yaml
# ~/.openclaw/config/cloud.yaml
aws:
  profile: default
  region: us-east-1

gcp:
  project: my-project
  zone: us-central1-a

azure:
  subscription: xxx-xxx-xxx
  resource_group: default
```

### DevOps 配置

```yaml
# ~/.openclaw/config/devops.yaml
docker:
  registry: docker.io
  namespace: my-namespace

k8s:
  context: production
  namespace: default

terraform:
  backend: s3
  state_bucket: tf-state
```

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/cli_toolkit/tests/ -v

# 测试 AWS
python3 -m pytest skills/cli_toolkit/tests/test_aws.py -v

# 测试 Docker
python3 -m pytest skills/cli_toolkit/tests/test_docker.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [AWS CLI 文档](https://awscli.amazonaws.com/v2/documentation/)
- [Docker 文档](https://docs.docker.com/)
- [Kubernetes 文档](https://kubernetes.io/docs/)

---

*维护：太一 AGI | CLI Toolkit v2.0*
