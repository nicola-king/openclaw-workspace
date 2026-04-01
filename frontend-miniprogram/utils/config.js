// 配置文件

const API_BASE_URL = 'https://api.sayelf.com'; // 生产环境
// const API_BASE_URL = 'http://localhost:8000'; // 测试环境

module.exports = {
  API_BASE_URL,
  
  ENDPOINTS: {
    // 分析接口
    ANALYZE: `${API_BASE_URL}/api/v1/analyze`,
    
    // Skills
    SKILL_PREVIEW: `${API_BASE_URL}/api/v1/skills`,
    SKILL_UNLOCK: `${API_BASE_URL}/api/v1/skills`,
    
    // 状态列表
    STATES: `${API_BASE_URL}/api/v1/states`,
    STAGES: `${API_BASE_URL}/api/v1/states`,
    
    // 支付
    CREATE_ORDER: `${API_BASE_URL}/api/v1/orders/create`,
    VERIFY_PAYMENT: `${API_BASE_URL}/api/v1/orders/verify`,
    
    // 用户
    USER_PROFILE: `${API_BASE_URL}/api/v1/user/profile`,
    USER_TRAJECTORY: `${API_BASE_URL}/api/v1/user/trajectory`,
    
    // 健康检查
    HEALTH: `${API_BASE_URL}/health`
  },
  
  // 价格配置
  PRICING: {
    STAGE_UNLOCK: 1.0,
    SKILL_UNLOCK: 9.9,
    MEMBERSHIP_MONTHLY: 19.0
  },
  
  // 测试配置
  TEST_CONFIG: {
    QUICK: { questions: 3, duration: 30 },
    STANDARD: { questions: 12, duration: 120 },
    DEEP: { questions: 36, duration: 300 }
  }
};
