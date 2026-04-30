# P0 · 微信免登录复用方案

**版本**: v0.1  
**创建**: 2026-03-25 16:26  
**执行**: 太一 + 素问  
**优先级**: P0（最高）

---

## 🎯 目标

复用人类已登录的微信浏览器状态，避免每次访问微信公众号/后台时重新登录。

---

## 📋 技术方案

### 方案 A：浏览器 Cookie 共享（推荐）

**原理**: 导出人类微信登录的 Cookie，导入到 Agent 浏览器会话

**步骤**:
1. 人类登录微信公众号后台 (mp.weixin.qq.com)
2. 使用浏览器插件导出 Cookie
3. 保存为 `~/.taiyi/cookies/wechat-mp.json`
4. Agent 启动浏览器时加载 Cookie
5. 直接访问，无需登录

**优点**:
- ✅ 简单直接
- ✅ 无需额外依赖
- ✅ 人类可控（随时更新 Cookie）

**缺点**:
- ⚠️ Cookie 有有效期（需定期更新）
- ⚠️ 需要人类首次手动导出

---

### 方案 B：浏览器 Profile 共享

**原理**: 人类和 Agent 共用同一个浏览器 Profile

**步骤**:
1. 创建专用浏览器 Profile: `~/.taiyi/browser/wechat-profile`
2. 人类用此 Profile 登录微信
3. Agent 启动时复用此 Profile
4. 共享登录状态

**优点**:
- ✅ 登录状态持久
- ✅ 无需手动导出 Cookie
- ✅ 人类可手动干预

**缺点**:
- ⚠️ 需要浏览器支持多 Profile
- ⚠️ 人类和 Agent 不能同时操作

---

### 方案 C：浏览器 CDP 远程控制（web-access 方案）

**原理**: 人类浏览器开启远程调试端口，Agent 通过 CDP 协议控制

**步骤**:
1. 人类浏览器启动时开启远程调试:
   ```bash
   chromium --remote-debugging-port=9222
   ```
2. Agent 通过 CDP 协议连接:
   ```python
   from playwright.sync_api import sync_playwright
   
   with sync_playwright() as p:
       browser = p.chromium.connect_over_cdp("http://localhost:9222")
       page = browser.pages[0]  # 复用人类已打开的页面
   ```
3. 直接复用人类的登录状态

**优点**:
- ✅ 完全共享人类浏览器
- ✅ 无需额外配置
- ✅ 实时同步

**缺点**:
- ⚠️ 人类浏览器需保持运行
- ⚠️ 需要固定端口

---

## 🔧 实现方案（采用 C + B 混合）

**决策**: 采用 **方案 C（CDP 远程控制）** 为主，**方案 B（Profile 共享）** 为备选

### 实施步骤

#### Step 1: 创建浏览器启动脚本

```bash
#!/bin/bash
# ~/.taiyi/scripts/browser-launch.sh

PROFILE_DIR="$HOME/.taiyi/browser/wechat-profile"
mkdir -p "$PROFILE_DIR"

# 启动浏览器（开启远程调试）
chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  &

echo "浏览器已启动，CDP 端口：9222"
echo "Profile 目录：$PROFILE_DIR"
```

#### Step 2: 创建 Cookie 导出工具

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/browser-cdp/export-cookie.py

import json
from playwright.sync_api import sync_playwright

def export_wechat_cookie():
    """导出微信公众号登录 Cookie"""
    with sync_playwright() as p:
        # 连接人类浏览器
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # 访问微信公众号后台
        page.goto("https://mp.weixin.qq.com")
        page.wait_for_timeout(5000)
        
        # 获取 Cookie
        cookies = context.cookies()
        wechat_cookies = [c for c in cookies if 'weixin' in c.get('domain', '') or 'qq' in c.get('domain', '')]
        
        # 保存
        with open("$HOME/.taiyi/cookies/wechat-mp.json", "w") as f:
            json.dump(wechat_cookies, f, indent=2)
        
        print(f"✅ 已导出 {len(wechat_cookies)} 个 Cookie")
        return wechat_cookies

if __name__ == "__main__":
    export_wechat_cookie()
