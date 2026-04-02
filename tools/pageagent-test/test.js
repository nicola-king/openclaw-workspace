/**
 * PageAgent 测试脚本
 * 演示如何用自然语言操控网页
 */

const { PageAgent } = require('page-agent');

// 创建 PageAgent 实例
const agent = new PageAgent({
  // 配置大模型 API（可选，支持多种模型）
  model: {
    provider: 'openai',  // 或 'anthropic', 'google', 'ollama'
    apiKey: process.env.OPENAI_API_KEY || '',
    model: 'gpt-4o'
  },
  
  // 配置选项
  options: {
    debug: true,        // 调试模式
    timeout: 30000,     // 超时时间
    maxRetries: 3       // 最大重试次数
  }
});

// 示例：自动化操作
async function runDemo() {
  console.log('🚀 PageAgent 测试开始...\n');
  
  try {
    // 1. 打开网页
    console.log('📄 打开网页：https://example.com');
    await agent.navigate('https://example.com');
    
    // 2. 用自然语言描述操作
    console.log('\n🎯 执行操作："点击页面上的链接"');
    await agent.act('点击页面上的链接');
    
    // 3. 获取页面信息
    console.log('\n📊 获取页面信息...');
    const pageInfo = await agent.observe();
    console.log('页面标题:', pageInfo.title);
    console.log('可操作元素:', pageInfo.elements?.length || 0);
    
    // 4. 表单填写示例（注释掉，需要实际表单页面）
    // await agent.act('在搜索框输入 "PageAgent" 并提交');
    
    console.log('\n✅ 测试完成！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
  } finally {
    // 清理资源
    await agent.destroy();
  }
}

// 运行测试
runDemo();

// 导出供其他模块使用
module.exports = { agent };
