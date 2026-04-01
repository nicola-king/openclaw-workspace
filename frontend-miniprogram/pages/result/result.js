// pages/result/result.js
const request = require('../../utils/request');
const config = require('../../utils/config');

Page({
  data: {
    result: null
  },

  onLoad(options) {
    if (options.data) {
      const result = JSON.parse(decodeURIComponent(options.data));
      this.setData({ result });
    }
  },

  // 解锁阶段解读 (¥1)
  async unlockStage() {
    try {
      const { result } = this.data;
      
      // 创建订单
      const order = await request.createOrder('stage', `${result.state.id}-${result.stage.step}`, config.PRICING.STAGE_UNLOCK);
      
      // 发起支付
      await request.requestPayment(order);
      
      // 支付成功，解锁内容
      wx.showToast({
        title: '解锁成功',
        icon: 'success'
      });
      
      // TODO: 跳转到阶段详情页
    } catch (error) {
      if (error.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({
          title: '解锁失败',
          icon: 'none'
        });
      }
    }
  },

  // 解锁完整方案 (¥9.9)
  async unlockSkill() {
    try {
      const { result } = this.data;
      const skillId = result.skill_preview.id;
      
      // 创建订单
      const order = await request.createOrder('skill', skillId, config.PRICING.SKILL_UNLOCK);
      
      // 发起支付
      await request.requestPayment(order);
      
      // 支付成功，解锁 Skill
      const skill = await request.unlockSkill(skillId, order.payment_token);
      
      wx.showToast({
        title: '解锁成功',
        icon: 'success'
      });
      
      // 跳转到 Skill 详情页
      wx.navigateTo({
        url: `/pages/skill-detail/skill-detail?data=${JSON.stringify(skill)}`
      });
      
    } catch (error) {
      if (error.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({
          title: '解锁失败',
          icon: 'none'
        });
      }
    }
  },

  // 解锁会员 (¥19/月)
  async unlockMembership() {
    try {
      // 创建订单
      const order = await request.createOrder('membership', 'monthly', config.PRICING.MEMBERSHIP_MONTHLY);
      
      // 发起支付
      await request.requestPayment(order);
      
      wx.showToast({
        title: '开通成功',
        icon: 'success'
      });
      
      // 跳转到会员中心
      wx.navigateTo({
        url: '/pages/profile/profile'
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
});
