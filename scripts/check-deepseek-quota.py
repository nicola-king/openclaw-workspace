#!/usr/bin/env python3
import os, sys, json, requests
from datetime import datetime
from pathlib import Path

STATUS_FILE = Path.home() / ".openclaw/workspace/data/model-router-status.json"
LOG_FILE    = Path.home() / ".openclaw/workspace/logs/model-router.log"
THRESHOLD   = 3
API_KEY     = os.getenv("DEEPSEEK_API_KEY", "sk-668e35356ac24d27801d87e684e8fdd6")
URL         = "https://api.deepseek.com/v1/chat/completions"
PRIMARY     = "deepseek-v4-flash"
SECONDARY   = "deepseek-v4-pro"
FALLBACK    = "bailian/qwen3.5-plus"

def load():
    if not STATUS_FILE.exists():
        return {"current_model": PRIMARY, "deepseek_status": "normal",
                "last_check": None, "last_switch_at": None,
                "switch_count_today": 0, "consecutive_failures": 0, "notes": ""}
    return json.loads(STATUS_FILE.read_text())

def save(s):
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2))

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

def probe(model):
    try:
        r = requests.post(URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5},
            timeout=15)
        if r.status_code == 200:
            return True, None
        if r.status_code == 429:
            return False, "quota_exceeded" if "quota" in r.text.lower() else "rate_limit"
        if r.status_code == 402:
            return False, "quota_exceeded"
        if r.status_code == 401:
            return False, "auth_error"
        return False, f"http_{r.status_code}"
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.ConnectionError:
        return False, "connection_error"
    except Exception as e:
        return False, f"unknown_{type(e).__name__}"

def main():
    s = load()
    now = datetime.now()
    log("=" * 60)
    log(f"DeepSeek监控 | 当前:{s['current_model']} | 状态:{s['deepseek_status']}")

    ok, err = probe(PRIMARY)
    log(f"探测 {PRIMARY}: {'成功' if ok else '失败(' + str(err) + ')'}")

    if ok:
        s["consecutive_failures"] = 0
        if s["deepseek_status"] in ("exhausted", "secondary"):
            s["current_model"] = PRIMARY
            s["deepseek_status"] = "normal"
            s["notes"] = "恢复，切回主模型"
            save(s)
            log(f"切回主模型 {PRIMARY}")
        else:
            s["deepseek_status"] = "normal"
            log("状态正常")
    else:
        s["consecutive_failures"] = s.get("consecutive_failures", 0) + 1
        log(f"连续失败:{s['consecutive_failures']}/{THRESHOLD}")
        if s["consecutive_failures"] >= THRESHOLD:
            cur = s["current_model"]
            if cur == PRIMARY:
                ok2, err2 = probe(SECONDARY)
                log(f"探测 {SECONDARY}: {'成功' if ok2 else '失败(' + str(err2) + ')'}")
                if ok2:
                    s["current_model"] = SECONDARY
                    s["deepseek_status"] = "secondary"
                    s["last_switch_at"] = now.isoformat()
                    s["switch_count_today"] = s.get("switch_count_today", 0) + 1
                    s["consecutive_failures"] = 0
                    s["notes"] = "Flash失败，切Pro"
                    save(s)
                    log(f"切换到 {SECONDARY}")
                else:
                    s["current_model"] = FALLBACK
                    s["deepseek_status"] = "exhausted"
                    s["last_switch_at"] = now.isoformat()
                    s["switch_count_today"] = s.get("switch_count_today", 0) + 1
                    s["consecutive_failures"] = 0
                    s["notes"] = "Flash和Pro均失败，切百炼兜底"
                    save(s)
                    log("Flash和Pro均失败，切换百炼兜底")
            elif cur == SECONDARY:
                s["current_model"] = FALLBACK
                s["deepseek_status"] = "exhausted"
                s["last_switch_at"] = now.isoformat()
                s["consecutive_failures"] = 0
                s["notes"] = "Pro失败，切百炼兜底"
                save(s)
                log("Pro失败，切换百炼兜底")
            else:
                log("已在兜底模型，保持")
        else:
            log("未达阈值，暂不切换")
            s["deepseek_status"] = "warning"

    s["last_check"] = now.isoformat()
    save(s)
    log(f"完成 model={s['current_model']} status={s['deepseek_status']}")
    log("=" * 60)
    return s

if __name__ == "__main__":
    try:
        s = main()
        print(f"模型:{s['current_model']} 状态:{s['deepseek_status']}")
    except Exception as e:
        print(f"失败:{e}")
        sys.exit(1)
