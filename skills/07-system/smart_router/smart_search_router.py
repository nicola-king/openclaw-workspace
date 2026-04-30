#!/usr/bin/env python3
"""
智能搜索路由引擎
国内内容搜索 → 国内微软必应 → 国内流量
国外搜索 → Chromium → 代理流量
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SmartSearchRouter:
    """智能搜索路由器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.config_dir = self.workspace / "smart-search-router"
        self.config_dir.mkdir(exist_ok=True)
        
        # 路由规则
        self.routing_rules = {
            'domestic_search': {
                'name': '国内内容搜索',
                'keywords': ['中国', '国内', '中文', '大陆', '内地', 'CN', 'china domestic'],
                'search_engine': 'bing_cn',
                'endpoint': 'https://cn.bing.com',
                'proxy': False,
                'traffic': 'domestic',
                'priority': 1
            },
            'international_search': {
                'name': '国外内容搜索',
                'keywords': ['国外', '国际', '海外', 'US', 'global', 'international'],
                'search_engine': 'chromium',
                'endpoint': 'https://www.google.com',
                'proxy': True,
                'traffic': 'proxy',
                'priority': 2
            },
            'default': {
                'name': '默认搜索',
                'search_engine': 'bing_cn',
                'endpoint': 'https://cn.bing.com',
                'proxy': False,
                'traffic': 'domestic',
                'priority': 3
            }
        }
        
        # 流量配置
        self.traffic_config = {
            'domestic': {
                'name': '国内流量',
                'proxy_enabled': False,
                'proxy_url': None,
                'dns': '114.114.114.114',
                'timeout': 10
            },
            'proxy': {
                'name': '代理流量',
                'proxy_enabled': True,
                'proxy_url': 'http://127.0.0.1:7890',
                'dns': '8.8.8.8',
                'timeout': 30
            }
        }
    
    def detect_search_type(self, query: str) -> str:
        """检测搜索类型"""
        query_lower = query.lower()
        
        # 检测国内搜索关键词
        for keyword in self.routing_rules['domestic_search']['keywords']:
            if keyword.lower() in query_lower:
                return 'domestic_search'
        
        # 检测国外搜索关键词
        for keyword in self.routing_rules['international_search']['keywords']:
            if keyword.lower() in query_lower:
                return 'international_search'
        
        # 默认搜索
        return 'default'
    
    def get_route_config(self, query: str) -> dict:
        """获取路由配置"""
        search_type = self.detect_search_type(query)
        route = self.routing_rules.get(search_type, self.routing_rules['default'])
        traffic = self.traffic_config.get(route['traffic'], self.traffic_config['domestic'])
        
        return {
            'search_type': search_type,
            'route': route,
            'traffic': traffic,
            'timestamp': datetime.now().isoformat()
        }
    
    def execute_search(self, query: str) -> dict:
        """执行搜索"""
        config = self.get_route_config(query)
        
        result = {
            'query': query,
            'search_type': config['search_type'],
            'search_engine': config['route']['search_engine'],
            'endpoint': config['route']['endpoint'],
            'proxy_enabled': config['traffic']['proxy_enabled'],
            'traffic_type': config['route']['traffic'],
            'timestamp': datetime.now().isoformat()
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
        
        # 只保留最近 100 条记录
        logs['searches'] = logs['searches'][-100:]
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def save_config(self):
        """保存配置"""
        config = {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'routing_rules': self.routing_rules,
            'traffic_config': self.traffic_config
        }
        
        with open(self.config_dir / "router_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def generate_report(self) -> str:
        """生成配置报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        report = """# 🔄 智能搜索路由配置

> **更新时间**: """ + timestamp + """  
> **版本**: v1.0

---

## 📋 路由规则

### 1. 国内内容搜索

**触发关键词**:
```
中国，国内，中文，大陆，内地，CN, china domestic
```

**路由配置**:
- search_engine: bing_cn
- endpoint: https://cn.bing.com
- proxy: false
- traffic: domestic

**流量类型**: 国内流量 (不走代理)

---

### 2. 国外内容搜索

**触发关键词**:
```
国外，国际，海外，US, global, international
```

**路由配置**:
- search_engine: chromium
- endpoint: https://www.google.com
- proxy: true
- traffic: proxy

**流量类型**: 代理流量 (走代理)

---

### 3. 默认搜索

**触发条件**: 未匹配到国内/国外关键词

**路由配置**:
- search_engine: bing_cn
- endpoint: https://cn.bing.com
- proxy: false
- traffic: domestic

**流量类型**: 国内流量 (默认)

---

## 🌐 流量配置

### 国内流量

- name: 国内流量
- proxy_enabled: false
- proxy_url: null
- dns: 114.114.114.114
- timeout: 10

### 代理流量

- name: 代理流量
- proxy_enabled: true
- proxy_url: http://127.0.0.1:7890
- dns: 8.8.8.8
- timeout: 30

---

## 📊 使用示例

### 国内搜索示例

查询："中国最新科技新闻"
结果:
- search_type: domestic_search
- search_engine: bing_cn
- proxy_enabled: false
- traffic_type: domestic

### 国外搜索示例

查询："US latest technology news"
结果:
- search_type: international_search
- search_engine: chromium
- proxy_enabled: true
- traffic_type: proxy

---

## 🚀 优势

### 智能切换
- ✅ 自动识别搜索类型
- ✅ 自动选择搜索引擎
- ✅ 自动切换流量类型

### 性能优化
- ✅ 国内搜索走国内流量 (快速)
- ✅ 国外搜索走代理流量 (可访问)
- ✅ 默认配置最优体验

### 灵活配置
- ✅ 关键词可自定义
- ✅ 代理配置可调整
- ✅ 搜索引擎可切换

---

*太一 AGI · 智能搜索路由 v1.0 · """ + timestamp + """*

**🔄 智能搜索路由配置完成！国内/国外自动切换！**
"""
        return report


def main():
    """主函数"""
    print("=" * 60)
    print("智能搜索路由引擎")
    print("=" * 60)
    
    router = SmartSearchRouter()
    
    # 保存配置
    print("\n💾 保存路由配置...")
    router.save_config()
    print("✅ 配置已保存：" + str(router.config_dir / "router_config.json"))
    
    # 测试搜索
    print("\n🔍 测试搜索路由...")
    test_queries = [
        "中国最新科技新闻",
        "US latest technology news",
        "国内旅游攻略",
        "international flight booking",
        "默认搜索测试"
    ]
    
    for query in test_queries:
        result = router.execute_search(query)
        print("\n  查询：" + query)
        print("  类型：" + result['search_type'])
        print("  引擎：" + result['search_engine'])
        print("  代理：" + ('✅' if result['proxy_enabled'] else '❌'))
        print("  流量：" + result['traffic_type'])
    
    # 生成报告
    print("\n📄 生成配置报告...")
    report = router.generate_report()
    
    report_path = Path("/home/nicola/.openclaw/workspace/reports/smart-search-router-config.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 配置报告已保存：" + str(report_path))
    
    # 发送 Telegram
    print("\n📱 发送到 Telegram...")
    os.system("python3 /home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py " + str(report_path) + " 2>&1")
    
    print("\n" + "=" * 60)
    print("智能搜索路由配置完成！")
    print("=" * 60)
    print("\n📊 路由规则:")
    print("  国内搜索：bing_cn (国内流量)")
    print("  国外搜索：chromium (代理流量)")
    print("  默认搜索：bing_cn (国内流量)")


if __name__ == "__main__":
    main()
