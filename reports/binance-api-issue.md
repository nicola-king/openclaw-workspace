# ⚠️ 币安 API 权限问题诊断

**时间**: 2026-03-30 22:30  
**状态**: 公开 API ✅ / 私有 API ❌

---

## 问题现象

```
公开 API: ✅ ETH 价格 $2053.16
私有 API: ❌ 401 - Invalid API-key, IP, or permissions for action
```

---

## 可能原因

### 1. IP 白名单未配置
- 当前公网 IP: `103.172.182.26`
- 币安 API Key 需要添加此 IP 到白名单

### 2. 权限未启用
需要检查币安 API Key 权限：
- ✅ Enable Reading
- ✅ Spot & Margin Trading
- ❓ IP Whitelist

### 3. API Key 失效
- Key 可能已过期或被撤销
- 需要重新生成

---

## 解决方案

### 方案 1: 添加 IP 白名单 (推荐)
1. 登录币安：https://www.binance.com
2. API 管理 → 找到当前 Key
3. 编辑 IP 白名单 → 添加 `103.172.182.26`
4. 保存

### 方案 2: 重新生成 API Key
1. 删除旧 Key
2. 创建新 Key
3. 启用权限：Reading + Spot Trading
4. 添加 IP 白名单
5. 更新配置文件

---

## 配置文件位置

`/home/nicola/.openclaw/workspace/config/binance-config.json`

---

## 下一步

- [ ] SAYELF 确认币安 API Key 状态
- [ ] 添加 IP 白名单或重新生成 Key
- [ ] 更新配置文件
- [ ] 重新测试私有 API

---

*诊断：太一 AGI | 2026-03-30 22:30*
