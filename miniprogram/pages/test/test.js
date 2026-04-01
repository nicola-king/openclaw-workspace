const app = getApp()

Page({
  onLoad(options) {
    const input = options.input || ''
    
    // 简单匹配情景 (实际应该用更复杂的算法)
    const stages = app.globalData.stages
    const stageKeys = Object.keys(stages)
    
    // 根据关键词匹配
    let matchedStageId = '2' // 默认路径错配期
    
    if (input.includes('累') || input.includes('疲惫')) {
      matchedStageId = '6'
    } else if (input.includes('努力') && input.includes('结果')) {
      matchedStageId = '1'
    } else if (input.includes('方向') || input.includes('错')) {
      matchedStageId = '2'
    }
    
    const stage = stages[matchedStageId]
    const randomStep = Math.floor(Math.random() * 6)
    
    app.globalData.currentStage = stage
    app.globalData.currentStep = randomStep
    
    // 延迟一下跳转到结果页
    setTimeout(() => {
      wx.navigateTo({
        url: `/pages/result/result?stageId=${matchedStageId}&step=${randomStep}`
      })
    }, 1500)
  }
})
