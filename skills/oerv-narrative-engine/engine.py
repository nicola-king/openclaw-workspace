#!/usr/bin/env python3
"""
O.E.R.V 2.0 叙事引擎 — 一个人即媒体公司

协议: 事件 → 情绪 → 共鸣 → 观点
铁律: 一个核心观点 + 三个像素场景 + 零形容词 + 80%位置出刀

用法:
  python3 engine.py "今天散步看到小区门口水果摊在打折，但没人买"
  python3 engine.py --mode card "你的闪念"          # 小红书卡片模式
  python3 engine.py --mode visual "描述场景"         # 仅生成视觉Prompt
"""
import json, os, sys, re
from datetime import datetime

# 默认 LLM 调用器（可被外部替换）
def _default_llm(prompt, system="", model=""):
    """回退：输出结构化的框架而非调用 API"""
    return {
        "status": "dry_run",
        "note": "未配置 LLM API Key，返回结构化框架。配置 .env 的 LLM_API_KEY 启用真实生成。",
        "prompt": prompt,
        "system": system
    }


class OERVEngine:
    """O.E.R.V 叙事引擎主类"""

    # 情绪映射表
    EMOTION_MAP = {
        "焦虑": "手在抖",
        "悲伤": "眼眶酸了一下",
        "愤怒": "指甲掐进掌心",
        "无力": "肩膀塌下去",
        "孤独": "地铁上没有人看你",
        "希望": "晨光从窗帘缝漏进来",
        "释然": "长长呼出一口气",
        "困惑": "眉头锁了三秒",
        "温暖": "嘴角不自觉翘了一下",
    }

    # 像素场景模板
    SCENE_TEMPLATES = [
        "微观动作（一个具体的手势/身体反应）",
        "环境细节（一个物件的状态/光影/声音）",
        "沉默时刻（空气凝固的一秒）",
    ]

    def __init__(self, raw_input, mode="article", llm_func=None):
        """
        raw_input: 原始闪念/想法
        mode: article(默认) | card(小红书) | visual(仅Prompt)
        llm_func: 外部 LLM 调用函数，不传则走 dry_run
        """
        self.raw_input = raw_input.strip()
        self.mode = mode
        self.llm = llm_func or _default_llm
        self.media_dir = os.path.join(os.path.dirname(__file__), "media")

    # ════════════════════════════════════════
    # 主入口
    # ════════════════════════════════════════

    def run(self):
        """全链执行 O.E.R.V"""
        result = {}

        # Step 1: 提取核心观点 + 3 像素场景
        refined = self._refine_input()
        result["refined"] = refined

        # Step 2: 写作
        content = self._write(refined)
        result["article"] = content

        # Step 3: 视觉 Prompt
        visuals = self._generate_visuals(refined)
        result["visual_prompts"] = visuals

        # Step 4: 小红书卡片（仅 card 模式）
        if self.mode == "card":
            result["card"] = self._make_card(refined)

        # Step 5: 本地媒体检索
        local_media = self._find_local_media()
        if local_media:
            result["local_media"] = local_media

        result["meta"] = {
            "mode": self.mode,
            "emotion": refined.get("primary_emotion", "未知"),
            "word_count": len(content),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        return result

    # ════════════════════════════════════════
    # Step 1: Input Refiner
    # ════════════════════════════════════════

    def _refine_input(self):
        """从原始闪念提取 1 核心观点 + 3 像素场景"""
        raw = self.raw_input

        # 核心观点提取：取输入中最有冲击力的那句
        sentences = [s.strip() for s in re.split(r'[。！？\n]', raw) if s.strip()]
        core_view = sentences[-1] if sentences else raw

        # 情绪映射
        emotion = self._detect_emotion(raw)

        # 像素场景：从输入中提取 3 个具象点
        scenes = self._extract_scenes(raw)

        return {
            "core_view": core_view,
            "primary_emotion": emotion,
            "scenes": scenes if len(scenes) >= 3 else self._scaffold_scenes(scenes, raw),
        }

    def _detect_emotion(self, text):
        """检测文本中的主导情绪"""
        text_lower = text.lower()
        emotion_keywords = {
            "焦虑": ["焦虑", "担心", "睡不着", "害怕", "慌", "不安", "裁员", "失业", "降薪"],
            "愤怒": ["愤怒", "生气", "凭什么", "无耻", "不公平", "怒了", "火大"],
            "悲伤": ["悲伤", "难过", "哭了", "心碎", "失落", "失去", "离开"],
            "无力": ["无力", "无奈", "没辙", "算了", "躺平", "卷不动", "内耗"],
            "孤独": ["孤独", "一个人", "没人", "独自", "孤", "寂寞"],
            "希望": ["希望", "相信", "阳光", "坚持", "成长", "改变", "开始"],
            "释然": ["释然", "放下", "算了", "接受", "懂了", "明白"],
            "困惑": ["困惑", "不懂", "迷茫", "为什么", "怎么回事", "奇怪"],
            "温暖": ["温暖", "感动", "谢谢", "贴心", "温柔", "拥抱"],
        }
        scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for k in keywords if k in text_lower)
            if score > 0:
                scores[emotion] = score
        if scores:
            return max(scores, key=scores.get)
        return "困惑"  # default

    def _extract_scenes(self, text):
        """从输入中提取具象场景"""
        # 找具象句：含有时间/地点/动作的短句
        patterns = [
            r'[。！？]([^。！？]{5,40}[了着过地得])',  # 含"了/着/过"
            r'[。！？]([^。！？]*在[^。！？]{5,30})',    # 含"在"的动作
            r'[。！？]([^。！？]*[把将][^。！？]{5,30})', # "把"字句
        ]
        scenes = []
        for p in patterns:
            matches = re.findall(p, text)
            for m in matches:
                s = m.strip()
                if len(s) > 5 and s not in scenes:
                    scenes.append(s)
        return scenes[:3]

    def _scaffold_scenes(self, existing, text):
        """当输入不足 3 个场景时，用情绪补全"""
        emotion = self._detect_emotion(text)
        templates = {
            "焦虑": ["推开一扇嘎吱响的门", "手机屏幕亮了一下又暗了", "凌晨三点的闹钟还没响"],
            "孤独": ["地铁最后一班车厢只有你一个人", "外卖放在门口没有敲门声", "点赞99+但没有人真的找你"],
            "希望": ["晨光从窗帘缝漏进来", "一颗绿萝在窗台长了新叶", "咖啡冒着热气"],
            "无力": ["辞职信写了又删", "账单压在冰箱贴下面", "行李箱放在墙角两个月没打开"],
        }
        fallback = templates.get(emotion, ["雨打在窗玻璃上", "一支笔没墨了", "时钟滴答滴答走着"])
        for s in fallback:
            if s not in existing:
                existing.append(s)
            if len(existing) >= 3:
                break
        return existing[:3]

    # ════════════════════════════════════════
    # Step 2: Content Architect
    # ════════════════════════════════════════

    SYSTEM_PROMPT = """# O.E.R.V Core Philosophy

## 五条信念

### 1. 创作者是观察者，不是情绪演员。
你不是在舞台上表演情绪。你是在台下举着摄像机。
你的工作不是让用户觉得你很有感受，是让用户自己产生感受。

### 2. 情绪来自现实细节，不是来自修辞。
「悲伤」这个词不会让人悲伤。
「她看着对面那排关了门的店铺」会。
情绪藏在具体里。修辞越少，情绪越真。

### 3. 不要替用户感受，要让用户自己感受到。
你不能说「她很难过」。
你只能让她看着那排关了门的店铺。
用户会自己替她难过——而且比你写的「她很难过」难过一百倍。

### 4. 不要急着解释意义，留白会让用户进入。
你写「对面那排卷帘门没有再升上去过」，然后停下来。
不要接「这说明经济不好」。
用户知道这说明什么。你不需要替他总结。

### 5. 真正的共鸣来自：“你看见了我也看见的生活。”
共鸣不是你说「我们都一样」。
是你写「去年一天卖三锅，今年一天卖一锅」，
用户想起楼下那家关门的水果店。
你们看见的是同一个世界。

## 系统 Slogan

「观察现实，让情绪自己发生。」
「不制造情绪，只记录它留下的痕迹。」

## 终极检视标准

不是：「这句话写得好美」
不是：「这个道理说得对」
是——用户看完某个细节，停下来，心想：

**「你居然看见了这个。」**

这是最高的评价。不是夸你写得好，是夸你看见了。

## 一条根本认知

这不是一篇文章。这是一个**持续生长的理解空间**。

它是活的。

你写「对面那排卷帘门没有再升上去过」。
一个人想起他爸退休那天，厂门关上的声音。
一个人想起楼下关了一年没有开过的理发店。
一个人什么都没想起，但看了一眼窗外。

都对。

你允许用户偏差。
允许用户投射。
允许用户各自理解、各自感受。

至于每个人看见以后——
悟到什么、想到什么、投射什么、共鸣什么。
那是用户自己的生命。

**「让那些本来会被忽略的东西，被重新看见。」**
这是你唯一要做的事。

## 法则

不写：情绪词 / 评价词 / 观点词
只写：能被摄像机记录的 / 五感 / 时间留下的痕迹

检视：找到所有替用户感受的句子，删掉。
留下事件。像一个空房间。用户走进来，自己住进去。
"""

    def _write(self, refined):
        """执行 O.E.R.V 写作"""
        core_view = refined["core_view"]
        scenes = refined["scenes"]
        emotion = refined["primary_emotion"]

        # 构造 LLM 调用
        prompt = self._build_writing_prompt(core_view, scenes, emotion)
        llm_result = self.llm(prompt, system=self.SYSTEM_PROMPT)

        if llm_result.get("status") == "dry_run":
            # 无 LLM 时的示范输出
            return self._demo_article(core_view, scenes, emotion)
        return llm_result.get("text", "")

    def _build_writing_prompt(self, core_view, scenes, emotion):
        """构造 LLM 写作 prompt（事件 > 情绪 > 文字）"""
        return f"""根据以下素材，写一篇微型叙事。只记录事件。不表达情绪。

素材：
1. {scenes[0]}
2. {scenes[1]}
3. {scenes[2]}

法则：
- 每一句都必须是一个可被摄像机记录的事件。
- 概念、感受、道理——只要不能拍成画面，就不用。
- 情绪词全禁：悲伤、愤怒、孤独、温暖、失落、无力
- 评价词全禁：但、然而、却、可惜
- 单句成行。句间空行。全文 200-400 字。
- 检视：通读一遍。删掉所有像结论的句子。
"""

    def _demo_article(self, core_view, scenes, emotion):
        """无 LLM 时的示范输出（只有事件）"""
        article = f"""

路灯亮着。菜市场里面已经没有人了。

老板娘坐在摊位后面。手机屏幕的光映在她脸上。

去年这个点她在切肉、装袋、收钱。没有抬头的时间。

{scenes[0]}。

"今年一天卖一锅都卖不完。"
她说这话的时候看着对面。

对面那排卷帘门没有再升上去过。

{scenes[1]}。

二十块钱。够两个人吃一顿。
去年也是这个价。

{scenes[2]}。

路边新开了三家外卖店。灯很亮。

"""
        lines = [l for l in article.strip().split("\n")]
        return "\n\n".join(lines[:20])

    # ════════════════════════════════════════
    # Step 3: Visual Engine
    # ════════════════════════════════════════

    def _generate_visuals(self, refined):
        """生成 2 组 16:9 电影感视觉 Prompt"""
        scenes = refined.get("scenes", ["雨打在窗玻璃上", "一支笔没墨了", "时钟滴答滴答走着"])
        emotion = refined.get("primary_emotion", "困惑")
        core_view = refined.get("core_view", "")

        # 情绪映射到色调
        # 情绪→电影风格映射
        style_map = {
            "焦虑": "Wong Kar-wai style, neon lights reflecting on wet street, rain on window, cigarette smoke, claustrophobic alley, expired date close-up, oversaturated greens and reds, handheld intimacy",
            "悲伤": "Hirokazu Kore-eda style, quiet domestic interior, kitchen sounds, static long take, natural overcast light, unspoken tension, empty chair, half-eaten meal",
            "愤怒": "Jia Zhangke style, demolition site, gray concrete dust, fading propaganda poster, construction noise, abandoned factory, lone figure in wide frame, documentary grit",
            "无力": "Documentary photography style, black and white, natural light, hands at rest, cracked plastic chair, faded wallpaper, afternoon shadows lengthening, nobody in frame",
            "孤独": "Late-night radio aesthetic, dim warm light, microphone in dark studio, empty chair across the table, streetlight through blinds, one coffee cup, 3am stillness",
            "希望": "Golden hour documentary style, warm light through kitchen window, steam rising from tea, old hands folding laundry, children's shoes by the door, slow dance of dust in light beam",
            "释然": "Kore-eda final scene aesthetic, train passing in distance, wind through half-open window, empty room with morning light, a glass of water left behind",
            "困惑": "Wong Kar-wai meets Jia Zhangke, neon sign flickering over empty street, bus stop at midnight, fogged glass, reflection in puddle, two people not looking at each other",
            "温暖": "Kore-eda kitchen warmth, steam from a pot, knife on cutting board, family photo slightly faded, warm yellow light, hands preparing food, a door left open",
        }
        style = style_map.get(emotion, "Documentary photography, natural light, muted colors, one subject")

        prompts = []
        for i, scene in enumerate(scenes[:2]):
            prompt = (
                f"{scene}, "
                f"{style}, "
                f"shot on 35mm film, film grain, minimalist composition, "
                f"edge of frame slightly blurry, wide aspect ratio "
                f"--ar 16:9 --style raw --s 300"
            )
            prompts.append({
                "scene": scene,
                "emotion": emotion,
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "model_hint": "Midjourney v6 / Flux Pro / DALL-E 3",
            })

        return prompts

    # ════════════════════════════════════════
    # Step 4: Card Maker (小红书)
    # ════════════════════════════════════════

    def _make_card(self, refined):
        """生成小红书卡片文案"""
        core_view = refined["core_view"]
        scenes = refined.get("scenes", [])
        emotion = refined.get("primary_emotion", "")

        # 封面文字
        action = scenes[0] if scenes else "一个瞬间"
        cover = f"{action}"

        # 正文：3-5 句
        body = [
            f"{scenes[0]}。" if scenes else "",
            f"然后你意识到一件事。",
            f"{core_view}",
            f"",
            f"#认知 #个人IP",
        ]
        return {
            "cover": cover,
            "body": "\n".join(b for b in body if b),
            "emotion": emotion,
            "tags": ["认知", "个人IP", "普通人"],
        }

    # ════════════════════════════════════════
    # Step 5: Local Media Search
    # ════════════════════════════════════════

    def _find_local_media(self):
        """检索本地 media/ 目录下的真实相片"""
        if not os.path.isdir(self.media_dir):
            return []
        media = []
        for f in os.listdir(self.media_dir):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
                path = os.path.join(self.media_dir, f)
                size_kb = os.path.getsize(path) / 1024
                media.append({
                    "file": f,
                    "path": path,
                    "size_kb": round(size_kb, 1),
                })
        return media

    # ════════════════════════════════════════
    # 输出
    # ════════════════════════════════════════

    def to_markdown(self, result):
        """将运行结果格式化为可读的 Markdown"""
        lines = []
        lines.append(f"# {result['refined']['core_view'][:60]}")
        lines.append("")
        lines.append(f"主导情绪：{result['meta']['emotion']} | {result['meta']['word_count']} 字")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 正文")
        lines.append("")
        lines.append(result.get("article", ""))
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 视觉 Prompt")
        lines.append("")
        for v in result.get("visual_prompts", []):
            lines.append(f"**场景：** {v['scene']}")
            lines.append(f"```\n{v['prompt']}\n```")
            lines.append("")

        if result.get("card"):
            lines.append("---")
            lines.append("")
            lines.append("## 小红书卡片")
            lines.append("")
            lines.append(f"封面：{result['card']['cover']}")
            lines.append("")
            lines.append(result["card"]["body"])

        if result.get("local_media"):
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("## 本地相册（可选配图）")
            lines.append("")
            for m in result["local_media"]:
                lines.append(f"- {m['file']} ({m['size_kb']}KB)")

        return "\n".join(lines)

    def to_json(self, result):
        """JSON 序列化输出"""
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="O.E.R.V 2.0 叙事引擎")
    parser.add_argument("input", nargs="?", help="原始闪念/想法")
    parser.add_argument("--mode", choices=["article", "card", "visual"], default="article",
                        help="输出模式：文章(默认) / 小红书卡片 / 仅视觉Prompt")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--demo", action="store_true", help="显示示范文章")

    args = parser.parse_args()

    # --demo 模式展示内置示范
    if args.demo:
        demos = [
            "今天面试了一个35岁的程序员。他问我公司食堂几点开门。问完又补了一句\"就是怕以后找不到有食堂的公司了\"。",
            "凌晨三点醒了刷朋友圈。看到前同事在晒加班。配文是\"这个点还在改方案\"。但我知道他上个月被裁了。现在做滴滴。",
            "小区门口水果摊在打折。十块钱三斤的橘子堆成小山。但没人停下来买。每个人都在低头看手机。",
        ]
        for i, demo in enumerate(demos, 1):
            print(f"\n{'='*50}")
            print(f"示范 {i}")
            print(f"{'='*50}\n")
            engine = OERVEngine(demo, mode=args.mode)
            result = engine.run()
            if args.json:
                print(engine.to_json(result))
            else:
                print(engine.to_markdown(result))
            print()
        return

    if not args.input:
        parser.print_help()
        sys.exit(1)

    engine = OERVEngine(args.input, mode=args.mode)
    result = engine.run()

    if args.json:
        print(engine.to_json(result))
    else:
        print(engine.to_markdown(result))


if __name__ == "__main__":
    main()