```

#### Step 3: 创建 Agent 浏览器启动器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/browser-cdp/agent-browser.py

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

class WechatBrowser:
    """微信浏览器（复用人类登录状态）"""
    
    def __init__(self):
        self.cdp_url = "http://localhost:9222"
        self.cookie_file = Path.home() / ".taiyi" / "cookies" / "wechat-mp.json"
    
    def connect_to_human(self):
        """连接人类浏览器（方案 C）"""
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.connect_over_cdp(self.cdp_url)
            print("✅ 已连接人类浏览器")
            return browser
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return None
    
    def load_profile(self):
        """加载共享 Profile（方案 B）"""
        profile_dir = Path.home() / ".taiyi" / "browser" / "wechat-profile"
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=False
            )
            print("✅ 已加载共享 Profile")
            return browser
        except Exception as e:
            print(f"❌ 加载失败：{e}")
            return None
    
    def get_page(self, url="https://mp.weixin.qq.com"):
        """获取页面（优先连接人类，失败则加载 Profile）"""
        # 尝试连接人类浏览器
        browser = self.connect_to_human()
        if browser:
            context = browser.contexts[0]
            if context.pages:
                page = context.pages[0]
                page.goto(url)
                return page
        
        # 备选：加载 Profile
        browser = self.load_profile()
        if browser:
            page = browser.new_page()
            page.goto(url)
            return page
        
        raise Exception("无法获取浏览器会话")
    
    def publish_article(self, title, content):
        """发布微信公众号文章"""
        page = self.get_page()
        
        # 导航到发布页面
        page.goto("https://mp.weixin.qq.com/cgi-bin/appmsg")
        page.wait_for_timeout(2000)
        
        # 点击新建按钮
        page.click('text=新建')
        page.wait_for_timeout(1000)
        
        # 选择图文消息
        page.click('text=图文消息')
        page.wait_for_timeout(3000)
        
        # 填写标题
        page.fill('#title', title)
        
        # 填写内容（简化版，实际需要处理富文本编辑器）
        page.frame_locator('#edui23_body iframe').locator('body').fill(content)
        
        print("✅ 文章已填入，等待人工确认发布")
        return True

# 测试
if __name__ == "__main__":
    browser = WechatBrowser()
    page = browser.get_page()
    print("浏览器已就绪")
```

---

## 📋 使用流程

### 首次配置

```bash
# 1. 启动人类浏览器（开启 CDP）
~/.taiyi/scripts/browser-launch.sh

# 2. 手动登录微信公众号后台
# 在浏览器中访问 https://mp.weixin.qq.com 并登录

# 3. 测试 Agent 连接
python3 ~/.openclaw/workspace/skills/taiyi/browser-cdp/agent-browser.py
```

### 日常使用

```bash
# 人类先启动浏览器
~/.taiyi/scripts/browser-launch.sh

# Agent 自动复用（无需登录）
python3 ~/.openclaw/workspace/skills/taiyi/browser-cdp/agent-browser.py
```

---

## 🔒 安全控制

### 宪法级审查

1. **权限最小化**: 仅访问微信公众号相关域名
2. **操作审计**: 所有浏览器操作记录日志
3. **人类确认**: 发布文章前需人类确认
4. **Cookie 加密**: 敏感 Cookie 本地加密存储

### 禁止行为

- ❌ 访问非授权网站
- ❌ 修改人类浏览器设置
- ❌ 删除人类 Cookie
- ❌ 未经确认发布内容

---

## 📊 验收标准

| 指标 | 目标 | 当前 |
|------|------|------|
| 登录状态复用 | ✅ 无需重新登录 | 🟡 待实现 |
| 连接成功率 | >95% | 🟡 待测试 |
| 操作延迟 | <3 秒 | 🟡 待测试 |
| 人类干预频率 | <1 次/天 | 🟡 待测试 |

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-011` | 浏览器启动脚本 | 🟡 待执行 | - |
| `TASK-20260325-012` | Cookie 导出工具 | 🟡 待执行 | - |
| `TASK-20260325-013` | Agent 浏览器启动器 | 🟡 待执行 | - |
| `TASK-20260325-014` | 微信公众号发布测试 | 🟡 待执行 | - |
| `TASK-20260325-015` | 安全审查 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:26 | 执行 Bot：太一 + 素问*
