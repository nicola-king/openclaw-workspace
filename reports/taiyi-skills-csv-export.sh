#!/bin/bash
# 导出 Skills 为 CSV 格式

OUTPUT="/tmp/taiyi-skills.csv"

echo "编号,英文名,中文名,类别,关键功能 EN,关键功能 CN,安装命令" > "$OUTPUT"

# P0 核心工具
echo "S001,git-integration,Git 集成，核心工具,Git clone/commit/push/PR,Git 版本控制全工作流，clawhub install git-integration" >> "$OUTPUT"
echo "S002,npm-audit,NPM 审计，核心工具,Dependency vulnerability scan，依赖漏洞扫描，clawhub install npm-audit" >> "$OUTPUT"
echo "S003,docker-ctl,Docker 管理，核心工具,Container/image/Compose lifecycle，容器/镜像/Compose 全生命周期，clawhub install docker-ctl" >> "$OUTPUT"

# P1 云原生
echo "S004,k8s-deploy,K8s 部署，云原生，Kubernetes deploy/scale/logs,K8s 应用部署/扩缩容，clawhub install k8s-deploy" >> "$OUTPUT"
echo "S005,terraform-apply,Terraform，云原生，Infrastructure as Code，基础设施即代码，clawhub install terraform-apply" >> "$OUTPUT"
echo "S006,aws-cli,AWS 命令行，云原生，AWS EC2/S3/Lambda operations,AWS 云服务操作，clawhub install aws-cli" >> "$OUTPUT"
echo "S007,gcp-cli,GCP 命令行，云原生，GCP Compute/GKE operations,GCP 云服务操作，clawhub install gcp-cli" >> "$OUTPUT"
echo "S008,azure-cli,Azure 命令行，云原生，Azure VM/AKS operations,Azure 云服务操作，clawhub install azure-cli" >> "$OUTPUT"

echo ""
echo "✅ CSV 已导出：$OUTPUT"
echo ""
echo "前 10 行预览:"
head -11 "$OUTPUT"
