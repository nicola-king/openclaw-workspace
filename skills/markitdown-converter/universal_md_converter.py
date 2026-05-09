#!/usr/bin/env python3
"""
Universal File-to-Markdown Auto-Converter — 智能自动化转 MD 系统

功能:
  1. 扫描指定目录，识别可转换的非 MD 文件
  2. 自动调用 MarkItDown 转换为 Markdown
  3. 在源文件旁生成 .md 副本（保留原始文件）
  4. 跟踪已转换记录，避免重复劳动
  5. 支持批量/增量/全量三种模式

用法:
  python3 universal_md_converter.py                # 增量扫描（跳过已转的）
  python3 universal_md_converter.py --full         # 全量扫描所有文件
  python3 universal_md_converter.py --dir 路径     # 指定目录
  python3 universal_md_converter.py --watch        # 持续监听（需要 watchdog）
  python3 universal_md_converter.py --status       # 报告系统状态
"""
import os, sys, json, hashlib, time, subprocess, argparse
from datetime import datetime
from pathlib import Path

# ─── 配置 ───────────────────────────────────────────

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEDIA_DIR = os.path.expanduser("~/.openclaw/media")
SKILL_DIR = os.path.join(WORKSPACE, "skills", "markitdown-converter")
STATE_FILE = os.path.join(SKILL_DIR, "converter_state.json")
LOG_FILE = os.path.join(SKILL_DIR, "converter.log")

# MarkItDown 可执行路径
MARKITDOWN_BIN = os.path.expanduser("~/.local/venvs/markitdown/bin/markitdown")
if not os.path.exists(MARKITDOWN_BIN):
    MARKITDOWN_BIN = "markitdown"  # fallback

# 可转换的后缀（扩展名 → 格式名）
CONVERTIBLE_EXTS = {
    ".pdf": "PDF",
    ".docx": "Word",
    ".xlsx": "Excel",
    ".xls": "Excel (old)",
    ".pptx": "PPT",
    ".ppt": "PPT (old)",
    ".html": "HTML",
    ".htm": "HTML",
    ".csv": "CSV",
    ".xml": "XML",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".txt": "Text",
    ".rtf": "Rich Text",
}

# 扫描路径（相对于 WORKSPACE）
SCAN_PATHS = [
    ".",              # workspace 根目录
    "data",           # 数据目录
    "reports",        # 报告目录
    "notes",          # 笔记目录
]

# 排除目录
EXCLUDE_DIRS = [
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "venv-feishu", ".agents", ".cache", ".claude",
]

# 排除文件模式
EXCLUDE_PATTERNS = [
    ".exe", ".dll", ".so", ".dylib", ".bin", ".png", ".jpg",
    ".jpeg", ".gif", ".webp", ".svg", ".ico", ".mp3", ".mp4",
    ".avi", ".mov", ".zip", ".tar", ".gz", ".7z", ".rar",
    ".pyc", ".pyo", ".ttf", ".otf", ".woff", ".woff2",
]


# ─── 状态管理 ───────────────────────────────────────

