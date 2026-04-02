/**
 * PageAgent OpenClaw Skill 封装
 * 让太一和其他 Bot 可以用自然语言操控网页
 */

const { PageAgent } = require('page-agent');

class PageAgentSkill {
  constructor(config = {}) {
    this.agent = null;
    this.config = {
      model: config.model || {
        provider: process.env.LLM_PROVIDER || 'openai',
        apiKey: process.env.LLM_API_KEY || '',
        model: process.env.LLM_MODEL || 'gpt-4o'
      },
      options: {
        debug: config.debug || false,
        timeout: config.timeout || 30000,
        maxRetries: config.maxRetries || 3
      }
    };
  }

  // 初始化 Agent
  async init() {
    if (!this.agent) {
      this.agent = new PageAgent(this.config);
      console.log('✅ PageAgent 初始化完成');
    }
    return this.agent;
  }

  // 导航到网页
  async navigate(url) {
    await this.init();
    console.log(`📄 导航到：${url}`);
    return await this.agent.navigate(url);
  }

  // 执行操作（自然语言）
  async act(instruction) {
    await this.init();
    console.log(`🎯 执行：${instruction}`);
    return await this.agent.act(instruction);
  }

  // 观察页面
  async observe() {
    await this.init();
    console.log('👀 观察页面...');
    return await this.agent.observe();
  }

  // 截图
  async screenshot() {
    await this.init();
    console.log('📸 截图...');
    return await this.agent.screenshot();
  }

  // 清理资源
  async destroy() {
    if (this.agent) {
      await this.agent.destroy();
      this.agent = null;
      console.log('🧹 PageAgent 已清理');
    }
  }

  // 执行工作流（多步骤）
  async workflow(url, steps) {
    await this.navigate(url);
    
    const results = [];
    for (const step of steps) {
      console.log(`\n📍 执行步骤：${step}`);
      const result = await this.act(step);
      results.push({ step, result });
    }
    
    return results;
  }
}

// 导出单例
const pageAgentSkill = new PageAgentSkill();

// OpenClaw Skill 接口
module.exports = {
  name: 'pageagent',
  description: '用自然语言操控网页的 GUI Agent',
  
  // 触发词
  triggers: [
    '打开网页',
    '点击',
    '输入',
    '填写表单',
    '操作网页',
    '自动化',
    'pageagent',
    'PageAgent'
  ],
  
  // 执行函数
  async execute(context) {
    const { input, channel } = context;
    
    try {
      // 解析用户指令
      let url = null;
      let action = null;
      
      // 提取 URL
      const urlMatch = input.match(/https?:\/\/[^\s]+/);
      if (urlMatch) {
        url = urlMatch[0];
      }
      
      // 提取操作
      const actionPatterns = [
        /点击 (.+)/,
        /输入 (.+)/,
        /填写 (.+)/,
        /搜索 (.+)/,
        /滚动 (.+)/
      ];
      
      for (const pattern of actionPatterns) {
        const match = input.match(pattern);
        if (match) {
          action = match[0];
          break;
        }
      }
      
      if (!action) {
        action = input.replace(url, '').trim();
      }
      
      // 执行操作
      if (url) {
        await pageAgentSkill.navigate(url);
      }
      
      if (action) {
        const result = await pageAgentSkill.act(action);
        return {
          success: true,
          message: `✅ 执行完成：${action}`,
          data: result
        };
      }
      
      return {
        success: false,
        message: '❌ 请提供操作指令，例如："打开 https://example.com 并点击登录按钮"'
      };
      
    } catch (error) {
      return {
        success: false,
        message: `❌ 执行失败：${error.message}`,
        error: error.toString()
      };
    }
  },
  
  // 清理
  async cleanup() {
    await pageAgentSkill.destroy();
  }
};

// 直接运行测试
if (require.main === module) {
  (async () => {
    console.log('🚀 PageAgent Skill 测试\n');
    
    // 示例：自动化工作流
    const testWorkflow = async () => {
      await pageAgentSkill.init();
      
      // 测试导航
      await pageAgentSkill.navigate('https://example.com');
      
      // 测试观察
      const pageInfo = await pageAgentSkill.observe();
      console.log('\n📊 页面信息:');
      console.log('- 标题:', pageInfo.title);
      
      // 测试操作
      await pageAgentSkill.act('点击页面上的链接');
      
      await pageAgentSkill.destroy();
      console.log('\n✅ 测试完成！');
    };
    
    await testWorkflow();
  })();
}
