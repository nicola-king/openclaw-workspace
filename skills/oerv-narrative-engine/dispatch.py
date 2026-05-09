#!/usr/bin/env python3
"""
O.E.R.V 分发服务器 — 接收叙事引擎输出，推送至公众号/小红书

部署在 N150 工业电脑或本地服务器。

用法:
  python3 dispatch.py                    # 启动 Webhook 服务（端口 5200）
  python3 dispatch.py --test             # 用本地测试文章验证流程
  python3 dispatch.py --dry-run "闪念"    # 直接运行完整流水线（不含推送）
"""
import json, os, sys, requests, hashlib, time, re
from datetime import datetime

# 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_PATH = os.path.join(SCRIPT_DIR, "engine.py")
WORKSPACE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))

# 加载 .env
_ENV = {}
_env_path = os.path.join(SCRIPT_DIR, ".env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                _ENV[k.strip()] = v.strip().strip("\"'")

# 配置
WECHAT_APP_ID = _ENV.get("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = _ENV.get("WECHAT_APP_SECRET", "")
LLM_API_KEY = _ENV.get("LLM_API_KEY", "")
PORT = int(_ENV.get("DISPATCH_PORT", "5200"))
WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

# 配置目录
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
MEDIA_DIR = os.path.join(SCRIPT_DIR, "media")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)


# ════════════════════════════════════════
# 公众号推送
# ════════════════════════════════════════

