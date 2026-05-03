#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO Auditor - 免费开源版
版本：v1.0 (零成本)
创建：2026-04-20 21:22
功能：使用开源工具进行 AI 可见度审计

技术栈:
- Ollama (本地 LLM)
- Google Custom Search (免费额度)
- Firecrawl (网页爬取)
- ChromaDB (向量存储)

GitHub 开源项目:
- Ollama: https://github.com/ollama/ollama
- Firecrawl: https://github.com/mendableai/firecrawl
- Crawl4AI: https://github.com/unclecode/crawl4ai
"""

import json
import asyncio
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from collections import Counter


@dataclass
class MentionResult:
    """提及结果"""
    engine: str
    query: str
    mentioned: bool
    position: Optional[int]
    sentiment: str
    sources: List[str]
    timestamp: str


class GEOAuditorOpenSource:
    """GEO 审计器 (开源版)"""
    
    # 标准测试查询模板
    STANDARD_QUERIES = [
        "best {product} brands 2026",
        "buy {product} online",
        "{product} reviews and recommendations",
        "{product} comparison guide",
        "top rated {product}",
    ]
    
    def __init__(
        self,
        brand: str,
        config_path: Optional[str] = None,
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "llama3.1:8b",
        google_api_key: Optional[str] = None,
        google_cse_id: Optional[str] = None
    ):
        """
        初始化审计器
        
        Args:
            brand: 品牌名称
            config_path: 可选的配置文件路径
            ollama_url: Ollama API 地址
            ollama_model: Ollama 模型名称
            google_api_key: Google Custom Search API Key (免费)
            google_cse_id: Google Custom Search Engine ID
        """
        self.brand = brand
        self.config_path = config_path
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id
        
        # 加载配置
        if config_path and Path(config_path).exists():
            self._load_config(config_path)
        
        # 检查 Ollama 连接
        self.ollama_available = self._check_ollama()
    
    def _load_config(self, config_path: str):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
            # 从 geo_config.json 加载
            if "google_api_key" in config:
                self.google_api_key = config["google_api_key"]
            if "google_cse_id" in config:
                self.google_cse_id = config["google_cse_id"]
        
        print(f"✅ 加载配置：{config_path}")
    
    def _check_ollama(self) -> bool:
        """检查 Ollama 连接"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✅ Ollama 连接成功：{self.ollama_url}")
                return True
            else:
                print(f"⚠️  Ollama 响应异常：{response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️  Ollama 连接失败：{e}")
            print("\n💡 提示：请先安装并启动 Ollama:")
            print("   curl -fsSL https://ollama.com/install.sh | sh")
            print("   ollama pull llama3.1:8b\n")
            return False
    
    def query_ollama(self, prompt: str) -> str:
        """查询本地 Ollama"""
        if not self.ollama_available:
            return "Ollama 不可用"
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"错误：{response.status_code}"
                
        except Exception as e:
            return f"查询失败：{e}"
    
    def google_search(self, query: str) -> List[Dict]:
        """Google Custom Search (免费 100 次/天)"""
        if not self.google_api_key or not self.google_cse_id:
            print("⚠️  未配置 Google API，使用模拟结果")
            return self._mock_search_results(query)
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "q": query,
                "key": self.google_api_key,
                "cx": self.google_cse_id,
                "num": 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                items = result.get("items", [])
                return [
                    {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    }
                    for item in items[:10]
                ]
            else:
                print(f"Google Search 错误：{response.status_code}")
                return self._mock_search_results(query)
                
        except Exception as e:
            print(f"Google Search 异常：{e}")
            return self._mock_search_results(query)
    
    def _mock_search_results(self, query: str) -> List[Dict]:
        """模拟搜索结果 (无 API 时使用)"""
        # 实际使用时，这里可以替换为 Bing API 或其他免费搜索
        return [
            {
                "title": f"Result for: {query}",
                "link": "https://example.com",
                "snippet": "This is a mock search result for testing."
            }
        ]
    
    def analyze_sentiment(self, text: str) -> str:
        """使用 Ollama 分析情感"""
        if not self.ollama_available:
            return "neutral"
        
        prompt = f"""分析以下文本的情感倾向，只回答 positive/neutral/negative 之一：

{text}

情感倾向："""
        
        result = self.query_ollama(prompt)
        result = result.strip().lower()
        
        if "positive" in result:
            return "positive"
        elif "negative" in result:
            return "negative"
        else:
            return "neutral"
    
    def check_brand_mention(
        self,
        query: str,
        brand: str,
        search_results: List[Dict]
    ) -> MentionResult:
        """检查品牌是否被提及"""
        
        # 检查搜索结果中是否包含品牌
        mentioned = False
        position = None
        sources = []
        
        for i, result in enumerate(search_results, 1):
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            
            if brand.lower() in title or brand.lower() in snippet:
                mentioned = True
                position = i
                sources.append(result["link"])
        
        # 分析情感
        if search_results:
            combined_text = " ".join([
                r.get("title", "") + " " + r.get("snippet", "")
                for r in search_results[:5]
            ])
            sentiment = self.analyze_sentiment(combined_text)
        else:
            sentiment = "neutral"
        
        return MentionResult(
            engine="Google+Ollama",
            query=query,
            mentioned=mentioned,
            position=position,
            sentiment=sentiment,
            sources=sources[:5],
            timestamp=datetime.now().isoformat()
        )
    
    async def audit_brand(
        self,
        product_keywords: List[str],
        target_markets: List[str] = ["global"]
    ) -> Dict:
        """
        审计品牌 AI 可见度
        
        Args:
            product_keywords: 产品关键词
            target_markets: 目标市场
            
        Returns:
            审计报告字典
        """
        print(f"\n🎯 开始 GEO 审计 (开源免费): {self.brand}")
        print(f"📦 产品关键词：{product_keywords}")
        print(f"🌍 目标市场：{target_markets}")
        print(f"🤖 本地模型：{self.ollama_model}")
        print(f"🔍 搜索引擎：Google Custom Search (免费 100 次/天)\n")
        
        results = []
        
        # 生成查询
        queries = []
        for product in product_keywords:
            for market in target_markets:
                for template in self.STANDARD_QUERIES:
                    query = template.format(product=product)
                    if market != "global":
                        query = f"{query} in {market}"
                    queries.append(query)
        
        print(f"📊 总查询数：{len(queries)}\n")
        
        # 执行审计
        for i, query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] 审计：{query}")
            
            # Google 搜索
            search_results = self.google_search(query)
            
            # 检查品牌提及
            result = self.check_brand_mention(query, self.brand, search_results)
            results.append(result)
            
            # 速率限制 (避免触发 Google 限额)
            await asyncio.sleep(0.5)
        
        # 生成报告
        report = self._generate_report(results, queries)
        return report
    
    def _generate_report(self, results: List[MentionResult], queries: List[str]) -> Dict:
        """生成审计报告"""
        
        total = len(results)
        mentioned_count = sum(1 for r in results if r.mentioned)
        mention_rate = mentioned_count / total if total > 0 else 0
        
        positive_count = sum(1 for r in results if r.sentiment == "positive")
        neutral_count = sum(1 for r in results if r.sentiment == "neutral")
        negative_count = sum(1 for r in results if r.sentiment == "negative")
        
        # 收集所有来源
        all_sources = []
        for r in results:
            all_sources.extend(r.sources)
        
        # Top 来源
        top_sources = [
            source for source, _ in Counter(all_sources).most_common(10)
        ]
        
        report = {
            "brand": self.brand,
            "audit_date": datetime.now().isoformat(),
            "queries_tested": len(queries),
            "engine": "Google Custom Search + Ollama (开源免费)",
            "overall_mention_rate": mention_rate,
            "mentioned_count": mentioned_count,
            "sentiment_distribution": {
                "positive": positive_count,
                "neutral": neutral_count,
                "negative": negative_count,
            },
            "top_sources": top_sources,
            "recommendations": self._generate_recommendations(mention_rate),
            "cost": "$0 (免费开源方案)",
            "raw_results": [
                {
                    "query": r.query,
                    "mentioned": r.mentioned,
                    "position": r.position,
                    "sentiment": r.sentiment,
                }
                for r in results
            ],
        }
        
        return report
    
    def _generate_recommendations(self, mention_rate: float) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if mention_rate < 0.1:
            recommendations.append("📰 品牌曝光度低，优先建立 Earned Media 管道")
            recommendations.append("🏷️ 完善网站 Schema 标记 (Product/Organization)")
        
        if mention_rate < 0.3:
            recommendations.append("📝 创建高质量比较内容 ('品牌 A vs 品牌 B')")
            recommendations.append("🌐 针对每个目标市场创建本地化内容")
        
        recommendations.append("📊 持续监测，每周执行一次审计")
        recommendations.append("🎯 联系高 DA 媒体进行客座文章合作")
        recommendations.append("💰 当前使用免费开源方案，成本 $0/月")
        
        return recommendations
    
    def save_report(self, report: Dict, output_path: str):
        """保存报告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ 报告已保存：{output_path}")
    
    def print_summary(self, report: Dict):
        """打印摘要"""
        print("\n" + "=" * 60)
        print(f"📊 GEO 审计报告 (开源免费) - {report['brand']}")
        print("=" * 60)
        print(f"审计引擎：{report['engine']}")
        print(f"测试查询：{report['queries_tested']}")
        print(f"提及率：{report['overall_mention_rate']:.1%}")
        print(f"提及次数：{report['mentioned_count']}")
        print(f"成本：{report['cost']}")
        print(f"\n情感分布:")
        for sentiment, count in report['sentiment_distribution'].items():
            print(f"  - {sentiment}: {count}")
        print(f"\n优化建议:")
        for rec in report['recommendations']:
            print(f"  {rec}")
        print("=" * 60 + "\n")


async def main():
    """主函数示例"""
    # 从配置文件加载
    config_file = Path(__file__).parent / "geo_config.json"
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            brand = config.get("brand", "YourBrand")
            product_keywords = config.get("product_keywords", ["wireless earbuds"])
            target_markets = config.get("target_markets", ["global"])
    else:
        brand = "YourBrand"
        product_keywords = ["wireless earbuds", "smart water bottle"]
        target_markets = ["USA", "global"]
    
    # 创建审计器
    auditor = GEOAuditorOpenSource(
        brand=brand,
        config_path=str(config_file) if config_file.exists() else None
    )
    
    # 执行审计
    report = await auditor.audit_brand(
        product_keywords=product_keywords,
        target_markets=target_markets
    )
    
    # 输出结果
    auditor.print_summary(report)
    
    # 保存报告
    output_file = Path(__file__).parent / "geo_audit_report_open_source.json"
    auditor.save_report(report, str(output_file))


if __name__ == "__main__":
    asyncio.run(main())
