# 学习笔记：Cloudflare Worker 零成本代理池

> 学习时间：2026-04-06 01:09  
> 来源：Twitter @shachepi（刹车皮）/ @eternityspring（烁皓）  
> 项目：Cloudflare Worker + 域名搭建私人代理池  
> 成本：仅域名费用（~¥60/年）  
> 额度：每天 10 万次请求  
> 节点：全球 300+ 边缘节点

---

## 📊 核心数据

### Cloudflare Worker 免费额度
- **请求量**: 100,000 次/天
- **计算时间**: 10ms CPU 时间/请求
- **带宽**: 足够个人使用
- **节点**: 全球 300+ 边缘节点
- **IP 分布**: 几十个国家

### 成本结构
| 项目 | 费用 |
|------|------|
| Worker | ¥0（免费） |
| 域名 | ~¥60/年 |
| 服务器 | ¥0（无需） |
| 代理 IP | ¥0（使用 CF 节点 IP） |
| **总计** | **~¥60/年** |

### 性能对比
| 方案 | 成本 | 部署时间 | 维护成本 |
|------|------|---------|---------|
| **自建代理** | ¥500+/月 | 1 小时+ | 高 |
| **购买代理** | ¥200+/月 | 即买即用 | 低 |
| **CF Worker** | ¥5/月 | 10 分钟 | 极低 ✅ |

---

## 🏗️ 架构原理

```
用户请求
    ↓
Cloudflare Worker（边缘节点）
    ↓
目标网站（爬虫请求）
    ↓
返回数据
    ↓
用户接收
```

### 核心优势

1. **出口 IP 多样化**
   - 300+ 节点，每个节点 IP 不同
   - 自动轮换（无需手动配置）
   - 分布在几十个国家

2. **反爬虫绕过**
   - Cloudflare 域名信任度高
   - 请求看起来像正常用户
   - 适合反爬不强的场景

3. **零运维**
   - 无需服务器
   - 无需维护代理池
   - Cloudflare 自动扩缩容

---

## 💡 核心洞察

### 1. "稳如老狗"的免费服务

**刹车皮评价**：
> "大善人 Cloudflare 又是那种'稳如老狗'的免费服务"

**Cloudflare 免费层特点**：
- ✅ 额度充足（10 万请求/天）
- ✅ 稳定性高（上市公司）
- ✅ 不会突然收费/关停
- ✅ 全球 CDN 网络

**太一借鉴**：
- 太一可集成 CF Worker 作为代理方案
- 适合数据采集场景（气象/热点/新闻）
- 成本从¥200/月→¥5/月

### 2. 反爬不强但又要量的场景

**典型场景**：
- ✅ 社交媒体数据（微博/知乎/小红书）
- ✅ 新闻网站采集
- ✅ 公开 API 调用
- ❌ 强反爬网站（需要付费代理）

**太一当前**：
- 气象数据：Open-Meteo（免费 API，无需代理）
- 热点数据：模拟数据（待接入真实 API）
- 新闻数据：免费 API（无需代理）

**未来需求**：
- 🟡 可能需要代理的场景
- 🟡 批量数据采集
- 🟡 跨国数据获取

### 3. 10 分钟部署，域名是唯一成本

**部署流程**：
1. 注册 Cloudflare 账号（免费）
2. 购买域名（~¥60/年）
3. 创建 Worker（免费）
4. 绑定域名
5. 部署代理代码（10 分钟）

**代码示例**：
```javascript
// Worker 代理代码（~50 行）
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const target = url.searchParams.get('url');
    
    if (!target) {
      return new Response('Missing URL', { status: 400 });
    }
    
    // 转发请求到目标网站
    const response = await fetch(target);
    return response;
  }
};
```

---

## 🎯 太一应用方向

### 1. 数据采集代理增强（P2）

**当前**：
- 数据采集：直接调用 API
- 无代理需求

**未来**：
- 批量数据采集可能需要代理
- 跨国数据获取需要海外 IP
- 高频请求需要 IP 轮换

**CF Worker 方案**：
```python
# skills/cf-worker-proxy/SKILL.md
class CFWorkerProxy:
    def __init__(self, worker_url):
        self.worker_url = worker_url
    
    def fetch(self, target_url):
        """通过 CF Worker 代理获取数据"""
        proxy_url = f"{self.worker_url}?url={target_url}"
        response = requests.get(proxy_url)
        return response.text
```

