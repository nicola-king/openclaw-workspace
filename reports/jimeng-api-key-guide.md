# 🔑 即梦 API Key 获取指南

> 创建时间：2026-04-06 09:27  
> 状态：🟡 需要 API Key 才能使用即梦 CLI

---

## 📋 为什么需要 API Key？

**即梦 CLI** 通过火山引擎平台进行身份认证和配额管理，每次调用都会：
- ✅ 验证用户身份
- ✅ 扣除生成配额
- ✅ 记录使用日志

---

## 🎯 获取步骤

### 步骤 1: 登录即梦官网

访问：https://jimeng.jianying.com

**支持的账号**:
- 抖音账号
- 头条账号
- 火山引擎账号
- 手机号注册

### 步骤 2: 进入 API 控制台

1. 登录成功后
2. 点击左上角 **API 调用** 或 **控制台**
3. 进入 API 管理页面

### 步骤 3: 创建 API Key

1. 点击 **创建新密钥**
2. 填写应用名称 (如 "太一 AGI")
3. 选择权限范围：
   - ✅ 文生图
   - ✅ 文生视频
   - ✅ 图生图
   - ✅ 图生视频
4. 点击 **确认创建**

### 步骤 4: 保存密钥

**重要**: 密钥只显示一次！立即保存：

```
AccessKeyID: ak_xxxxxxxxxxxxxxxxxxxx
SecretAccessKey: sk_xxxxxxxxxxxxxxxxxxxx
```

**建议**: 存入密码管理器或加密文件

---

## 🔧 配置到太一系统

### 方式 1: CLI 配置

```bash
jimeng config set access_key_id YOUR_ACCESS_KEY_ID
jimeng config set secret_access_key YOUR_SECRET_ACCESS_KEY
```

### 方式 2: 环境变量

```bash
export JIMENG_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
export JIMENG_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
```

### 方式 3: 配置文件

编辑 `~/.jimeng/config.json`:
```json
{
  "access_key_id": "YOUR_ACCESS_KEY_ID",
  "secret_access_key": "YOUR_SECRET_ACCESS_KEY",
  "model": "seedance-2.0",
  "default_resolution": "1080p"
}
```

---

## 💰 配额与价格

### 免费配额 (参考)

| 功能 | 免费额度 | 说明 |
|------|---------|------|
| 文生图 | 10-50 张/天 | 根据账号等级 |
| 文生视频 | 5-10 条/天 | 5 秒 720p |
| 图生视频 | 5-10 条/天 | 5 秒 720p |

### 付费套餐 (参考)

| 套餐 | 价格 | 配额 |
|------|------|------|
| 基础版 | ¥99/月 | 500 张图 + 50 条视频 |
| 专业版 | ¥299/月 | 2000 张图 + 200 条视频 |
| 企业版 | 定制 | 无限 + 专属支持 |

**注意**: 具体价格以官方为准

---

## 🔒 安全建议

### ✅ 推荐做法
- 使用环境变量存储密钥
- 定期轮换密钥 (每 90 天)
- 设置配额告警
- 监控异常调用

### ❌ 避免做法
- 不要将密钥提交到 Git
- 不要在公开场合分享
- 不要硬编码在代码中
- 不要多人共享同一密钥

---

## 🛠️ 测试连接

```bash
# 查看配额
jimeng balance

# 测试生成
jimeng generate image --prompt "测试" --resolution 512x512

# 查看使用记录
jimeng usage --days 7
```

---

## 📞 遇到问题？

### 常见问题

**Q: 提示 "Invalid API Key"**
- 检查密钥是否正确复制
- 确认密钥未过期
- 重新创建密钥

**Q: 提示 "Quota exceeded"**
- 查看剩余配额：`jimeng balance`
- 升级套餐或等待次日重置

**Q: CLI 无法安装**
- 检查网络连接
- 使用镜像源
- 手动下载二进制

### 官方支持

- **文档**: https://jimeng.jianying.com/docs
- **工单**: 火山引擎控制台
- **社区**: 即梦官方 Discord/微信群

---

## 🔗 相关链接

- **即梦官网**: https://jimeng.jianying.com
- **API 文档**: https://www.volcengine.com/docs/85621/1817045
- **火山引擎**: https://www.volcengine.com

---

*指南创建：太一 AGI | 2026-04-06 09:27*  
*状态：🟡 待用户获取 API Key*
