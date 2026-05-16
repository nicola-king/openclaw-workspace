# 东方精神美学融 art-agent 方案

> 方案日期：2026-05-16
> 目标：为 art-agent 的 58 品牌规格库扩展 4 个新模块 + 新增路由逻辑

---

## 一、路由集成方案

### dispatcher.py 新增路由规则

在现有智能风格匹配表中插入优先级最高的新规则：

| 内容关键词 | 匹配风格 | 适用场景 |
|-----------|---------|---------|
| **东方/宋代/禅意/道/儒/园林/山水** | **song-dynasty 宋代美学** | **文化/酒店/空间设计** |
| **安藤忠雄/卒姆托/隈研吾/路易斯康/大师** | **world-master 世界大师** | **建筑分析/高端方案** |
| **焦虑/疲惫/独处/冥想/疗愈/情绪** | **emotion-space 情绪空间** | **疗愈/酒店/SPA/民宿** |
| **森林/湖畔/山居/沙漠/自然/生态** | **eco-landscape 生态景观** | **文旅/度假村/康养** |

**优先级：** 东方美学 > 情绪空间 > 生态景观 > 世界大师 > 原58品牌

**未指定风格时的默认匹配规则：**
- 含「空间」「建筑」「酒店」「民宿」「文旅」→ 优先匹配东方美学/生态景观
- 含「疗愈」「SPA」「冥想」「禅修」→ 优先匹配情绪空间/东方美学
- 含「大师」「设计」「建筑史」「理论」→ 优先匹配世界大师

---

## 二、设计令牌扩展（design-tokens.json 新增模块）

### Module 1: Song Dynasty Aesthetic Module（宋代美学）

```json
{
  "song-dynasty": {
    "name": "宋代美学",
    "description": "基于宋代文人画论（郭熙《林泉高致》）、宋代建筑遗存（佛光寺/晋祠/宋陵）及日本禅宗美学传承（受宋文化影响的枯山水/茶道美学），建立起「静、雅、淡、远」的东方精神空间视觉系统。",
    "colors": {
      "primary": "#6B5B4F",
      "primary-muted": "#8B7355",
      "primary-soft": "#A0926B",
      "accent": "#C4A882",
      "accent-soft": "#D4C5A0",
      "ink": "#2C2416",
      "body": "#3A3226",
      "body-on-canvas": "#4A4236",
      "ink-muted": "#6A6256",
      "hairline": "#D8D2C8",
      "hairline-soft": "#E8E2D8",
      "canvas": "#F5F0E8",
      "canvas-parchment": "#EDE8DE",
      "canvas-silk": "#F8F4EC",
      "surface-bamboo": "#D4D0C4",
      "surface-stone": "#C8C0B4",
      "surface-ink": "#1A1A1A",
      "on-primary": "#F5F0E8",
      "on-dark": "#F5F0E8",
      "accent-red": "#9E3B2A",
      "accent-gold": "#B8976A",
      "accent-jade": "#5A7A6A",
      "scrim": "#1A1610"
    },
    "typography": {
      "display-xl": {
        "fontFamily": "'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', serif",
        "fontSize": "56px",
        "fontWeight": 700,
        "lineHeight": 1.2,
        "letterSpacing": "0.12em"
      },
      "display-lg": {
        "fontFamily": "'Noto Serif SC', 'Source Han Serif SC', 'STSong', serif",
        "fontSize": "36px",
        "fontWeight": 600,
        "lineHeight": 1.3,
        "letterSpacing": "0.08em"
      },
      "display-md": {
        "fontFamily": "'Noto Serif SC', 'Source Han Serif SC', serif",
        "fontSize": "28px",
        "fontWeight": 600,
        "lineHeight": 1.4,
        "letterSpacing": "0.06em"
      },
      "lead": {
        "fontFamily": "'Noto Sans SC', 'Source Han Sans SC', sans-serif",
        "fontSize": "21px",
        "fontWeight": 300,
        "lineHeight": 1.8,
        "letterSpacing": "0.04em"
      },
      "body": {
        "fontFamily": "'Noto Sans SC', 'Source Han Sans SC', sans-serif",
        "fontSize": "17px",
        "fontWeight": 400,
        "lineHeight": 1.8,
        "letterSpacing": "0.02em"
      },
      "body-serif": {
        "fontFamily": "'Noto Serif SC', 'STSong', serif",
        "fontSize": "17px",
        "fontWeight": 400,
        "lineHeight": 2.0,
        "letterSpacing": "0.04em"
      },
      "caption": {
        "fontFamily": "'Noto Sans SC', 'Source Han Sans SC', sans-serif",
        "fontSize": "14px",
        "fontWeight": 300,
        "lineHeight": 1.6,
        "letterSpacing": "0.06em"
      },
      "fine-print": {
        "fontFamily": "'Noto Sans SC', sans-serif",
        "fontSize": "12px",
        "fontWeight": 300,
        "lineHeight": 1.5,
        "letterSpacing": "0.04em"
      }
    },
    "spacing": {
      "breath": "16px",
      "flow": "32px",
      "walk": "48px",
      "garden": "64px",
      "grove": "96px",
      "horizon": "128px"
    },
    "radius": {
      "soft": "2px",
      "round": "4px",
      "circle": "50%"
    },
    "principles": ["留白系统（White Space）", "借景系统（Borrowed Scenery）", "枯山水（Dry Landscape）", "不对称（Asymmetry）", "素雅（Subdued Elegance）", "时间痕迹（Wabi-Sabi）"],
    "mood": "静（Tranquility）· 雅（Elegance）· 淡（Subtlety）· 远（Depth）"
  }
}
```

