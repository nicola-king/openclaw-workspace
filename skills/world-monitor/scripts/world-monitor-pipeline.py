#!/usr/bin/env python3
"""
世界监控日报增强流水线 v2.0
===================================
功能：
1. 从免费 API 获取实时数据（汇率/大宗商品/天气）
2. 调用 Gemini CLI 生成30条全球情报（注入实时数据+要求来源）
3. 调用 art-agent 自动匹配品牌风格并美化排版
4. 生成 PDF (weasyprint)
5. 输出使用记录

使用：python3 world-monitor-pipeline.py
""" 

import json, os, subprocess, sys
import re
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request

# ── 路径 ──────────────────────────
WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
SKILL_DIR = WORKSPACE / "skills" / "world-monitor"
OUTPUT_DIR = WORKSPACE / "exports"
ART_DIR = WORKSPACE / "skills" / "art-agent"
GEMINI_CLI = os.path.expanduser("~/.npm-global/bin/gemini")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATE = datetime.now().strftime("%Y%m%d")
MD_FILE = OUTPUT_DIR / f"world-monitor-daily-{DATE}.md"
HTML_FILE = OUTPUT_DIR / f"world-monitor-daily-{DATE}.html"
PDF_FILE = OUTPUT_DIR / f"world-monitor-daily-{DATE}.pdf"
JSON_FILE = OUTPUT_DIR / f"world-monitor-daily-{DATE}.json"


# ── 步骤 1：获取实时数据 ──────────────
def fetch_real_data() -> dict:
    """从免费 API 获取实时市场数据"""
    data = {"timestamp": datetime.now().isoformat(), "sources": {}}

    # 1. 汇率 (ExchangeRate-API, 免费, 无需 key)
    try:
        req = Request("https://api.exchangerate-api.com/v4/latest/USD",
                       headers={"User-Agent": "Taiyi/1.0"})
        resp = json.loads(urlopen(req, timeout=10).read())
        rates = resp.get("rates", {})
        data["fx"] = {
            "USDCNY": rates.get("CNY"),
            "USDJPY": rates.get("JPY"),
            "USDEUR": rates.get("EUR"),
            "USDGBP": rates.get("GBP"),
            "USDAUD": rates.get("AUD"),
            "USDKRW": rates.get("KRW"),
            "USDSGD": rates.get("SGD"),
            "USDINR": rates.get("INR"),
            "CNYEUR": round(rates.get("EUR", 0) / rates.get("CNY", 1), 6) if rates.get("CNY") else None,
            "CNYJPY": round(rates.get("JPY", 0) / rates.get("CNY", 1), 4) if rates.get("CNY") else None,
        }
        data["sources"]["fx"] = "ExchangeRate-API (free, no key required)"
        print(f"  ✅ FX: USD/CNY={data['fx']['USDCNY']}, USD/JPY={data['fx']['USDJPY']}")
    except Exception as e:
        print(f"  ⚠️ FX fetch failed: {e}")

    # 2. 加密货币 (CoinGecko, 免费)
    try:
        req = Request("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true",
                       headers={"User-Agent": "Taiyi/1.0", "accept": "application/json"})
        resp = json.loads(urlopen(req, timeout=10).read())
        data["crypto"] = {
            "BTC": resp.get("bitcoin", {}).get("usd"),
            "BTC_24h": resp.get("bitcoin", {}).get("usd_24h_change"),
            "ETH": resp.get("ethereum", {}).get("usd"),
            "ETH_24h": resp.get("ethereum", {}).get("usd_24h_change"),
            "SOL": resp.get("solana", {}).get("usd"),
        }
        data["sources"]["crypto"] = "CoinGecko API (free)"
        print(f"  ✅ Crypto: BTC=${data['crypto']['BTC']}, ETH=${data['crypto']['ETH']}")
    except Exception as e:
        print(f"  ⚠️ Crypto fetch failed: {e}")

    # 3. 天气 (Open-Meteo, 免费, 无需 key) - 主要城市
    cities = {
        "Manila": {"lat": 14.58, "lon": 120.98},
        "Jakarta": {"lat": -6.21, "lon": 106.85},
        "Shanghai": {"lat": 31.23, "lon": 121.47},
        "Dubai": {"lat": 25.20, "lon": 55.27},
    }
    data["weather"] = {}
    for city, coord in cities.items():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coord['lat']}&longitude={coord['lon']}&current=temperature_2m,weather_code,wind_speed_10m"
            resp = json.loads(urlopen(url, timeout=10).read())
            w = resp.get("current", {})
            data["weather"][city] = {
                "temp": w.get("temperature_2m"),
                "weather_code": w.get("weather_code"),
                "wind": w.get("wind_speed_10m"),
            }
        except:
            pass
    data["sources"]["weather"] = "Open-Meteo (free, no key)"
    print(f"  ✅ Weather: {len(data['weather'])} cities")

    # 4. 波罗的海干散货指数 (BDI) — 通过网页抓取
    try:
        req = Request("https://www.worldfreightrates.com/freight-indices",
                       headers={"User-Agent": "Mozilla/5.0"})
        # BDI not easily available via simple API; skip for now
        pass
    except:
        pass

    return data


