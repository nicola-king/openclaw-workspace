const app = getApp()

Page({
  data: {
    inputValue: ''
  },

  onInput(e) {
    this.setData({
      inputValue: e.detail.value
    })
  },

  startTest() {
    const input = this.data.inputValue
    wx.navigateTo({
      url: `/pages/test/test?input=${encodeURIComponent(input)}`
    })
  },

  randomTest() {
    // 随机选择一个情景
    const stages = app.globalData.stages
    const randomIndex = Math.floor(Math.random() * Object.keys(stages).length)
    const stageId = Object.keys(stages)[randomIndex]
    const stage = stages[stageId]
    
    // 随机选择一个步骤
    const steps = [
      "刚开始不对劲", "逐渐察觉问题", "开始怀疑路径",
      "尝试调整方式", "逐步适应", "进入新状态"
    ]
    const randomStep = Math.floor(Math.random() * 6)
    
    // 保存到全局
    app.globalData.currentStage = stage
    app.globalData.currentStep = randomStep
    
    wx.navigateTo({
      url: `/pages/result/result?stageId=${stageId}&step=${randomStep}`
    })
  }
})