#### CSS 规范核心原则

```css
/* 留白系统 - 不少于40%的负空间 */
.white-space-principle {
  padding: min(8vw, 120px);
  max-width: 680px;
  margin: 0 auto;
}

/* 借景系统 - 框景式构图 */
.borrowed-scenery {
  overflow: hidden;
  position: relative;
}
.borrowed-scenery::after {
  content: '';
  position: absolute;
  border: 1px solid rgba(107, 91, 79, 0.3);
  top: 10%; left: 10%; right: 10%; bottom: 10%;
  pointer-events: none;
}

/* 宋式色彩 - 大地色系为主，点缀朱砂/金/玉 */
.song-palette {
  background: #F5F0E8;
  color: #3A3226;
  border-color: #D8D2C8;
}

/* 不对称构图 */
.asymmetric-layout {
  grid-template-columns: 3fr 2fr 5fr;
}
```

---

### Module 2: World Master Module（世界建筑大师）

```json
{
  "world-master-ando": {
    "name": "安藤忠雄 — 光之叙事",
    "description": "安藤忠雄以裸露混凝土（清水混凝土）为画布，以自然光为画笔，创造出「光与影的寂静交响」的建筑语言。他的空间是让现代人在喧嚣中找回内心的修行场所。",
    "colors": {
      "primary": "#4A4A4A",
      "primary-concrete": "#8A8A8A",
      "primary-light": "#B0B0B0",
      "accent-light": "#F0E8D8",
      "ink": "#1A1A1A",
      "body": "#2A2A2A",
      "canvas": "#D8D0C4",
      "canvas-dark": "#1E1E1E",
      "on-dark": "#E8E0D4",
      "shadow-volume": "#363636",
      "light-beam": "#FFF8E8",
      "water-reflection": "#8A9AAC"
    },
    "typography": {
      "display-xl": {
        "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif",
        "fontSize": "48px",
        "fontWeight": 300,
        "lineHeight": 1.15,
        "letterSpacing": "0.2em"
      },
      "body": {
        "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif",
        "fontSize": "16px",
        "fontWeight": 300,
        "lineHeight": 1.9,
        "letterSpacing": "0.05em"
      }
    },
    "spacing": {
      "volume": "60px",
      "void": "80px",
      "passage": "120px"
    },
    "principles": ["清水混凝土（Exposed Concrete）", "光的教堂化（Sacred Light）", "几何体积（Geometric Volumes）", "水与自然（Water & Nature）", "静谧与纯粹（Stillness & Purity）"]
  },
  "world-master-zumthor": {
    "name": "卒姆托 — 材料之诗",
    "description": "卒姆托的建筑是对材料本质的极致探索。每一块木材、每一片石材都在他的手中释放出原初的感知力量。空间成为身体记忆的容器。",
    "colors": {
      "primary": "#3D352A",
      "primary-wood": "#6B5B4A",
      "primary-stone": "#7A7266",
      "accent-warmth": "#C8B898",
      "ink": "#1A1610",
      "body": "#3A3226",
      "canvas": "#E8E2D8",
      "canvas-dark": "#1E1C18",
      "material-raw": "#8A8276",
      "material-oxidized": "#6A6A60"
    },
    "typography": {
      "display-xl": {
        "fontFamily": "'Akkurat', 'Helvetica Neue', sans-serif",
        "fontSize": "40px",
        "fontWeight": 300,
        "lineHeight": 1.2,
        "letterSpacing": "0.15em"
      },
      "body": {
        "fontFamily": "'Akkurat', 'Helvetica Neue', sans-serif",
        "fontSize": "16px",
        "fontWeight": 300,
        "lineHeight": 1.8,
        "letterSpacing": "0.03em"
      }
    },
    "principles": ["材料感知（Material Perception）", "场所精神（Genius Loci）", "手工感（Craftsmanship）", "时间性（Patina of Time）", "氛围（Atmosphere）"]
  },
  "world-master-kengo-kuma": {
    "name": "隈研吾 — 木之呼吸",
    "description": "隈研吾的「负建筑」哲学让建筑消隐于自然。木材、竹子、和纸等天然材料以现代构造方式重新诠释东方建筑精神，创造建筑与环境的共生关系。",
    "colors": {
      "primary": "#5A4A3A",
      "primary-cedar": "#7A6A52",
      "primary-bamboo": "#8A9A5A",
      "primary-paper": "#F0E8D8",
      "accent": "#C8B898",
      "ink": "#2A2218",
      "body": "#4A4236",
      "canvas": "#F0ECE4",
      "canvas-dark": "#2A261E",
      "wood-light": "#C8B8A0",
      "wood-dark": "#5A4A3A",
      "shadow-lattice": "#3A362E",
      "sky-through": "#8AA8C4"
    },
    "principles": ["负建筑（Weak Architecture）", "消隐（Disappearing）", "层叠（Layering）", "编织（Weaving）", "透光（Translucency）"]
  },
  "world-master-louis-kahn": {
    "name": "路易斯·康 — 光之精神",
    "description": "路易斯·康将建筑视为「光的赋形」。他用厚重的砖石体量捕捉光线，让材料诉说它们的意志。他的空间充满某种古典的神圣感与永恒性。",
    "colors": {
      "primary": "#6A5A4A",
      "primary-brick": "#9A826A",
      "primary-stone": "#B8A898",
      "accent-light": "#F0E8D0",
      "ink": "#1A1612",
      "body": "#3A3228",
      "canvas": "#D8D0C4",
      "shadow-deep": "#1E1A16",
      "light-golden": "#E8D8B8",
      "material-concrete": "#8A8276"
    },
    "typography": {
      "display-xl": {
        "fontFamily": "'Century Schoolbook', 'Georgia', serif",
        "fontSize": "44px",
        "fontWeight": 400,
        "lineHeight": 1.2,
        "letterSpacing": "0.1em"
      },
      "body": {
        "fontFamily": "'Century Schoolbook', 'Georgia', serif",
        "fontSize": "16px",
        "fontWeight": 400,
        "lineHeight": 1.8,
        "letterSpacing": "0.02em"
      }
    },
    "principles": ["光的精神性（Spirit of Light）", "砖想成为拱（What Brick Wants）", "服务与被服务空间（Servant & Served）", "几何原初性（Primordial Geometry）", "沉默与光（Silence & Light）"]
  }
}
```

