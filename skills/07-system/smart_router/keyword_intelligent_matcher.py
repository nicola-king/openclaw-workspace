#!/usr/bin/env python3
"""
搜索关键词智能匹配引擎
自动识别国内/国外搜索意图
智能匹配关键词
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

class KeywordMatcher:
    """关键词智能匹配器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.config_dir = self.workspace / "smart-search-router"
        self.config_dir.mkdir(exist_ok=True)
        
        # 国内搜索关键词 (分层级)
        self.domestic_keywords = {
            'level_1': [  # 高优先级，直接匹配
                '中国', '国内', '中文', '大陆', '内地',
                'CN', 'china domestic', 'prc',
                '北京', '上海', '广州', '深圳',
                '华为', '小米', '腾讯', '阿里', '百度'
            ],
            'level_2': [  # 中优先级，结合上下文
                '国产', '本土', '本国', '境内',
                '国内新闻', '国内政策', '国内市场',
                '国内旅游', '国内航班', '国内快递'
            ],
            'level_3': [  # 低优先级，需要更多上下文
                '国内品牌', '国内企业', '国内产品',
                '国内大学', '国内医院', '国内景点'
            ]
        }
        
        # 国外搜索关键词 (分层级)
        self.international_keywords = {
            'level_1': [  # 高优先级，直接匹配
                '国外', '国际', '海外', '境外',
                'US', 'USA', 'America', '美国',
                'global', 'international', 'overseas',
                'Google', 'GitHub', 'Twitter', 'YouTube',
                'UK', 'Canada', 'Australia', 'Japan'
            ],
            'level_2': [  # 中优先级，结合上下文
                '外国', '西洋', '欧美', '西方',
                '国外新闻', '国际政策', '国际市场',
                '国外旅游', '国际航班', '海外购物'
            ],
            'level_3': [  # 低优先级，需要更多上下文
                '国外品牌', '外国企业', '进口产品',
                '国外大学', '国外医院', '国外景点'
            ]
        }
        
        # 排除关键词 (即使匹配到也使用国内搜索)
        self.exclude_keywords = [
            '国内国外对比', '中外对比', '国内外差异'
        ]
    
    def detect_search_type(self, query: str) -> dict:
        """智能检测搜索类型"""
        query_lower = query.lower()
        
        result = {
            'query': query,
            'search_type': 'default',
            'confidence': 0.0,
            'matched_keywords': [],
            'match_level': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # 检查排除关键词
        for keyword in self.exclude_keywords:
            if keyword.lower() in query_lower:
                result['search_type'] = 'default'
                result['confidence'] = 0.5
                result['matched_keywords'].append(keyword)
                result['reason'] = '排除关键词，使用默认搜索'
                return result
        
        # 检测国内关键词
        domestic_match = self._match_keywords(query_lower, self.domestic_keywords)
        if domestic_match['matched']:
            result['search_type'] = 'domestic_search'
            result['confidence'] = domestic_match['confidence']
            result['matched_keywords'] = domestic_match['keywords']
            result['match_level'] = domestic_match['level']
            result['reason'] = '匹配到国内关键词'
            return result
        
        # 检测国外关键词
        international_match = self._match_keywords(query_lower, self.international_keywords)
        if international_match['matched']:
            result['search_type'] = 'international_search'
            result['confidence'] = international_match['confidence']
            result['matched_keywords'] = international_match['keywords']
            result['match_level'] = international_match['level']
            result['reason'] = '匹配到国外关键词'
            return result
        
        # 默认搜索
        result['search_type'] = 'default'
        result['confidence'] = 1.0
        result['reason'] = '未匹配到关键词，使用默认搜索'
        return result
    
    def _match_keywords(self, query: str, keyword_dict: dict) -> dict:
        """匹配关键词"""
        for level in ['level_1', 'level_2', 'level_3']:
            keywords = keyword_dict.get(level, [])
            matched = [kw for kw in keywords if kw.lower() in query]
            
            if matched:
                confidence = {
                    'level_1': 0.95,
                    'level_2': 0.8,
                    'level_3': 0.6
                }.get(level, 0.5)
                
                return {
                    'matched': True,
                    'confidence': confidence,
                    'keywords': matched,
                    'level': level
                }
        
        return {'matched': False, 'confidence': 0, 'keywords': [], 'level': None}
    
    def execute_search(self, query: str) -> dict:
        """执行搜索"""
        detection = self.detect_search_type(query)
        
        result = {
            'query': query,
            'search_type': detection['search_type'],
            'confidence': detection['confidence'],
            'matched_keywords': detection['matched_keywords'],
            'match_level': detection['match_level'],
            'reason': detection.get('reason', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # 根据搜索结果设置路由
        if detection['search_type'] == 'domestic_search':
            result['route'] = {
                'search_engine': 'bing_cn',
                'endpoint': 'https://cn.bing.com',
                'proxy': False,
                'traffic': 'domestic'
            }
        elif detection['search_type'] == 'international_search':
            result['route'] = {
                'search_engine': 'chromium',
                'endpoint': 'https://www.google.com',
                'proxy': True,
                'traffic': 'proxy'
            }
        else:
            result['route'] = {
                'search_engine': 'bing_cn',
                'endpoint': 'https://cn.bing.com',
                'proxy': False,
                'traffic': 'domestic'
            }
        
        # 记录搜索日志
        self._log_search(result)
        
        return result
    
    def _log_search(self, result: dict):
        """记录搜索日志"""
        log_file = self.config_dir / "search_log.json"
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = {'searches': []}
        
        logs['searches'].append(result)
        logs['searches'] = logs['searches'][-100:]
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def save_config(self):
        """保存配置"""
        config = {
            'version': '2.0',
            'created_at': datetime.now().isoformat(),
            'domestic_keywords': self.domestic_keywords,
            'international_keywords': self.international_keywords,
            'exclude_keywords': self.exclude_keywords
        }
        
        with open(self.config_dir / "keyword_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def generate_report(self) -> str:
        """生成配置报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        report = """# 🧠 搜索关键词智能匹配配置

> **更新时间**: """ + timestamp + """  
> **版本**: v2.0 (智能匹配版)

---

## 📋 国内搜索关键词

### Level 1 (高优先级 - 直接匹配)

```
"""
        report += ', '.join(self.domestic_keywords['level_1'])
        report += """
```

**置信度**: 95%

---

### Level 2 (中优先级 - 结合上下文)

```
"""
        report += ', '.join(self.domestic_keywords['level_2'])
        report += """
```

**置信度**: 80%

---

### Level 3 (低优先级 - 需要更多上下文)

```
"""
        report += ', '.join(self.domestic_keywords['level_3'])
        report += """
```

**置信度**: 60%

---

## 📋 国外搜索关键词

### Level 1 (高优先级 - 直接匹配)

```
"""
        report += ', '.join(self.international_keywords['level_1'])
        report += """
```

**置信度**: 95%

---

### Level 2 (中优先级 - 结合上下文)

```
"""
        report += ', '.join(self.international_keywords['level_2'])
        report += """
```

**置信度**: 80%

---

### Level 3 (低优先级 - 需要更多上下文)

```
"""
        report += ', '.join(self.international_keywords['level_3'])
        report += """
```

**置信度**: 60%

---

## ⛔ 排除关键词

```
"""
        report += ', '.join(self.exclude_keywords)
        report += """
```

**说明**: 即使匹配到国内/国外关键词，如果包含排除词，使用默认搜索

---

## 🧪 测试示例

### 国内搜索示例

| 查询 | 匹配关键词 | 置信度 | 结果 |
|------|------------|--------|------|
| 中国最新科技新闻 | 中国 | 95% | domestic_search |
| 国内旅游攻略 | 国内 | 95% | domestic_search |
| 国产手机品牌 | 国产 | 80% | domestic_search |
| 北京天气预报 | 北京 | 95% | domestic_search |

### 国外搜索示例

| 查询 | 匹配关键词 | 置信度 | 结果 |
|------|------------|--------|------|
| US latest news | US | 95% | international_search |
| 国外旅游景点 | 国外 | 95% | international_search |
| 国际航班查询 | 国际 | 95% | international_search |
| GitHub 使用教程 | GitHub | 95% | international_search |

### 默认搜索示例

| 查询 | 结果 |
|------|------|
| 默认搜索测试 | default |
| 今天天气怎么样 | default |
| 如何学习编程 | default |

---

## 🚀 智能匹配规则

### 优先级规则

```
1. 检查排除关键词
   → 如果匹配，使用 default

2. 检查 Level 1 关键词
   → 如果匹配，置信度 95%

3. 检查 Level 2 关键词
   → 如果匹配，置信度 80%

4. 检查 Level 3 关键词
   → 如果匹配，置信度 60%

5. 未匹配任何关键词
   → 使用 default，置信度 100%
```

### 置信度阈值

```
> 90%: 高置信度，直接执行
80-90%: 中置信度，可执行
60-80%: 低置信度，建议确认
< 60%: 极低置信度，使用 default
```

---

*太一 AGI · 搜索关键词智能匹配 v2.0 · """ + timestamp + """*

**🧠 智能关键词匹配！国内/国外自动识别！**
"""
        return report


def main():
    """主函数"""
    print("=" * 60)
    print("搜索关键词智能匹配引擎")
    print("=" * 60)
    
    matcher = KeywordMatcher()
    
    # 保存配置
    print("\n💾 保存关键词配置...")
    matcher.save_config()
    print("✅ 配置已保存：" + str(matcher.config_dir / "keyword_config.json"))
    
    # 测试搜索
    print("\n🧪 测试关键词匹配...")
    test_queries = [
        # 国内搜索
        "中国最新科技新闻",
        "国内旅游攻略",
        "国产手机品牌",
        "北京天气预报",
        "华为最新产品",
        
        # 国外搜索
        "US latest technology news",
        "国外旅游景点",
        "国际航班查询",
        "GitHub 使用教程",
        "Google 搜索技巧",
        
        # 默认搜索
        "默认搜索测试",
        "今天天气怎么样",
        "如何学习编程",
        
        # 排除关键词
        "国内国外对比分析"
    ]
    
    print("\n📊 测试结果:\n")
    for query in test_queries:
        result = matcher.execute_search(query)
        print(f"查询：{query}")
        print(f"  类型：{result['search_type']}")
        print(f"  置信度：{result['confidence']:.0%}")
        print(f"  关键词：{', '.join(result['matched_keywords']) if result['matched_keywords'] else '无'}")
        print(f"  匹配级别：{result['match_level'] or '无'}")
        print(f"  原因：{result['reason']}")
        print(f"  路由：{result['route']['search_engine']} ({result['route']['traffic']})")
        print()
    
    # 生成报告
    print("\n📄 生成配置报告...")
    report = matcher.generate_report()
    
    report_path = Path("/home/nicola/.openclaw/workspace/reports/keyword-intelligent-matching.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 配置报告已保存：" + str(report_path))
    
    # 发送 Telegram
    print("\n📱 发送到 Telegram...")
    os.system("python3 /home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py " + str(report_path) + " 2>&1")
    
    print("\n" + "=" * 60)
    print("关键词智能匹配配置完成！")
    print("=" * 60)
    print(f"\n📊 关键词统计:")
    print(f"  国内关键词：{sum(len(v) for v in matcher.domestic_keywords.values())} 个")
    print(f"  国外关键词：{sum(len(v) for v in matcher.international_keywords.values())} 个")
    print(f"  排除关键词：{len(matcher.exclude_keywords)} 个")
    print(f"\n🧠 匹配规则:")
    print(f"  Level 1: 95% 置信度")
    print(f"  Level 2: 80% 置信度")
    print(f"  Level 3: 60% 置信度")


if __name__ == "__main__":
    main()
