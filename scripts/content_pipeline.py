#!/usr/bin/env python3
"""
太一内容流水线 — 经历→事件→配图→设计→公众号

流程:
  1. 用户输入经历/概念
  2. O.E.R.V 引擎提取事件、生成叙事
  3. 搜索配图 或 生成视觉 Prompt
  4. art-agent 品牌匹配 + 美学排版
  5. 生成公众号 HTML → 推送草稿箱

用法:
  python3 content_pipeline.py "你的经历描述"

示例:
  python3 content_pipeline.py "今天去菜市场买菜，卖菜大妈说她儿子今年大学毕业没找到工作，在送外卖"
"""
import os, sys, json, subprocess, re
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
OERV_DIR = os.path.join(WORKSPACE, "skills", "oerv-narrative-engine")
ART_DIR = os.path.join(WORKSPACE, "skills", "art-agent")
OUTPUT_DIR = os.path.join(OERV_DIR, "output", "wechat")
MEDIA_DIR = os.path.join(OERV_DIR, "media")
VENV_PYTHON = os.path.join(OERV_DIR, ".venv", "bin", "python3")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", file=sys.stderr)


# ════════════════════════════════════════════
# Step 1-2: O.E.R.V 引擎 — 提取事件 + 生成叙事
# ════════════════════════════════════════════

def run_oerv(raw_input):
    """调用 O.E.R.V 引擎生成文章 + 场景提取"""
    log("🎨 O.E.R.V 叙事引擎...")

    sys.path.insert(0, OERV_DIR)
    from engine import OERVEngine

    engine = OERVEngine(raw_input, mode="article")
    result = engine.run()

    article = result.get("article", "")
    refined = result.get("refined", {})
    scenes = refined.get("scenes", [])
    core_view = refined.get("core_view", "")
    emotion = refined.get("primary_emotion", "")

    log(f"   ✅ 文章生成 ({len(article)} 字)")
    log(f"   ✅ 核心观点: {core_view[:40]}...")
    log(f"   ✅ 像素场景: {len(scenes)} 个")
    log(f"   ✅ 主导情绪: {emotion}")

    return {
        "article": article,
        "core_view": core_view,
        "scenes": scenes,
        "emotion": emotion,
        "raw": result,
    }


# ════════════════════════════════════════════
# Step 3: 配图 — 搜索或生成 Prompt
# ════════════════════════════════════════════

