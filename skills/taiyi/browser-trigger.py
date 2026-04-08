#!/usr/bin/env python3
# Browser Automation 自然语言触发器 - 太一 AGI
import subprocess, sys, re

BROWSER_CLI = "/home/nicola/.openclaw/workspace/skills/browser-automation/browser-cli.sh"

def parse_command(text: str) -> dict:
    text = text.lower().strip()
    result = {"action": None, "url": None, "selector": None, "params": {}}
    
    if any(kw in text for kw in ["打开", "访问", "open"]):
        result["action"] = "open"
        url_match = re.search(r'(https?://[^\s]+)', text)
        if url_match: result["url"] = url_match.group(1)
    elif any(kw in text for kw in ["截图", "screenshot"]):
        result["action"] = "screenshot"
    elif any(kw in text for kw in ["提取", "extract"]):
        result["action"] = "extract" if "链接" not in text else "extract-links"
    elif any(kw in text for kw in ["点击", "click"]):
        result["action"] = "click"
    
    return result

def execute(parsed: dict) -> str:
    if not parsed["action"]: return "❌ 无法识别命令"
    cmd = [BROWSER_CLI, parsed["action"]]
    if parsed["url"]: cmd.append(parsed["url"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except Exception as e: return f"❌ 错误：{e}"

if __name__ == "__main__":
    if len(sys.argv) < 2: print("用法：python3 browser-trigger.py <命令>"); sys.exit(1)
    parsed = parse_command(" ".join(sys.argv[1:]))
    print(execute(parsed))
