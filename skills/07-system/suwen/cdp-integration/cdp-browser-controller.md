# P3 · CDP 协议深度集成方案

**版本**: v0.1  
**创建**: 2026-03-25 16:26  
**执行**: 素问  
**优先级**: P3（中长期）

---

## 🎯 目标

深度集成 Chrome DevTools Protocol (CDP)，实现完整的浏览器控制能力。

---

## 📋 CDP 协议简介

### 什么是 CDP？

**Chrome DevTools Protocol** 是 Chrome/Chromium 的底层控制协议，允许外部程序：
- 控制浏览器行为
- 拦截网络请求
- 操作 DOM
- 执行 JavaScript
- 获取性能数据
- 调试页面

### 为什么选择 CDP？

| 特性 | Playwright/Selenium | CDP 原生 |
|------|-------------------|---------|
| 控制粒度 | 高层 API | 底层精细控制 |
| 性能 | 中等 | 最优 |
| 功能覆盖 | 80% | 100% |
| 学习曲线 | 低 | 中等 |
| 灵活性 | 受限 | 完全灵活 |

**决策**: Playwright 作为高层封装（易用），CDP 作为底层补充（强大）

---

## 🔧 技术方案

### 方案架构

```
太一浏览器控制体系
├── 高层：Playwright（日常任务）
│   ├── 页面导航
│   ├── 表单填写
│   └── 截图录屏
│
└── 底层：CDP 原生协议（高级任务）
    ├── 网络拦截
    ├── 性能分析
    ├── JavaScript 注入
    └── 浏览器配置
```

---

### 核心功能实现

#### 1. 浏览器远程控制

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/cdp-integration/remote-control.py

import requests
import json

