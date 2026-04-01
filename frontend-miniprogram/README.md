# 情景模式小程序前端框架

> 创建：2026-03-31 11:59  
> 平台：微信小程序  
> 状态：🟡 框架设计中

---

## 🎯 产品定位

**名称**: 心景 · MindScape  
**Slogan**: "看清你正在经历什么"

---

## 📱 核心页面

### 1. 首页 (pages/index/index)

```
┌─────────────────────────────┐
│     心景 · MindScape        │
│  "看清你正在经历什么"        │
├─────────────────────────────┤
│                             │
│   ┌─────────────────┐       │
│   │  🧪 情景测试    │       │
│   │  30 秒快速版    │       │
│   └─────────────────┘       │
│                             │
│   ┌─────────────────┐       │
│   │  📖 64 情景库    │       │
│   │  浏览所有情景   │       │
│   └─────────────────┘       │
│                             │
│   ┌─────────────────┐       │
│   │  📊 我的轨迹    │       │
│   │  情景变化记录   │       │
│   └─────────────────┘       │
│                             │
└─────────────────────────────┘
```

### 2. 测试页 (pages/test/test)

```
快速测试 (3 题):

Q1: 你最近的状态更接近？
○ A. 努力但没有回报
○ B. 进展顺利但有波动
○ C. 感到迷茫不知道方向
○ D. 疲惫想停下来休息

Q2: 你当前的主要困扰是？
○ A. 外部阻力 (人际关系/资源不足)
○ B. 内部困惑 (方向/方法/信心)
○ C. 时机问题 (太早/太晚/等待)
○ D. 决策压力 (需要选择/害怕选错)

Q3: 你希望得到什么帮助？
○ A. 具体行动建议
○ B. 心理层面的理解
○ C. 趋势和方向判断
○ D. 情绪支持和鼓励
```

### 3. 结果页 (pages/result/result)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【情景名称】积累未显期
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 你当前的位置
情景类型：调整型
阶段进度：Step 3/6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 最优动作：停止当前，重新评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆓 免费内容:
✓ 状态识别
✓ 阶段判断

💰 付费解锁:
¥1   - 阶段详细解读
¥9.9 - 完整行动方案
¥19  - 会员 (384 Skills 无限访问)

[立即解锁 ¥9.9] [开通会员 ¥19]
```

---

## 🔌 API 集成

### 基础配置

```javascript
// utils/config.js
const API_BASE_URL = 'https://api.sayelf.com'; // 或本地测试 http://localhost:8000

module.exports = {
  API_BASE_URL,
  ENDPOINTS: {
    ANALYZE: `${API_BASE_URL}/api/v1/analyze`,
    SKILL_PREVIEW: `${API_BASE_URL}/api/v1/skills/`,
    SKILL_UNLOCK: `${API_BASE_URL}/api/v1/skills/`,
    STATES: `${API_BASE_URL}/api/v1/states`,
  }
}
```

### 请求封装

```javascript
// utils/request.js
const config = require('./config');

function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(res);
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}

module.exports = {
  request,
  get: (url, data) => request({ url, method: 'GET', data }),
  post: (url, data) => request({ url, method: 'POST', data }),
};
```

### 分析接口调用

```javascript
// pages/test/test.js
const request = require('../../utils/request');
const config = require('../../utils/config');

