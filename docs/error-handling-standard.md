# 错误处理与自愈系统规范

> 版本：v1.0 | 创建：2026-04-09  
> 状态：✅ 强制执行  
> 优先级：P0

---

## 🎯 核心原则

**原则 1: 写前检查**
```python
# ❌ 错误写法
with open("/path/to/file.txt", "w") as f:
    f.write(content)

# ✅ 正确写法
path = Path("/path/to/file.txt")
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "w") as f:
    f.write(content)
```

**原则 2: 绝对路径优先**
```python
# ❌ 错误写法 (相对路径)
config = json.load(open("config.json"))

# ✅ 正确写法 (绝对路径)
config_file = Path(__file__).parent / "config.json"
with open(config_file) as f:
    config = json.load(f)
```

**原则 3: 变量命名一致**
```python
# ❌ 错误写法 (大小写不一致)
Results = []
for result in results:  # NameError!
    pass

# ✅ 正确写法 (统一小写)
results = []
for result in results:
    pass
```

**原则 4: Git 操作前检查**
```python
# ✅ Git 操作前检查锁
git_lock = Path(".git/index.lock")
if git_lock.exists():
    git_lock.unlink()
# 然后执行 git 操作
```

**原则 5: 端口使用前检查**
```python
# ✅ 检查端口占用
import socket
def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# 使用前检查
if is_port_in_use(8080):
    # 清理或选择其他端口
    pass
```

---

## 🛡️ 错误处理装饰器

**所有新脚本必须使用**:
```python
from skills.error-handler.error_analyzer import error_handler

@error_handler
def main():
    # 主逻辑
    pass
```

---

## 📊 错误日志位置

| 日志类型 | 位置 |
|---------|------|
| 错误分析 | `logs/error_analysis.jsonl` |
| 指标数据 | `logs/error_metrics.json` |
| 处理日志 | `logs/error_handler.log` |

---

## 🔧 常见错误修复清单

### 1. 文件未找到

**症状**: `FileNotFoundError: [Errno 2] No such file or directory`

**修复**:
```bash
# 确保目录存在
mkdir -p /path/to/directory
```

**代码修复**:
```python
Path("/path/to/file").parent.mkdir(parents=True, exist_ok=True)
```

---

### 2. Git 锁冲突

**症状**: `fatal: .git/index.lock: File exists`

**修复**:
```bash
# 删除锁文件
rm .git/index.lock

# 或运行 gc
git gc --prune=now
```

---

### 3. 端口占用

**症状**: `OSError: [Errno 98] Address already in use`

**修复**:
```bash
# 查找占用进程
lsof -i :8080

# 清理进程
kill -9 <PID>

# 或等待端口释放
time.sleep(5)
```

---

### 4. 变量名错误

**症状**: `NameError: name 'Results' is not defined`

**修复**:
- 统一使用小写
- 使用 IDE 检查
- 运行前 lint 检查

---

### 5. 路径错误

**症状**: 相对路径导致文件找不到

**修复**:
```python
# 统一使用绝对路径
BASE_DIR = Path(__file__).parent.parent
config_file = BASE_DIR / "config" / "config.json"
```

---

## 📈 度量指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 重复错误率 | <10% | 待统计 |
| 自动修复率 | >80% | 待统计 |
| 平均修复时间 | <1 分钟 | 待统计 |

---

## ✅ 检查清单

**新脚本创建时**:
- [ ] 使用 `@error_handler` 装饰器
- [ ] 所有路径使用 `Path` 对象
- [ ] 写文件前创建目录
- [ ] 变量命名统一小写
- [ ] Git 操作前检查锁

**脚本执行失败时**:
- [ ] 查看错误日志
- [ ] 分析根因
- [ ] 应用自动修复
- [ ] 记录修复结果
- [ ] 更新预防措施

---

*创建：2026-04-09 21:30 | 太一 AGI · 错误处理规范*