# ── 步骤 2：调用 Gemini CLI ──────────
def generate_report(real_data: dict) -> str:
    """调用 Gemini CLI 生成30条全球情报，注入实时数据"""
    
    # 构造实时数据摘要作为 prompt context
    context_lines = []
    fx = real_data.get("fx", {})
    if fx:
        context_lines.append(f"📊 实时汇率 (来源: ExchangeRate-API):")
        context_lines.append(f"  USD/CNY = {fx.get('USDCNY')}, USD/JPY = {fx.get('USDJPY')}")
        context_lines.append(f"  USD/EUR = {fx.get('USDEUR')}, USD/GBP = {fx.get('USDGBP')}")
        context_lines.append(f"  USD/AUD = {fx.get('USDAUD')}, USD/KRW = {fx.get('USDKRW')}")
        context_lines.append(f"  CNY/EUR = {fx.get('CNYEUR')}, CNY/JPY = {fx.get('CNYJPY')}")
    
    crypto = real_data.get("crypto", {})
    if crypto:
        context_lines.append(f"\n📊 加密货币 (来源: CoinGecko):")
        context_lines.append(f"  BTC = ${crypto.get('BTC')}, ETH = ${crypto.get('ETH')}, SOL = ${crypto.get('SOL')}")
    
    weather = real_data.get("weather", {})
    if weather:
        context_lines.append(f"\n🌤 主要城市天气 (来源: Open-Meteo):")
        for city, w in weather.items():
            context_lines.append(f"  {city}: {w.get('temp')}°C, code={w.get('weather_code')}, wind={w.get('wind')}km/h")
    
    context_str = "\n".join(context_lines)
    
    prompt = f"""你是世界监控日报编辑，正在编辑 {datetime.now().strftime('%Y年%m月%d日')} 的全球情报日报。

【重要：真实数据锚点】
以下数据是今天从实时 API 获取的确定值，请将其融入对应条目中作为事实基础，切勿编造：

{context_str}

【要求】
请生成一份《全球情报日报》，包含30条过去24小时最重要的全球动态，分类如下：
1. 地缘政治 (5条)
2. 国际贸易/关税 (5条)
3. 金融市场/汇率 (5条)
4. 大宗商品/能源 (5条)
5. 科技/AI (5条)
6. 自然灾害/疫情 (3条)
7. 其他重要 (2条)

【每条格式】
## 标题（一句话概括）
**摘要**：详细描述事件经过、数据和影响。
**影响分析**：对该事件对跨境贸易/全球经济的影响评估。
**来源**：[来源名称](参考URL或来源描述)

【铁律】
1. **所有内容必须使用中文**（专有名词、人名、机构缩写如 WTO/IMF 除外），标题、摘要、影响分析、来源描述全部用中文撰写
2. 每条必须附带来源（真实新闻源如 Reuters / Bloomberg / Xinhua / FT / WSJ 等）
3. 涉及到以下数据时，必须使用上面提供的实时数据锚点：汇率、加密货币、天气
4. 不知道精确数字时标注 [待核实]，不要编造
5. 每条之间空一行
6. 使用 Markdown 格式"""

    # 写入临时 prompt 文件（避免 shell 转义问题）
    prompt_file = OUTPUT_DIR / f"world-monitor-prompt-{DATE}.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print("\n[WORLD-MONITOR] 📡 调用 Gemini CLI 生成情报...")
    # 从 bashrc 读取 API key（Python 环境不继承 bashrc）
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        bashrc = Path(os.path.expanduser("~/.bashrc"))
        if bashrc.exists():
            for line in bashrc.read_text().split("\n"):
                if "GEMINI_API_KEY" in line and "export" in line.lower():
                    # Extract key from export GEMINI_API_KEY="xxx"
                    m = re.search(r'"([^"]+)"', line)
                    if m:
                        api_key = m.group(1)
                        break

    result = subprocess.run(
        [GEMINI_CLI, "-m", "gemini-2.0-flash", "-p", prompt],
        capture_output=True, text=True, timeout=120,
        env={
            **os.environ,
            "GEMINI_API_KEY": api_key,
            "GEMINI_CLI_TRUST_WORKSPACE": "true",
            "NO_COLOR": "1",
        }
    )
    
    if result.returncode != 0:
        err = result.stderr[:1000]
        print(f"  ❌ Gemini CLI failed")
        
        # 检查是否配额耗尽 → fallback 到本地 ollama
        if "TerminalQuotaError" in err or "quota" in err.lower():
            print(f"  ⚠️ Gemini 配额耗尽，尝试本地 ollama fallback...")
            try:
                import urllib.request
                payload = json.dumps({
                    "model": "minicpm-v",
                    "prompt": f"{_build_fallback_prompt(real_data)}",
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 4096}
                }).encode()
                req = urllib.request.Request(
                    "http://localhost:11434/api/generate",
                    data=payload,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read())
                    response = data.get("response", "")
                    if response and len(response) > 300 and "我无法" not in response and "知识截止" not in response:
                        print(f"  ✅ ollama fallback 成功 ({len(response)}字符)")
                    else:
                        print(f"  ⚠️ ollama 响应太短或无内容 ({len(response) if response else 0}字符), 降级数据驱动报告")
                        raise Exception("无有效内容")
            except Exception as e:
                print(f"  ❌ ollama fallback 失败: {e}")
                print(f"  ⚠️ 使用数据驱动报告模板")
                response = _build_data_report(real_data)
        else:
            response = result.stdout or result.stderr
    else:
        response = result.stdout
    
    # 尝试从 JSON 输出提取文本
    try:
        parsed = json.loads(response)
        response = parsed.get("response", response)
    except:
        pass
    
    prompt_file.unlink(missing_ok=True)
    return response.strip()