def find_images(scenes, core_view):
    """搜索配图（从本地/unsplash/pelexs 获取，也生成视觉 Prompt 备选）"""
    log("🖼️ 配图搜索...")

    keywords = " ".join(scenes[:2]) if scenes else core_view
    images = []

    # 方案 A: 搜索 Unsplash（通过代理）
    search_queries = [re.sub(r'[^\u4e00-\u9fff\w]', ' ', s)[:30] for s in scenes[:2]]
    for q in search_queries:
        if not q.strip():
            continue
        try:
            result = subprocess.run(
                [VENV_PYTHON, "-c", f"""
import requests, json, re
# Unsplash 搜索
r = requests.get('https://unsplash.com/napi/search?query={q}&per_page=3',
    headers={{'User-Agent': 'Mozilla/5.0'}},
    proxies={{'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}},
    timeout=10)
data = r.json()
for item in data.get('results', [])[:2]:
    print(json.dumps({{
        'url': item.get('urls', {{}}).get('regular', ''),
        'alt': item.get('alt_description', '') or q,
    }}))
"""],
                capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        img = json.loads(line)
                        images.append(img)
                        log(f"   ✅ 找到配图: {img['alt'][:30]}...")
                    except:
                        pass
        except:
            pass

    # 方案 B: 检查本地 media 目录是否有合适的
    if os.path.isdir(MEDIA_DIR):
        for f in os.listdir(MEDIA_DIR):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                images.append({
                    "url": os.path.join(MEDIA_DIR, f),
                    "alt": os.path.splitext(f)[0],
                    "local": True,
                })

    # 方案 C: 生成视觉 Prompt 作为备选
    sys.path.insert(0, OERV_DIR)
    from engine import OERVEngine
    dummy = OERVEngine(core_view)
    prompts = dummy._generate_visuals({"scenes": scenes[:2], "emotion": "思考", "core_view": core_view})

    log(f"   ✅ 配图: {len(images)} 张搜索到, {len(prompts)} 组视觉 Prompt 备选")

    return {"images": images[:3], "prompts": prompts}


# ════════════════════════════════════════════
# Step 4: art-agent 品牌匹配 + 排版
# ════════════════════════════════════════════

def style_with_art_agent(oerv_result, images):
    """用 art-agent 品牌匹配 + 生成公众号 HTML"""
    log("🎨 art-agent 智能排版...")

    emotion = oerv_result["emotion"]
    core_view = oerv_result["core_view"]

    # 情绪→品牌匹配
    brand_map = {
        "焦虑": "stripe", "孤独": "apple", "愤怒": "binance",
        "无力": "spotify", "希望": "nike", "释然": "patagonia",
        "温暖": "starbucks", "困惑": "notion",
    }
    brand = brand_map.get(emotion, "minimal")

    # 调用 brand-studio 获取品牌 token
    sys.path.insert(0, os.path.join(ART_DIR, "modules", "brand-studio"))
    sys.path.insert(0, WORKSPACE)
    try:
        from core import BrandStudio
        studio = BrandStudio()
        brand_spec = studio.get_spec(brand)
        bname = brand_spec.get("name", brand)
        log(f"   ✅ 品牌匹配: {bname} (情绪: {emotion})")
    except Exception as e:
        bname = "极简"
        log(f"   ⚠️ 品牌库加载: {e}")

    # 获取品牌色
    brand_color = "#333333"
    brand_bg = "#FFFFFF"
    if 'design_tokens' in str(type(brand_spec)) or isinstance(brand_spec, dict):
        tokens = brand_spec.get("design_tokens", {}) if isinstance(brand_spec, dict) else {}
        brand_color = tokens.get("color_primary", "#333333") if isinstance(tokens, dict) else "#333333"
        brand_bg = tokens.get("color_background", "#FFFFFF") if isinstance(tokens, dict) else "#FFFFFF"
        if isinstance(brand_color, dict):
            brand_color = brand_color.get("value", "#333333")
        if isinstance(brand_bg, dict):
            brand_bg = brand_bg.get("value", "#FFFFFF")

    # 组装文章段落
    paragraphs = [p.strip() for p in oerv_result["article"].split("\n\n") if p.strip()]

    # 构建公众号 HTML（极简电影风 · 无品牌干扰）
    html_parts = []
    html_parts.append('<section>')
    html_parts.append(f'<article style="max-width: 600px; margin: 0 auto; padding: 8px 16px;">')

    # 标题（极简，无装饰）
    title = core_view[:40]
    html_parts.append(f'<h1 style="font-weight: 400; font-size: 20px; color: #111; line-height: 1.6; margin: 0 0 32px 0; letter-spacing: 1px;">{title}</h1>')

    # 段落 + 配图（中段插一张）
    img_idx = 0
    for i, para in enumerate(paragraphs):
        if not para:
            html_parts.append('<p style="margin: 0; height: 0.8em;"></p>')
            continue
        para = re.sub(r'\*\*', '', para)
        para = re.sub(r'^#+\s*', '', para)
        if not para:
            continue
        html_parts.append(f'<p style="margin: 0 0 18px 0; font-size: 15px; color: #222; line-height: 2; letter-spacing: 0.5px;">{para}</p>')

        # 只在中段插一张配图
        if images and i == max(1, len(paragraphs) // 2) and img_idx < len(images):
            img = images[img_idx]
            img_idx += 1
            url = img.get("url", "")
            html_parts.append(f'<p style="margin: 28px 0; text-align: center;"><img src="{url}" style="width:100%;border-radius:4px;max-width:100%;"></p>')

    html_parts.append('</article>')
    html_parts.append('</section>')

    html = "\n".join(html_parts)
    log(f"   ✅ HTML 排版完成 ({len(html)} 字符)")

    return {
        "html": html,
        "title": title,
        "brand": bname,
        "brand_color": brand_color,
    }


# ════════════════════════════════════════════
# Step 5: 推送公众号草稿
# ════════════════════════════════════════════

def push_to_wechat(html, title, images, local_images):
    """推送排版后的文章到公众号草稿箱 (图片上传微信CDN后替换URL)"""
    log("📤 推送公众号草稿...")

    # 读取凭证
    env_file = os.path.join(OERV_DIR, ".env")
    app_id = ""
    app_secret = ""
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.strip().startswith("WECHAT_APP_ID="):
                    app_id = line.strip().split("=", 1)[1].strip().strip("\"'")
                if line.strip().startswith("WECHAT_APP_SECRET="):
                    app_secret = line.strip().split("=", 1)[1].strip().strip("\"'")

    if not app_id or not app_secret:
        log("   ⚠️ 公众号未配置，跳过推送")
        return {"status": "skipped"}

    try:
        import requests
        # Token
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token',
            params={'grant_type': 'client_credential', 'appid': app_id, 'secret': app_secret}
        ).json()
        if 'access_token' not in r:
            log(f"   ❌ Token获取失败: {r}")
            return {"status": "failed"}
        token = r['access_token']

        # 收集本地图片路径
        local_paths = []
        for item in local_images:
            p = item.get("url", "") if isinstance(item, dict) else ""
            if p and os.path.exists(p):
                local_paths.append(p)

        # 上传封面图 (type=thumb)
        cover_id = None
        if local_paths:
            p = local_paths[0]
            with open(p, 'rb') as f:
                r2 = requests.post(
                    f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb',
                    files={'media': ('cover.jpg', f, 'image/jpeg')}
                ).json()
            log(f"   封面: {r2.get('media_id','失败')[:20]}...")
            if 'media_id' in r2:
                cover_id = r2['media_id']

        # 上传正文配图到微信CDN (type=image) 并替换 HTML 中的外链
        fixed_html = html
        unsplash_urls = re.findall(r'https://images\.unsplash\.com[^\'"]+', html)
        for i, unsplash_url in enumerate(unsplash_urls):
            if i < len(local_paths):
                with open(local_paths[i], 'rb') as f:
                    resp = requests.post(
                        f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image',
                        files={'media': ('img.jpg', f, 'image/jpeg')}
                    ).json()
                wx_url = resp.get('url', '')
                if wx_url:
                    fixed_html = fixed_html.replace(unsplash_url, wx_url)
                    log(f"   ✅ 配图替换为微信CDN")

        # 创建草稿
        article = {
            'title': title[:64],
            'author': 'SAYELF',
            'content': fixed_html,
            'need_open_comment': 1,
            'only_fans_can_comment': 0,
        }
        if cover_id:
            article['thumb_media_id'] = cover_id

        r3 = requests.post(
            f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}',
            json={'articles': [article]}
        ).json()

        if 'media_id' in r3:
            log(f"   ✅ 草稿推送成功: {r3['media_id'][:30]}...")
            return {"status": "success", "media_id": r3['media_id']}
        else:
            log(f"   ❌ 推送失败: {r3}")
            return {"status": "failed", "error": str(r3)}

    except Exception as e:
        log(f"   ❌ 推送异常: {e}")
        return {"status": "error", "error": str(e)}


