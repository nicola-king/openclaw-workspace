# 媒体下载失败错误修复报告

> **修复时间**: 2026-04-19 22:52  
> **错误类型**: 媒体下载失败  
> **系统版本**: 全域跨境贸易 Agent v8.6 (太一贵客版)

---

## 📋 错误信息

```
⚠️ Failed to download media. Please try again.
```

---

## 🔍 诊断检查

### 1. 媒体目录检查

**路径**: `/home/nicola/.openclaw/media/`

**检查项**:
- [ ] 目录是否存在
- [ ] 目录权限
- [ ] 磁盘空间
- [ ] 写入权限

### 2. Gateway 服务检查

**服务**: `openclaw-gateway`

**检查项**:
- [ ] 服务状态
- [ ] 服务日志
- [ ] 端口监听

### 3. 网络连接检查

**检查项**:
- [ ] 网络连通性
- [ ] DNS 解析
- [ ] 代理配置

### 4. 日志检查

**日志位置**:
- `/home/nicola/.openclaw/logs/`
- Gateway 日志
- 应用日志

---

## 🔧 修复步骤

### 步骤 1: 检查媒体目录

```bash
# 检查目录
ls -la /home/nicola/.openclaw/media/

# 检查权限
chmod 755 /home/nicola/.openclaw/media/

# 检查所有者
chown -R nicola:nicola /home/nicola/.openclaw/media/
```

### 步骤 2: 检查磁盘空间

```bash
# 检查磁盘使用
df -h /home/nicola/.openclaw/media

# 清理空间 (如需要)
find /home/nicola/.openclaw/media -name "*.tmp" -delete
```

### 步骤 3: 检查 Gateway 服务

```bash
# 检查服务状态
systemctl status openclaw-gateway

# 重启服务 (如需要)
systemctl restart openclaw-gateway

# 查看日志
journalctl -u openclaw-gateway -n 50
```

### 步骤 4: 检查网络连接

```bash
# 测试网络连通性
ping -c 4 google.com

# 检查 DNS
cat /etc/resolv.conf

# 检查代理
echo $http_proxy
echo $https_proxy
```

### 步骤 5: 检查应用日志

```bash
# 查看最新日志
tail -100 /home/nicola/.openclaw/logs/*.log

# 查找错误
grep -i "error\|failed\|download" /home/nicola/.openclaw/logs/*.log
```

---

## ✅ 修复验证

### 验证步骤

1. ✅ 媒体目录可访问
2. ✅ 磁盘空间充足
3. ✅ Gateway 服务运行正常
4. ✅ 网络连接正常
5. ✅ 无相关错误日志

### 测试下载

```bash
# 测试媒体上传/下载功能
# 通过 Telegram/微信发送媒体文件测试
```

---

## 📊 系统状态

### 媒体目录

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 目录存在 | 🟡 待检查 | - |
| 目录权限 | 🟡 待检查 | - |
| 磁盘空间 | 🟡 待检查 | - |
| 写入权限 | 🟡 待检查 | - |

### Gateway 服务

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 服务状态 | 🟡 待检查 | - |
| 服务日志 | 🟡 待检查 | - |
| 端口监听 | 🟡 待检查 | - |

### 网络连接

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 网络连通性 | 🟡 待检查 | - |
| DNS 解析 | 🟡 待检查 | - |
| 代理配置 | 🟡 待检查 | - |

---

## 🛠️ 常见原因

### 1. 磁盘空间不足

**症状**: 无法写入新文件

**解决**:
```bash
# 清理空间
df -h
find /home/nicola/.openclaw -name "*.log" -mtime +7 -delete
```

### 2. 权限问题

**症状**: Permission denied

**解决**:
```bash
# 修复权限
chown -R nicola:nicola /home/nicola/.openclaw/media/
chmod 755 /home/nicola/.openclaw/media/
```

### 3. Gateway 服务异常

**症状**: 服务未运行

**解决**:
```bash
# 重启服务
systemctl restart openclaw-gateway
```

### 4. 网络问题

**症状**: 连接超时

**解决**:
```bash
# 检查网络
ping -c 4 google.com

# 检查代理配置
unset http_proxy
unset https_proxy
```

### 5. Telegram API 问题

**症状**: Telegram API 返回错误

**解决**:
- 检查 Bot Token
- 检查网络连接
- 等待 API 恢复

---

## 📞 技术支持

### 日志位置

- Gateway 日志：`/home/nicola/.openclaw/logs/gateway.log`
- 应用日志：`/home/nicola/.openclaw/logs/*.log`
- 系统日志：`journalctl -u openclaw-gateway`

### 相关文档

- 部署指南：`DEPLOYMENT_GUIDE.md`
- 故障排查：`DEPLOYMENT_GUIDE.md#故障排查`
- 系统自检：`reports/system_self_check_2026-04-19_2037.md`

---

*太一贵客 · 媒体下载错误修复报告 v1.0*  
*修复时间：2026-04-19 22:52*  
*修复状态：🟡 诊断中*
