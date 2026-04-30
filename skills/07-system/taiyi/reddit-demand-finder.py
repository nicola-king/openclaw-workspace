#!/usr/bin/env python3
"""
太一版需求发现器
用 MCP 工具自动化发现技能市场需求

灵感来源：Om Patel 的$10K MRR 创业点子发现法

用法：
    python3 reddit-demand-finder.py --subreddit polymarket --keywords "wish,complaint"
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class DemandFinder:
    """需求发现器"""
    
    def __init__(self):
        self.output_dir = Path.home() / ".taiyi" / "demand-research"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def search_reddit(self, subreddit, query, limit=50):
        """搜索 Reddit 帖子"""
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {
            'q': query,
            'limit': limit,
            'sort': 'relevance',
            't': 'month'
        }
        
        headers = {'User-Agent': 'TaiyiAGI/1.0'}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            
            posts = []
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                posts.append({
                    'title': post.get('title', ''),
                    'selftext': post.get('selftext', ''),
                    'score': post.get('score', 0),
                    'num_comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'created': datetime.fromtimestamp(post.get('created_utc', 0)).strftime('%Y-%m-%d')
                })
            
            return posts
        except Exception as e:
            print(f"❌ 搜索失败：{e}")
            return []
    
    def find_pain_points(self, subreddit):
        """发现痛点帖子"""
        queries = [
            "wish there was a tool",
            "complaints about",
            "frustrated with",
            "too expensive",
            "how to automate",
            "struggling with"
        ]
        
        all_posts = []
        for query in queries:
            print(f"🔍 搜索：r/{subreddit} - '{query}'")
            posts = self.search_reddit(subreddit, query, limit=20)
            all_posts.extend(posts)
            print(f"  找到 {len(posts)} 条")
        
        return all_posts
    
    def analyze_patterns(self, posts):
        """分析重复模式"""
        from collections import Counter
        
        # 提取关键词
        keywords = []
        for post in posts:
            title = post['title'].lower()
            text = post['selftext'].lower()
            
            # 简单分词
            words = title.split() + text.split()
            keywords.extend([w for w in words if len(w) > 5])
        
        # 统计频率
        counter = Counter(keywords)
        top_keywords = counter.most_common(20)
        
        return top_keywords
    
    def save_results(self, subreddit, posts, keywords):
        """保存结果"""
        output_file = self.output_dir / f"{subreddit}_demand_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = {
            'subreddit': subreddit,
            'search_time': datetime.now().isoformat(),
            'total_posts': len(posts),
            'top_keywords': keywords,
            'posts': posts[:20]  # 只保存前 20 条
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 结果已保存：{output_file}")
        return output_file
    
    def run(self, subreddit):
        """主流程"""
        print("=" * 70)
        print(f"  太一需求发现器 - r/{subreddit}")
        print("=" * 70)
        print()
        
        # 发现痛点
        print("【1/3】发现痛点帖子...")
        posts = self.find_pain_points(subreddit)
        print(f"  总计：{len(posts)} 条")
        print()
        
        # 分析模式
        print("【2/3】分析重复模式...")
        keywords = self.analyze_patterns(posts)
        print(f"  Top 关键词:")
        for kw, count in keywords[:10]:
            print(f"    {kw}: {count} 次")
        print()
        
        # 保存结果
        print("【3/3】保存结果...")
        output_file = self.save_results(subreddit, posts, keywords)
        print()
        
        # 输出建议
        print("=" * 70)
        print("  技能市场机会")
        print("=" * 70)
        print()
        
        if keywords:
            print("建议技能方向：")
            for kw, count in keywords[:5]:
                if count >= 3:
                    print(f"  • {kw} ({count} 次提及)")
        
        print()
        print("下一步：")
        print("  1. 查看保存的 JSON 文件")
        print("  2. 找出 5 个以上重复痛点")
        print("  3. 创建对应技能")
        print("  4. DM 发帖人（种子用户）")
        print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="太一需求发现器")
    parser.add_argument("--subreddit", required=True, help="Reddit 圈子")
    
    args = parser.parse_args()
    
    finder = DemandFinder()
    finder.run(args.subreddit)
