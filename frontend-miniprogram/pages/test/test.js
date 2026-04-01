// pages/test/test.js
const request = require('../../utils/request');
const config = require('../../utils/config');

Page({
  data: {
    questions: [
      {
        id: 1,
        content: "你最近的状态更接近？",
        options: [
          { label: "A", text: "努力但没有回报" },
          { label: "B", text: "进展顺利但有波动" },
          { label: "C", text: "感到迷茫不知道方向" },
          { label: "D", text: "疲惫想停下来休息" }
        ]
      },
      {
        id: 2,
        content: "你当前的主要困扰是？",
        options: [
          { label: "A", text: "外部阻力 (人际关系/资源不足)" },
          { label: "B", text: "内部困惑 (方向/方法/信心)" },
          { label: "C", text: "时机问题 (太早/太晚/等待)" },
          { label: "D", text: "决策压力 (需要选择/害怕选错)" }
        ]
      },
      {
        id: 3,
        content: "你希望得到什么帮助？",
        options: [
          { label: "A", text: "具体行动建议" },
          { label: "B", text: "心理层面的理解" },
          { label: "C", text: "趋势和方向判断" },
          { label: "D", text: "情绪支持和鼓励" }
        ]
      }
    ],
    currentQuestion: 0,
    selectedAnswer: null,
    answers: [],
    progress: 0,
    showResult: false,
    result: null
  },

  // 选择答案
  selectOption(e) {
    this.setData({
      selectedAnswer: e.currentTarget.dataset.label
    });
  },

  // 下一题
  nextQuestion() {
    const { currentQuestion, selectedAnswer, answers, questions } = this.data;
    
    // 保存答案
    answers.push(selectedAnswer);
    
    if (currentQuestion < questions.length - 1) {
      // 下一题
      this.setData({
        currentQuestion: currentQuestion + 1,
        selectedAnswer: null,
        answers: answers,
        progress: ((currentQuestion + 1) / questions.length) * 100
      });
    } else {
      // 提交测试
      this.submitTest(answers);
    }
  },

  // 提交测试
  async submitTest(answers) {
    try {
      // 构建用户输入文本
      const answerTexts = {
        A: "努力但没有回报",
        B: "进展顺利但有波动",
        C: "感到迷茫不知道方向",
        D: "疲惫想停下来休息"
      };
      
      const userInput = answers.map(a => answerTexts[a]).join(" ");
      
      // 调用 API 分析
      const result = await request.analyzeUserInput(userInput, 'quick');
      
      this.setData({
        showResult: true,
        result: result
      });
      
      // 记录轨迹
      this.trackTest(result);
      
    } catch (error) {
      wx.showToast({
        title: '分析失败，请重试',
        icon: 'none'
      });
    }
  },

  // 查看完整结果
  viewFullResult() {
    const { result } = this.data;
    wx.navigateTo({
      url: `/pages/result/result?data=${JSON.stringify(result)}`
    });
  },

  // 重新测试
  retakeTest() {
    this.setData({
      currentQuestion: 0,
      selectedAnswer: null,
      answers: [],
      progress: 0,
      showResult: false,
      result: null
    });
  },

  // 记录测试轨迹
  trackTest(result) {
    // TODO: 调用 API 记录用户轨迹
    console.log('Track test:', result);
  }
});
