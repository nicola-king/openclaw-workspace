App({
  globalData: {
    stages: [],
    currentStage: null,
    currentStep: 0,
    userInfo: null
  },

  onLaunch() {
    // 加载 64 个情景状态数据
    this.loadStagesData()
  },

  loadStagesData() {
    // 从本地或服务器加载 64 个情景状态数据
    const stages = require('./data/stages-64-final.json')
    this.globalData.stages = stages.stages || stages
  }
})
