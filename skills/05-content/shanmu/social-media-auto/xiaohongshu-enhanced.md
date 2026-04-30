# P1 · 小红书自动发布增强方案

**版本**: v0.1  
**创建**: 2026-03-25 16:26  
**执行**: 山木 + 素问  
**优先级**: P1（高）

---

## 🎯 目标

增强小红书自动发布能力，实现免登录、批量发布、智能配图。

---

## 📋 现状分析

### 当前流程（山木 Bot）

```
1. 生成内容 → 2. 手动打开小红书 → 3. 复制粘贴 → 4. 手动发布
```

**痛点**:
- ❌ 每次需重新登录
- ❌ 手动复制粘贴（低效）
- ❌ 无法批量发布
- ❌ 配图需手动上传

---

## 🚀 增强方案

### 方案 A：浏览器自动化（Playwright）

**原理**: 使用 Playwright 控制浏览器，自动完成发布流程

**流程**:
```
1. 加载 Cookie（复用登录状态）
   ↓
2. 打开小红书发布页面
   ↓
3. 自动填入标题/内容
   ↓
4. 自动上传图片
   ↓
5. 点击发布（或等待人工确认）
```

**代码框架**:
```python
from playwright.sync_api import sync_playwright

class XiaohongshuPublisher:
    def __init__(self):
        self.cookie_file = Path.home() / ".taiyi" / "cookies" / "xiaohongshu.json"
    
    def load_cookie(self):
        """加载小红书登录 Cookie"""
        # 同微信方案，复用人类登录状态
    
    def publish(self, title, content, images=[]):
        """发布小红书笔记"""
        browser = self.connect()
        page = browser.new_page()
        
        # 访问发布页面
        page.goto("https://creator.xiaohongshu.com/publish")
        
        # 填入标题
        page.fill('.title-input', title)
        
        # 填入内容
        page.fill('.content-textarea', content)
        
        # 上传图片
        if images:
            page.set_input_files('.upload-input', images)
        
        # 发布（或等待确认）
        # page.click('.publish-button')
        
        return True
```

---

### 方案 B：API 逆向（不推荐）

**原理**: 逆向小红书 API，直接调用发布接口

**风险**:
- 🔴 违反平台条款
- 🔴 账号封禁风险
- 🔴 技术维护成本高

**决策**: ❌ 不采用

---

### 方案 C：RPA 工具（备选）

**原理**: 使用影刀/UiPath 等 RPA 工具录制发布流程

**优点**:
- ✅ 无需编程
- ✅ 可视化配置
- ✅ 稳定可靠

**缺点**:
- ⚠️ 需要额外软件
- ⚠️ 灵活性较低

**决策**: 🟡 备选方案

---

## 🔧 实现方案（采用 A 方案）

### Step 1: 创建小红书发布器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/shanmu/social-media-auto/xhs-publisher.py

from playwright.sync_api import sync_playwright
from pathlib import Path
import json