class CDPBrowserController:
    """CDP 浏览器控制器"""
    
    def __init__(self, cdp_url="http://localhost:9222"):
        self.cdp_url = cdp_url
        self.session_id = None
    
    def get_version(self):
        """获取浏览器版本信息"""
        response = requests.get(f"{self.cdp_url}/json/version")
        return response.json()
    
    def get_targets(self):
        """获取所有目标页面"""
        response = requests.get(f"{self.cdp_url}/json/list")
        return response.json()
    
    def create_target(self, url):
        """创建新页面"""
        response = requests.get(f"{self.cdp_url}/json/new?{url}")
        return response.json()
    
    def close_target(self, target_id):
        """关闭页面"""
        response = requests.get(f"{self.cdp_url}/json/close/{target_id}")
        return response.json()
    
    def send_command(self, target_id, method, params=None):
        """发送 CDP 命令"""
        # 获取 WebSocket URL
        targets = self.get_targets()
        target = next((t for t in targets if t['id'] == target_id), None)
        if not target:
            raise Exception(f"Target {target_id} not found")
        
        ws_url = target['webSocketDebuggerUrl']
        
        # 通过 WebSocket 发送命令（需要使用 websocket 库）
        import websocket
        
        ws = websocket.create_connection(ws_url)
        
        # 构建命令
        command = {
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        ws.send(json.dumps(command))
        result = ws.recv()
        ws.close()
        
        return json.loads(result)
    
    # ========== 高级功能 ==========
    
    def intercept_network(self, target_id, url_pattern):
        """拦截网络请求"""
        return self.send_command(target_id, "Network.enable")
    
    def inject_javascript(self, target_id, script):
        """注入 JavaScript"""
        return self.send_command(target_id, "Runtime.evaluate", {
            "expression": script
        })
    
    def take_screenshot(self, target_id):
        """截图"""
        result = self.send_command(target_id, "Page.captureScreenshot", {
            "format": "png"
        })
        return result['result']['data']  # Base64 图片数据
    
    def get_performance(self, target_id):
        """获取性能数据"""
        self.send_command(target_id, "Performance.enable")
        result = self.send_command(target_id, "Performance.getMetrics")
        return result['result']['metrics']


# 测试
if __name__ == "__main__":
    controller = CDPBrowserController()
    
    # 获取浏览器信息
    version = controller.get_version()
    print(f"浏览器版本：{version['Browser']}")
    
    # 获取所有页面
    targets = controller.get_targets()
    print(f"打开的页面数：{len(targets)}")
    
    # 创建新页面
    new_target = controller.create_target("https://www.baidu.com")
    print(f"新页面 ID: {new_target['id']}")
```

---

#### 2. 网络请求拦截

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/cdp-integration/network-interceptor.py

import websocket
import json
import threading

class NetworkInterceptor:
    """网络请求拦截器（用于监控/修改请求）"""
    
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.ws = None
        self.request_handler = None
        self.response_handler = None
    
    def connect(self):
        """连接到 CDP"""
        self.ws = websocket.create_connection(self.ws_url)
        
        # 启用 Network 域
        self.send_command("Network.enable")
        
        # 启动监听线程
        thread = threading.Thread(target=self._listen)
        thread.daemon = True
        thread.start()
    
    def send_command(self, method, params=None):
        """发送 CDP 命令"""
        command = {
            "id": 1,
            "method": method,
            "params": params or {}
        }
        self.ws.send(json.dumps(command))
    
    def _listen(self):
        """监听 CDP 事件"""
        while True:
            message = self.ws.recv()
            data = json.loads(message)
            
            # 处理事件
            if 'method' in data:
                method = data['method']
                params = data.get('params', {})
                
                if method == 'Network.requestWillBeSent':
                    if self.request_handler:
                        self.request_handler(params)
                
                elif method == 'Network.responseReceived':
                    if self.response_handler:
                        self.response_handler(params)
    
    def set_request_handler(self, handler):
        """设置请求处理函数"""
        self.request_handler = handler
    
    def set_response_handler(self, handler):
        """设置响应处理函数"""
        self.response_handler = handler


# 使用示例
if __name__ == "__main__":
    # 获取 WebSocket URL（从 CDP /json/list 接口）
    ws_url = "ws://localhost:9222/devtools/page/xxx"
    
    interceptor = NetworkInterceptor(ws_url)
    interceptor.connect()
    
    # 设置请求处理函数
    def on_request(params):
        print(f"📡 请求：{params['request']['url']}")
    
    def on_response(params):
        print(f"📥 响应：{params['response']['status']}")
    
    interceptor.set_request_handler(on_request)
    interceptor.set_response_handler(on_response)
    
    # 保持运行
    import time
    while True:
        time.sleep(1)
```

---

#### 3. 性能监控

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/cdp-integration/performance-monitor.py

import websocket
import json
from datetime import datetime

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.metrics = {}
    
    def connect(self):
        """连接到 CDP"""
        self.ws = websocket.create_connection(self.ws_url)
        self.send_command("Performance.enable")
    
    def send_command(self, method, params=None):
        """发送 CDP 命令"""
        command = {
            "id": 1,
            "method": method,
            "params": params or {}
        }
        self.ws.send(json.dumps(command))
        result = self.ws.recv()
        return json.loads(result)
    
    def get_metrics(self):
        """获取性能指标"""
        result = self.send_command("Performance.getMetrics")
        self.metrics = {
            m['name']: m['value']
            for m in result['result']['metrics']
        }
        return self.metrics
    
    def report(self):
        """生成性能报告"""
        metrics = self.get_metrics()
        
        report = f"""
📊 性能报告 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━
文档加载时间：{metrics.get('DomContentLoaded', 0):.2f}s
页面加载时间：{metrics.get('LoadEventEnd', 0):.2f}s
DOM 节点数：{metrics.get('Nodes', 0):.0f}
JS 堆内存：{metrics.get('JSHeapUsedSize', 0) / 1024 / 1024:.2f} MB
━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(report)
        return report


# 使用示例
if __name__ == "__main__":
    ws_url = "ws://localhost:9222/devtools/page/xxx"
    monitor = PerformanceMonitor(ws_url)
    monitor.connect()
    monitor.report()
```

---

## 🔗 太一集成路径

### 阶段 1: 基础集成（本周）

- [ ] 安装 CDP 依赖库
- [ ] 创建浏览器启动脚本
- [ ] 测试基础连接

### 阶段 2: 功能增强（下周）

- [ ] 网络拦截集成到罔两 Bot
- [ ] 性能监控集成到素问 Bot
- [ ] 截图功能集成到山木 Bot

### 阶段 3: 深度优化（本月）

- [ ] 三层通道调度实现
- [ ] 并行处理优化
- [ ] 安全审查机制

---

## 📊 验收标准

| 指标 | 目标 | 当前 |
|------|------|------|
| CDP 连接成功率 | >95% | 🟡 待测试 |
| 网络拦截延迟 | <100ms | 🟡 待测试 |
| 性能数据准确性 | >99% | 🟡 待测试 |
| 浏览器控制粒度 | 100% CDP 覆盖 | 🟡 部分 |

---

## 🔒 安全控制

### 宪法级审查

1. **权限控制**: 仅允许访问授权域名
2. **操作审计**: 所有 CDP 命令记录日志
3. **人类确认**: 敏感操作需人工确认
4. **数据加密**: 敏感数据本地加密

### 禁止行为

- ❌ 访问非授权网站
- ❌ 拦截敏感信息（密码/支付）
- ❌ 修改人类浏览器设置
- ❌ 未经确认执行敏感操作

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-022` | CDP 依赖安装 | 🟡 待执行 | - |
| `TASK-20260325-023` | 基础控制器实现 | 🟡 待执行 | - |
| `TASK-20260325-024` | 网络拦截器实现 | 🟡 待执行 | - |
| `TASK-20260325-025` | 性能监控器实现 | 🟡 待执行 | - |
| `TASK-20260325-026` | 太一集成测试 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:26 | 执行 Bot：素问*
