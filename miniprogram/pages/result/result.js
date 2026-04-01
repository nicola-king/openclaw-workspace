const app = getApp()

Page({
  data: {
    stageId: '',
    stageName: '',
    step: 0,
    stepName: '',
    stateText: '',
    personalityTag: ''
  },

  onLoad(options) {
    const stageId = options.stageId || '2'
    const step = parseInt(options.step) || 0
    
    const stages = app.globalData.stages
    const stage = stages[stageId]
    
    if (!stage) {
      wx.showToast({
        title: '状态加载失败',
        icon: 'none'
      })
      return
    }

    // 心理发展阶段名称 (6 个演化阶段)
    const stepNames = [
      "初始阶段", "发展阶段", "强化阶段",
      "转化阶段", "整合阶段", "完成阶段"
    ]

    // 人格标签映射 (简化版)
    const personalityTags = {
      '1': '积累潜力型人格',
      '2': '路径学习型人格',
      '3': '开创探索型人格',
      '4': '认知升级型人格',
      '5': '耐心等待型人格',
      '6': '冲突管理型人格'
    }

    this.setData({
      stageId: stageId,
      stageName: stage.name || '未知状态',
      step: step + 1,
      stepName: stepNames[step] || '未知步骤',
      stateText: stage.content?.state || '你正在经历一个结构与认知需要重新匹配的阶段',
      personalityTag: personalityTags[stageId] || '探索型人格'
    })
  },

  unlock() {
    // 跳转到解锁页
    wx.navigateTo({
      url: `/pages/unlock/unlock?stageId=${this.data.stageId}`
    })
  },

  retry() {
    // 返回首页
    wx.navigateBack({
      delta: 2
    })
  }
})
