#!/usr/bin/env python3
# scripts/check-bailian-quota.py

"""
百炼配额监控脚本

功能：
1. 每 5 分钟检查百炼 API 配额状态
2. 配额耗尽时自动切换到 Gemini
3. 配额恢复时自动切换回百炼
4. 记录状态变更到 JSON 文件

使用：
    python3 scripts/check-bailian-quota.py

Cron：
    */5 * * * * python3 /home/nicola/.openclaw/workspace/scripts/check-bailian-quota.py
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
STATUS_FILE = Path.home() / ".openclaw" / "workspace" / "data" / "model-router-status.json"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "logs" / "model-router.log"
SWITCH_COOLDOWN = 1800  # 30 分钟冷却时间
CONSECUTIVE_FAILURES_THRESHOLD = 3  # 连续失败次数阈值

# API 配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DASHSCOPE_PROBE_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

def load_status() -> dict:
    """加载状态文件"""
    if not STATUS_FILE.exists():
        return {
            "current_model": "qwen3.5-plus",
            "bailian_status": "normal",
            "last_check": None,
            "last_switch_to_gemini": None,
            "last_switch_to_bailian": None,
            "switch_count_today": 0,
            "consecutive_failures": 0,
            "notes": ""
        }
    
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_status(status: dict):
    """保存状态文件"""
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

def log_message(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(log_entry.strip())

def probe_bailian_api() -> tuple:
    """
    探测百炼 API 状态
    
    Returns:
        (success: bool, error_type: str|None)
    """
    if not DASHSCOPE_API_KEY:
        return False, "no_api_key"
    
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 轻量探测请求（最小 token 消耗）
    payload = {
        "model": "qwen3.5-plus",
        "input": {
            "messages": [
                {"role": "user", "content": "Hi"}
            ]
        },
        "parameters": {
            "max_tokens": 10
        }
    }
    
    try:
        response = requests.post(
            DASHSCOPE_PROBE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, None
        elif response.status_code == 429:
            return False, "rate_limit"
        elif response.status_code == 402:
            return False, "quota_exceeded"
        elif response.status_code == 401:
            return False, "auth_error"
        else:
            return False, f"http_{response.status_code}"
    
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.ConnectionError:
        return False, "connection_error"
    except Exception as e:
        return False, f"unknown_{type(e).__name__}"

def switch_to_gemini(status: dict) -> bool:
    """切换到 Gemini"""
    now = datetime.now()
    
    # 检查冷却时间
    if status.get("last_switch_to_gemini"):
        last_switch = datetime.fromisoformat(status["last_switch_to_gemini"])
        if (now - last_switch).total_seconds() < SWITCH_COOLDOWN:
            log_message("⚠️  冷却期内，暂不切换到 Gemini")
            return False
    
    # 执行切换
    old_model = status["current_model"]
    status["current_model"] = "gemini-2.5-pro"
    status["bailian_status"] = "exhausted"
    status["last_switch_to_gemini"] = now.isoformat()
    status["switch_count_today"] = status.get("switch_count_today", 0) + 1
    status["consecutive_failures"] = 0
    
    save_status(status)
    log_message(f"🔄 切换到 Gemini（原因：百炼配额耗尽，今日第{status['switch_count_today']}次切换）")
    
    return True

def switch_to_bailian(status: dict) -> bool:
    """切换回百炼"""
    now = datetime.now()
    
    # 检查冷却时间
    if status.get("last_switch_to_gemini"):
        last_switch = datetime.fromisoformat(status["last_switch_to_gemini"])
        if (now - last_switch).total_seconds() < SWITCH_COOLDOWN:
            log_message("⚠️  冷却期内，暂不切换回百炼")
            return False
    
    # 执行切换
    status["current_model"] = "qwen3.5-plus"
    status["bailian_status"] = "normal"
    status["last_switch_to_bailian"] = now.isoformat()
    status["consecutive_failures"] = 0
    
    save_status(status)
    log_message("✅ 切换回百炼（原因：配额已恢复）")
    
    return True

def check_and_switch():
    """主检查逻辑"""
    status = load_status()
    now = datetime.now()
    
    log_message("=" * 60)
    log_message("🔍 开始检查百炼配额状态")
    log_message(f"当前模型：{status['current_model']}")
    log_message(f"当前状态：{status['bailian_status']}")
    
    # 探测百炼 API
    success, error_type = probe_bailian_api()
    
    log_message(f"探测结果：{'✅ 成功' if success else '❌ 失败'} ({error_type})")
    
    if success:
        # 百炼正常
        status["consecutive_failures"] = 0
        
        if status["bailian_status"] == "exhausted":
            # 之前是耗尽状态，现在恢复了，切换回百炼
            log_message("🎉 百炼配额已恢复，准备切换回百炼")
            switch_to_bailian(status)
        else:
            log_message("✅ 百炼状态正常，保持当前配置")
            status["bailian_status"] = "normal"
    
    else:
        # 百炼失败
        status["consecutive_failures"] = status.get("consecutive_failures", 0) + 1
        log_message(f"连续失败次数：{status['consecutive_failures']}/{CONSECUTIVE_FAILURES_THRESHOLD}")
        
        # 检查是否达到切换阈值
        if status["consecutive_failures"] >= CONSECUTIVE_FAILURES_THRESHOLD:
            if status["current_model"] == "qwen3.5-plus":
                # 当前使用百炼，需要切换到 Gemini
                log_message("🚨 连续失败达到阈值，切换到 Gemini")
                switch_to_gemini(status)
            else:
                log_message("⚠️  已在使用 Gemini，保持当前配置")
        else:
            log_message("⚠️  失败次数未达阈值，暂不切换")
        
        # 更新状态
        if error_type in ["quota_exceeded", "rate_limit"]:
            status["bailian_status"] = "warning"
    
    # 更新最后检查时间
    status["last_check"] = now.isoformat()
    save_status(status)
    
    log_message("=" * 60)
    log_message(f"最终状态：current_model={status['current_model']}, bailian_status={status['bailian_status']}")
    
    return status

if __name__ == "__main__":
    try:
        status = check_and_switch()
        print(f"\n📊 当前配置:")
        print(f"  模型：{status['current_model']}")
        print(f"  百炼状态：{status['bailian_status']}")
        print(f"  最后检查：{status['last_check']}")
        sys.exit(0)
    except Exception as e:
        log_message(f"❌ 检查失败：{e}")
        sys.exit(1)
