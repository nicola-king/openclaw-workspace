#!/bin/bash
# send-report-pdf.sh - Markdown → PDF → Telegram
# Usage: send-report-pdf.sh <markdown_file> [chat_id]

set -e
MD="$1"; CHAT="${2:-7073481596}"
[ ! -f "$MD" ] && { echo "ERR: no file $MD"; exit 1; }

TOKEN=$(python3 -c "
import json
d=json.load(open('/home/sayelf/.openclaw/openclaw.json'))
acct=d.get('channels',{}).get('telegram',{}).get('accounts',{}).get('default',{})
print(acct.get('botToken','')or'')" 2>/dev/null)
[ -z "$TOKEN" ] && { echo "ERR: no token"; exit 1; }

NAME=$(basename "$MD" .md)
PDF="${MD%.*}.pdf"
HTML="${MD%.*}.html"
SITE=$(python3 -c "import site; print(site.getusersitepackages())" 2>/dev/null)

# MD → HTML
PYTHONPATH="$SITE" MD="$MD" HTML="$HTML" python3 << 'PY' 2>&1
import markdown, os
with open(os.environ['MD']) as f: md = f.read()
h = '<html><meta charset=utf-8><style>'
h += 'body{font-family:sans-serif;max-width:780px;margin:30px auto;padding:0 20px;line-height:1.6;color:#333;font-size:14px}'
h += 'h1{color:#1a1a2e;border-bottom:2px solid #e94560;padding-bottom:5px}'
h += 'h2{color:#16213e;border-bottom:1px solid #ddd;padding-bottom:3px;margin-top:22px}'
h += 'code{background:#f4f4f4;padding:2px 5px;border-radius:3px}'
h += 'pre{background:#f4f4f4;padding:10px;border-radius:4px}'
h += 'blockquote{border-left:3px solid #e94560;padding-left:12px;color:#666}'
h += 'table{border-collapse:collapse;width:100%;margin:8px 0}'
h += 'td,th{border:1px solid #ddd;padding:5px 8px;text-align:left;font-size:13px}'
h += 'th{background:#f2f2f2}'
h += '.footer{margin-top:25px;padding-top:8px;border-top:1px solid #eee;font-size:11px;color:#999;text-align:center}'
h += '</style><body>' + markdown.markdown(md, extensions=['extra']) + '</body></html>'
with open(os.environ['HTML'], 'w') as f: f.write(h)
print('HTML OK')
PY

# HTML → PDF
~/.local/bin/weasyprint "$HTML" "$PDF" 2>&1
[ -f "$PDF" ] || { echo "ERR: PDF failed"; exit 1; }
echo "PDF: $(du -h "$PDF" | cut -f1)"

# Send via Telegram
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
    -F "chat_id=${CHAT}" \
    -F "document=@${PDF}" \
    -F "filename=${NAME}.pdf" > /dev/null && echo "Sent ✅"

rm -f "$HTML" "$PDF"
