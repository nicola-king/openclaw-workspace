#!/bin/bash
# OpenOCR CLI Wrapper for OpenClaw tools.media
# Fast CPU-based OCR for inbound images - ~0.2s per image
# Architecture: OpenClaw detects image → calls this → OCR text → DeepSeek

IMAGE_PATH="$1"
VENV_PYTHON="/home/sayelf/.venvs/vlm/bin/python3"

if [ ! -f "$IMAGE_PATH" ]; then
    echo "[OCR] 图片不存在: $IMAGE_PATH"
    exit 1
fi

$VENV_PYTHON -c "
import sys, json
sys.path.insert(0, '/home/sayelf/.venvs/vlm/lib/python3.14/site-packages')
from openocr import OpenOCR

try:
    engine = OpenOCR(task='ocr', backend='onnx')
    results, time_dicts = engine(image_path='$IMAGE_PATH')
    
    # results[0] = filename + tab + JSON array
    json_str = results[0].split('\t')[-1]
    items = json.loads(json_str)
    lines = []
    for item in items:
        text = item.get('transcription', '').strip()
        score = item.get('score', 0)
        if text:
            lines.append(f'[{score:.0%}] {text}')
    
    if lines:
        print('【OCR 识别结果】')
        for l in lines:
            print(l)
    else:
        print('【未检测到文字】')
except Exception as e:
    print(f'[OCR错误] {e}')
    sys.exit(1)
" 2>/dev/null

exit $?
