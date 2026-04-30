# 🌐 微信公众号 IP 白名单配置指南

> **创建时间**: 2026-04-11 17:30  
> **状态**: ⚠️ 需要配置

---

## ❌ 错误信息

```
errcode: 40164
errmsg: invalid ip 106.92.109.148 ipv6 ::ffff:106.92.109.148, not in whitelist
```

**原因**: 当前服务器 IP 不在微信公众号 API 白名单中

---

## 📊 当前 IP 信息

**服务器 IP**:
- IPv4: `106.92.109.148`
- IPv6: `::ffff:106.92.109.148`

---

## 🔧 配置步骤

### 步骤 1: 登录微信公众平台

访问：https://mp.weixin.qq.com/

使用账号密码登录

### 步骤 2: 进入基本配置

1. 点击左侧菜单 **设置与开发**
2. 点击 **基本配置**

### 步骤 3: 配置 IP 白名单

1. 找到 **IP 白名单** 部分
2. 点击 **修改**
3. 添加以下 IP 地址：
   ```
   106.92.109.148
   ```
4. 点击 **保存**

### 步骤 4: 验证配置

等待 5-10 分钟让配置生效

然后测试：
```bash
python3 /home/nicola/.openclaw/workspace/skills/shanmu/wechat-auto-publish.py --topic "AI 管家" --mode api
```

---

## 📋 完整 IP 列表

**需要添加到白名单的 IP**:
```
# 主服务器 IP
106.92.109.148

# 备用 IP (如有)
# 添加其他需要的 IP
```

---

## ⚠️ 注意事项

**IP 白名单规则**:
- 最多可添加 10 个 IP
- 支持 IPv4 和 IPv6
- 修改后 5-10 分钟生效
- 定期检查和更新

**安全建议**:
- ✅ 只添加必要的服务器 IP
- ✅ 定期审查白名单
- ✅ 移除不再使用的 IP
- ✅ 记录 IP 变更日志

---

## 🧪 测试命令

**测试 API 访问**:
```bash
# 测试访问令牌
curl -G "https://api.weixin.qq.com/cgi-bin/token" \
  -d "grant_type=client_credential" \
  -d "appid=wx720a4c489fec9df3" \
  -d "secret=94066275ad79af78b29b3c5f1ef7660c"
```

**预期结果** (配置后):
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

**当前结果** (未配置):
```json
{
  "errcode": 40164,
  "errmsg": "invalid ip x.x.x.x, not in whitelist"
}
```

---

## 📞 如需帮助

**微信公众平台客服**:
- 官网：https://mp.weixin.qq.com/
- 客服邮箱：weixin@qq.com

**太一 AGI 支持**:
- 自动检测配置状态
- 自动重试机制
- 错误日志记录

---

**🌐 配置 IP 白名单后即可使用微信公众号 API！**

**太一 AGI · 2026-04-11 17:30** ✨
