# npm 发布安全检查清单

> 创建时间：2026-03-31 22:05
> 触发事件：Claude Code 源码泄露 (512K 行代码通过 .map 文件暴露)

---

## 🚨 风险等级

| 项目 | 风险等级 | 状态 |
|------|---------|------|
| 太一 workspace | ✅ 安全 | private: true |
| .npmignore | ✅ 已配置 | 523 bytes |
| .map 文件 | ⚠️ 依赖包有 | 5412 个 (viem/ethers) |

---

## ✅ 已执行检查

### 1. package.json 配置
```json
{
  "private": true
}
```
**状态**: ✅ 已设置，防止意外发布

### 2. .npmignore 配置
**忽略内容**:
- `*.map` - Source maps
- `.env*` - 环境变量
- `.git/` - 版本历史
- `tests/` - 测试文件
- `*.log` - 日志文件
- `node_modules/` - 依赖
- `docs/` - 文档

**状态**: ✅ 已创建 (523 bytes)

### 3. 发布前验证命令
```bash
# 检查是否会包含 .map 文件
npm pack --dry-run | grep "\.map$"

# 检查完整文件列表
npm pack --dry-run
```

**状态**: ✅ 验证通过 (private: true 阻止发布)

---

## 📋 未来发布检查清单

**发布任何 npm 包前必须执行**:

```bash
# 1. 检查 .map 文件
find . -name "*.map" -type f

# 2. 检查 .env 文件
find . -name ".env*" -type f

# 3.  dry-run 验证
npm pack --dry-run

# 4. 人工审查文件列表
npm pack --dry-run | grep -v "^npm notice"

# 5. 检查敏感信息
grep -r "API_KEY\|SECRET\|TOKEN" --include="*.ts" --include="*.js" src/
```

---

## 🔍 依赖包 .map 文件处理

**当前状态**: 5412 个 .map 文件 (来自 viem/ethers 等依赖)

**风险评估**:
- ✅ 本地使用：无风险
- ✅ 不发布：无风险
- ⚠️ 如发布项目：需删除 node_modules

**建议**: 
- 保持 node_modules 在 .gitignore 中
- 发布时只发布源码，用户自行安装依赖
- 或使用 `npm publish --ignore-scripts`

---

## 📚 参考事件

**Claude Code 源码泄露 (2026-03-31)**:
- 原因：npm 包未删除 .map 文件
- 规模：1900 文件，512K 行代码
- 影响：完整业务逻辑暴露

**教训**: 发布前必须检查 .map 文件！

---

*创建时间：2026-03-31 22:05*
*状态：✅ 安全检查完成*
*下次检查：发布任何 npm 包前*
