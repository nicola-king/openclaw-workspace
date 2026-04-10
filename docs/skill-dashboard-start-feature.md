# ✅ 太一 Skill 管理中心 - 启动功能已实现

> 实现时间：2026-04-10 17:39  
> 状态：✅ 已就绪

---

## 🎯 功能说明

现在在 **太一 Skill 管理中心** (http://localhost:5002) 中：

### 点击"启动"按钮

1. **自动查找可执行文件**
   - 优先级：main.py > app.py > server.py > run.py > index.py 等
   - 支持 Shell 脚本：run.sh, start.sh

2. **自动检测端口**
   - 从代码中解析 `port = XXXX` 配置
   - 默认端口映射：5000, 3000, 8080, 8000

3. **启动应用进程**
   - 后台运行
   - 日志记录到 `/tmp/skill-{skill_id}.log`
   - 进程信息保存到 `/tmp/skill-dashboard-processes.json`

### 点击"打开"按钮

- 在新标签页打开应用 URL
- 格式：`http://localhost:{port}`

### 点击"日志"按钮

- 查看应用运行日志
- 实时刷新
- 最多显示 200 行

### 点击"状态"按钮

- 查看 PID、端口、启动时间
- 检查运行状态

---

## 📋 支持的 Skill 类型

| 文件 | 优先级 | 说明 |
|------|--------|------|
| `main.py` | 1 | 主程序入口 |
| `app.py` | 2 | Flask/FastAPI 应用 |
| `server.py` | 3 | 服务器程序 |
| `run.py` | 4 | 运行脚本 |
| `index.py` | 5 | 索引程序 |
| `dashboard.py` | 6 | 仪表盘应用 |
| `web.py` | 7 | Web 应用 |
| `api.py` | 8 | API 服务 |
| `run.sh` | 9 | Shell 启动脚本 |

---

## 🔧 API 接口

### 启动应用
```
POST /api/skills/{skill_id}/start
```

**响应**：
```json
{
  "status": "started",
  "pid": 12345,
  "script": "app.py",
  "port": 5000,
  "url": "http://localhost:5000"
}
```

### 停止应用
```
POST /api/skills/{skill_id}/stop
```

### 获取状态
```
GET /api/skills/{skill_id}/status
```

**响应**：
```json
{
  "running": true,
  "pid": 12345,
  "port": 5000,
  "started_at": "2026-04-10T17:39:00",
  "url": "http://localhost:5000"
}
```

### 查看日志
```
GET /api/skills/{skill_id}/logs?lines=100
```

### 打开应用
```
POST /api/skills/{skill_id}/open
```

### 获取所有运行中的应用
```
GET /api/system/processes
```

---

## 📁 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 进程管理器 | `skills/skill-dashboard/api/process_manager.py` | 核心逻辑 |
| 后端 API | `skills/skill-dashboard/app.py` | Flask 应用 |
| 前端界面 | `skills/skill-dashboard/templates/index.html` | Web 界面 |
| 进程信息 | `/tmp/skill-dashboard-processes.json` | 运行状态 |
| 应用日志 | `/tmp/skill-{skill_id}.log` | 日志文件 |

---

## 🚀 使用示例

### 1. 访问 Skill 管理中心

打开浏览器：
```
http://localhost:5002
```

### 2. 查找 Skill

- 使用搜索框
- 浏览技能列表

### 3. 启动应用

点击 **"▶️ 启动"** 按钮

### 4. 打开应用

启动成功后，点击 **"🌐 打开"** 按钮

### 5. 查看日志

点击 **"📋 日志"** 按钮查看运行日志

---

## ⚠️ 注意事项

1. **Skill 需要有可执行文件**
   - main.py, app.py, server.py 等
   - 纯技能库（无应用）无法启动

2. **端口不能冲突**
   - 确保端口未被占用
   - 系统会自动检测

3. **日志查看**
   - 启动失败时查看日志
   - 日志文件：`/tmp/skill-{skill_id}.log`

4. **停止应用**
   - 会终止整个进程组
   - 清理进程记录

---

## 🐛 故障排查

### 启动失败

**错误**: "未找到可执行文件"
- **原因**: Skill 没有 main.py/app.py 等文件
- **解决**: 添加可执行文件或跳过该 Skill

**错误**: "端口被占用"
- **原因**: 端口已被其他应用使用
- **解决**: 修改 Skill 的端口配置

**错误**: "ImportError"
- **原因**: Python 导入问题
- **解决**: 修复 Skill 代码

### 无法打开浏览器

**检查**:
1. 应用是否运行中
2. 端口是否正确
3. URL 是否可访问

### 日志为空

**可能原因**:
- 应用未输出日志
- 启动失败
- 权限问题

---

## 📖 相关文档

- `docs/skill-dashboard-start-guide.md` - 使用指南
- `skills/skill-dashboard/README.md` - Skill Dashboard 说明
- `skills/skill-dashboard/api/process_manager.py` - 进程管理器代码

---

*太一 AGI 自主实现 | 2026-04-10 17:39*
