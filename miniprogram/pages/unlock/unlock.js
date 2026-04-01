const app = getApp()

Page({
  data: {
    stageId: '',
    bottomProblem: '',
    advice: [],
    warning: '',
    actions: []
  },

  onLoad(options) {
    const stageId = options.stageId || '2'
    const stages = app.globalData.stages
    const stage = stages[stageId]

    if (!stage) {
      wx.showToast({
        title: '状态加载失败',
        icon: 'none'
      })
      return
    }

    // 生成解锁内容
    const bottomProblem = `你在用${stage.content?.reason || '当前模式'}解决自己的问题`
    const advice = stage.content?.advice || ['建立自己的判断标准', '降低依赖', '小范围试错']
    const warning = stage.content?.warning || '参考可以，但不能替代思考'
    const actions = [
      '写下 3 个你自己的判断',
      '减少一次"问别人"',
      '做一个小决定 (不咨询任何人)'
    ]

    this.setData({
      stageId: stageId,
      bottomProblem: bottomProblem,
      advice: advice,
      warning: warning,
      actions: actions
    })
  },

  buyVip() {
    // 这里接入微信支付
    wx.showToast({
      title: '支付功能开发中',
      icon: 'none'
    })
  }
})
