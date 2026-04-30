# 🌳 太一进化树可视化

> 一个人的代码，变成全世界的进化树

---

## 🚀 快速开始

### 方式 1: 本地运行

```bash
# 进入目录
cd evolution-tree

# 用浏览器打开
open index.html

# 或者用 Python 启动服务器
python3 -m http.server 8000

# 访问 http://localhost:8000
```

### 方式 2: GitHub Pages

```bash
# 推送到 GitHub
git add evolution-tree
git commit -m "feat: 添加进化树可视化"
git push origin main

# 启用 GitHub Pages
# Settings → Pages → Source → main branch → /evolution-tree
```

### 方式 3: Vercel/Netlify 部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
vercel

# 按照提示操作
```

---

## 📁 文件结构

```
evolution-tree/
├── index.html          # 主页面
├── data.js            # 数据文件
├── tree.js            # 树形可视化逻辑
├── app.js             # 应用主逻辑
├── README.md          # 本文档
└── screenshots/       # 截图（待添加）
```

---

## 🎨 功能特性

### 1. 进化树可视化

- 🌳 D3.js 树形图
- 🎨 渐变色彩
- ✨ 交互动画
- 📱 响应式设计

### 2. 实时统计

- 🤖 Agent 数量
- 📚 技能数量
- 👥 贡献者数量
- 💾 提交次数

### 3. 进化时间线

- ⏰ 最近事件
- 📝 事件类型
- 👤 创建者信息
- 🔗 Commit 链接

### 4. 贡献者墙

- 🖼️ 头像展示
- 📊 贡献统计
- 🏆 角色标识
- 📈 成长路径

---

## 🔧 自定义配置

### 修改数据

编辑 `data.js` 文件：

```javascript
const TAIYI_DATA = {
    tree: {
        root: { ... },
        branches: [ ... ]
    },
    contributors: [ ... ],
    events: [ ... ],
    statistics: { ... }
};
```

### 修改样式

编辑 `index.html` 中的 `<style>` 部分。

### 修改逻辑

编辑 `tree.js` 或 `app.js`。

---

## 📊 数据源

### GitHub API

```javascript
// 获取仓库信息
fetch('https://api.github.com/repos/nicola-king/taiyi-agents')
    .then(response => response.json())
    .then(data => {
        // stars, forks, contributors 等
    });
```

### 本地数据

数据存储在 `data.js` 中，可以手动更新或自动同步。

---

## 🚧 待开发功能

### 第 1 阶段（本周）

- [ ] 基本树形可视化 ✅
- [ ] 统计数据展示 ✅
- [ ] 进化时间线 ✅
- [ ] 贡献者墙 ✅
- [ ] 响应式设计 ✅

### 第 2 阶段（下周）

- [ ] GitHub API 自动同步
- [ ] 实时数据更新
- [ ] 搜索功能
- [ ] 过滤功能
- [ ] 导出功能

### 第 3 阶段（本月）

- [ ] 3D 可视化
- [ ] VR/AR 支持
- [ ] 社交分享
- [ ] 评论系统
- [ ] 成就系统

---

## 🎯 成功指标

| 指标 | 目标 | 当前 |
|------|------|------|
| **页面访问** | ≥1,000/月 | 0 |
| **停留时间** | ≥3 分钟 | - |
| **分享次数** | ≥100/月 | 0 |
| **贡献转化** | ≥10% | - |
| **用户满意度** | ≥4.5/5.0 | - |

---

## 🤝 贡献指南

### 报告 Bug

在 GitHub Issues 中创建 Issue，标签为 `bug`。

### 提出新功能

在 GitHub Issues 中创建 Issue，标签为 `enhancement`。

### 提交代码

1. Fork 项目
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 许可证

MIT License - 查看主项目 LICENSE 文件

---

## 🙏 致谢

- **D3.js** - 数据可视化库
- **TailwindCSS** - CSS 框架
- **Karpathy** - 开源哲学启发
- **太一社区** - 所有贡献者

---

## 📞 联系方式

- **GitHub**: https://github.com/nicola-king/taiyi-agents
- **Email**: taiyi@openclaw.ai
- **Telegram**: @taiyi_bot
- **微信**: 太一 AGI

---

*太一进化树可视化 · v1.0 · 2026-04-17*
