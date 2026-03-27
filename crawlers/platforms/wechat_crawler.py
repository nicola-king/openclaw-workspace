#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号采集器 - 使用 wechatarticles 库
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base import BaseCrawler


class WechatCrawler(BaseCrawler):
    """微信公众号采集器"""
    
    def __init__(self, output_dir: str = "output", max_results: int = 50):
        super().__init__("wechat", output_dir)
        self.max_results = max_results
        self.api = None
    
    def _init_api(self):
        """初始化 API"""
        try:
            from wechatarticles import ArticlesAPI
            # 注意：wechatarticles 需要 Cookie，首次使用需要手动获取
            self.api = ArticlesAPI()
            self.logger.info("微信公众号 API 初始化成功")
        except ImportError:
            self.logger.warning("wechatarticles 未安装，使用备用方案")
            self.api = None
        except Exception as e:
            self.logger.error(f"API 初始化失败：{e}")
            self.api = None
    
    async def fetch(self, target: str, **kwargs) -> List[Dict[str, Any]]:
        """
        采集单个公众号
        
        Args:
            target: 公众号名称或 ID
        """
        results = []
        
        if self.api is None:
            self.logger.warning("API 未初始化，跳过采集")
            return results
        
        try:
            self.logger.info(f"采集公众号：{target}")
            
            # 获取公众号文章列表
            # 注意：实际使用需要提供 __cookie 和 __token
            articles = await asyncio.to_thread(
                self._fetch_articles,
                target,
                kwargs.get("max_results", self.max_results)
            )
            
            results = articles
            
        except Exception as e:
            self.logger.error(f"采集失败 {target}: {e}")
        
        return results
    
    def _fetch_articles(self, mp_name: str, max_results: int) -> List[Dict[str, Any]]:
        """获取公众号文章（同步）"""
        results = []
        
        try:
            # 注意：这里需要实际的 Cookie 和 Token
            # 首次使用需要手动从微信获取
            # 参考：https://github.com/taojy123/wechatarticles
            
            # 示例代码（需要替换为实际凭证）
            # articles = self.api.account_articles(
            #     mp_name=mp_name,
            #     begin=0,
            #     count=max_results
            # )
            
            self.logger.warning("需要提供 Cookie 和 Token 才能采集公众号文章")
            self.logger.info("请参考：https://github.com/taojy123/wechatarticles 获取凭证")
            
        except Exception as e:
            self.logger.error(f"获取文章失败：{e}")
        
        return results
    
    async def fetch_batch(self, targets: List[str], **kwargs) -> List[Dict[str, Any]]:
        """批量采集"""
        all_results = []
        
        for target in targets:
            results = await self.fetch(target, **kwargs)
            all_results.extend(results)
            await asyncio.sleep(2)  # 避免请求过快
        
        return all_results
    
    def setup_guide(self) -> str:
        """返回配置指南"""
        return """
# 微信公众号采集配置指南

## 步骤 1：获取 Cookie 和 Token

1. 登录微信公众号后台：https://mp.weixin.qq.com
2. 打开浏览器开发者工具 (F12)
3. 切换到 Network 标签
4. 刷新页面，找到任意请求
5. 复制 Request Headers 中的：
   - Cookie
   - __token (在 URL 参数中)

## 步骤 2：写入配置

编辑 `config/wechat_config.json`:

```json
{
  "cookie": "你的 Cookie",
  "token": "你的 Token"
}
```

## 步骤 3：测试

```bash
python -m platforms.wechat_crawler --test
```

## 注意事项

- Cookie 有效期约 24 小时，需要定期更新
- 频繁采集可能触发风控，建议设置合理间隔
- 仅采集公开文章，遵守平台规则

## 替代方案

如果 Cookie 获取困难，可以考虑：
1. 使用 RSS 订阅（部分公众号支持）
2. 使用搜狗微信搜索（无需登录，但有限制）
3. 手动导出文章列表
"""
    
    async def test(self) -> bool:
        """测试采集器"""
        self.logger.info("测试微信公众号采集器...")
        
        if self.api is None:
            self._init_api()
        
        if self.api is None:
            self.logger.warning("⚠️ API 未初始化，需要先配置 Cookie/Token")
            print(self.setup_guide())
            return False
        
        try:
            # 测试采集（需要一个实际的公众号）
            results = await self.fetch("AI 科技评论", max_results=1)
            if results:
                self.logger.info(f"✅ 测试成功，采集到 {len(results)} 条")
                return True
            else:
                self.logger.warning("⚠️ 未采集到数据")
                return False
        except Exception as e:
            self.logger.error(f"❌ 测试失败：{e}")
            return False


# CLI 入口
if __name__ == "__main__":
    import argparse
    import asyncio
    
    parser = argparse.ArgumentParser(description="微信公众号采集器")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--target", type=str, help="采集目标（公众号名称）")
    parser.add_argument("--setup", action="store_true", help="显示配置指南")
    args = parser.parse_args()
    
    crawler = WechatCrawler()
    
    if args.setup:
        print(crawler.setup_guide())
    elif args.test:
        asyncio.run(crawler.test())
    elif args.target:
        results = asyncio.run(crawler.fetch(args.target))
        print(f"采集到 {len(results)} 条结果")
    else:
        parser.print_help()
