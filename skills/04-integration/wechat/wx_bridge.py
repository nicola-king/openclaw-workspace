#!/usr/bin/env python3
import hashlib, xml.etree.ElementTree as ET, time, requests
from flask import Flask, request, make_response

app = Flask(__name__)

WX_TOKEN     = "taiyi2026"
OPENCLAW_URL = "http://127.0.0.1:18789/v1/chat/completions"
AGENT_NAME   = "taiyi"

def verify_signature(token, timestamp, nonce, signature):
    items = sorted([token, timestamp, nonce])
    s = hashlib.sha1("".join(items).encode()).hexdigest()
    return s == signature

def call_openclaw(user_msg):
    try:
        payload = {"model": AGENT_NAME, "messages": [{"role": "user", "content": user_msg}], "stream": False}
        resp = requests.post(OPENCLAW_URL, json=payload, timeout=25)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[太一暂时无法响应: {str(e)}]"

def build_reply(to_user, from_user, content):
    return f"<xml><ToUserName><![CDATA[{to_user}]]></ToUserName><FromUserName><![CDATA[{from_user}]]></FromUserName><CreateTime>{int(time.time())}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{content}]]></Content></xml>"

@app.route("/wx/callback", methods=["GET", "POST"])
def wx_callback():
    timestamp = request.args.get("timestamp", "")
    nonce     = request.args.get("nonce", "")
    signature = request.args.get("signature", "")
    echostr   = request.args.get("echostr", "")
    if not verify_signature(WX_TOKEN, timestamp, nonce, signature):
        return "Invalid signature", 403
    if request.method == "GET":
        return echostr
    try:
        xml_data  = ET.fromstring(request.data)
        msg_type  = xml_data.findtext("MsgType", "")
        from_user = xml_data.findtext("FromUserName", "")
        to_user   = xml_data.findtext("ToUserName", "")
        content   = xml_data.findtext("Content", "")
    except Exception:
        return "parse error", 400
    if msg_type != "text" or not content:
        return make_response(build_reply(from_user, to_user, "暂时只支持文字消息～"), 200, {"Content-Type": "text/xml"})
    return make_response(build_reply(from_user, to_user, call_openclaw(content)), 200, {"Content-Type": "text/xml"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
