// 网络请求封装

const config = require('./config');

/**
 * 请求封装
 */
function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      timeout: options.timeout || 10000,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          wx.showToast({
            title: `请求失败：${res.statusCode}`,
            icon: 'none'
          });
          reject(res);
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误，请重试',
          icon: 'none'
        });
        reject(err);
      }
    });
  });
}

/**
 * GET 请求
 */
function get(url, data) {
  return request({ url, method: 'GET', data });
}

/**
 * POST 请求
 */
function post(url, data) {
  return request({ url, method: 'POST', data });
}

/**
 * 分析用户输入
 */
async function analyzeUserInput(userInput, testType = 'quick') {
  try {
    wx.showLoading({ title: '分析中...' });
    
    const result = await post(config.ENDPOINTS.ANALYZE, {
      user_input: userInput,
      test_type: testType
    });
    
    wx.hideLoading();
    return result;
  } catch (error) {
    wx.hideLoading();
    throw error;
  }
}

/**
 * 获取 Skill 预览
 */
async function getSkillPreview(skillId) {
  return get(`${config.ENDPOINTS.SKILL_PREVIEW}/${skillId}`);
}

/**
 * 解锁 Skill (付费)
 */
async function unlockSkill(skillId, paymentToken) {
  return post(`${config.ENDPOINTS.SKILL_UNLOCK}/${skillId}/unlock`, {
    skill_id: skillId,
    payment_token: paymentToken
  });
}

/**
 * 创建支付订单
 */
async function createOrder(itemType, itemId, amount) {
  return post(config.ENDPOINTS.CREATE_ORDER, {
    item_type: itemType,
    item_id: itemId,
    amount: amount
  });
}

/**
 * 发起微信支付
 */
function requestPayment(order) {
  return new Promise((resolve, reject) => {
    wx.requestPayment({
      timeStamp: order.timeStamp,
      nonceStr: order.nonceStr,
      package: order.package,
      signType: 'RSA',
      paySign: order.paySign,
      success: resolve,
      fail: reject
    });
  });
}

module.exports = {
  request,
  get,
  post,
  analyzeUserInput,
  getSkillPreview,
  unlockSkill,
  createOrder,
  requestPayment
};
