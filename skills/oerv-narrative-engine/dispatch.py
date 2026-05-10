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
LAYOUT_STYLE = _ENV.get("OERV_LAYOUT_STYLE", "muji")  # muji | minimal | patagonia | notion | apple
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

    def create_draft(self, title, content, emotion="", cover_media_id=""):
        """创建公众号草稿（自动匹配排版风格）"""
        token = self._get_token()
        if not token:
            return {"status": "skipped", "reason": "微信未配置"}

        # 智能匹配风格：情绪优先，内容兜底
        style_name = self.smart_match_style(emotion=emotion, content=content)
        # 环境变量可强制覆盖
        env_style = LAYOUT_STYLE  # from .env
        if env_style in self.LAYOUT_STYLES and env_style != self.STYLE_FALLBACK:
            style_name = env_style if os.environ.get("OERV_LAYOUT_STYLE_FORCE") else style_name

        matched_style = self.LAYOUT_STYLES.get(style_name, self.LAYOUT_STYLES[self.STYLE_FALLBACK])
        print(f"  🎨 排版风格: {matched_style['name']} ({style_name})", file=sys.stderr)

        article = {
            "title": title[:64],
            "author": "SAYELF",
            "content": self._to_wechat_html(content, style_name=style_name),
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

    # ════════════════════════════════════════
    # 排版风格系统 (v1.0 — 2026-05-10)
    # ════════════════════════════════════════

    # 情绪 → 排版风格 智能匹配
    EMOTION_STYLE_MAP = {
        "焦虑": "minimal",     # 纯净，不添加任何情绪干扰
        "愤怒": "minimal",     # 硬边，直白，不修饰
        "悲伤": "muji",        # 米白暖灰，包容且有温度
        "无力": "muji",        # 柔软，有温度但不煽情
        "孤独": "muji",        # 暖底色像陪伴，但不是安慰
        "困惑": "minimal",     # 洁净，让思绪自己浮现
        "温暖": "patagonia",   # 手工感的暖，不精致但有温度
        "释然": "apple",       # 呼吸感，留白多，字少
        "希望": "apple",       # 明亮、高对比、轻松
        "怀旧": "patagonia",   # 旧报纸质感，时间留下了痕迹
    }
    CONTENT_STYLE_MAP = {
        "知识": "notion", "学习": "notion", "笔记": "notion", "教程": "notion",
        "科技": "apple", "ai": "apple", "AI": "apple", "编程": "apple", "数码": "apple",
        "社会": "minimal", "政治": "minimal", "新闻": "minimal",
        "日常": "muji", "生活": "muji", "情感": "muji", "家庭": "muji",
        "旅行": "patagonia", "自然": "patagonia", "户外": "patagonia",
    }
    STYLE_FALLBACK = "muji"

    @classmethod
    def smart_match_style(cls, emotion: str = "", content: str = "") -> str:
        """根据情绪和内容智能匹配排版风格"""
        if emotion:
            style = cls.EMOTION_STYLE_MAP.get(emotion)
            if style:
                return style
        for keyword, style in cls.CONTENT_STYLE_MAP.items():
            if keyword in content:
                return style
        return cls.STYLE_FALLBACK

    LAYOUT_STYLES = {
        "muji": {
            "name": "MUJI 无印良品",
            "bg": "#F8F6F3",
            "text": "#555555",
            "text_strong": "#333333",
            "text_muted": "#888888",
            "link": "#8B7355",
            "accent": "#8B7355",
            "divider": "#E8E6E3",
            "font_family": '"Noto Serif SC", "Source Han Serif SC", "STSong", "SimSun", serif',
            "font_size": "16px",
            "line_height": 2.0,
            "paragraph_gap": "1.6em",
            "header_font_family": '"Noto Serif SC", "Source Han Serif SC", "STSong", serif',
            "header_weight": 450,
            "letter_spacing": "0.03em",
            "max_width": "680px",
            "border_radius": "0",
            "blockquote_border": "#D4C9B8",
            "description": "米白底色 + 暖灰文字 + 充足留白。没有装饰，没有多余的东西。适于生活纪实类叙事。",
        },
        "minimal": {
            "name": "Minimal 极简",
            "bg": "#FFFFFF",
            "text": "#333333",
            "text_strong": "#111111",
            "text_muted": "#999999",
            "link": "#0066CC",
            "accent": "#000000",
            "divider": "#EEEEEE",
            "font_family": '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif',
            "font_size": "15px",
            "line_height": 1.8,
            "paragraph_gap": "1.4em",
            "header_font_family": '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif',
            "header_weight": 600,
            "letter_spacing": "0",
            "max_width": "700px",
            "border_radius": "0",
            "blockquote_border": "#DDD",
            "description": "纯白背景 + 深灰文字 + 零装饰。最干净的容器。",
        },
        "patagonia": {
            "name": "Patagonia 巴塔哥尼亚",
            "bg": "#F5F3EE",
            "text": "#2D2D2D",
            "text_strong": "#1A1A1A",
            "text_muted": "#7A7A7A",
            "link": "#8B5E3C",
            "accent": "#5A7A5A",
            "divider": "#DED9CE",
            "font_family": '"Noto Serif SC", "Source Han Serif SC", serif',
            "font_size": "14px",
            "line_height": 1.9,
            "paragraph_gap": "1.4em",
            "header_font_family": '"Noto Serif SC", "Source Han Serif SC", serif',
            "header_weight": 500,
            "letter_spacing": "0.02em",
            "max_width": "660px",
            "border_radius": "0",
            "blockquote_border": "#C4B8A8",
            "description": "自然米色底 + 粗糙质感。像旧报纸或再生纸。有手工感、有温度。",
        },
        "notion": {
            "name": "Notion",
            "bg": "#FFFFFF",
            "text": "#222222",
            "text_strong": "#000000",
            "text_muted": "#AAAAAA",
            "link": "#0075DE",
            "accent": "#5645D4",
            "divider": "#EFEFEF",
            "font_family": '"-apple-system", "PingFang SC", "Helvetica Neue", sans-serif',
            "font_size": "15px",
            "line_height": 1.7,
            "paragraph_gap": "1.2em",
            "header_font_family": '"-apple-system", "PingFang SC", "Helvetica Neue", sans-serif',
            "header_weight": 600,
            "letter_spacing": "0",
            "max_width": "720px",
            "border_radius": "6px",
            "blockquote_border": "#DDD",
            "description": "极简无装饰 + 系统字体。像在看一个人的笔记。",
        },
        "apple": {
            "name": "Apple",
            "bg": "#FFFFFF",
            "text": "#1D1D1F",
            "text_strong": "#000000",
            "text_muted": "#86868B",
            "link": "#0066CC",
            "accent": "#0066CC",
            "divider": "#F0F0F0",
            "font_family": '"SF Pro Text", "PingFang SC", "Helvetica Neue", sans-serif',
            "font_size": "15px",
            "line_height": 1.7,
            "paragraph_gap": "1.2em",
            "header_font_family": '"SF Pro Display", "PingFang SC", "Helvetica Neue", sans-serif',
            "header_weight": 400,
            "letter_spacing": "-0.01em",
            "max_width": "660px",
            "border_radius": "0",
            "blockquote_border": "#E0E0E0",
            "description": "大面积留白 + 细体字 + 高对比度。版面呼吸感最强。",
        },
    }

    LAYOUT_STYLE_DEFAULT = "muji"  # 默认排版风格 — 2026-05-10 从 minimal 切换到 muji

    def _to_wechat_html(self, markdown_text, style_name=None):
        """Markdown → 适配风格化 HTML（支持多种排版风格）"""
        style_name = style_name or os.environ.get("OERV_LAYOUT_STYLE", self.LAYOUT_STYLE_DEFAULT)
        style = self.LAYOUT_STYLES.get(style_name, self.LAYOUT_STYLES["muji"])

        # 构建完整 CSS 块
        css_block = f'''<style>
body {{ background: {style['bg']}; padding: 20px 0; margin: 0; }}
.article-container {{
    max-width: {style['max_width']};
    margin: 0 auto;
    background: {style['bg']};
    padding: 30px 24px;
    font-family: {style['font_family']};
    font-size: {style['font_size']};
    color: {style['text']};
    line-height: {style['line_height']};
    letter-spacing: {style['letter_spacing']};
}}
.article-container h2 {{
    font-family: {style['header_font_family']};
    font-weight: {style['header_weight']};
    font-size: 1.5em;
    color: {style['text_strong']};
    margin: 1.8em 0 0.8em;
    letter-spacing: {style['letter_spacing']};
}}
.article-container h3 {{
    font-family: {style['header_font_family']};
    font-weight: {style['header_weight']};
    font-size: 1.25em;
    color: {style['text_strong']};
    margin: 1.5em 0 0.6em;
}}
.article-container p {{
    margin: {style['paragraph_gap']} 0;
    text-align: justify;
}}
.article-container strong {{
    color: {style['text_strong']};
    font-weight: 500;
}}
.article-container blockquote {{
    border-left: 3px solid {style['blockquote_border']};
    margin: 1.5em 0;
    padding: 0.5em 1em;
    color: {style['text_muted']};
    font-style: italic;
}}
.article-container hr {{
    border: none;
    border-top: 1px solid {style['divider']};
    margin: 2em 0;
}}
.article-container a {{ color: {style['link']}; text-decoration: none; }}
</style>'''

        html = [f'<div class="article-container">']
        for line in markdown_text.strip().split("\n"):
            line = line.strip()
            if not line:
                html.append(f'<p style="margin: {style["paragraph_gap"]} 0;"></p>')
            elif line.startswith("# "):
                html.append(f"<h2>{line[2:]}</h2>")
            elif line.startswith("## "):
                html.append(f"<h3>{line[3:]}</h3>")
            elif line.startswith("> "):
                html.append(f"<blockquote>{line[2:]}</blockquote>")
            elif line.startswith("**") and line.endswith("**"):
                html.append(f"<p><strong>{line[2:-2]}</strong></p>")
            elif line.startswith("---"):
                html.append("<hr>")
            else:
                html.append(f"<p>{line}</p>")
        html.append("</div>")

        return css_block + "\n".join(html)

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
                emotion = result.get("meta", {}).get("emotion", "")
                pub.create_draft(
                    title=result["refined"]["core_view"][:64],
                    content=result["article"],
                    emotion=emotion,
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
                emotion = data.get("emotion", "")
                pub.create_draft(title, content, emotion=emotion)
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
