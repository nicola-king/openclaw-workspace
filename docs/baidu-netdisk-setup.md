# 百度网盘集成配置指南

> 创建时间：2026-04-10  
> 系统：Ubuntu 24.04 LTS  
> 状态：✅ bypy 已安装

---

## ✅ 已安装工具

| 工具 | 版本 | 状态 |
|------|------|------|
| **bypy** | v1.8.9 | ✅ 已安装 |

---

## 🔐 登录绑定流程

### 步骤 1: 授权百度网盘

**在终端执行**：
```bash
bypy info
```

**或者**：
```bash
bypy authorize
```

### 步骤 2: 获取授权码

1. 命令会输出一个 URL 链接
2. 在浏览器中打开该链接
3. 使用百度账号登录
4. 授予应用访问权限
5. 复制授权码

### 步骤 3: 完成绑定

将授权码输入终端，完成绑定。

---

## 📋 常用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `bypy info` | 查看网盘信息 | `bypy info` |
| `bypy list` | 列出文件 | `bypy list /apps` |
| `bypy upload` | 上传文件 | `bypy upload local.txt remote.txt` |
| `bypy download` | 下载文件 | `bypy download remote.txt local.txt` |
| `bypy mkdir` | 创建目录 | `bypy mkdir /apps/taiyi` |
| `bypy remove` | 删除文件 | `bypy remove remote.txt` |
| `bypy search` | 搜索文件 | `bypy search keyword` |
| `bypy quota` | 查看配额 | `bypy quota` |

---

## 📁 文件位置

| 项目 | 路径 |
|------|------|
| 配置文件 | `~/.bypy` |
| 授权令牌 | `~/.bypy.json` |
| 默认下载目录 | `~/BaiduNetdiskDownload` |

---

## 🚀 自动化集成

### 太一自动备份

配置完成后，太一可以：
- ✅ 自动备份重要文件到百度网盘
- ✅ 自动下载指定文件
- ✅ 同步工作区文件
- ✅ 远程文件管理

### Cron 定时备份

```bash
# 每天凌晨 2 点备份
0 2 * * * bypy upload /home/nicola/.openclaw/workspace /apps/taiyi/workspace
```

---

## ⚠️ 注意事项

1. **API 限制**: 百度网盘 API 有调用频率限制
2. **文件大小**: 单文件最大 4GB (非会员)
3. **下载速度**: 非会员可能限速
4. **授权有效期**: 授权令牌长期有效，除非手动撤销

---

## 🔧 故障排查

### 授权失败
```bash
# 删除旧授权，重新授权
rm ~/.bypy.json
bypy authorize
```

### 上传失败
```bash
# 检查网络连接
bypy info

# 检查配额
bypy quota
```

### 下载失败
```bash
# 检查文件路径
bypy list /apps

# 重试下载
bypy download -d remote.txt
```

---

## 📞 获取帮助

```bash
# 查看帮助
bypy --help

# 查看子命令帮助
bypy upload --help
```

---

*太一 AGI 协助配置 | 2026-04-10*
