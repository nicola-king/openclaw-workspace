# 百度网盘自动集成配置

> 创建时间：2026-04-10 16:28  
> 状态：🟡 等待授权

---

## ✅ 已完成的准备工作

| 项目 | 状态 | 说明 |
|------|------|------|
| **bypy 工具** | ✅ 已安装 | v1.8.9 |
| **配置文件** | ✅ 已创建 | `~/.bypy.json` |
| **baidupcs-web** | ✅ 已下载 | Web 客户端 |
| **安装脚本** | ✅ 已准备 | `~/下载/baidu-netdisk-install.sh` |

---

## 🔐 授权流程 (只需 1 分钟)

### 方式 1: bypy 命令行授权 (推荐)

**在终端执行**：
```bash
bypy info
```

**然后**：
1. 复制输出的 URL 到浏览器打开
2. 登录百度账号
3. 点击"同意"授权
4. 复制授权码
5. 在终端粘贴授权码，按回车

**授权成功后**：
- 太一会自动检测授权状态
- 自动配置备份任务
- 自动同步工作区文件

---

### 方式 2: Web 客户端

**启动 Web 客户端**：
```bash
cd ~/下载/baidupcs-web
./baidupcs-web
```

**访问**：
```
http://localhost:8080
```

**扫码登录**即可使用。

---

## 📋 授权后可用功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **查看配额** | `bypy quota` | 查看网盘容量 |
| **查看信息** | `bypy info` | 查看账号信息 |
| **列出文件** | `bypy list` | 列出网盘文件 |
| **上传文件** | `bypy upload 本地 远程` | 上传文件 |
| **下载文件** | `bypy download 远程 本地` | 下载文件 |
| **创建目录** | `bypy mkdir /路径` | 创建文件夹 |

---

## 🤖 太一自动化集成

授权完成后，太一会自动：

### 1. 工作区备份
```bash
# 每天凌晨 2 点自动备份
0 2 * * * bypy upload /home/nicola/.openclaw/workspace /apps/taiyi/workspace
```

### 2. 配置文件同步
```bash
# 同步配置文件
bypy sync /home/nicola/.openclaw/workspace-taiyi/config /apps/taiyi/config
```

### 3. 报告归档
```bash
# 自动归档日报/周报
bypy upload /home/nicola/.openclaw/workspace/reports /apps/taiyi/reports
```

---

## 📁 文件位置

| 项目 | 路径 |
|------|------|
| bypy 配置 | `~/.bypy.json` |
| bypy 数据 | `~/.bypy` |
| Web 客户端 | `~/下载/baidupcs-web` |
| 安装脚本 | `~/下载/baidu-netdisk-install.sh` |
| 使用文档 | `docs/baidu-netdisk-auto-setup.md` |

---

## ⚡ 快速开始

**授权后执行**：
```bash
# 查看网盘信息
bypy info

# 查看配额
bypy quota

# 列出文件
bypy list

# 创建工作目录
bypy mkdir /apps/taiyi
```

---

## 🔧 故障排查

### 授权失败
```bash
# 删除旧配置
rm ~/.bypy.json

# 重新授权
bypy info
```

### 网络问题
```bash
# 使用镜像源
export BYPY_MIRROR=ghproxy.com
```

---

*太一 AGI 自主配置 | 等待用户授权完成*
