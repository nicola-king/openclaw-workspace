#!/bin/bash
# md2md — MarkItDown 快捷命令
# Usage: md2md 文档.pdf -o 文档.md

DIR="$(cd "$(dirname "$0")" && pwd)"
# 如果通过 symlink 调用，追溯到真实路径
if [ -L "$0" ]; then
    DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
fi
python3 "$DIR/md2md.py" "$@"