def load_state():
    """加载转换状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"converted": {}, "skipped_ext": {}, "last_scan": "", "total_converted": 0}

def save_state(state):
    """保存转换状态"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    state["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def log(msg, level="INFO"):
    """统一日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line, file=sys.stderr)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ─── 文件发现 ───────────────────────────────────────

def discover_files(scan_dirs, full_scan=False, state=None):
    """发现需要转换的文件"""
    if state is None:
        state = load_state()
    converted = state.get("converted", {})

    files = []
    for base_dir in scan_dirs:
        abs_dir = os.path.join(WORKSPACE, base_dir) if not os.path.isabs(base_dir) else base_dir
        if not os.path.isdir(abs_dir):
            continue
        for root, dirs, filenames in os.walk(abs_dir):
            # 排除目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS
                       and not any(d.startswith(e) for e in ["venv", ".venv"])]

            for fname in filenames:
                fpath = os.path.join(root, fname)
                ext = os.path.splitext(fname)[1].lower()

                # 跳过不可转换格式
                if ext not in CONVERTIBLE_EXTS or ext in EXCLUDE_PATTERNS:
                    continue

                # 跳过 .md 文件
                if ext == ".md":
                    continue

                # 计算文件指纹
                file_key = _file_key(fpath)

                # 跳过已转换且未变更的（增量模式）
                if not full_scan and file_key in converted:
                    if converted[file_key] == _file_mtime(fpath):
                        continue

                files.append((fpath, ext, file_key))

    return files

def _file_key(path):
    """生成文件唯一标识"""
    rel = os.path.relpath(path, WORKSPACE)
    return rel

def _file_mtime(path):
    """文件修改时间戳"""
    try:
        return os.path.getmtime(path)
    except:
        return 0


# ─── 转换引擎 ───────────────────────────────────────

def convert_file(fpath, ext, state):
    """转换单个文件为 Markdown"""
    base = os.path.splitext(fpath)[0]
    md_path = base + ".md"

    # 如果 .md 已存在且比源文件新，跳过
    if os.path.exists(md_path):
        if os.path.getmtime(md_path) >= os.path.getmtime(fpath):
            return "skipped (newer md exists)"

    # 执行转换
    try:
        result = subprocess.run(
            [MARKITDOWN_BIN, fpath, "-o", md_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and os.path.exists(md_path) and os.path.getsize(md_path) > 0:
            size = os.path.getsize(md_path)
            return f"ok ({_fmt_size(size)})"
        else:
            err = result.stderr.strip()[:200] if result.stderr else "unknown error"
            return f"failed: {err}"
    except subprocess.TimeoutExpired:
        return "failed: timeout"
    except FileNotFoundError:
        return "failed: markitdown not found"
    except Exception as e:
        return f"failed: {str(e)[:200]}"


def _fmt_size(bytes):
    for unit in ["B", "KB", "MB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}GB"


# ─── 扫描与转换主循环 ───────────────────────────────

def run_scan(full_scan=False, scan_dirs=None, report_only=False):
    """执行扫描与转换"""
    if scan_dirs is None:
        scan_dirs = SCAN_PATHS

    state = load_state()
    files = discover_files(scan_dirs, full_scan=full_scan, state=state)

    if not files:
        log("未发现需要转换的文件")
        return

    log(f"发现 {len(files)} 个待转换文件{'（全量）' if full_scan else '（增量）'}")

    results = {"ok": 0, "skipped": 0, "failed": 0}
    for fpath, ext, file_key in files:
        fname = os.path.basename(fpath)
        fmt = CONVERTIBLE_EXTS.get(ext, ext)

        if report_only:
            log(f"  [待转换] {fmt}: {_file_key(fpath)}")
            continue

        status = convert_file(fpath, ext, state)

        if status.startswith("ok"):
            state["converted"][file_key] = _file_mtime(fpath)
            results["ok"] += 1
            log(f"  ✅ [{fmt}] {fname} → {status}")
        elif status.startswith("skipped"):
            state["converted"][file_key] = _file_mtime(fpath)
            results["skipped"] += 1
        else:
            results["failed"] += 1
            log(f"  ❌ [{fmt}] {fname}: {status}")

        # 每转换一个保存一次状态（防中断丢失）
        if not status.startswith("skipped"):
            save_state(state)

    state["total_converted"] = len(state["converted"])
    save_state(state)

    summary = f"转换完成: ✅ {results['ok']} 成功, ⏭ {results['skipped']} 跳过, ❌ {results['failed']} 失败"
    log(summary)
    return results


# ─── 初始化 ─────────────────────────────────────────

def init_system():
    """初始化智能转换系统"""
    os.makedirs(os.path.join(SKILL_DIR, "logs"), exist_ok=True)

    # 检查 MarkItDown 可用性
    try:
        r = subprocess.run([MARKITDOWN_BIN, "--help"], capture_output=True, timeout=10)
        available = r.returncode == 0
    except:
        available = False

    state = load_state()
    info = {
        "status": "ready" if available else "degraded (markitdown not found)",
        "markitdown": MARKITDOWN_BIN,
        "markitdown_ok": available,
        "state_file": STATE_FILE,
        "watch_dirs": SCAN_PATHS,
        "total_converted": len(state.get("converted", {})),
        "last_scan": state.get("last_scan", "never"),
        "version": "1.0",
    }
    return info


# ─── 持续监听（可选）────────────────────────────────

def start_watch():
    """使用 watchdog 持续监听文件变更（需 pip install watchdog）"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        log("需要安装 watchdog: pip install watchdog", "ERROR")
        return

    class MDEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            ext = os.path.splitext(event.src_path)[1].lower()
            if ext in CONVERTIBLE_EXTS:
                log(f"检测到新文件: {event.src_path}")
                run_scan(full_scan=False)

        def on_modified(self, event):
            if event.is_directory:
                return
            ext = os.path.splitext(event.src_path)[1].lower()
            if ext in CONVERTIBLE_EXTS:
                run_scan(full_scan=False)

    observer = Observer()
    for d in SCAN_PATHS:
        path = os.path.join(WORKSPACE, d)
        if os.path.isdir(path):
            observer.schedule(MDEventHandler(), path, recursive=True)
            log(f"监听中: {path}")

    observer.start()
    log("持续监听模式启动（Ctrl+C 停止）")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# ─── CLI ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="智能文件转 MD 转换系统")
    parser.add_argument("--full", action="store_true", help="全量扫描所有文件")
    parser.add_argument("--dir", help="指定扫描目录（可多次使用）", action="append")
    parser.add_argument("--watch", action="store_true", help="持续监听模式（需 watchdog）")
    parser.add_argument("--status", action="store_true", help="报告系统状态")
    parser.add_argument("--report", action="store_true", help="仅报告待转换文件，不执行转换")
    parser.add_argument("--file", help="转换单个文件")
    parser.add_argument("--init", action="store_true", help="初始化转换系统")

    args = parser.parse_args()

    if args.init:
        info = init_system()
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return

    if args.status:
        info = init_system()
        print(f"📊 智能转换系统状态")
        print(f"   状态: {info['status']}")
        print(f"   已转换: {info['total_converted']} 个文件")
        print(f"   上次扫描: {info['last_scan']}")
        print(f"   扫描路径: {len(info['watch_dirs'])} 个")
        # 列出待转换
        run_scan(report_only=True)
        return

    if args.watch:
        init_system()
        start_watch()
        return

    if args.file:
        fpath = args.file
        if not os.path.exists(fpath):
            print(f"❌ 文件不存在: {fpath}", file=sys.stderr)
            sys.exit(1)
        ext = os.path.splitext(fpath)[1].lower()
        if ext not in CONVERTIBLE_EXTS:
            print(f"⚠️ 格式 {ext} 不在已知转换列表，仍尝试...", file=sys.stderr)
        state = load_state()
        result = convert_file(fpath, ext, state)
        print(f"结果: {result}")
        return

    # 默认：增量扫描
    init_system()
    run_scan(full_scan=args.full, scan_dirs=args.dir)


if __name__ == "__main__":
    main()
