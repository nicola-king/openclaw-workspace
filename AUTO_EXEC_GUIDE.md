# 🚀 自动执行指南

> **创建时间**: 2026-04-11 11:45  
> **状态**: 脚本已就绪，需手动执行一次 sudo

---

## ⚠️ 为什么需要手动执行？

以下操作需要 sudo 权限，无法自动执行：
1. 安装系统依赖 (mdb-tools, libchm-bin)
2. GitHub CLI 认证

---

## 🎯 一键执行 (推荐)

**复制并运行以下命令**:

```bash
bash /home/nicola/.openclaw/workspace/skills/cost-agent/AUTO_INSTALL_AND_PUSH.sh
```

**或者分步执行**:

```bash
# 1. 安装依赖
sudo apt-get update && sudo apt-get install -y mdb-tools libchm-bin

# 2. 安装 Python 库
pip install python-chm --break-system-packages -q

# 3. 转换 Access 和 CHM
cd /home/nicola/.openclaw/workspace/skills/cost-agent
python3 scripts/convert_mdb_python.py
python3 scripts/convert_chm_python.py

# 4. GitHub 认证
gh auth login

# 5. 推送 Cost.Agent
cd /home/nicola/.openclaw/workspace/skills/cost-agent
gh repo create nicola-king/cost-agent --public --source=. --push

# 6. 推送太一记忆宫殿
cd /home/nicola/.openclaw/workspace/skills/taiyi-memory-palace
gh repo create nicola-king/taiyi-memory-palace --public --source=. --push
```

---

## ⏱️ 预计时间

- 安装依赖：2 分钟
- 转换文件：5 分钟
- GitHub 推送：3 分钟
- **总计：10 分钟**

---

## ✅ 执行后效果

**完成内容**:
- ✅ Access 数据库转换 (4 个.mdb)
- ✅ CHM 文件转换 (5 个.chm)
- ✅ Cost.Agent GitHub 仓库
- ✅ 太一记忆宫殿 GitHub 仓库

**进度**: 90% → **100%** 🟢

---

## 📊 仓库链接

执行后可访问:
- Cost.Agent: https://github.com/nicola-king/cost-agent
- Taiyi Memory Palace: https://github.com/nicola-king/taiyi-memory-palace

---

**太一 AGI · 2026-04-11**

**等待用户执行 sudo 命令后即可 100% 完成！**