# ── 步骤 3：使用 art-agent 智能美化 ──
def beautify_with_art_agent(md_content: str) -> str:
    """通过 art-agent 自动匹配品牌风格，生成精美 HTML"""
    # 加载 art-agent dispatcher
    sys.path.insert(0, str(ART_DIR))
    from dispatcher import ArtDispatcher, CONTENT_BRAND_MAP
    
    dispatch = ArtDispatcher()
    
    # 智能品牌匹配：统计内容关键词命中
    scores = {}
    for kw, brand in CONTENT_BRAND_MAP.items():
        if kw.lower() in md_content.lower():
            scores[brand] = scores.get(brand, 0) + 1
    
    matched_brand = max(scores, key=scores.get) if scores else "binance"
    print(f"\n[WORLD-MONITOR] ✨ art-agent 品牌匹配: {matched_brand} (命中{scores.get(matched_brand, 0)}次)")
    
    # 获取品牌 CSS token
    try:
        bs_path = ART_DIR / "modules" / "brand-studio" / "core.py"
        sys.path.insert(0, str(bs_path.parent))
        from core import BrandStudio
        studio = BrandStudio()
        css = studio.get_css(matched_brand)
        spec = studio.get_spec(matched_brand)
    except Exception as e:
        print(f"  ⚠️ BrandStudio load failed: {e}")
        css = None
        spec = None
    
    # 如果品牌 CSS 不可用，使用内置 fallback
    if not css:
        brand_styles = {
            "binance": {
                "bg": "#0b0e11", "text": "#e8e8e8", "accent": "#f0b90b",
                "heading": "#f0b90b", "subheading": "#e8e8e8", "border": "#2b2f36",
                "card_bg": "#1e2329", "strong": "#f0b90b",
                "font": "'Inter', -apple-system, 'Segoe UI', sans-serif",
            },
            "hashicorp": {
                "bg": "#1a1a2e", "text": "#e0e0e0", "accent": "#5a5af0",
                "heading": "#7b7bff", "subheading": "#c0c0ff", "border": "#333366",
                "card_bg": "#242450", "strong": "#7b7bff",
                "font": "'Inter', -apple-system, sans-serif",
            },
            "nvidia": {
                "bg": "#0a0a0a", "text": "#d4d4d4", "accent": "#76b900",
                "heading": "#76b900", "subheading": "#a0d060", "border": "#2a2a2a",
                "card_bg": "#141414", "strong": "#76b900",
                "font": "'Inter', -apple-system, sans-serif",
            },
        }
        style = brand_styles.get(matched_brand, brand_styles["binance"])
    else:
        # 从 CSS 提取颜色
        style = {
            "bg": "#0b0e11", "text": "#e8e8e8", "accent": "#f0b90b",
            "heading": "#f0b90b", "subheading": "#e8e8e8", "border": "#2b2f36",
            "card_bg": "#1e2329", "strong": "#f0b90b",
            "font": "'Inter', -apple-system, sans-serif",
        }
    
    # 解析 Markdown 内容为 HTML 段落
    html_body = ""
    items = md_content.split("\n## ")
    for i, section in enumerate(items):
        if i == 0 and not section.startswith("##"):
            # Header section
            html_body += f"<div class='header'>{md_to_html(section)}</div>"
            continue
        lines = section.strip().split("\n")
        if not lines:
            continue
        title = lines[0].lstrip("#").strip()
        body_lines = lines[1:]
        
        # Detect section divider (category headers like "地缘政治")
        if "**" not in section and len(body_lines) < 3:
            html_body += f"<h2 class='category'>{title}</h2>"
        else:
            html_body += f"<div class='news-item'>"
            html_body += f"<h3>{title}</h3>"
            html_body += f"<div class='content'>{md_to_html('\n'.join(body_lines))}</div>"
            html_body += f"</div>"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球情报日报 | {DATE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
@page {{ size: A4; margin: 20mm 18mm; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Noto Sans SC', 'Inter', -apple-system, sans-serif;
    background: {style['bg']};
    color: {style['text']};
    line-height: 1.8;
    padding: 0;
}}
.header {{
    padding: 30px 0 20px;
    border-bottom: 3px solid {style['accent']};
    margin-bottom: 15px;
}}
.header h1 {{
    font-size: 28px;
    color: {style['heading']};
    font-weight: 700;
    letter-spacing: 1px;
}}
.header blockquote {{
    margin: 10px 0 0;
    padding: 8px 15px;
    background: {style['card_bg']};
    border-left: 4px solid {style['accent']};
    font-size: 13px;
    color: #999;
}}
h2.category {{
    font-size: 18px;
    color: {style['subheading']};
    border-bottom: 2px solid {style['border']};
    padding: 15px 0 8px;
    margin: 25px 0 15px;
    text-transform: uppercase;
    letter-spacing: 2px;
}}
.news-item {{
    background: {style['card_bg']};
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 10px;
    border-left: 3px solid {style['accent']};
}}
.news-item h3 {{
    font-size: 15px;
    color: {style['heading']};
    font-weight: 600;
    margin-bottom: 6px;
    line-height: 1.5;
}}
.news-item .content {{
    font-size: 13px;
    line-height: 1.7;
}}
.news-item .content p {{ margin-bottom: 6px; }}
.news-item .content strong {{ color: {style['strong']}; }}
.news-item .content em {{ color: #888; font-size: 12px; }}
.news-item .content blockquote {{
    background: {style['bg']};
    padding: 6px 10px;
    border-left: 3px solid {style['accent']};
    margin: 6px 0;
    font-size: 12px;
}}
.footer {{
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid {style['border']};
    font-size: 11px;
    color: #666;
    text-align: center;
    line-height: 1.6;
}}
.tag {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    margin-right: 5px;
    background: {style['accent']}22;
    color: {style['accent']};
    border: 1px solid {style['accent']}44;
}}
hr {{ border: none; border-top: 1px solid {style['border']}; margin: 20px 0; }}
</style>
</head>
<body>
{html_body}
<div class="footer">
    <p>🌍 全球情报日报 | {datetime.now().strftime('%Y年%m月%d日')}</p>
    <p>数据来源: 实时API (ExchangeRate-API / CoinGecko / Open-Meteo) + Gemini AI 聚合</p>
    <p>太一系统自动生成 · 关键信息建议核实</p>
    <p>品牌风格: {matched_brand} (art-agent 自动匹配)</p>
</div>
</body>
</html>"""
    
    return html


def md_to_html(text: str) -> str:
    """简易 markdown → HTML 转换"""
    import html
    text = html.escape(text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # Blockquotes
    lines = text.split('\n')
    result = []
    in_block = False
    for line in lines:
        if line.startswith('> '):
            if not in_block:
                result.append('<blockquote>')
                in_block = True
            result.append(f'<p>{line[2:]}</p>')
        else:
            if in_block:
                result.append('</blockquote>')
                in_block = False
            result.append(f'<p>{line}</p>' if line.strip() else '')
    if in_block:
        result.append('</blockquote>')
    return '\n'.join(result)


# ── 步骤 4：生成 PDF ────────────────
def generate_pdf(html: str) -> bool:
    """用 weasyprint 生成 PDF"""
    try:
        from weasyprint import HTML as WHTML
        WHTML(string=html, base_url=str(OUTPUT_DIR)).write_pdf(str(PDF_FILE))
        size = PDF_FILE.stat().st_size
        print(f"\n[WORLD-MONITOR] 📄 PDF 已生成: {PDF_FILE} ({size//1024}KB)")
        return True
    except Exception as e:
        print(f"  ❌ weasyprint failed: {e}")
        # Fallback: save HTML only
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ HTML fallback: {HTML_FILE}")
        return False


# ── 备用：数据驱动报告模板（不依赖任何 AI 模型） ──
def _build_data_report(real_data: dict) -> str:
    """当所有 AI 模型都不可用时，用实时数据生成结构化报告"""
    today = datetime.now().strftime('%Y年%m月%d日')
    lines = [f"# 🌍 全球情报日报（数据快照版）\n> {today}\n"]
    
    # 核心资产价格仪表盘
    lines.append("## 📊 核心市场数据\n")
    lines.append("| 品种 | 价格 | 来源 |")
    lines.append("|------|------|------|")
    
    fx = real_data.get("fx", {})
    if fx:
        lines.append(f"| USD/CNY | {fx.get('USDCNY')} | ExchangeRate-API |")
        lines.append(f"| USD/JPY | {fx.get('USDJPY')} | ExchangeRate-API |")
        lines.append(f"| USD/EUR | {fx.get('USDEUR')} | ExchangeRate-API |")
        lines.append(f"| USD/GBP | {fx.get('USDGBP')} | ExchangeRate-API |")
        lines.append(f"| USD/AUD | {fx.get('USDAUD')} | ExchangeRate-API |")
        if fx.get('CNYEUR'):
            lines.append(f"| CNY/EUR | {fx.get('CNYEUR')} | ExchangeRate-API |")
    
    crypto = real_data.get("crypto", {})
    if crypto:
        lines.append(f"| BTC | ${crypto.get('BTC')} | CoinGecko |")
        lines.append(f"| ETH | ${crypto.get('ETH')} | CoinGecko |")
        if crypto.get('BTC_24h'):
            sign = "+" if crypto['BTC_24h'] > 0 else ""
            lines.append(f"| BTC 24h | {sign}{crypto['BTC_24h']:.1f}% | CoinGecko |")
    
    lines.append("\n")
    
    # 天气
    weather = real_data.get("weather", {})
    if weather:
        lines.append("## 🌤 主要城市天气\n")
        lines.append("| 城市 | 温度 | 风速 |")
        lines.append("|------|------|------|")
        for city, w in weather.items():
            lines.append(f"| {city} | {w.get('temp')}°C | {w.get('wind')}km/h |")
        lines.append("\n> 来源: Open-Meteo (free)\n")
    
    lines.append("\n---\n")
    lines.append("> ⚠️ 今日AI情报生成因API配额限制暂不可用。")
    lines.append("> 数据驱动版日报包含实时汇率、加密货币和天气数据。")
    lines.append("> 完整情报将在配额恢复后自动补充。")
    
    return "\n".join(lines) + "\n"


def _build_fallback_prompt(real_data: dict) -> str:
    """为本地模型构建精简版 prompt"""
    today = datetime.now().strftime('%Y年%m月%d日')
    fx = real_data.get("fx", {})
    crypto = real_data.get("crypto", {})
    
    # 使用指令式prompt
    return f'''[INST] 你现在是太一全球情报系统编辑。今天是{today}。

你收到的实时数据如下，请直接使用它们：
- USD/CNY汇率: {fx.get("USDCNY")}
- USD/JPY汇率: {fx.get("USDJPY")}
- USD/EUR汇率: {fx.get("USDEUR")}
- BTC价格: ${crypto.get("BTC")}
- ETH价格: ${crypto.get("ETH")}

请生成全球情报日报，包含以下5个分类，每个分类2条：
1. 地缘政治 2. 国际贸易 3. 金融市场 4. 大宗商品 5. 科技

重要：所有内容必须用中文撰写，不允许出现英文内容（专有名词、机构缩写如WTO/IMF除外）。

每条格式：
**标题** - 内容摘要。

回复时不要加任何前缀说明，直接开始输出。[/INST]'''


# ── 主流程 ──────────────────────────
def main():
    print("=" * 60)
    print("🌍 世界监控日报流水线 v2.0")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Step 1: Fetch real-time data
    print("\n[1/4] 📡 获取实时数据...")
    real_data = fetch_real_data()
    
    # Step 2: Generate report via Gemini
    print("\n[2/4] 🧠 调用 Gemini CLI 生成情报...")
    report = generate_report(real_data)
    
    # Save raw markdown
    header = f"""# 🌍 全球情报日报
> 生成日期：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
> 数据来源：实时API (ExchangeRate-API / CoinGecko / Open-Meteo) + Gemini AI 聚合

---
"""
    md_content = header + "\n" + report
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  ✅ Markdown 已保存: {MD_FILE}")
    
    # Step 3: Beautify with art-agent
    print("\n[3/4] 🎨 art-agent 智能美化...")
    html = beautify_with_art_agent(md_content)
    
    # Save HTML
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ HTML 已保存: {HTML_FILE}")
    
    # Step 4: Generate PDF
    print("\n[4/4] 📄 生成 PDF...")
    pdf_ok = generate_pdf(html)
    
    # Write record
    record = {
        "date": DATE,
        "time": datetime.now().strftime("%H:%M"),
        "items": 30,
        "file": str(PDF_FILE) if pdf_ok else str(HTML_FILE),
        "real_data_sources": list(real_data.get("sources", {}).values()),
        "status": "ok" if pdf_ok else "partial",
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成! 输出: {PDF_FILE if pdf_ok else HTML_FILE}")
    print(f"{'='*60}")
    
    # Return file path for Telegram sending
    if pdf_ok:
        print(f"\nPDF_PATH:{PDF_FILE}")
    else:
        print(f"\nPDF_PATH:{HTML_FILE}")


if __name__ == "__main__":
    main()