---

### Module 3: Emotion Space Module（情绪空间）

JSON 格式（添加到 design-tokens.json）：

```json
{
  "emotion-anxiety": {
    "name": "湖居疗愈 — 焦虑",
    "description": "宽旷湖景+水平视线+水声白噪音+柔和晨光的空间配方。治愈都市焦虑，让视觉回归地平线。",
    "colors": {
      "primary": "#4A7A8A",
      "primary-water": "#6A9AAA",
      "primary-sky": "#8AB4C8",
      "accent-mist": "#C8D8E0",
      "accent-warm": "#E8D8C0",
      "ink": "#2A363A",
      "body": "#4A5A5E",
      "canvas": "#F0F0EA",
      "canvas-water": "#D8E4E8",
      "light-morning": "#FFF8E8"
    },
    "typography": {
      "display-lg": {
        "fontFamily": "'Noto Sans SC', sans-serif",
        "fontSize": "32px",
        "fontWeight": 300,
        "lineHeight": 1.5,
        "letterSpacing": "0.1em"
      },
      "body": {
        "fontFamily": "'Noto Sans SC', sans-serif",
        "fontSize": "16px",
        "fontWeight": 300,
        "lineHeight": 2.0,
        "letterSpacing": "0.05em"
      }
    },
    "spatial_character": "开阔、水平、连续、柔和",
    "healing_elements": ["水景", "水平视线", "自然光渐变", "白噪音", "大留白"],
    "mood": "平静 · 释放 · 安全"
  },
  "emotion-fatigue": {
    "name": "森林疗愈 — 疲惫",
    "description": "浓荫覆盖+负氧离子+树影斑驳+苔藓触感。用于职场倦怠、信息过载、身心疲惫人群。",
    "colors": {
      "primary": "#3A6A4A",
      "primary-leaf": "#5A8A5A",
      "primary-moss": "#6A7A5A",
      "accent-light": "#A0C8A0",
      "accent-bark": "#5A4A3A",
      "ink": "#1A2A1E",
      "body": "#3A4A3E",
      "canvas": "#E8ECE4",
      "light-dappled": "#D8E8C8",
      "shadow-green": "#2A3A2E"
    },
    "spatial_character": "围合、层叠、斑驳、湿润",
    "healing_elements": ["树冠覆盖", "苔藓地面", "斑驳光影", "植物香气", "木质触感"],
    "mood": "安宁 · 恢复 · 滋养"
  },
  "emotion-solitude": {
    "name": "山居独处 — 独处",
    "description": "山巅小筑+云雾缭绕+粗粝石壁+壁炉暖光的独处空间。适合需要与自己对话的人。",
    "colors": {
      "primary": "#5A4A3A",
      "primary-stone": "#7A6A5A",
      "primary-cloud": "#C8C0B8",
      "accent-fire": "#B86A3A",
      "accent-warmth": "#D8A878",
      "ink": "#1A1612",
      "body": "#3A3228",
      "canvas": "#E8E2D8",
      "canvas-twillight": "#3A3A3A",
      "text-on-dark": "#D8D0C4",
      "light-warm": "#E8D0B8"
    },
    "spatial_character": "高处、围合、庇护、温暖",
    "healing_elements": ["壁炉", "高处俯瞰", "石质", "温暖光线", "静谧"],
    "mood": "内省 · 清醒 · 完整"
  },
  "emotion-meditation": {
    "name": "禅修空间 — 冥想",
    "description": "绝对极简的坐禅空间。一面白墙、一束天光、一席竹榻。空间本身就是修行。",
    "colors": {
      "primary": "#4A4238",
      "primary-warm": "#5A5248",
      "accent": "#C8C0B4",
      "accent-gold": "#B8A070",
      "ink": "#1A1814",
      "body": "#3A3630",
      "canvas": "#F0ECE4",
      "canvas-silence": "#E8E4DC",
      "light-zen": "#FFF8F0",
      "void": "#D8D4CC"
    },
    "typography": {
      "display-lg": {
        "fontFamily": "'Noto Serif SC', serif",
        "fontSize": "24px",
        "fontWeight": 300,
        "lineHeight": 2.0,
        "letterSpacing": "0.3em"
      },
      "body": {
        "fontFamily": "'Noto Sans SC', sans-serif",
        "fontSize": "15px",
        "fontWeight": 200,
        "lineHeight": 2.0,
        "letterSpacing": "0.1em"
      }
    },
    "spatial_character": "极简、虚空、寂静、时间感",
    "healing_elements": ["天光", "空白墙", "竹材", "香/茶", "寂静"],
    "mood": "空 · 定 · 觉"
  }
}
```

