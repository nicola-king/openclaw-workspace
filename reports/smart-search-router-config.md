# 🔄 智能搜索路由配置

> **更新时间**: 2026-04-16 14:08  
> **版本**: v1.0

---

## 📋 路由规则

### 1. 国内内容搜索

**触发关键词**:
```
中国，国内，中文，大陆，内地，CN, china domestic
```

**路由配置**:
- search_engine: bing_cn
- endpoint: https://cn.bing.com
- proxy: false
- traffic: domestic

**流量类型**: 国内流量 (不走代理)

---

### 2. 国外内容搜索

**触发关键词**:
```
国外，国际，海外，US, global, international
```

**路由配置**:
- search_engine: chromium
- endpoint: https://www.google.com
- proxy: true
- traffic: proxy

**流量类型**: 代理流量 (走代理)

---

### 3. 默认搜索

**触发条件**: 未匹配到国内/国外关键词

**路由配置**:
- search_engine: bing_cn
- endpoint: https://cn.bing.com
- proxy: false
- traffic: domestic

**流量类型**: 国内流量 (默认)

---

## 🌐 流量配置

### 国内流量

- name: 国内流量
- proxy_enabled: false
- proxy_url: null
- dns: 114.114.114.114
- timeout: 10

### 代理流量

- name: 代理流量
- proxy_enabled: true
- proxy_url: http://127.0.0.1:7890
- dns: 8.8.8.8
- timeout: 30

---

## 📊 使用示例

### 国内搜索示例

查询："中国最新科技新闻"
结果:
- search_type: domestic_search
- search_engine: bing_cn
- proxy_enabled: false
- traffic_type: domestic

### 国外搜索示例

查询："US latest technology news"
结果:
- search_type: international_search
- search_engine: chromium
- proxy_enabled: true
- traffic_type: proxy

---

## 🚀 优势

### 智能切换
- ✅ 自动识别搜索类型
- ✅ 自动选择搜索引擎
- ✅ 自动切换流量类型

### 性能优化
- ✅ 国内搜索走国内流量 (快速)
- ✅ 国外搜索走代理流量 (可访问)
- ✅ 默认配置最优体验

### 灵活配置
- ✅ 关键词可自定义
- ✅ 代理配置可调整
- ✅ 搜索引擎可切换

---

*太一 AGI · 智能搜索路由 v1.0 · 2026-04-16 14:08*

**🔄 智能搜索路由配置完成！国内/国外自动切换！**
