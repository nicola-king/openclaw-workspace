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

// 示例：自动化操作 - 小红书截图
async function runXiaohongshuScreenshot() {
  console.log('🚀 PageAgent 小红书截图测试开始...\n');
  
  try {
    // 1. 打开小红书
    console.log('📄 打开网页：https://www.xiaohongshu.com');
    await agent.navigate('https://www.xiaohongshu.com');
    
    // 2. 等待页面加载
    console.log('\n⏳ 等待页面加载...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 3. 获取页面信息
    console.log('\n📊 获取页面信息...');
    const pageInfo = await agent.observe();
    console.log('页面标题:', pageInfo.title);
    
    // 4. 截图
    console.log('\n📸 执行截图...');
    const screenshot = await agent.screenshot();
    console.log('截图完成:', screenshot?.path || 'Base64 数据已获取');
    
    // 5. 保存截图到文件
    const fs = require('fs');
    const path = require('path');
    const screenshotPath = path.join(__dirname, 'xiaohongshu-screenshot.png');
    
    if (screenshot && screenshot.data) {
      fs.writeFileSync(screenshotPath, screenshot.data, 'base64');
      console.log('\n✅ 截图已保存到:', screenshotPath);
    } else {
      console.log('\n⚠️ 截图数据为空，可能需要在浏览器中手动验证');
    }
    
    console.log('\n✅ 小红书截图测试完成！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('堆栈:', error.stack);
  } finally {
    // 清理资源
    await agent.destroy();
  }
}

// 运行小红书截图测试
const runDemo = runXiaohongshuScreenshot;

// 运行测试
runDemo();

// 导出供其他模块使用
module.exports = { agent };