---

### Module 4: Eco-Landscape Module（生态景观）

```json
{
  "eco-forest": {
    "name": "森林场景",
    "description": "密林深处，光影斑驳，材质以木材苔藓为主，自然的庇护场。",
    "colors": {
      "primary": "#2A5A3A",
      "primary-light": "#6A9A5A",
      "accent": "#8ABA6A",
      "ink": "#1A2A1A",
      "canvas": "#E8ECE0",
      "wood": "#5A4A32",
      "moss": "#5A7A4A"
    },
    "materials": ["原木", "苔藓", "石板", "藤编"],
    "principles": ["生态共生", "垂直分层", "自然材质"]
  },
  "eco-lake": {
    "name": "湖畔场景",
    "description": "水平水面，远山倒影，空间以水平延伸和通透为主。",
    "colors": {
      "primary": "#3A6A7A",
      "primary-light": "#6A9AAA",
      "accent": "#8AB8C8",
      "ink": "#1A2A32",
      "canvas": "#E8ECEE",
      "water": "#4A7A8A",
      "sky": "#8AB4C8"
    },
    "materials": ["石材", "玻璃", "原木甲板", "亚麻"],
    "principles": ["水平构图", "镜像反射", "通透性"]
  },
  "eco-mountain": {
    "name": "山居场景",
    "description": "海拔高处，云雾缭绕，粗粝石材与温暖火光的对话。",
    "colors": {
      "primary": "#4A3A2A",
      "primary-light": "#7A6A5A",
      "accent": "#C8A878",
      "ink": "#1A1612",
      "canvas": "#E8E4DC",
      "stone": "#6A5A4A",
      "cloud": "#C8C8C8"
    },
    "materials": ["粗石", "原木", "毛毯", "陶器"],
    "principles": ["高差利用", "庇护感", "粗粝质感"]
  },
  "eco-desert": {
    "name": "沙漠场景",
    "description": "大地色系，极简几何，光影强烈的极端空间体验。",
    "colors": {
      "primary": "#6A5A3A",
      "primary-light": "#8A7A5A",
      "accent": "#C8A86A",
      "ink": "#2A2216",
      "canvas": "#E8DCC8",
      "sand": "#8A7A5A",
      "sky": "#C8C8D0"
    },
    "materials": ["夯土", "石灰", "粗陶", "亚麻"],
    "principles": ["极端光影", "厚重墙体", "纯粹几何"]
  }
}
```

