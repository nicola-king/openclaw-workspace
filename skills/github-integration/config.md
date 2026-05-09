# 太一 GitHub 集成配置
# 采用系统内部信息架构

github:
  # 认证方式 (token/ssh)
  auth_type: "token"

  # Personal Access Token (从环境变量读取优先)
  token: "${GITHUB_TOKEN}"

  # SSH 密钥路径
  ssh_key: "~/.ssh/id_rsa"

  # 默认仓库
  default_repo: "sayelf/taiyi-system"

  # 用户名
  username: "sayelf"

# 提交配置
commit:
  # 默认提交信息前缀
  prefix: "[太一]"

  # 自动提交启用
  auto_commit: true

  # 自动提交间隔 (分钟)
  auto_commit_interval: 60

# 同步配置
sync:
  # 自动同步配置到 GitHub
  auto_sync: true

  # 同步的文件模式
  patterns:
    - "constitution/**"
    - "skills/**"
    - "memory/**"
    - "*.md"
    - "*.yaml"
    - "*.json"

  # 排除的文件
  exclude:
    - "*.pyc"
    - "__pycache__/"
    - "venv*/"
    - ".env"

# 备份配置
backup:
  # 自动创建备份分支
  auto_backup: true

  # 备份分支前缀
  branch_prefix: "backup/"

  # 保留的备份数量
  keep_count: 10
