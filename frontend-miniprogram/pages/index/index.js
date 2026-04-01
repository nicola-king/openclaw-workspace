// pages/index/index.js
const app = getApp();

Page({
  data: {
    userInfo: null
  },

  onLoad() {
    this.setData({
      userInfo: app.globalData.userInfo
    });
  },

  // 开始测试
  startTest() {
    wx.navigateTo({
      url: '/pages/test/test'
    });
  },

  // 浏览情景库
  viewStates() {
    wx.navigateTo({
      url: '/pages/states/states'
    });
  },

  // 查看个人轨迹
  viewProfile() {
    wx.navigateTo({
      url: '/pages/profile/profile'
    });
  }
});