**成本**：¥60/年（域名） vs ¥2,400/年（商业代理）

### 2. 全球化数据采集（P2）

**场景**：
- 采集海外社交媒体数据
- 跨国电商价格监控
- 全球新闻聚合

**CF Worker 优势**：
- 300+ 全球节点
- 自动选择最近节点
- IP 分布在几十个国家

**太一集成**：
```python
# 全球热点数据采集
def fetch_global_hot_topics():
    proxy = CFWorkerProxy('https://proxy.taiyi.works')
    
    # 美国热点
    us_topics = proxy.fetch('https://twitter.com/trending/US')
    
    # 日本热点
    jp_topics = proxy.fetch('https://twitter.com/trending/JP')
    
    return {'US': us_topics, 'JP': jp_topics}
```

### 3. 技能部署新方案（P1）

**当前**：
- 技能部署：本地运行
- 远程访问：需要公网 IP/内网穿透

**CF Worker 方案**：
- 技能 API 部署到 Worker
- 全球可访问
- 零成本（免费额度内）

**示例**：
```javascript
// Worker 部署太一技能 API
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const action = url.pathname;
    
    if (action === '/api/roi-tracker') {
      // 调用 ROI 追踪器
      const result = await runROITracker();
      return Response.json(result);
    }
    
    if (action === '/api/hot-topics') {
      // 调用热点选题生成器
      const result = await generateHotTopics();
      return Response.json(result);
    }
  }
};
```

**优势**：
- 无需服务器
- 全球 CDN 加速
- 自动扩缩容
- 成本≈0

---

## 📋 立即行动（宪法：不过夜）

### ✅ 已完成
- [x] 学习笔记创建
- [x] 核心洞察提炼
- [x] 太一应用方向

### 🟡 进行中
- [ ] 更新 HEARTBEAT.md
- [ ] 更新记忆日志

### 🔴 待执行
- [ ] CF Worker 代理 Skill 开发（P2）
- [ ] 技能 API Worker 部署方案（P1）
- [ ] 全球化数据采集测试（P2）

---

## 📊 与太一对比

| 维度 | CF Worker 代理 | 太一当前 |
|------|---------------|---------|
| **代理方案** | CF Worker（¥60/年） | 无代理需求 |
| **部署方式** | Worker（零成本） | 本地运行 |
| **全球访问** | 300+ 节点 CDN | 本地访问 |
| **维护成本** | 极低 | 低 |
| **扩展性** | 自动扩缩容 | 手动扩展 |

**太一可借鉴**：
- ✅ 零成本部署方案
- ✅ 全球化访问能力
- ✅ 自动扩缩容

---

## 🚀 执行计划

### 本周（P1）
- [ ] 研究 CF Worker 部署技能 API
- [ ] 测试 Worker 代理方案
- [ ] 评估成本/收益

### 下周（P2）
- [ ] CF Worker Proxy Skill 开发
- [ ] 全球数据采集测试
- [ ] 文档完善

### 本月（P3）
- [ ] 技能 API  Worker 部署
- [ ] 全球化版本发布
- [ ] 性能优化

---

## 💭 核心反思

### 1. 免费资源的价值

**Cloudflare**：
- 免费层：10 万请求/天
- 稳定性：上市公司背书
- 全球网络：300+ 节点

**太一借鉴**：
- 充分利用免费资源
- 降低成本（¥2,400/年→¥60/年）
- 提高可靠性（CDN 加速）

### 2. 轻量级方案优势

**传统代理**：
- 自建服务器：¥500/月
- 维护成本：高
- 扩展性：手动

**CF Worker**：
- 域名：¥5/月
- 维护成本：极低
- 扩展性：自动

**启示**：
- 优先选择轻量级方案
- 充分利用云服务免费层
- 降低运维负担

### 3. 全球化思维

**CF Worker**：
- 300+ 全球节点
- 自动路由到最近节点
- IP 分布在几十个国家

**太一目标**：
- 技能全球化部署
- 数据采集全球化
- 用户全球化（出海战略）

---

*学习笔记：太一 AGI · 2026-04-06 01:10*  
*状态：✅ 学习完成，执行中（不过夜！）*