# ════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════

def run_pipeline(raw_input, auto_push=True):
    """完整流水线"""
    log(f"\n{'='*50}")
    log(f"📝 输入: {raw_input[:80]}...")
    log(f"{'='*50}\n")

    # Step 1-2: O.E.R.V
    oerv = run_oerv(raw_input)
    if not oerv["article"]:
        log("❌ O.E.R.V 生成失败")
        return

    # Step 3: 配图
    img_result = find_images(oerv["scenes"], oerv["core_view"])
    images = img_result["images"]
    prompts = img_result["prompts"]

    # Step 4: art-agent 排版
    styled = style_with_art_agent(oerv, images)
    # 从 styled 中提取字段
    html = styled["html"]
    title = styled["title"]
    brand = styled["brand"]

    # 保存本地
    timestamp = datetime.now().strftime("%m%d_%H%M")
    safe_title = re.sub(r'[^\u4e00-\u9fff\w]', '', title)[:20]
    md_file = os.path.join(OUTPUT_DIR, f"{timestamp}_{safe_title}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(oerv["article"])
        f.write(f"\n\n---\n品牌: {brand}\n")
        f.write(f"\n视觉Prompt:\n")
        for p in prompts:
            f.write(f"\n{p['prompt']}\n")
    log(f"\n📁 本地保存: {md_file}")

    # Step 5: 推送
    if auto_push:
        push_result = push_to_wechat(html, title, images, images)
        log(f"\n{'='*50}")
        if push_result.get("status") == "success":
            log(f"✅ 全链路完成！草稿已推送 → 公众号草稿箱")
        else:
            log(f"⚠️ 文章已保存，推送状态: {push_result.get('status')}")

    log(f"{'='*50}\n")

    return {
        "article": oerv["article"],
        "html": html,
        "title": title,
        "brand": brand,
        "images": images,
        "prompts": prompts,
        "file": md_file,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="太一内容流水线")
    parser.add_argument("input", nargs="?", help="经历描述")
    parser.add_argument("--dry-run", action="store_true", help="不推送，只生成本地")
    parser.add_argument("--demo", action="store_true", help="运行示范")

    args = parser.parse_args()

    if args.demo:
        demo_inputs = [
            "今天去菜市场买菜，卖菜大妈说她儿子今年大学毕业没找到工作，在送外卖。她说这孩子本科毕业的时候全班50个人，现在只有3个人签了正式合同。",
            "下雨天打车，司机是个50多岁的大叔。他说以前是开工厂的，去年倒闭了，欠了200万。现在每天跑12个小时滴滴。他说起码比坐在家里强。",
        ]
        for inp in demo_inputs:
            run_pipeline(inp, auto_push=not args.dry_run)
        return

    if not args.input:
        parser.print_help()
        return

    run_pipeline(args.input, auto_push=not args.dry_run)


if __name__ == "__main__":
    main()
