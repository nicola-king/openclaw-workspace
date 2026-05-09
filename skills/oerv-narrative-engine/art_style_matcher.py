#!/usr/bin/env python3
"""
艺术风格匹配引擎 — 根据闪念/事件自动匹配最合适的艺术风格

涵盖：电影、摄影、绘画、建筑、雕塑、文学、音乐…
每种风格包含：名称、媒介、核心手法、适用情绪、适用场景、Signature元素

接入 O.E.R.V 引擎后，自动为每篇叙事匹配风格。
后期可无限扩展风格库。
"""

STYLE_LIBRARY = [

    # ═══════════════════════════════════════
    # 电影导演
    # ═══════════════════════════════════════

    {
        "id": "wong_kar_wai",
        "name": "王家卫",
        "medium": "电影",
        "mood": ["孤独", "困惑", "无力", "怀旧"],
        "scene": ["城市夜晚", "雨", "小餐馆", "酒吧", "狭窄的公寓", "便利店"],
        "signature": "潮湿的夜色、霓虹灯在雨地上的倒影、烟、过期的日期、不看对方的对话、钟表特写、慢镜头",
        "senses": ["视觉: 高饱和红绿蓝/烟", "听觉: 爵士乐/雨声/留白", "触觉: 潮湿/闷热"],
        "voice": "画外音独白，语速慢，带着过期日期的重量",
        "prompt": "Wong Kar-wai aesthetic, neon lights reflecting on wet street, cigarette smoke, claustrophobic city night, oversaturated colors, handheld camera, intimate close-up",
    },

    {
        "id": "kore_eda",
        "name": "是枝裕和",
        "medium": "电影",
        "mood": ["温暖", "悲伤", "释然", "孤独"],
        "scene": ["厨房", "餐桌", "老房子", "海边", "医院走廊", "便利店门口"],
        "signature": "切菜声、折叠的衣服、吃剩的饭菜、便利店塑料袋、没说出口的话、静谧的长镜头",
        "senses": ["听觉: 切菜/淘米/水烧开", "视觉: 柔和自然光/衣物纹理", "嗅觉: 味噌汤/洗衣粉"],
        "voice": "沉默比对话多，话里有话，总是欲言又止",
        "prompt": "Hirokazu Kore-eda style, quiet domestic interior, natural light, kitchen sounds, static long take, unspoken tension, empty chair at table, half-eaten meal",
    },

    {
        "id": "jia_zhangke",
        "name": "贾樟柯",
        "medium": "电影",
        "mood": ["无力", "困惑", "愤怒", "孤独"],
        "scene": ["拆迁废墟", "长途车站", "城中村", "工厂门口", "小城市街道", "KTV"],
        "signature": "背景电视声/手机铃声/施工噪音、粗糙的手、暮色街道、褪色的标语、下岗工人",
        "senses": ["听觉: 电视/手机/施工噪音", "视觉: 灰/尘土/褪色标语", "触觉: 粗糙/冷"],
        "voice": "方言，不标准的普通话，时代比人 louder",
        "prompt": "Jia Zhangke style, demolition site, gray concrete dust, fading propaganda poster, construction noise, abandoned factory, lone figure in wide frame, documentary grit",
    },

    {
        "id": "hou_hsiao_hsien",
        "name": "侯孝贤",
        "medium": "电影",
        "mood": ["怀旧", "悲伤", "释然"],
        "scene": ["台湾乡村", "老屋", "火车", "稻田", "医院", "庙口"],
        "signature": "极长的固定镜头、风吹树叶、远处的声音、远景中的人物、沉默的吃饭场景、时间的流逝感",
        "senses": ["听觉: 风声/蝉鸣/远处火车", "视觉: 自然光/雾/绿", "触觉: 风/热"],
        "voice": "什么也不说，让镜头替你说话",
        "prompt": "Hou Hsiao-hsien style, extreme long take, Taiwan countryside, wind through trees, distant train sound, figures in landscape, natural light, meditative stillness",
    },

    {
        "id": "abbas_kiarostami",
        "name": "阿巴斯",
        "medium": "电影",
        "mood": ["困惑", "希望", "释然"],
        "scene": ["乡村公路", "山坡", "车内", "樱桃树", "黄昏", "无人的风景"],
        "signature": "车内的对话、窗外的风景、真实与虚构的边界、简单的故事藏着全部、孩子的视角",
        "senses": ["视觉: 金色黄昏/尘土", "听觉: 车内安静/引擎声", "触觉: 风/干燥"],
        "voice": "用最简单的词，问最重的问题",
        "prompt": "Abbas Kiarostami style, Iranian landscape, car interior conversation, golden hour dust, road winding through hills, simple frame, deep philosophical stillness",
    },

    {
        "id": "tsai_ming_liang",
        "name": "蔡明亮",
        "medium": "电影",
        "mood": ["孤独", "无力"],
        "scene": ["出租屋", "空荡的公寓", "雨中", "商场", "卫生间"],
        "signature": "极慢极长的镜头、沉默、雨水、潮湿、身体的疲惫、都市疏离",
        "senses": ["触觉: 潮湿/粘腻", "听觉: 雨声/滴水声/沉默", "视觉: 冷色/暗"],
        "voice": "人物不说话的时候，房间在说话",
        "prompt": "Tsai Ming-liang style, extreme slow cinema, empty apartment, rain on window, solitude in urban space, long static shot, muted colors, physical exhaustion",
    },

    # ═══════════════════════════════════════
    # 摄影
    # ═══════════════════════════════════════

    {
        "id": "moriyama_daido",
        "name": "森山大道",
        "medium": "摄影",
        "mood": ["孤独", "无力", "困惑"],
        "scene": ["城市街头", "小巷", "深夜", "地下通道", "便利店", "流浪"],
        "signature": "高反差黑白、粗颗粒、失焦、晃动、街头流浪者的视角、城市的背面",
        "senses": ["视觉: 黑白粗颗粒/高反差", "听觉: 城市白噪音", "触觉: 粗糙"],
        "voice": "像一张曝光不足的照片，暗处比亮处多",
        "prompt": "Daido Moriyama photography, high contrast black and white, rough grain, out of focus urban street, stray dog perspective, alley at night, raw documentary",
    },

    {
        "id": "saul_leiter",
        "name": "Saul Leiter",
        "medium": "摄影",
        "mood": ["温暖", "孤独", "怀旧"],
        "scene": ["雪天的街道", "咖啡馆窗口", "公交车内", "雨伞下", "纽约街头"],
        "signature": "透过玻璃/雨/雾气拍摄、柔和的色彩、抽象的城市局部、模糊的人影",
        "senses": ["视觉: 柔焦/粉色/白色", "触觉: 冷/温暖室内", "听觉: 城市远处的声音"],
        "voice": "世界在玻璃的另一边，模糊但美",
        "prompt": "Saul Leiter style, shot through rain-streaked glass, soft muted colors, blurred urban figure, painterly abstraction, intimate street photography, snowy city",
    },

    {
        "id": "alex_webb",
        "name": "Alex Webb",
        "medium": "摄影",
        "mood": ["困惑", "活力", "孤独"],
        "scene": ["热闹的街头市场", "拥挤的公交", "小巷", "色彩强烈的街头"],
        "signature": "复杂的构图、强烈的色彩冲突、多层纵深、拥挤中的孤独",
        "senses": ["视觉: 多层/色彩冲突", "听觉: 街头喧嚣", "触觉: 热/拥挤"],
        "voice": "画面里塞满了人，但每个人都是孤独的",
        "prompt": "Alex Webb style, complex layered composition, intense color contrast, crowded street, solitary figure in chaos, deep depth, documentary street photography",
    },

    # ═══════════════════════════════════════
    # 绘画
    # ═══════════════════════════════════════

    {
        "id": "edward_hopper",
        "name": "Edward Hopper",
        "medium": "绘画",
        "mood": ["孤独", "无力", "困惑"],
        "scene": ["深夜餐馆", "空荡的办公室", "旅馆房间", "加油站", "火车车厢"],
        "signature": "孤立的个人、大片的空墙、窗外的光、静止的时间、城市的沉默",
        "senses": ["视觉: 大片空墙/锐利光影", "触觉: 冷/空", "听觉: 沉默"],
        "voice": "画里的人都像在等什么，但不知道自己等的是什么",
        "prompt": "Edward Hopper painting, solitary figure in empty interior, harsh light through window, long shadows, urban isolation, stillness, melancholic atmosphere",
    },

    {
        "id": "van_gogh",
        "name": "梵高",
        "medium": "绘画",
        "mood": ["焦虑", "温暖", "希望"],
        "scene": ["麦田", "咖啡馆", "卧室", "星空下", "田野小路"],
        "signature": "粗犷的笔触、旋转的天空、明亮的黄色、厚涂的颜料、生命力的挣扎",
        "senses": ["视觉: 厚涂/旋转/黄蓝", "触觉: 颜料堆叠的质感", "听觉: 风声"],
        "voice": "每个笔触都在喊，但喊的是什么连他自己也不知道",
        "prompt": "Van Gogh style, thick impasto brushstrokes, swirling sky, vibrant yellow and blue, emotional intensity, starry night, wheat field, expressive texture",
    },

    {
        "id": "andrew_wyeth",
        "name": "Andrew Wyeth",
        "medium": "绘画",
        "mood": ["孤独", "悲伤", "怀旧"],
        "scene": ["农场", "山坡", "老房子", "冬天的田野", "窗口"],
        "signature": "蛋彩画的干燥质感、苍白的草、远方的山坡、一个背影、风干了的温度",
        "senses": ["视觉: 蛋彩干枯质感/苍白", "触觉: 干燥/冷", "听觉: 风"],
        "voice": "那是一种干了之后不会消失的情绪",
        "prompt": "Andrew Wyeth painting, tempera texture, dry winter grass, distant hill, lone figure in landscape, pale light, nostalgic rural America, muted earth tones",
    },

    # ═══════════════════════════════════════
    # 建筑
    # ═══════════════════════════════════════

    {
        "id": "tadao_ando",
        "name": "安藤忠雄",
        "medium": "建筑",
        "mood": ["孤独", "释然", "困惑"],
        "scene": ["清水混凝土走廊", "光之教堂", "无人的庭院", "海边", "地下"],
        "signature": "清水混凝土、光从缝隙中射入、极简几何、水的反射、空间的孤独感",
        "senses": ["视觉: 灰/光缝/几何", "触觉: 混凝土冷/光滑", "听觉: 脚步声的回响/水声"],
        "voice": "空间本身就是一种沉默的叙述",
        "prompt": "Tadao Ando architecture, bare concrete walls, light streaming through geometric slit, reflecting water pool, minimal space, solitude, meditative shadow play",
    },

    {
        "id": "peter_zumthor",
        "name": "卒姆托",
        "medium": "建筑",
        "mood": ["温暖", "释然", "怀旧"],
        "scene": ["小教堂", "温泉浴场", "山间小屋", "木头房子"],
        "signature": "材料的质感被放到最大、石头/木头/水的触感、光影的缓慢移动、场所的精神",
        "senses": ["触觉: 木头纹理/石头冷", "嗅觉: 木头/潮湿石头", "听觉: 水滴/脚步声"],
        "voice": "材料会说话。你只需要安静下来听",
        "prompt": "Peter Zumthor architecture, material sensuality, stone texture, warm wood, steam rising, slow moving light, sacred atmosphere, sensory experience of space",
    },

    # ═══════════════════════════════════════
    # 文学
    # ═══════════════════════════════════════

    {
        "id": "raymond_carver",
        "name": "Raymond Carver",
        "medium": "文学",
        "mood": ["无力", "孤独", "悲伤"],
        "scene": ["不起眼的厨房", "小酒馆", "停车场", "廉租房", "医院等候室"],
        "signature": "蓝领的生活碎片、没说出口的话、一瓶啤酒在桌上、一个突然结束的短篇",
        "senses": ["视觉: 廉价/破旧", "听觉: 沉默大于对话", "触觉: 廉价的质感"],
        "voice": "故事结束了。但你没觉得它结束。你觉得它还在那里，在某个人的厨房里继续。",
        "prompt": "Raymond Carver literary aesthetic, working class interior, half-empty beer bottle, unspoken tension, ordinary moment, quiet devastation, minimal detail",
    },

    {
        "id": "murakami_haruki",
        "name": "村上春树",
        "medium": "文学",
        "mood": ["孤独", "困惑"],
        "scene": ["深夜的厨房", "空荡的公寓", "爵士酒吧", "井底", "高速公路"],
        "signature": "煮意大利面、听爵士乐、井、猫、不存在的入口、日常中的超现实",
        "senses": ["听觉: 爵士乐/煮水声", "视觉: 冷/蓝/清晰", "触觉: 孤独的重量"],
        "voice": "用最平静的语气，说最奇怪的事情",
        "prompt": "Haruki Murakami atmosphere, late night kitchen, jazz playing, cooking pasta, empty apartment, surreal in everyday, blue tone, melancholic solitude",
    },

    # ═══════════════════════════════════════
    # 雕塑 / 装置
    # ═══════════════════════════════════════

    {
        "id": "donald_judd",
        "name": "Donald Judd",
        "medium": "雕塑",
        "mood": ["释然", "困惑"],
        "scene": ["白色展厅", "沙漠中的盒子", "重复的几何体", "空旷"],
        "signature": "极简的金属盒子、重复的间距、材料即内容、不表达任何情绪但让人产生情绪",
        "senses": ["视觉: 精确的重复/金属", "触觉: 冷/精确", "空间: 间距的节奏感"],
        "voice": "什么都不表达，本身就是一种表达",
        "prompt": "Donald Judd sculpture, minimalist metal boxes, precise repetition, clean lines, industrial materials, object in space, Texas desert, pure form",
    },
]