class WeChatPublisher:
    """微信公众号草稿箱推送"""

    def __init__(self):
        self._token = None
        self._token_expires = 0

    def _get_token(self):
        """获取 access_token（自动缓存）"""
        if time.time() < self._token_expires and self._token:
            return self._token
        if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
            return None
        resp = requests.get(
            f"{WECHAT_API_BASE}/token",
            params={"grant_type": "client_credential",
                    "appid": WECHAT_APP_ID, "secret": WECHAT_APP_SECRET}
        ).json()
        if "access_token" in resp:
            self._token = resp["access_token"]
            self._token_expires = time.time() + resp.get("expires_in", 7200) - 300
            return self._token
        print(f"⚠️ 微信 token 获取失败: {resp}", file=sys.stderr)
        return None

    def is_configured(self):
        return bool(WECHAT_APP_ID and WECHAT_APP_SECRET)

    def create_draft(self, title, content, cover_media_id=""):
        """创建公众号草稿"""
        token = self._get_token()
        if not token:
            return {"status": "skipped", "reason": "微信未配置"}

        article = {
            "title": title[:64],
            "author": "SAYELF",
            "content": self._to_wechat_html(content),
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }
        if cover_media_id:
            article["thumb_media_id"] = cover_media_id

        resp = requests.post(
            f"{WECHAT_API_BASE}/draft/add?access_token={token}",
            json={"articles": [article]}
        ).json()

        if "media_id" in resp:
            print(f"✅ 公众号草稿创建成功: media_id={resp['media_id']}", file=sys.stderr)
            self._save_record("wechat_draft", title, resp["media_id"])
        else:
            print(f"⚠️ 创建草稿失败: {resp}", file=sys.stderr)

        return resp

    def _to_wechat_html(self, markdown_text):
        """极简黑客风 → 公众号适配 HTML"""
        html = []
        for line in markdown_text.strip().split("\n"):
            line = line.strip()
            if not line:
                html.append('<p style="margin: 1.5em 0;"></p>')
            elif line.startswith("# "):
                html.append(f"<h2>{line[2:]}</h2>")
            elif line.startswith("## "):
                html.append(f"<h3>{line[3:]}</h3>")
            elif line.startswith("**") and line.endswith("**"):
                html.append(f"<p><strong>{line[2:-2]}</strong></p>")
            else:
                html.append(f"<p style='margin: 1em 0; line-height: 1.8;'>{line}</p>")
        return "\n".join(html)

    def _save_record(self, channel, title, media_id):
        """记录发布历史"""
        record = {
            "channel": channel,
            "title": title,
            "media_id": media_id,
            "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        history_file = os.path.join(OUTPUT_DIR, "publish_history.jsonl")
        with open(history_file, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ════════════════════════════════════════
# O.E.R.V 流水线
# ════════════════════════════════════════

class OERVPipeline:
    """完整叙事流水线：闪念 → 文章 → 配图 → 分发"""

    def __init__(self):
        sys.path.insert(0, SCRIPT_DIR)
        from engine import OERVEngine
        self.Engine = OERVEngine

    def run(self, raw_input, mode="article", publish=False):
        """执行流水线"""
        engine = self.Engine(raw_input, mode=mode)
        result = engine.run()

        # 保存输出
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = re.sub(r'[^\u4e00-\u9fff\w]', '_', result["refined"]["core_view"][:30])
        output_file = os.path.join(OUTPUT_DIR, f"{timestamp}_{safe_title}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(engine.to_markdown(result))
        print(f"✅ 文章已保存: {output_file}", file=sys.stderr)

        # 额外保存 JSON
        json_file = output_file.replace(".md", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(engine.to_json(result))

        result["_files"] = {"md": output_file, "json": json_file}

        # 推送
        if publish and mode == "article":
            pub = WeChatPublisher()
            if pub.is_configured():
                pub.create_draft(
                    title=result["refined"]["core_view"][:64],
                    content=result["article"],
                )
            else:
                print("ℹ️ 微信未配置，跳过推送（设置 .env 中的 WECHAT_APP_ID/密")  # 截断防敏感
                result["_publish"] = "skipped"

        return result


# ════════════════════════════════════════
# Webhook 服务
# ════════════════════════════════════════

def start_webhook(port=None):
    """启动 Flask Webhook 服务（如果可用）"""
    actual_port = port or globals().get("PORT", 5200)
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("⚠️ Flask 未安装。pip install flask 后可启动 Webhook 服务。")
        print("   暂时仅支持命令行模式：python3 dispatch.py --dry-run '闪念'")
        return

    app = Flask(__name__)
    pipeline = OERVPipeline()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "module": "oerv-dispatch", "version": "2.0"})

    @app.route("/publish", methods=["POST"])
    def handle_publish():
        """接收叙事引擎输出，推送至公众号"""
        data = request.json or {}

        # 支持两种输入模式
        if data.get("content") and data.get("title"):
            # 直接收到内容（从 TaskFlow webhook）
            title = data["title"]
            content = data["content"]
            visual_prompts = data.get("visual_prompts", [])

            # 保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(OUTPUT_DIR, f"webhook_{timestamp}.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{content}\n\n## Visual\n{json.dumps(visual_prompts, indent=2)}")

            # 推送公众号
            pub = WeChatPublisher()
            if pub.is_configured():
                pub.create_draft(title, content)
                return jsonify({"status": "success", "msg": "已推送公众号", "output": output_file})
            else:
                return jsonify({"status": "success", "msg": "已保存（微信未配置）", "output": output_file})

        elif data.get("raw_input"):
            # 走完整流水线
            result = pipeline.run(
                raw_input=data["raw_input"],
                mode=data.get("mode", "article"),
                publish=data.get("publish", False),
            )
            return jsonify({"status": "success", "result": result})

        else:
            return jsonify({"status": "error", "msg": "需要 content+title 或 raw_input"}), 400

    @app.route("/history", methods=["GET"])
    def history():
        """查看发布历史"""
        history_file = os.path.join(OUTPUT_DIR, "publish_history.jsonl")
        if not os.path.exists(history_file):
            return jsonify({"records": []})
        records = []
        with open(history_file) as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        return jsonify({"records": records, "count": len(records)})

    print(f"\n🚀 O.E.R.V 分发服务器启动 → http://0.0.0.0:{PORT}")
    print(f"   Webhook: POST /publish")
    print(f"   健康检查: GET /health")
    print(f"   发布历史: GET /history")
    print(f"   输出目录: {OUTPUT_DIR}")
    if not WeChatPublisher().is_configured():
        print(f"   微信公众号: ❌ 未配置（配置 .env 中的 WECHAT_APP_ID/密")
    else:
        print(f"   微信公众号: ✅ 已配置")
    print()
    app.run(host="0.0.0.0", port=actual_port)


# ════════════════════════════════════════
# CLI
# ════════════════════════════════════════

def run_dry_run(raw_input):
    """命令行直接运行流水线"""
    pipeline = OERVPipeline()
    result = pipeline.run(raw_input, publish=False)
    # 输出 markdown 到 stdout
    from engine import OERVEngine
    engine = OERVEngine(raw_input)
    print(engine.to_markdown(result))
    print(f"\n📁 文件已保存到: {OUTPUT_DIR}/", file=sys.stderr)


def run_test():
    """运行测试：生成一篇示范文章"""
    demo = '今天面试了一个35岁的程序员。他问我公司食堂几点开门。问完又补了一句"就是怕以后找不到有食堂的公司了"。'

    # 检查 engine.py 可用
    sys.path.insert(0, SCRIPT_DIR)
    from engine import OERVEngine
    engine = OERVEngine(demo, mode="article")
    result = engine.run()

    # 保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"test_{timestamp}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(engine.to_markdown(result))

    print(f"✅ 测试文章已生成: {output_file}")
    print(f"   情绪: {result['meta']['emotion']}")
    print(f"   字数: {result['meta']['word_count']}")
    print(f"   场景: {len(result['refined']['scenes'])} 个")
    print(f"   视觉 Prompt: {len(result['visual_prompts'])} 组")
    print(f"\n查看内容: cat {output_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="O.E.R.V 分发服务器")
    parser.add_argument("--dry-run", metavar="闪念", help="直接运行流水线（不含推送）")
    parser.add_argument("--test", action="store_true", help="生成测试文章")
    parser.add_argument("--mode", choices=["article", "card", "visual"], default="article")
    parser.add_argument("--publish", action="store_true", help="启用公众号推送")
    parser.add_argument("--port", type=int, default=PORT, help="Webhook 端口")

    args = parser.parse_args()

    if args.dry_run:
        run_dry_run(args.dry_run)
    elif args.test:
        run_test()
    else:
        _port = args.port or PORT
        start_webhook()


if __name__ == "__main__":
    main()
