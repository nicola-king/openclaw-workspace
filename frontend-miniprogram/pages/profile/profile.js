// pages/profile/profile.js
const app = getApp();
const request = require('../../utils/request');

Page({
  data: {
    userInfo: null,
    isMember: false,
    memberExpire: null,
    testCount: 0,
    unlockedCount: 0,
    favoriteCount: 0
  },

  onLoad() {
    this.loadUserInfo();
    this.loadStats();
  },

  onShow() {
    // 每次显示时刷新数据
    this.loadStats();
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = app.globalData.userInfo;
    this.setData({ userInfo });
  },

  // 加载统计数据
  async loadStats() {
    try {
      // TODO: 从 API 加载真实数据
      // 这里使用模拟数据
      this.setData({
        testCount: 12,
        unlockedCount: 5,
        favoriteCount: 3,
        isMember: false,
        memberExpire: null
      });
    } catch (error) {
      console.error('加载统计失败:', error);
    }
  },

  // 升级会员
  upgradeMember() {
    wx.showModal({
      title: '开通会员',
      content: '¥19/月\n\n• 384 Skills 无限访问\n• 用户轨迹追踪\n• 专属心理学解读\n• 优先新功能体验',
      confirmText: '立即开通',
      confirmColor: '#667eea',
      success: async (res) => {
        if (res.confirm) {
          try {
            // 创建订单
            const order = await request.createOrder('membership', 'monthly', 19.0);
            
            // 发起支付
            await request.requestPayment(order);
            
            // 支付成功
            wx.showToast({
              title: '开通成功',
              icon: 'success'
            });
            
            // 刷新数据
            this.setData({
              isMember: true,
              memberExpire: '2026-04-30'
            });
            
          } catch (error) {
            if (error.errMsg !== 'requestPayment:fail cancel') {
              wx.showToast({
                title: '开通失败',
                icon: 'none'
              });
            }
          }
        }
      }
    });
  },

  // 查看轨迹
  viewTrajectory() {
    wx.showToast({
      title: '开发中',
      icon: 'none'
    });
  },

  // 查看收藏
  viewFavorites() {
    wx.showToast({
      title: '开发中',
      icon: 'none'
    });
  },

  // 查看历史
  viewHistory() {
    wx.showToast({
      title: '开发中',
      icon: 'none'
    });
  },

  // 查看订单
  viewOrders() {
    wx.showToast({
      title: '开发中',
      icon: 'none'
    });
  },

  // 联系我们
  contactUs() {
    wx.showModal({
      title: '联系我们',
      content: '微信公众号：SAYELF 山野精灵\n\n邮箱：chuanxituzhu@gmail.com',
      showCancel: false
    });
  },

  // 关于心景
  aboutUs() {
    wx.showModal({
      title: '关于心景',
      content: '心景 · MindScape\n\n384 个具体体验单元\n64 种人生情景\n\n帮助你：\n• 看清你正在经历什么\n• 知道接下来会发生什么\n• 找到具体时刻的位置\n\nVersion 1.0.0',
      showCancel: false
    });
  }
});