Page({
  data: {
    questions: [
      {
        id: 1,
        content: "你最近的状态更接近？",
        options: [
          { label: "A", text: "努力但没有回报" },
          { label: "B", text: "进展顺利但有波动" },
          { label: "C", text: "感到迷茫不知道方向" },
          { label: "D", text: "疲惫想停下来休息" }
        ]
      },
      // ... 更多题目
    ],
    answers: [],
    result: null
  },

  // 提交测试
  async submitTest() {
    try {
      const userInput = this.buildUserInput();
      
      const result = await request.post(config.ENDPOINTS.ANALYZE, {
        user_input: userInput,
        test_type: "quick"
      });
      
      this.setData({ result });
      
      // 跳转到结果页
      wx.navigateTo({
        url: `/pages/result/result?data=${JSON.stringify(result)}`
      });
      
    } catch (error) {
      wx.showToast({
        title: '分析失败，请重试',
        icon: 'none'
      });
    }
  },

  buildUserInput() {
    // 根据答案构建用户输入文本
    const answerTexts = {
      A: "努力但没有回报",
      B: "进展顺利但有波动",
      C: "感到迷茫不知道方向",
      D: "疲惫想停下来休息"
    };
    
    return this.data.answers
      .map(a => answerTexts[a])
      .join(" ");
  }
});
```

---

## 💰 支付集成

### 微信支付流程

```javascript
// pages/result/result.js
const request = require('../../utils/request');

Page({
  // 解锁 Skill
  async unlockSkill(skillId) {
    try {
      // Step 1: 创建支付订单
      const order = await request.post(`/api/v1/orders/create`, {
        item_type: "skill",
        item_id: skillId,
        amount: 9.9
      });
      
      // Step 2: 调起微信支付
      wx.requestPayment({
        timeStamp: order.timeStamp,
        nonceStr: order.nonceStr,
        package: order.package,
        signType: 'RSA',
        paySign: order.paySign,
        success: async (res) => {
          // Step 3: 支付成功，解锁 Skill
          const skill = await request.post(
            `/api/v1/skills/${skillId}/unlock`,
            { payment_token: order.payment_token }
          );
          
          // Step 4: 显示完整内容
          this.showFullSkill(skill);
          
          wx.showToast({
            title: '解锁成功',
            icon: 'success'
          });
        },
        fail: (err) => {
          wx.showToast({
            title: '支付取消',
            icon: 'none'
          });
        }
      });
      
    } catch (error) {
      wx.showToast({
        title: '解锁失败',
        icon: 'none'
      });
    }
  }
});
```

---

## 📊 数据追踪

### 用户轨迹记录

```javascript
// 记录用户测试历史
function trackTest(userId, result) {
  wx.request({
    url: `${config.API_BASE_URL}/api/v1/track/test`,
    method: 'POST',
    data: {
      user_id: userId,
      state_id: result.state.id,
      stage: result.stage.step,
      confidence: result.confidence,
      timestamp: new Date().toISOString()
    }
  });
}
```

---

## 🎨 UI 组件

使用 Vant Weapp 组件库：

```bash
# 安装
npm i @vant/weapp -S --production
```

```json
// app.json
{
  "usingComponents": {
    "van-button": "@vant/weapp/button/index",
    "van-cell": "@vant/weapp/cell/index",
    "van-dialog": "@vant/weapp/dialog/index",
    "van-toast": "@vant/weapp/toast/index"
  }
}
```

---

## 📁 项目结构

```
frontend-miniprogram/
├── app.js                 # 小程序入口
├── app.json               # 小程序配置
├── app.wxss               # 全局样式
├── pages/
│   ├── index/             # 首页
│   ├── test/              # 测试页
│   ├── result/            # 结果页
│   ├── skill-detail/      # Skill 详情
│   └── profile/           # 个人中心
├── components/            # 自定义组件
├── utils/                 # 工具函数
│   ├── config.js
│   ├── request.js
│   └── auth.js
└── images/                # 图片资源
```

---

## 🚀 开发计划

### Phase 1 (MVP - 3 天)
- [ ] 首页框架
- [ ] 测试页 (3 题快速版)
- [ ] 结果页 (免费层)
- [ ] API 集成

### Phase 2 (5 天)
- [ ] 支付集成
- [ ] Skill 详情页
- [ ] 64 情景库浏览
- [ ] 用户轨迹记录

### Phase 3 (7 天)
- [ ] 会员中心
- [ ] 分享功能
- [ ] 内测部署
- [ ] 50 人测试

---

*创建：2026-03-31 11:59 | 太一 AGI · 情景模式系统*
*状态：🟡 框架设计中 | 版本：v1.0*
