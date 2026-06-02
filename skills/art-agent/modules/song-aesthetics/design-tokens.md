{
  "schema": "song-aesthetics-v1",
  "description": "宋式美学设计令牌 — 九大特征映射到具体 CSS/设计参数",
  "version": "1.0.0",

  "color": {
    "description": "宋式用色原则：低饱和·自然色·以青为主·墨色为骨",

    "palette": {
      "primary": {
        "name": "天青",
        "hex": "#7EC8E3",
        "description": "雨过天青云破处 — 宋汝窑标志色，作为主色调"
      },
      "secondary": {
        "name": "黛色",
        "hex": "#4A6670",
        "description": "远山如黛，沉稳深邃，作为辅色"
      },
      "accent": {
        "name": "瑾瑜",
        "hex": "#5B8C7B",
        "description": "美玉之色，温润含蓄，点缀用色"
      },
      "background": {
        "name": "缥色",
        "hex": "#C8D9CE",
        "description": "淡青绿色，背景基调，透亮不刺眼"
      },
      "surface": {
        "name": "莹白",
        "hex": "#E8E2D3",
        "description": "温润玉白，卡片/面板底色"
      },
      "text_primary": {
        "name": "墨色",
        "hex": "#323232",
        "description": "书画之色，正文用色"
      },
      "text_secondary": {
        "name": "鸦青",
        "hex": "#575757",
        "description": "暗青黑，辅助文字，柔和"
      },
      "border": {
        "name": "相思灰",
        "hex": "#9C8E8E",
        "description": "灰色边框，若有若无"
      },
      "highlight": {
        "name": "海棠红",
        "hex": "#DB5A6B",
        "description": "点睛之色，仅在关键处使用（<5%面积）"
      },
      "success": {
        "name": "竹青",
        "hex": "#789262",
        "description": "翠竹之色，成功状态"
      },
      "warning": {
        "name": "秋香",
        "hex": "#A3A87C",
        "description": "秋日黄绿，警告状态"
      },
      "error": {
        "name": "朱砂",
        "hex": "#C23B22",
        "description": "辟邪正红，错误状态"
      },
      "overlay": {
        "name": "玄色",
        "hex": "#1A1A1A",
        "description": "天道之色，遮罩层，半透使用"
      }
    },

    "rules": {
      "saturation_max": 30,
      "contrast_ratio_min": 4.5,
      "accent_usage_max_pct": 5,
      "color_count_max": 5,
      "avoid": [
        "纯白色 #FFFFFF（刺眼，破坏通透感）",
        "纯黑色 #000000（死黑，缺乏层次）",
        "荧光色系（与朴素/含蓄冲突）",
        "多色渐变（破坏朴素/自然）"
      ]
    }
  },

  "typography": {
    "description": "宋式字体原则：温和·清晰·有书卷气",

    "fonts": {
      "display": {
        "family": "Noto Serif CJK SC, Songti SC, serif",
        "size": "36px",
        "weight": 400,
        "line_height": 1.4,
        "letter_spacing": "0.05em",
        "usage": "大标题/展示文字"
      },
      "heading": {
        "family": "Noto Serif CJK SC, Songti SC, serif",
        "size": "24px",
        "weight": 400,
        "line_height": 1.5,
        "letter_spacing": "0.03em",
        "usage": "H2/H3 标题"
      },
      "subheading": {
        "family": "Noto Serif CJK SC, Songti SC, serif",
        "size": "18px",
        "weight": 400,
        "line_height": 1.6,
        "letter_spacing": "0.02em",
        "usage": "小标题/导航"
      },
      "body": {
        "family": "Noto Sans CJK SC, sans-serif",
        "size": "16px",
        "weight": 300,
        "line_height": 1.8,
        "letter_spacing": "0.01em",
        "usage": "正文"
      },
      "caption": {
        "family": "Noto Sans CJK SC, sans-serif",
        "size": "13px",
        "weight": 300,
        "line_height": 1.6,
        "letter_spacing": "0.02em",
        "usage": "标注/注释"
      }
    },

    "rules": {
      "max_line_length": "75字符 (保持可读性)",
      "orphan_control": true,
      "widow_control": true,
      "avoid_justify": "两端对齐破坏留白节奏",
      "prefer_serif": "宋体/楷体优先于黑体"
    }
  },

  "spacing": {
    "description": "宋式留白原则：呼吸感·节奏感·非对称",

    "tokens": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "xxl": "48px",
      "section": "64px",
      "page_margin": "8%"
    },

    "rules": {
      "content_width_max": "68ch (避免行太长)",
      "line_spacing": "1.8 (正文), 1.4 (标题)",
      "paragraph_gap": "1.5em (段落间距 = 1.5倍行高)",
      "section_gap": "2.5em (章节间距)",
      "breathing_ratio": "0.618 (黄金比例留白)",
      "blank_space_min_pct": 30
    }
  },

  "layout": {
    "description": "宋式构图原则：非对称平衡·围合感·远山式层次",

    "grid": {
      "columns": 12,
      "gutter": "24px",
      "margin": "auto",
      "max_width": "1200px"
    },

    "compositions": [
      {
        "name": "枯山水",
        "pattern": "大面积留白+偏右下焦点+水平长线",
        "usage": "首页/Hero/Splash",
        "ratio": "留白70%:内容30%"
      },
      {
        "name": "手卷式",
        "pattern": "水平叙事+渐次展开+分段留白",
        "usage": "长页面/文章/故事",
        "ratio": "内容60%:留白40%"
      },
      {
        "name": "双屏式",
        "pattern": "左右二分+一静一动+非对称平衡",
        "usage": "对比/并列信息",
        "ratio": "内容50%:留白50%"
      },
      {
        "name": "册页式",
        "pattern": "标准网格+清晰分层+小面积点缀",
        "usage": "仪表盘/表单/数据",
        "ratio": "内容55%:留白45%"
      }
    ],

    "rules": {
      "asymmetry_preferred": true,
      "avoid_center_symmetry": "太正=死板,宋式重活气",
      "z_depth_layers": 3,
      "float_elements": "允许内容浮动非齐整边缘"
    }
  },

  "borders_effects": {
    "description": "宋式精致原则：细腻·若有若无·温润如玉",

    "tokens": {
      "border_radius": {
        "sm": "2px",
        "md": "4px",
        "lg": "8px"
      },
      "border_width": {
        "thin": "0.5px",
        "normal": "1px",
        "thick": "2px"
      },
      "shadow": {
        "none": "none",
        "subtle": "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
        "paper": "0 2px 8px rgba(0,0,0,0.08)",
        "float": "0 4px 16px rgba(0,0,0,0.1)"
      }
    },

    "rules": {
      "avoid_sharp_corners": true,
      "shadow_must_be_subtle": "最大透明度<0.12",
      "no_glow_no_neon": true,
      "prefer_paper_like_effects": true,
      "border_opacity_max": 0.3
    }
  },

  "imagery": {
    "description": "宋式图像原则：水墨·留白·写意",

    "styles": [
      "水墨画效果（高对比低饱和）",
      "自然材质纹理（麻纸/绢帛/竹木）",
      "负空间构图（大量留白）",
      "淡彩渲染（低饱和水彩感）",
      "枯山水纹理（砂纹/石纹）",
      "书法笔触（非装饰性书写）"
    ],

    "filters": {
      "song_filter": "brightness(1.05) contrast(0.9) saturate(0.7) sepia(0.1)",
      "ink_wash": "brightness(0.95) contrast(1.15) saturate(0.3) grayscale(0.4)",
      "paper_texture": "blend with #E8E2D3 at 15% opacity"
    },

    "rules": {
      "no_high_contrast_images": true,
      "avoid_photorealistic": true,
      "prefer_line_drawings": true
    }
  },

  "motion": {
    "description": "宋式动效原则：慢·柔·自然",

    "tokens": {
      "duration": {
        "fast": "200ms",
        "normal": "400ms",
        "slow": "800ms",
        "zen": "1200ms"
      },
      "easing": {
        "natural": "cubic-bezier(0.25, 0.1, 0.25, 1.0)",
        "zen": "cubic-bezier(0.65, 0, 0.35, 1)",
        "fade": "ease-in-out",
        "scroll": "cubic-bezier(0.22, 1, 0.36, 1)"
      }
    },

    "rules": {
      "no_bounce_no_spring": true,
      "fade_before_slide": true,
      "parallax_speed": "0.3x (远山式视差)",
      "scroll_behavior": "smooth",
      "avoid_aggressive_animations": true
    }
  },

  "nine_characteristics_map": {
    "留白": {
      "css_rules": [
        "padding: use spacing tokens, minimum 16px",
        "margin: generous, at least 8% on outer containers",
        "max-width: 68ch for text content",
        "line-height: 1.8 for body text",
        "white-space preservation"
      ],
      "parameters": {
        "blank_ratio_min": 0.35,
        "content_density_max": 0.65
      }
    },
    "朴素": {
      "css_rules": [
        "background: solid colors, no gradients",
        "no decorative borders, no flourishes",
        "single font family per project",
        "color count: max 5 (including black & white)",
        "no unnecessary icons or illustrations"
      ],
      "parameters": {
        "color_count_max": 5,
        "gradient_forbidden": true,
        "decoration_forbidden": true
      }
    },
    "自然": {
      "css_rules": [
        "colors from natural palette (earth, sky, plant, mineral)",
        "saturation: max 30% for main colors",
        "textures: subtle paper, ink, bamboo, stone",
        "shapes: organic, avoid perfect geometric when possible",
        "imagery: nature motifs, landscapes, botanicals"
      ],
      "parameters": {
        "color_saturation_max": 0.3,
        "natural_palette_only": true,
        "organic_shapes_preferred": true
      }
    },
    "通透": {
      "css_rules": [
        "light backgrounds (#C8D9CE, #E8E2D3, #D6ECF0)",
        "subtle transparency for overlays",
        "box-shadow: paper-like, not floating",
        "light borders (border-color: #9C8E8E at 0.3 opacity)",
        "avoid heavy backgrounds"
      ],
      "parameters": {
        "bg_brightness_min": 0.75,
        "shadow_opacity_max": 0.12,
        "transparency_layers_allowed": true
      }
    },
    "淡雅": {
      "css_rules": [
        "saturation: 15-30% for all colors except accents",
        "contrast: soft, avoid stark black/white",
        "text: #323232 on #E8E2D3 surface (not #000 on #FFF)",
        "accent colors: used sparingly (<5% of visual area)",
        "tone: muted, refined, never garish"
      ],
      "parameters": {
        "saturation_range": [0.15, 0.30],
        "accent_area_max_pct": 5,
        "contrast_soft": true
      }
    },
    "精致": {
      "css_rules": [
        "border-radius: 2-4px for all elements",
        "typography: precise letter-spacing (0.01-0.05em)",
        "alignment: pixel-perfect grid alignment",
        "border-width: 0.5-1px, subtle",
        "every pixel placed deliberately"
      ],
      "parameters": {
        "border_radius_range": [2, 4],
        "pixel_perfect_required": true,
        "letter_spacing_required": true
      }
    },
    "含蓄": {
      "css_rules": [
        "don't make all information front-facing",
        "use progressive disclosure: show on hover/scroll",
        "let negative space communicate",
        "avoid explicit labels when context suffices",
        "iconography: minimal, abstract, suggestive"
      ],
      "parameters": {
        "directness_level": "low",
        "progressive_disclosure": true,
        "suggestion_over_explicitness": true
      }
    },
    "禅意": {
      "css_rules": [
        "asymmetric compositions (odds > evens in layout)",
        "wabi-sabi: accept imperfection, avoid perfect symmetry",
        "stillness: motion only when functional",
        "empty space as active composition element",
        "vertical rhythm: Chinese scroll-inspired"
      ],
      "parameters": {
        "asymmetry_preferred": true,
        "symmetry_forbidden": true,
        "motion_duration_min_ms": 400
      }
    },
    "有序": {
      "css_rules": [
        "consistent 12-column grid",
        "clear visual hierarchy (scale, weight, position)",
        "repetition: patterns bring order",
        "alignment: every element has a grid reason",
        "information architecture: progressive reveal"
      ],
      "parameters": {
        "grid_required": true,
        "hierarchy_clear": true,
        "alignment_strict": true
      }
    }
  },

  "prohibitions": [
    "荧光色 / 霓虹效果",
    "粗边框 (>2px)",
    "多色渐变",
    "弹跳/弹簧动效",
    "纯黑#000 纯白#FFF",
    "对称居中构图",
    "照片级写实图片（除非内容是照片本身）",
    "弹出式/模态窗口（破坏禅意）",
    "滚动条自定义（保持原生轻量）",
    "图片圆角 >8px",
    "阴影透明度 >12%",
    "同时出现 3 种以上字体"
  ]
}