class XiaohongshuPublisher:
    """小红书自动发布器"""
    
    def __init__(self):
        self.cookie_file = Path.home() / ".taiyi" / "cookies" / "xiaohongshu.json"
        self.profile_dir = Path.home() / ".taiyi" / "browser" / "xiaohongshu-profile"
    
    def connect(self):
        """连接浏览器（复用登录状态）"""
        # 方案 A: 连接人类浏览器（CDP）
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ 已连接人类浏览器")
            return browser
        except:
            pass
        
        # 方案 B: 加载 Profile
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=False
        )
        print("✅ 已加载 Profile")
        return browser
    
    def publish(self, title, content, images=[], auto_publish=False):
        """
        发布小红书笔记
        
        Args:
            title: 标题（≤20 字）
            content: 正文（≤1000 字）
            images: 图片列表（最多 9 张）
            auto_publish: 是否自动发布（False=等待人工确认）
        """
        browser = self.connect()
        context = browser.contexts[0]
        
        # 尝试复用已有页面
        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()
        
        # 访问发布页面
        print("📱 访问小红书发布页面...")
        page.goto("https://creator.xiaohongshu.com/publish")
        page.wait_for_timeout(5000)
        
        # 检查登录状态
        if "login" in page.url:
            print("⚠️  未登录，请手动登录")
            page.wait_for_timeout(60000)  # 等待 1 分钟
        
        # 填入标题
        print(f"📝 填入标题：{title}")
        try:
            page.fill('.publish-title-input', title)
        except:
            print("⚠️  标题填入失败，可能页面结构变化")
        
        # 填入内容
        print(f"📝 填入内容：{len(content)}字")
        try:
            page.fill('.publish-textarea', content)
        except:
            print("⚠️  内容填入失败，可能页面结构变化")
        
        # 上传图片
        if images:
            print(f"🖼️  上传 {len(images)} 张图片")
            try:
                page.set_input_files('.upload-input', images)
                page.wait_for_timeout(3000)  # 等待上传
            except:
                print("⚠️  图片上传失败")
        
        # 发布或等待确认
        if auto_publish:
            print("🚀 自动发布...")
            # page.click('.publish-button')  # 暂不自动点击，避免误操作
            print("⚠️  演示模式：未实际点击发布按钮")
        else:
            print("⏸️  等待人工确认发布")
            print("💡  浏览器保持打开，可手动检查后发布")
        
        # 保持浏览器打开
        page.wait_for_timeout(10000)
        
        return True

# 测试
if __name__ == "__main__":
    publisher = XiaohongshuPublisher()
    publisher.publish(
        title="测试笔记",
        content="这是测试内容",
        images=[],
        auto_publish=False
    )
```

---

### Step 2: 集成山木工作流

```python
# ~/.openclaw/workspace/skills/shanmu/xiaohongshu/hot-topic-monitor.py

# 现有热点监控 + 新增自动发布

from .xhs-publisher import XiaohongshuPublisher

def publish_hot_topic(topic, template):
    """发布热点话题"""
    # 生成内容
    title = generate_title(topic)
    content = generate_content(topic, template)
    images = generate_images(topic)
    
    # 发布
    publisher = XiaohongshuPublisher()
    publisher.publish(title, content, images, auto_publish=False)
    
    print(f"✅ 热点内容已填入，等待人工确认")
```

---

### Step 3: 定时任务集成

```bash
# crontab -l

# 小红书热点发布（现有）
0 8 * * * python3 ~/.openclaw/workspace/skills/shanmu/xiaohongshu/hot-topic-monitor.py

# 增强版：自动填入发布页面
0 8 * * * python3 ~/.openclaw/workspace/skills/shanmu/social-media-auto/auto-publish.py --platform xiaohongshu
```

---

## 📊 验收标准

| 指标 | 目标 | 当前 |
|------|------|------|
| 登录状态复用 | ✅ 无需重新登录 | 🟡 待实现 |
| 自动填入 | ✅ 标题 + 内容+ 图片 | 🟡 待实现 |
| 发布时间 | <30 秒/篇 | 🟡 待测试 |
| 人工干预 | 仅确认发布 | 🟡 待实现 |
| 批量发布 | ≥5 篇/次 | 🟡 待实现 |

---

## 🔒 安全控制

### 宪法级审查

1. **内容审查**: 发布前通过负熵法则检查
2. **人类确认**: 默认不自动发布，需人工确认
3. **频率限制**: ≤5 篇/天（防封号）
4. **操作日志**: 所有发布操作记录

### 禁止行为

- ❌ 未经确认自动发布
- ❌ 高频发布（>10 篇/天）
- ❌ 敏感内容
- ❌ 抄袭内容

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-017` | 小红书发布器核心 | 🟡 待执行 | - |
| `TASK-20260325-018` | 山木工作流集成 | 🟡 待执行 | - |
| `TASK-20260325-019` | 定时任务配置 | 🟡 待执行 | - |
| `TASK-20260325-020` | 安全审查 | 🟡 待执行 | - |
| `TASK-20260325-021` | 测试发布 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:26 | 执行 Bot：山木 + 素问*
