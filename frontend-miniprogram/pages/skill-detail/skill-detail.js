// pages/skill-detail/skill-detail.js
Page({
  data: {
    skill: null
  },

  onLoad(options) {
    if (options.data) {
      const skill = JSON.parse(decodeURIComponent(options.data));
      this.setData({ skill });
      
      // 设置页面标题
      wx.setNavigationBarTitle({
        title: skill.state_name
      });
    }
  },

  // 分享给朋友
  shareSkill() {
    const { skill } = this.data;
    
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });

    wx.showModal({
      title: '分享',
      content: `我在心景看到了「${skill.state_name}」的解读，分享给你看看～`,
      confirmText: '去分享',
      success: (res) => {
        if (res.confirm) {
          // 实际分享需要用户手动操作
          wx.showToast({
            title: '点击右上角分享',
            icon: 'none'
          });
        }
      }
    });
  },

  // 返回首页
  goHome() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  // 分享到朋友圈
  onShareTimeline() {
    const { skill } = this.data;
    return {
      title: `心景 · ${skill.state_name}`,
      query: `skill=${skill.id}`,
      imageUrl: ''
    };
  },

  // 分享给朋友
  onShareAppMessage() {
    const { skill } = this.data;
    return {
      title: `心景 · ${skill.state_name}`,
      path: `/pages/skill-detail/skill-detail?data=${encodeURIComponent(JSON.stringify(skill))}`,
      imageUrl: ''
    };
  }
});
