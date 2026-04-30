# Browser Automation Skill

> 太一 AGI v5.0 · 智能浏览器自动化

基于 Playwright 的浏览器自动化技能，支持网页导航、交互、截图、数据采集等功能。

---

## 🚀 快速开始

### 安装依赖

```bash
cd /home/nicola/.openclaw/workspace/skills/browser-automation
pip3 install -r requirements.txt
playwright install chromium
```

### 基本使用

```bash
# 打开网页
python3 browser_automation.py open https://github.com

# 截图
python3 browser_automation.py screenshot github.png

# 提取标题
python3 browser_automation.py eval "document.title"
```

---

## 📋 功能列表

| 类别 | 功能 | 命令 |
|------|------|------|
| **导航** | 打开/关闭/导航 | `open`, `close`, `navigate` |
| **交互** | 点击/填写/选择 | `click`, `fill`, `select` |
| **截图** | 页面/元素/PDF | `screenshot`, `pdf` |
| **采集** | 文本/HTML/链接 | `text`, `html`, `links` |
| **高级** | JS 执行/等待 | `eval`, `wait` |

---

## 📖 使用示例

### 示例 1: 打开网页并截图

```python
from browser_automation import BrowserAutomation

ba = BrowserAutomation()
ba.start()
ba.open('https://github.com')
ba.screenshot('github.png', full_page=True)
ba.close()
```

### 示例 2: 自动登录

```python
ba = BrowserAutomation()
ba.start()
ba.open('https://twitter.com/login')
ba.fill('#username', 'myuser')
ba.fill('#password', 'mypass')
ba.click('#login-btn')
ba.wait('.timeline')
ba.screenshot('logged-in.png')
ba.close()
```

### 示例 3: 数据采集

```python
ba = BrowserAutomation(headless=True)
ba.start()
ba.open('https://news.ycombinator.com')
titles = ba.text('.titleline > a', all=True)
print(titles)
ba.close()
```

---

## 🎯 与太一集成

通过自然语言触发：

```
用户：打开 GitHub 并截图
太一：✅ 已打开 GitHub，截图保存到 ~/screenshot.png

用户：抓取 Hacker News 标题
太一：✅ 已提取 30 个标题：
1. Show HN: ...
2. ...
```

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [Playwright 官方文档](https://playwright.dev)

---

*太一 AGI v5.0 | Browser Automation Skill v1.0*
