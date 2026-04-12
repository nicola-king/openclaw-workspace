# 百度网盘集成指南

> 创建时间：2026-04-10 19:19  
> 版本：1.0.0  
> 状态：✅ 已集成

---

## 📦 集成内容

百度网盘已深度集成到太一系统中，提供以下功能：

### 1. 百度网盘管理 API

**端口**: 5003

**访问地址**:
- 本地：http://localhost:5003
- 局域网：http://192.168.3.74:5003

### 2. 管理界面

**访问地址**:
- http://localhost:5001/baidu (通过太一 Dashboard)
- http://localhost:5003 (直接访问 API)

---

## 🎯 功能列表

### 状态监控
- ✅ 客户端运行状态
- ✅ bypy 配置状态
- ✅ 网盘配额信息

### 文件操作
- ✅ 上传文件
- ✅ 下载文件
- ✅ 列出目录
- ✅ 创建目录
- ✅ 删除文件
- ✅ 搜索文件

### 自动化
- ✅ 工作区备份
- ✅ 从网盘同步
- ✅ 定时备份 (配置中)

---

## 📊 API 接口

### 获取状态
```
GET /api/baidu/status
```

**响应**:
```json
{
  "client_running": true,
  "bypy_configured": true,
  "quota": {
    "quota": "2.007TB",
    "used": "926GB"
  },
  "backup_dir": "/tmp/baidu-backup"
}
```

### 获取配额
```
GET /api/baidu/quota
```

### 列出文件
```
GET /api/baidu/list?path=/apps/taiyi
```

### 上传文件
```
POST /api/baidu/upload
Content-Type: application/json

{
  "local_path": "/path/to/local/file",
  "remote_path": "/apps/taiyi"
}
```

### 下载文件
```
POST /api/baidu/download
Content-Type: application/json

{
  "remote_path": "/apps/taiyi/file.txt",
  "local_path": "/path/to/save"
}
```

### 备份工作区
```
POST /api/baidu/backup
```

### 从网盘同步
```
POST /api/baidu/sync
```

### 搜索文件
```
GET /api/baidu/search?keyword=keyword
```

### 创建目录
```
POST /api/baidu/mkdir
Content-Type: application/json

{
  "path": "/apps/taiyi/newdir"
}
```

### 删除文件
```
POST /api/baidu/remove
Content-Type: application/json

{
  "path": "/apps/taiyi/file.txt"
}
```

---

## 🖥️ 管理界面功能

### 状态概览
- 客户端运行状态
- bypy 配置状态
- 网盘配额使用

### 快捷操作
- 💾 备份工作区
- 📥 从网盘同步
- 🔄 刷新状态
- 🌐 打开客户端

### 文件管理
- 文件列表浏览
- 文件搜索
- 文件下载
- 文件删除

### 操作日志
- 实时记录所有操作
- 时间戳显示
- 成功/失败状态

---

## 🔧 使用示例

### Python 调用

```python
import requests

# 获取状态
response = requests.get('http://localhost:5003/api/baidu/status')
status = response.json()
print(f"客户端：{'运行中' if status['client_running'] else '已停止'}")
print(f"配额：{status['quota']}")

# 备份工作区
response = requests.post('http://localhost:5003/api/baidu/backup', json={})
result = response.json()
print(f"备份完成：{result['backed_up']} 个文件")

# 列出文件
response = requests.get('http://localhost:5003/api/baidu/list?path=/apps/taiyi')
files = response.json()
print(f"文件列表：{files['files']}")
```

### cURL 调用

```bash
# 获取状态
curl http://localhost:5003/api/baidu/status

# 备份工作区
curl -X POST http://localhost:5003/api/baidu/backup \
  -H "Content-Type: application/json"

# 列出文件
curl "http://localhost:5003/api/baidu/list?path=/apps/taiyi"

# 上传文件
curl -X POST http://localhost:5003/api/baidu/upload \
  -H "Content-Type: application/json" \
  -d '{"local_path":"/path/to/file","remote_path":"/apps/taiyi"}'
```

---

## 📁 文件结构

```
baidu-netdisk-integration/
├── baidu_client.py         # 百度网盘客户端
├── app.py                  # Flask API 服务
├── templates/
│   └── baidu_manager.html  # 管理界面
└── INTEGRATION-GUIDE.md    # 本文档
```

---

## 🚀 启动方式

### 手动启动 API
```bash
cd /home/nicola/.openclaw/workspace/skills/baidu-netdisk-integration
python3 app.py
```

### 后台启动
```bash
cd /home/nicola/.openclaw/workspace/skills/baidu-netdisk-integration
nohup python3 app.py > /tmp/baidu-api.log 2>&1 &
```

### 通过太一 Dashboard 访问
1. 访问 http://localhost:5001
2. 点击 "百度网盘" 卡片
3. 或访问 http://localhost:5001/baidu

---

## ⚙️ 配置说明

### bypy 配置
位置：`~/.bypy.json`

如果未配置，需要运行：
```bash
bypy info
```
然后按提示完成授权。

### 备份目录
默认：`/tmp/baidu-backup`

可修改 `baidu_client.py` 中的 `backup_dir` 设置。

### 网盘路径
默认备份到：`/apps/taiyi/workspace/`

---

## 📋 使用场景

### 场景 1: 自动备份工作区
```python
# 每天凌晨 2 点自动备份
POST /api/baidu/backup
```

### 场景 2: 灾难恢复
```python
# 从网盘同步所有文件
POST /api/baidu/sync
```

### 场景 3: 文件共享
```python
# 上传文件到共享目录
POST /api/baidu/upload
{
  "local_path": "/path/to/report.pdf",
  "remote_path": "/apps/taiyi/shared"
}
```

### 场景 4: 文件搜索
```python
# 搜索特定文件
GET /api/baidu/search?keyword=report
```

---

## 🔗 相关服务

| 服务 | 地址 | 说明 |
|------|------|------|
| 太一 Dashboard | http://localhost:5001 | 综合总览 |
| 百度网盘 API | http://localhost:5003 | 管理 API |
| 百度网盘管理 | http://localhost:5001/baidu | 管理界面 |
| Bot Dashboard | http://localhost:3000 | Bot 状态 |
| Skill Dashboard | http://localhost:5002 | 技能管理 |

---

## 🐛 故障排查

### bypy 未配置
**症状**: `bypy_configured: false`

**解决**:
```bash
bypy info
# 按提示完成授权
```

### 客户端未运行
**症状**: `client_running: false`

**解决**:
```bash
# 通过桌面快捷方式启动
# 或运行 /opt/baidunetdisk/baidunetdisk
```

### API 无法访问
**症状**: 连接失败

**解决**:
```bash
# 检查服务是否运行
ps aux | grep baidu-netdisk

# 重启服务
pkill -f baidu-netdisk
python3 app.py
```

---

*太一 AGI | 2026-04-10 19:19*
