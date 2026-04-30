# 📲 OpenClaw 微信安装命令

> **更新时间**: 2026-04-08 17:33  
> **状态**: ✅ 插件已安装

---

## 🔧 微信插件安装命令

### 方式 1: OpenClaw CLI (推荐)

```bash
# 安装微信插件
openclaw plugin install openclaw-wechat

# 安装微信插件 (备用源)
openclaw plugin install openclaw-weixin

# 查看已安装插件
openclaw plugin list

# 启用微信插件
openclaw plugin enable openclaw-wechat

# 禁用微信插件
openclaw plugin disable openclaw-wechat

# 卸载微信插件
openclaw plugin uninstall openclaw-wechat
```

---

### 方式 2: npm 手动安装

```bash
# 进入 OpenClaw 扩展目录
cd ~/.openclaw/extensions

# 安装微信插件
npm install @canghe/openclaw-wechat

# 或安装微信插件 (腾讯官方)
npm install @tencent-weixin/openclaw-weixin

# 验证安装
ls -la ~/.openclaw/extensions/openclaw-wechat/
```

---

### 方式 3: 从源码安装

```bash
# 克隆插件仓库
cd ~/.openclaw/extensions
git clone https://github.com/openclaw/openclaw-wechat.git

# 安装依赖
cd openclaw-wechat
npm install

# 重启 Gateway
openclaw gateway restart
```

---

## ⚙️ 微信插件配置

### 配置文件位置

```
~/.openclaw/openclaw.json
```

### 配置示例

```json
{
  "plugins": {
    "entries": {
      "openclaw-wechat": {
        "enabled": true
      }
    }
  },
  "channels": {
    "wechat": {
      "enabled": true,
      "type": "official-account",
      "appId": "wx720a4c489fec9df3",
      "appSecret": "94066275ad79af78b29b3c5f1ef7660c",
      "token": "",
      "encodingAesKey": ""
    }
  }
}
```

---

## 🔐 微信公众号配置

### 获取公众号凭证

1. **访问**: https://mp.weixin.qq.com/
2. **登录**: 使用公众号管理员微信
3. **设置**: 左侧菜单 → 设置与开发 → 基本配置
4. **获取**:
   - AppID (开发者 ID)
   - AppSecret (开发者密码)

### 配置服务器

```
URL: https://your-domain.com/wechat
Token: 自定义 (如：taiyi2026)
EncodingAESKey: 随机生成
```

---

## 🚀 重启 Gateway

```bash
# 重启 Gateway 使配置生效
openclaw gateway restart

# 查看 Gateway 状态
openclaw gateway status

# 查看日志
openclaw logs --follow
```

---

## 📊 验证安装

```bash
# 查看插件列表
openclaw plugin list

# 查看微信通道状态
openclaw status | grep -i wechat

# 测试微信通道
openclaw status --deep
```

---

## 🔍 故障排查

### Q: 插件安装失败？

```bash
# 清理缓存
npm cache clean --force

# 重新安装
openclaw plugin install openclaw-wechat --force
```

### Q: Gateway 启动失败？

```bash
# 查看日志
openclaw logs --follow

# 检查配置
cat ~/.openclaw/openclaw.json | grep -A 10 wechat

# 重置配置
openclaw gateway reset-config
```

### Q: 微信通道未显示？

```bash
# 检查插件是否启用
openclaw plugin list | grep wechat

# 手动启用
openclaw plugin enable openclaw-wechat

# 重启 Gateway
openclaw gateway restart
```

---

## 📚 相关文档

- **官方文档**: https://docs.openclaw.ai/channels/wechat
- **插件仓库**: https://github.com/openclaw/openclaw-wechat
- **配置指南**: `~/.openclaw/workspace-taiyi/config/wechat.json`

---

## ✅ 当前状态

| 项目 | 状态 |
|------|------|
| **openclaw-wechat** | ✅ 已安装 |
| **openclaw-weixin** | ✅ 已安装 |
| **公众号配置** | ✅ 已保存 |
| **SMTP 邮件** | ✅ 已配置 |

---

**太一 AGI · 2026-04-08**
