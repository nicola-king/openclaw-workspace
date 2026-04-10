# 百度网盘 Linux 客户端安装指南

> 创建时间：2026-04-10  
> 系统：Ubuntu 24.04 LTS

---

## 📦 安装方式

### 方式 1: 官方客户端 (推荐)

**步骤 1: 下载安装包**

访问百度网盘官网下载 Linux 版本：
```
https://pan.baidu.com/download
```

选择 **Linux 版本** (deb 格式)

**步骤 2: 保存到下载目录**

将下载的 `.deb` 文件保存到：
```
~/下载/BaiduNetdisk_linux_*.deb
```

**步骤 3: 自动安装**

运行安装脚本：
```bash
bash ~/下载/baidu-netdisk-install.sh
```

**或者手动安装**：
```bash
cd ~/下载
sudo dpkg -i BaiduNetdisk_linux_*.deb
sudo apt-get install -f -y
```

---

### 方式 2: 第三方客户端 (baidupcs-web)

**安装**：
```bash
# 从 GitHub 克隆
cd ~/下载
git clone https://github.com/PeterDing/baidupcs-web.git
cd baidupcs-web

# 安装依赖
npm install

# 启动
npm start
```

**访问**：
```
http://localhost:8080
```

---

### 方式 3: 命令行工具 (bypy)

**安装**：
```bash
pip3 install bypy --break-system-packages
```

**配置**：
```bash
bypy info
```

**使用**：
```bash
# 上传
bypy upload localfile remotefile

# 下载
bypy download remotefile localfile

# 列出文件
bypy list
```

---

## 🔐 登录绑定

### 官方客户端

1. 启动百度网盘：
   ```bash
   baidunetdisk
   ```
   或从应用程序菜单启动

2. 使用百度账号登录（扫码或账号密码）

3. 登录成功后，太一会自动检测并绑定

### 第三方客户端

1. 访问 http://localhost:8080

2. 扫码登录

3. 登录后即可使用

---

## 📁 文件位置

| 项目 | 路径 |
|------|------|
| 安装目录 | `/opt/baidunetdisk` |
| 配置文件 | `~/.config/baidunetdisk` |
| 下载目录 | `~/BaiduNetdiskDownload` |
| 缓存目录 | `~/.cache/baidunetdisk` |

---

## 🚀 启动方式

**图形界面**：
- 应用程序菜单 → 互联网 → 百度网盘
- 或搜索 "百度网盘"

**命令行**：
```bash
baidunetdisk
```

---

## ⚠️ 注意事项

1. **网络要求**: 需要稳定的网络连接
2. **账号安全**: 建议使用扫码登录
3. **存储空间**: 确保有足够的磁盘空间
4. **同步设置**: 可在设置中配置自动同步文件夹

---

## 🔧 故障排查

### 无法启动
```bash
# 检查安装
dpkg -l | grep baidunetdisk

# 修复依赖
sudo apt-get install -f -y

# 重新安装
sudo dpkg -i ~/下载/BaiduNetdisk_linux_*.deb
```

### 无法登录
- 检查网络连接
- 尝试扫码登录
- 清除缓存后重试

### 同步问题
- 检查文件夹权限
- 检查磁盘空间
- 重启客户端

---

*太一 AGI 协助配置*
