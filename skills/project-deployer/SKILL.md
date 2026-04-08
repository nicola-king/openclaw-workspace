---
name: project-deployer
version: 1.0.0
description: 自动化部署项目到 Railway/Vercel 等平台
category: auto-generated
tags: ['部署', 'Railway', 'Vercel', '自动化']
author: 太一 AGI (Auto-Generated)
created: 2026-04-09
---

# Project Deployer Skill

> 版本：v1.0 | 创建：2026-04-09 | 优先级：P2  
> 来源：从 3+ 次部署任务中自动提取

---

## 🎯 职责

自动化部署项目，包括：
- 准备部署文件
- 配置云平台项目
- 设置环境变量
- 推送代码
- 监控部署状态
- 测试访问

---

## 🔍 触发条件

- 用户提及：部署
- 用户提及：发布到 Railway
- 用户提及：发布到 Vercel
- 用户提及：上线

---

## 🛠️ 执行流程

1. **准备部署**
   - 检查项目结构
   - 准备 Dockerfile/railway.toml
   - 配置环境变量

2. **创建项目**
   - 登录云平台 CLI
   - 创建新项目（如不存在）
   - 关联 Git 仓库

3. **配置环境**
   - 设置环境变量
   - 配置构建命令
   - 配置启动命令

4. **推送部署**
   - git push 触发部署
   - 或 railway up / vercel deploy

5. **监控状态**
   - 等待部署完成
   - 检查部署日志
   - 验证部署成功

6. **测试访问**
   - 获取部署 URL
   - web_fetch 测试访问
   - 返回结果

---

## 📁 相关文件

- `railway.toml` - Railway 配置
- `vercel.json` - Vercel 配置
- `Dockerfile` - Docker 配置
- `.env` - 环境变量

---

## 📋 使用示例

```
# 示例 1: Railway 部署
太一，部署 Dashboard 到 Railway

# 示例 2: Vercel 部署
太一，部署前端到 Vercel

# 示例 3: 指定环境
太一，部署到生产环境
```

---

## 🔧 配置选项

```json
{
  "deployment": {
    "platform": "railway",
    "region": "asia-east1",
    "auto_ssl": true,
    "custom_domain": false
  }
}
```

---

## ✅ 质量检查

- [x] 命名规范检查
- [x] 元数据完整检查
- [x] 触发条件清晰检查
- [x] 步骤可执行检查
- [x] 无硬编码检查
- [x] 有使用示例检查
- [ ] 有错误处理检查

---

## 🚨 错误处理

| 错误 | 处理方式 |
|------|----------|
| 登录失败 | 提示用户重新登录 |
| 部署失败 | 查看日志，重试 1 次 |
| 域名冲突 | 生成随机子域名 |

---

*本技能由太一自动生成，经 SAYELF 确认后激活。*
