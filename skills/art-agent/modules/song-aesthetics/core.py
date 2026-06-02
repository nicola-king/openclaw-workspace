#!/usr/bin/env python3
"""
宋式美学模块 v1.0.0 — Song Dynasty Aesthetics Engine
太一系统 — 九大特征：留白·朴素·自然·通透·淡雅·精致·含蓄·禅意·有序

职责:
  1. 根据 9 特征自动评估 & 生成设计决策
  2. 提供 CSS/设计令牌 → 渲染引擎
  3. 与 aesthetic-filter/scoring-engine 联动
  4. 每个输出验证是否符合宋式美学
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum


class SongCharacteristic(Enum):
    """宋式美学九大特征"""
    LIUBAI = "留白"        # Empty Space / Ma
    PUSU = "朴素"          # Simplicity / Pu
    ZIRAN = "自然"         # Naturalness
    TONGTOU = "通透"       # Transparency / Luminosity
    DANYA = "淡雅"        # Elegant Subdued
    JINGZHI = "精致"       # Refined / Exquisite
    HANXU = "含蓄"        # Understated / Implicit
    CHANYI = "禅意"       # Zen Spirit
    YOUXU = "有序"         # Order / Structure


class SongAestheticsEngine:
    """宋式美学引擎"""

    def __init__(self, config_path: str = "config.json", tokens_path: str = "design-tokens.json"):
        self.logger = self._setup_logger()
        self.config = self._load_json(config_path)
        self.tokens = self._load_json(tokens_path)
        self.process_history: List[Dict[str, Any]] = []

    def _load_json(self, path: str) -> Dict[str, Any]:
        try:
            p = Path(__file__).parent / path
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"加载失败 {path}: {e}")
            return {}

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("song-aesthetics")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    # ═══════════════════════════════════════════
    # 主入口：评估内容是否符合宋式美学
    # ═══════════════════════════════════════════

    def evaluate(self, content: str, content_type: str = "markdown") -> Dict[str, Any]:
        """评估内容—返回 9 维度得分 + 综合等级"""
        results = {}
        total = 0

        for char in SongCharacteristic:
            scorer = getattr(self, f"_score_{char.name.lower()}", None)
            if scorer:
                score, detail = scorer(content, content_type)
                results[char.value] = {
                    "score": score,
                    "detail": detail
                }
                total += score

        avg = round(total / len(SongCharacteristic), 1)
        level = self._determine_level(avg)

        report = {
            "total_score": avg,
            "level": level,
            "dimensions": results,
            "content_type": content_type,
            "timestamp": datetime.now().isoformat()
        }

        self.process_history.append(report)
        return report

    def _determine_level(self, score: float) -> str:
        if score >= 90: return "S"
        elif score >= 75: return "A"
        elif score >= 60: return "B"
        else: return "C"

    # ═══════════════════════════════════════════
    # 九特征评分器
    # ═══════════════════════════════════════════

    def _score_liubai(self, content: str, ct: str) -> Tuple[float, Dict]:
        """留白：检查空白比例、段落间距、拥挤度"""
        score = 100.0
        details = {}

        lines = content.split('\n')
        total_lines = len(lines)
        blank_lines = sum(1 for l in lines if l.strip() == '')
        blank_ratio = blank_lines / max(total_lines, 1)

        details["blank_ratio"] = round(blank_ratio, 2)

        # 段落间距（连续空行 = 呼吸）
        double_blanks = content.count('\n\n\n')
        if double_blanks > 3:
            score -= 10
            details["issue"] = "过度留白，出现连续空行"

        # 理想留白 25-40%
        if blank_ratio < 0.15:
            score -= 20
            details["issue"] = f"留白不足 ({blank_ratio:.0%})，需要增加呼吸空间"
        elif blank_ratio < 0.25:
            score -= 8
            details["hint"] = "留白略少，建议增加段落间距"
        elif blank_ratio > 0.50:
            score -= 10
            details["hint"] = "留白过多，内容密度偏低"

        # 检查长段落（>500字视为太挤）
        long_paras = 0
        for para in content.split('\n\n'):
            if len(para) > 500:
                long_paras += 1
        if long_paras > 0:
            score -= 10 * min(long_paras, 3)
            details["long_paragraphs"] = long_paras

        return max(0, score), details

    def _score_pusu(self, content: str, ct: str) -> Tuple[float, Dict]:
        """朴素：是否有多余装饰、复杂格式"""
        score = 100.0
        details = {}

        # 检查装饰性元素
        decorations = {
            "分隔线过多": len(re.findall(r'^---+\s*$', content, re.MULTILINE)),
            "表格过多": len(re.findall(r'\|.*\|\n\|[-:\s|]+\|', content)),
            "代码块过多": content.count('```'),
            "Emoji过多": len(re.findall(r'[\U0001F300-\U0001F9FF\u2600-\u27BF]', content)),
        }

        # 装饰合理但不过量
        if decorations["分隔线过多"] > 5:
            score -= 10
        if decorations["表格过多"] > 8:
            score -= 8
        if decorations["Emoji过多"] > 30:
            score -= 12
            details["emoji_overload"] = True

        # 标题层级过多 = 繁杂
        heading_levels = set()
        for m in re.finditer(r'^(#{1,6})\s', content, re.MULTILINE):
            heading_levels.add(len(m.group(1)))
        if len(heading_levels) > 4:
            score -= 10
            details["heading_levels"] = len(heading_levels)

        details["decorations"] = decorations
        return max(0, score), details

    def _score_ziran(self, content: str, ct: str) -> Tuple[float, Dict]:
        """自然：语言自然度、不做作"""
        score = 100.0
        details = {}

        # 检查过度修饰词汇
        artificial_words = [
            '令人惊叹', '惊为天人', '叹为观止', '无与伦比',
            '极致', '完美', '绝对', '顶级', '最强',
            '革命性', '颠覆性', '划时代',
        ]
        found_artificial = [w for w in artificial_words if w in content]
        if found_artificial:
            score -= 10 * min(len(found_artificial), 3)
            details["artificial_words"] = found_artificial

        # 检查句式多样性（机械重复的固定句式）
        sentences = re.split(r'[。！？.!?]', content)
        sentence_starts = {}
        for s in sentences:
            s = s.strip()
            if s:
                start = s[:3]
                sentence_starts[start] = sentence_starts.get(start, 0) + 1

        repetitive = {k: v for k, v in sentence_starts.items() if v > 3}
        if repetitive:
            score -= 8
            details["repetitive_starts"] = repetitive

        # 自然语言应有长短句交替
        if sentences:
            short_count = sum(1 for s in sentences if len(s) < 10)
            long_count = sum(1 for s in sentences if len(s) > 50)
            if short_count == 0 and long_count == 0:
                score -= 5
                details["monotone_length"] = True

        return max(0, score), details

    def _score_tongtou(self, content: str, ct: str) -> Tuple[float, Dict]:
        """通透：清晰度、无障碍、层次感"""
        score = 100.0
        details = {}

        # 信息密度（字符/段落）
        paras = [p for p in content.split('\n\n') if p.strip()]
        if paras:
            densities = [len(p) for p in paras]
            avg_density = sum(densities) // len(paras)
            details["avg_paragraph_length"] = avg_density

            if avg_density > 400:
                score -= 15
                details["issue"] = "段落过长，影响通透感"

        # 使用多级标题 = 层次丰富（好）
        heading_count = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
        if heading_count < 2 and len(content) > 500:
            score -= 12
            details["missing_heading"] = True
        elif heading_count > 0:
            details["hierarchy_good"] = True

        # 使用列表 = 信息清晰
        list_count = len(re.findall(r'^[\-\*\+]\s', content, re.MULTILINE))
        if list_count > 0:
            details["lists_help_clarity"] = True

        return max(0, score), details

    def _score_danya(self, content: str, ct: str) -> Tuple[float, Dict]:
        """淡雅：克制、不张扬"""
        score = 100.0
        details = {}

        # 检查全大写（中文无大写，主要是语气夸张）
        exaggerations = [
            '!!!', '！！！', '😱', '🔥', '💥', '💯',
            '重磅', '震惊', '沸腾', '疯了', '炸了',
        ]
        found_ex = [w for w in exaggerations if w in content]
        if found_ex:
            score -= 15 * min(len(found_ex), 3)
            details["exaggerations"] = found_ex

        # 检查过多的加粗/强调
        bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))
        if bold_count > 8:
            score -= 10
            details["over_emphasis"] = True

        # 过多的语气词
        tone_particles = ['啊', '呢', '哟', '嘛', '哦', '哈', '啦']
        found_particles = sum(1 for p in tone_particles if p in content)
        if found_particles > 5:
            score -= 5

        return max(0, score), details

    def _score_jingzhi(self, content: str, ct: str) -> Tuple[float, Dict]:
        """精致：排版细腻、格式规范"""
        score = 100.0
        details = {}

        # 句号使用规范
        periods = content.count('。')
        missing_periods = 0
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith(('#', '-', '*', '+', '>', '`', '|')) \
               and not line.endswith(('。', '？', '！', '……', '——', '.', '?', '!', ':', ';', ',')) \
               and len(line) > 10:
                missing_periods += 1
        if missing_periods > 3:
            score -= 10
            details["missing_periods"] = missing_periods

        # 统一标点（中文标点 vs 英文标点混用）
        mixed_punctuation = False
        if '。' in content and '.' in content:
            mixed_punctuation = True
        if '，' in content and ',' in content:
            mixed_punctuation = True

        if mixed_punctuation:
            score -= 8
            details["mixed_punctuation"] = True

        # 列表格式统一性
        list_symbols = re.findall(r'^([\-\*\+])\s', content, re.MULTILINE)
        if list_symbols:
            unique_symbols = set(list_symbols)
            if len(unique_symbols) > 1:
                score -= 8
                details["list_inconsistency"] = True

        # 代码块有语言标注
        code_blocks = re.findall(r'```(\w*)', content)
        unmarked = sum(1 for lang in code_blocks if not lang)
        if unmarked > 0:
            score -= 5 * min(unmarked, 3)
            details["unmarked_code_blocks"] = unmarked

        return max(0, score), details

    def _score_hanxu(self, content: str, ct: str) -> Tuple[float, Dict]:
        """含蓄：不言尽、留想象空间"""
        score = 100.0
        details = {}

        # 过度使用确定性/绝对性词汇
        absolute_words = [
            '一定', '必须', '绝对', '永远', '所有', '任何',
            '总是', '从不', '就是', '只能', '只有',
        ]
        found_absolute = [w for w in absolute_words if w in content]
        if found_absolute:
            score -= 8 * min(len(found_absolute), 4)
            details["absolute_words"] = found_absolute

        # 带分寸感的词汇 = 加分
        nuanced_words = [
            '或许', '可能', '微妙', '似乎', '蕴含',
            '隐约', '若隐若现', '似是而非', '意在言外',
        ]
        found_nuanced = [w for w in nuanced_words if w in content]
        if found_nuanced:
            score += 5  # 加分

        # 过度使用"我"（主观性过强）
        i_count = len(re.findall(r'\b我\b', content))
        if i_count > 10:
            score -= 8
            details["self_reference_excessive"] = i_count

        return max(0, score), details

    def _score_chanyi(self, content: str, ct: str) -> Tuple[float, Dict]:
        """禅意：寂静、留白中的力量"""
        score = 100.0
        details = {}

        # 检查节奏段落（非对称感）
        paras = [p for p in content.split('\n\n') if p.strip()]
        if paras:
            lengths = [len(p) for p in paras]
            # 段落长度不均衡 = 有节奏美（加分）
            if lengths:
                max_l = max(lengths)
                min_l = min(lengths)
                if max_l > 0 and min_l > 0:
                    ratio = max_l / min_l
                    details["length_ratio"] = round(ratio, 1)
                    if ratio > 5:
                        score += 5  # 有节奏变化加分
                    if 1.0 < ratio < 1.2:
                        score -= 10  # 太均匀 = 死板

        # 太多功利性词汇
        profit_words = ['立即', '马上', '速抢', '限时', '优惠', '免费', '赚钱']
        found_profit = [w for w in profit_words if w in content]
        if found_profit:
            score -= 15 * min(len(found_profit), 3)
            details["profit_orientation"] = found_profit

        # 过多连接词 = 不够静（禅意需要留白）
        connectors = ['因此', '所以', '然而', '但是', '另外', '此外']
        found_conn = [c for c in connectors if c in content]
        if len(found_conn) > 5:
            score -= 5

        return max(0, score), details

    def _score_youxu(self, content: str, ct: str) -> Tuple[float, Dict]:
        """有序：结构清晰、层次分明"""
        score = 100.0
        details = {}

        # 标题层级连续性
        lines = content.split('\n')
        prev_level = 0
        jumps = 0
        for line in lines:
            m = re.match(r'^(#{1,6})\s', line)
            if m:
                level = len(m.group(1))
                if prev_level > 0 and level > prev_level + 1:
                    jumps += 1
                prev_level = level

        if jumps > 0:
            score -= 15 * min(jumps, 3)
            details["heading_jumps"] = jumps

        # 至少有一个 H1
        has_h1 = bool(re.search(r'^# ', content, re.MULTILINE))
        if not has_h1 and len(content) > 200:
            score -= 10
            details["missing_h1"] = True

        # 列表嵌套层级合理
        list_indents = []
        for line in lines:
            m = re.match(r'^(\s*)[\-\*\+]\s', line)
            if m:
                list_indents.append(len(m.group(1)))
        if list_indents:
            max_indent = max(list_indents)
            if max_indent > 12:
                score -= 8
                details["deep_list_nesting"] = True

        # 信息：代码块在前，说明在后 = 有序
        if '```' in content:
            # 检查是否有代码块说明
            has_code_title = bool(re.search(r'```\w*\n.*```', content))
            details["code_documented"] = has_code_title

        return max(0, score), details

    # ═══════════════════════════════════════════
    # 设计决策生成
    # ═══════════════════════════════════════════

    def generate_design_decisions(self, context: str = "") -> Dict[str, Any]:
        """根据 9 特征生成具体设计决策"""
        return {
            "color_palette": self.tokens.get("color", {}).get("palette", {}),
            "typography": self.tokens.get("typography", {}),
            "spacing": self.tokens.get("spacing", {}),
            "composition": self._suggest_composition(context),
            "prohibitions": self.tokens.get("prohibitions", []),
            "song_css_filter": self.tokens.get("imagery", {}).get("filters", {}).get("song_filter"),
        }

    def _suggest_composition(self, context: str) -> Dict:
        """根据内容建议构图方案"""
        compositions = self.tokens.get("layout", {}).get("compositions", [])

        if not context:
            return compositions[0] if compositions else {}

        # 按关键字匹配
        keyword_map = {
            "枯山水": ["首页", "hero", "splash", "欢迎", "landing"],
            "手卷式": ["文章", "故事", "长文", "blog", "article", "叙事"],
            "双屏式": ["对比", "并列", "vs", "比较", "对比分析"],
            "册页式": ["数据", "仪表", "表单", "grid", "dashboard", "报告"],
        }

        for comp_name, keywords in keyword_map.items():
            if any(k in context.lower() for k in keywords):
                for c in compositions:
                    if c["name"] == comp_name:
                        return c

        return compositions[0] if compositions else {}

    # ═══════════════════════════════════════════
    # CSS 生成
    # ═══════════════════════════════════════════

    def generate_css(self, scope: str = ":root") -> str:
        """生成宋式美学 CSS custom properties"""
        palette = self.tokens.get("color", {}).get("palette", {})
        spacing = self.tokens.get("spacing", {}).get("tokens", {})
        typography = self.tokens.get("typography", {}).get("fonts", {})

        css = f"""{scope} {{
  /* 宋式美学 - 色彩 */
  --song-bg: {palette.get('background', {}).get('hex', '#C8D9CE')};
  --song-surface: {palette.get('surface', {}).get('hex', '#E8E2D3')};
  --song-primary: {palette.get('primary', {}).get('hex', '#7EC8E3')};
  --song-secondary: {palette.get('secondary', {}).get('hex', '#4A6670')};
  --song-accent: {palette.get('accent', {}).get('hex', '#5B8C7B')};
  --song-text: {palette.get('text_primary', {}).get('hex', '#323232')};
  --song-text-secondary: {palette.get('text_secondary', {}).get('hex', '#575757')};
  --song-border: {palette.get('border', {}).get('hex', '#9C8E8E')};
  --song-highlight: {palette.get('highlight', {}).get('hex', '#DB5A6B')};

  /* 宋式美学 - 留白 */
  --song-space-xs: {spacing.get('xs', '4px')};
  --song-space-sm: {spacing.get('sm', '8px')};
  --song-space-md: {spacing.get('md', '16px')};
  --song-space-lg: {spacing.get('lg', '24px')};
  --song-space-xl: {spacing.get('xl', '32px')};
  --song-space-xxl: {spacing.get('xxl', '48px')};

  /* 宋式美学 - 字体 */
  --song-font-display: {typography.get('display', {}).get('family', 'serif')};
  --song-font-body: {typography.get('body', {}).get('family', 'sans-serif')};
  --song-font-caption: {typography.get('caption', {}).get('family', 'sans-serif')};

  /* 宋式美学 - 圆角 */
  --song-radius-sm: 2px;
  --song-radius-md: 4px;
  --song-radius-lg: 8px;

  /* 宋式美学 - 阴影 */
  --song-shadow-none: none;
  --song-shadow-subtle: 0 1px 3px rgba(0,0,0,0.06);
  --song-shadow-paper: 0 2px 8px rgba(0,0,0,0.08);
}}"""
        return css

    # ═══════════════════════════════════════════
    # 辅助接口
    # ═══════════════════════════════════════════

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "module": "song-aesthetics",
            "version": "1.0.0",
            "characteristics": [c.value for c in SongCharacteristic],
            "total_processed": len(self.process_history)
        }

    @property
    def name(self) -> str:
        return "song-aesthetics"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def dependencies(self) -> List[str]:
        return ["aesthetic-filter", "scoring-engine"]


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="宋式美学引擎")
    parser.add_argument("--input", "-i", help="评估文件路径")
    parser.add_argument("--text", help="直接评估文本")
    parser.add_argument("--css", action="store_true", help="生成 CSS custom properties")
    parser.add_argument("--tokens", action="store_true", help="输出设计令牌")
    parser.add_argument("--composition", help="建议构图方案（传入上下文）")
    parser.add_argument("--health", action="store_true", help="健康检查")

    args = parser.parse_args()

    engine = SongAestheticsEngine()

    if args.health:
        print(json.dumps(engine.health_check(), indent=2, ensure_ascii=False))
    elif args.css:
        print(engine.generate_css())
    elif args.tokens:
        print(json.dumps(engine.tokens, indent=2, ensure_ascii=False))
    elif args.composition:
        print(json.dumps(engine._suggest_composition(args.composition), indent=2, ensure_ascii=False))
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
        report = engine.evaluate(content)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.text:
        report = engine.evaluate(args.text)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(engine.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
