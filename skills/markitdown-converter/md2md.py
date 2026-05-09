#!/usr/bin/env python3
"""
MarkItDown 包装器 — 文件转 Markdown

用法:
  md2md 文档.pdf                        # 转换并输出到 stdout
  md2md 文档.pdf -o 文档.md              # 输出到文件
  md2md 文档.docx 表格.xlsx              # 批量转换
  md2md https://example.com             # 网页抓取转 md
"""
import os, sys, subprocess, tempfile, argparse, json

VENV_PYTHON = os.path.expanduser("~/.local/venvs/markitdown/bin/python3")
VENV_MARKITDOWN = os.path.expanduser("~/.local/venvs/markitdown/bin/markitdown")

# 如果 venv 不存在，回退到系统
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable
    VENV_MARKITDOWN = "markitdown"


def convert_file(input_path, output_path=None, llm_desc=False):
    """转换单个文件"""
    if not os.path.exists(input_path):
        # 尝试当 URL 处理
        return convert_url(input_path, output_path)

    input_path = os.path.abspath(input_path)

    if output_path:
        cmd = [VENV_MARKITDOWN, input_path, "-o", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size = os.path.getsize(output_path)
            print(f"✅ {os.path.basename(input_path)} → {os.path.basename(output_path)} ({_fmt_size(size)})")
            return True
        else:
            print(f"❌ {os.path.basename(input_path)}: {result.stderr.strip()}", file=sys.stderr)
            return False
    else:
        cmd = [VENV_MARKITDOWN, input_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"❌ {os.path.basename(input_path)}: {result.stderr.strip()}", file=sys.stderr)
            return False


def convert_url(url, output_path=None):
    """用 scraper 抓取网页转 md"""
    scraper = os.path.expanduser("~/.openclaw/workspace/scripts/scraper.sh")
    if not os.path.exists(scraper):
        print("❌ 需要 scripts/scraper.sh 来抓取网页", file=sys.stderr)
        return False

    result = subprocess.run(
        ["bash", scraper, "fetch", url],
        capture_output=True, text=True, timeout=30
    )
    content = result.stdout or result.stderr

    if output_path:
        with open(output_path, "w") as f:
            f.write(content)
        size = len(content)
        print(f"✅ {url} → {os.path.basename(output_path)} ({_fmt_size(size)})")
    else:
        print(content)
    return True


def _fmt_size(bytes):
    for unit in ["B", "KB", "MB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}GB"


def main():
    parser = argparse.ArgumentParser(description="MarkItDown 包装器 — 文件转 Markdown")
    parser.add_argument("input", nargs="+", help="输入文件或 URL")
    parser.add_argument("-o", "--output", help="输出文件（单文件时）")
    parser.add_argument("--llm-desc", action="store_true", help="启用 LLM 图片描述（需配 API Key）")
    parser.add_argument("--list-formats", action="store_true", help="列出支持的格式")

    args = parser.parse_args()

    if args.list_formats:
        print("""支持的格式:
  PDF        .pdf
  Word       .docx
  Excel      .xlsx
  PPT        .pptx
  HTML       .html / .htm
  Text       .txt / .csv / .json / .xml / .yaml
  Markdown   .md（原样输出）
  图片描述  .jpg / .png / .gif / .webp（需 --llm-desc）
  音频转写  .mp3 / .wav / .m4a（需 Whisper）
  URL        网页地址（自动抓取）""")
        return

    if len(args.input) == 1 and args.output:
        convert_file(args.input[0], args.output, args.llm_desc)
    else:
        for path in args.input:
            convert_file(path)


if __name__ == "__main__":
    main()