---

## 三、美学评分矩阵扩展

在 aesthetic-scorer 中新增维度：

```python
ORIENTAL_AESTHETIC_DIMENSIONS = {
    "留白度": 0.25,      # 负空间占比评估
    "借景效果": 0.20,    # 框景/透景的设计质量
    "色彩和谐": 0.20,    # 大地色系的和谐度
    "材质真实": 0.15,    # 天然材质的表现力
    "情绪匹配": 0.20     # 情绪疗愈维度的匹配度
}

def score_oriental(space_analysis: dict) -> dict:
    """对东方美学空间方案进行多维度评分"""
    scores = {}
    for dimension, weight in ORIENTAL_AESTHETIC_DIMENSIONS.items():
        # ... scoring logic
        pass
    return scores
```

---

## 四、可视化适配模板

### 新增 html-anything 模板

| 模板名 | 用途 | 调用模块 |
|--------|------|---------|
| `space-song-dynasty` | 宋代美学空间方案展示 | song-dynasty |
| `space-master-profile` | 世界大师风格分析 | world-master-* |
| `space-emotion-healing` | 情绪疗愈空间提案 | emotion-* |
| `space-eco-landscape` | 生态景观空间方案 | eco-* |

### 渲染指令示例

```
渲染请求: "为一家焦虑都市人群设计的湖居疗愈酒店，输出空间美学方案"
→ 识别: emotion-anxiety 模块（主要）+ eco-lake（辅助）+ song-dynasty（配色参考）
→ 输出: 情绪疗愈空间提案 + 氛围板（mood board）
```

---

## 五、实现路径

| 阶段 | 内容 | 工作量 |
|------|------|--------|
| Phase 1 | 新增 design-tokens.json 中4个模块的JSON规范 | 1天 |
| Phase 2 | 扩展 dispatcher.py 路由表（东方美学优先级规则） | 0.5天 |
| Phase 3 | 扩展 aesthetic-scorer（东方美学评分维度） | 0.5天 |
| Phase 4 | 新增 html-anything 空间方案模板 | 1天 |
| Phase 5 | 测试验证（20+测试用例） | 1天 |
| **合计** | | **4天** |

---

*本方案完成后，art-agent 从「58商业品牌设计系统」升级为「58商业品牌 + 东方美学 + 世界大师 + 情绪空间 + 生态景观」的深度美学引擎（73+规格）*