# ════════════════════════════════════════
# 风格匹配引擎
# ════════════════════════════════════════

class ArtStyleMatcher:
    """根据事件情绪和场景，自动匹配最优艺术风格"""

    def __init__(self):
        self.styles = STYLE_LIBRARY

    def match(self, emotion: str, scenes: list = None, text: str = "") -> list:
        """
        匹配最适合的艺术风格
        
        返回：按匹配度排序的 [(style, score), ...]
        """
        scored = []
        for style in self.styles:
            score = 0

            # 情绪匹配 (权重 0.4)
            if emotion in style.get("mood", []):
                score += 0.4
            else:
                # 部分匹配
                for m in style.get("mood", []):
                    if emotion and (m in emotion or emotion in m):
                        score += 0.15

            # 场景关键词匹配 (权重 0.3)
            if scenes:
                scene_text = " ".join(scenes).lower()
                for s in style.get("scene", []):
                    if s.lower() in scene_text:
                        score += 0.1

            # 文本情绪密度 (权重 0.3)
            if text:
                text_lower = text.lower()
                # 匹配 signature 中的关键词
                sig_words = style.get("signature", "").split("、")
                hits = sum(1 for w in sig_words if w.strip()[:2] in text_lower)
                score += min(hits * 0.05, 0.3)

            scored.append((style, min(score, 1.0)))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def best(self, emotion: str, scenes: list = None, text: str = "") -> dict:
        """返回最优风格及其置信度"""
        results = self.match(emotion, scenes, text)
        if results and results[0][1] > 0:
            return {"style": results[0][0], "confidence": results[0][1], "ranked": results[:5]}
        # 兜底：返回通用纪实风格
        return {
            "style": {
                "id": "documentary_default",
                "name": "纪实摄影",
                "medium": "摄影",
                "signature": "自然的凝视、人在中央、时间静止",
                "voice": "你只是在场",
                "prompt": "Documentary photography style, natural light, real moment, human in center, honest frame, no staging, decisive moment",
            },
            "confidence": 0.3,
            "ranked": results[:5],
        }

    def list_by_medium(self) -> dict:
        """按媒介分类列出所有风格"""
        groups = {}
        for s in self.styles:
            m = s.get("medium", "其他")
            if m not in groups:
                groups[m] = []
            groups[m].append(s["name"])
        return groups

    def get_by_id(self, style_id: str) -> dict:
        """按 ID 获取风格详情"""
        for s in self.styles:
            if s["id"] == style_id:
                return s
        return {}


# ════════════════════════════════════════
# 测试
# ════════════════════════════════════════

def demo():
    matcher = ArtStyleMatcher()

    test_cases = [
        ("孤独", ["深夜的便利店", "雨", "一个人吃饭"], "深夜去买东西"),
        ("温暖", ["厨房", "切菜", "一家人吃饭"], "妈妈做了我最爱吃的菜"),
        ("无力", ["拆迁", "空荡的街道", "卷帘门拉下来了"], "对面那排店关了"),
        ("困惑", ["面试", "冷", "公交站"], "面试官说你等通知"),
        ("希望", ["麦田", "黄昏", "回家的路"], "孩子放学了"),
    ]

    for emotion, scenes, text in test_cases:
        result = matcher.best(emotion, scenes, text)
        style = result["style"]
        print(f"\n情绪: {emotion}")
        print(f"  最优: {style['name']} ({style['medium']}) — 置信度 {result['confidence']:.0%}")
        print(f"  签名: {style['signature'][:40]}...")

    print("\n\n风格库总览:")
    for medium, names in matcher.list_by_medium().items():
        print(f"  {medium}: {', '.join(names)}")


if __name__ == "__main__":
    demo()
