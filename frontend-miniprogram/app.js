// app.js
App({
  onLaunch() {
    console.log('心景 · MindScape 启动');
    
    // 初始化用户信息
    this.initUser();
    
    // 检查更新
    this.checkUpdate();
  },
  
  globalData: {
    userInfo: null,
    apiBaseUrl: 'https://api.sayelf.com', // 生产环境
    // apiBaseUrl: 'http://localhost:8000', // 测试环境
    testType: 'quick' // quick/standard/deep
  },
  
  initUser() {
    // 从本地存储加载用户信息
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    } else {
      // 获取微信用户信息
      wx.getUserProfile({
        desc: '用于记录您的情景轨迹',
        success: (res) => {
          this.globalData.userInfo = res.userInfo;
          wx.setStorageSync('userInfo', res.userInfo);
        },
        fail: () => {
          console.log('用户拒绝授权');
        }
      });
    }
  },
  
  checkUpdate() {
    // 检查小程序更新
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager();
      updateManager.onCheckForUpdate((res) => {
        if (res.hasUpdate) {
          updateManager.onUpdateReady(() => {
            wx.showModal({
              title: '更新提示',
              content: '新版本已经准备好，是否重启应用？',
              success: (res) => {
                if (res.confirm) {
                  updateManager.applyUpdate();
                }
              }
            });
          });
        }
      });
    }
  }
});
