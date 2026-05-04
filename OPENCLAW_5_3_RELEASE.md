# OpenClaw 2026.5.3 版本发布说明

> **发布时间**: 2026-05-04
> **当前版本**: 2026.5.2
> **最新版本**: 2026.5.3 (Pre-release)
> **来源**: GitHub Releases

---

## 🎯 核心亮点

### 1. 文件传输插件 (Plugins/file-transfer)
- **新增** bundled file-transfer 插件
- **功能**: file_fetch, dir_list, dir_fetch, file_write
- **安全**: 每节点路径策略，默认拒绝，符号链接遍历默认关闭
- **限制**: 每次往返 16 MB 字节上限
- **PR**: #74742

### 2. 插件安装强化 (Plugins/install)
- 官方插件安装、卸载、更新加固
- 外部插件行为如一等包安装
- npm 依赖状态报告
- beta 通道更新路径

### 3. 网关性能优化 (Gateway/performance)
- **延迟加载**: 插件/运行时发现、cron、schema、shutdown
- **按需加载**: sessions、模型元数据
- **优化**: Control UI 热路径

### 4. 频道回复改进 (Channels/replies)
- Discord 状态反应优化
- WhatsApp Channel/Newsletter 目标支持
- Telegram、飞书、Matrix、Teams、Slack 交付/恢复行为优化

### 5. 安装/更新修复 (Install/update)
- 修复 macOS LaunchAgent 升级
- 拒绝仅源码插件包
- 修复更新期间的 Gateway/插件状态

### 6. Agent/运行时可靠性 (Agent/runtime reliability)
- 保留流式提供商回复
- 延迟 A2A 会话回复
- 提示/工具交付
- 记忆召回
- 网页搜索提供商发现
- 提供商特定思考/模型元数据

---

## 📝 详细变更

### 频道/流式 (Channels/streaming)
- **新增**: unified streaming.mode: "progress" drafts
- **功能**: 自动单字状态标签
- **共享**: 跨 Discord、Telegram、Matrix、Slack、Teams 进度配置

### Agent/命令 (Agents/commands)
- **新增**: `/steer` 命令
- **功能**: 队列独立转向当前会话运行
- **场景**: 会话空闲时不启动新回合
- **PR**: #76934

### 工具/BTW (Tools/BTW)
- **新增**: `/side` 别名
- **功能**: `/btw` 侧边问题的文本和原生斜杠命令别名

### Doctor/配置 (Doctor/config)
- **改进**: `doctor --fix` 现在提交安全的旧版迁移
- **场景**: 即使存在不相关的验证问题

---

## 🚀 升级建议

### 当前系统状态
| 组件 | 当前版本 | 最新版本 | 状态 |
|------|---------|---------|------|
| openclaw | 2026.5.2 | 2026.5.3 | 🟡 可升级 |
| @larksuite/openclaw-lark | 2026.4.10 | - | ✅ 最新 |

### 升级命令

```bash
# 升级 OpenClaw
npm update -g openclaw

# 或重新安装
npm install -g openclaw@latest

# 验证版本
openclaw --version
```

### 升级后检查

```bash
# 检查 Gateway 状态
openclaw gateway status

# 运行诊断
openclaw doctor

# 检查插件状态
openclaw plugins list
```

---

## ⚠️ 注意事项

1. **Pre-release**: 2026.5.3 是预发布版本，可能不稳定
2. **备份**: 升级前备份配置
3. **测试**: 在生产环境使用前测试
4. **依赖**: 确保所有插件兼容新版本

---

## 🔗 相关链接

- [GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [更新日志](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)
- [文档](https://docs.openclaw.ai)

---

*太一 AGI · OpenClaw 版本追踪*
*生成时间: 2026-05-04*
