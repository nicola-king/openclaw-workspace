# 技能元数据标准 (YAML Frontmatter)

> 版本：1.0 | 创建时间：2026-04-04 | 层级：Tier 2
> 触发：能力涌现 (Agent Skills 架构学习)

---

## 📋 标准格式

所有 `SKILL.md` 文件必须以 YAML Frontmatter 开头：

```yaml
---
skill: <skill-name>
version: <major.minor.patch>
author: <author-name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
status: <stable|beta|experimental|deprecated>
triggers:
  - <trigger-keyword-1>
  - <trigger-keyword-2>
permissions:
  - <permission-1>
  - <permission-2>
max_context_tokens: <number>
priority: <1|2|3>
description: <one-line-description>
tags:
  - <tag-1>
  - <tag-2>
dependencies:
  - <dependency-1>
  - <dependency-2>
config:
  <key>: <value>
---
```

---

## 🔑 必填字段

### `skill` (string)
**用途**: 技能唯一标识符

**规则**:
- 小写字母 + 连字符
- 与目录名一致
- 全局唯一

**示例**:
```yaml
skill: browser-automation
skill: zhiji-e-strategy
skill: gmgn-swap
```

---

### `version` (string)
**用途**: 语义化版本号

**规则**: `major.minor.patch`
- `major`: 破坏性变更
- `minor`: 向后兼容功能
- `patch`: 向后兼容修复

**示例**:
```yaml
version: 1.0.0
version: 2.1.3
version: 0.9.0-beta
```

---

### `author` (string)
**用途**: 技能作者

**示例**:
```yaml
author: 太一
author: 素问
author: 罔两
```

---

### `created` / `updated` (date)
**用途**: 创建/更新日期

**格式**: `YYYY-MM-DD`

**示例**:
```yaml
created: 2026-04-03
updated: 2026-04-04
```

---

### `status` (enum)
**用途**: 技能成熟度

**选项**:
| 状态 | 含义 | 使用建议 |
|------|------|---------|
| `stable` | 稳定版 | 生产环境可用 |
| `beta` | 测试版 | 功能完整，待验证 |
| `experimental` | 实验版 | 可能变更，谨慎使用 |
| `deprecated` | 已弃用 | 迁移到新技能 |

**示例**:
```yaml
status: stable
status: beta
status: experimental
```

---

### `triggers` (array)
**用途**: 触发关键词列表

**规则**:
- 5-15 个关键词
- 包含中英文
- 覆盖常见表述

**示例**:
```yaml
triggers:
  - 浏览器
  - 网页自动化
  - Playwright
  - browser
  - web automation
  - 截图
  - 抓取
```

---

### `permissions` (array)
**用途**: 所需权限列表

**选项**:
| 权限 | 用途 | 风险等级 |
|------|------|---------|
| `exec` | 执行 shell 命令 | 🔴 高 |
| `web_fetch` | 抓取网页 | 🟢 低 |
| `canvas` | 浏览器自动化 | 🟡 中 |
| `message` | 发送消息 | 🟡 中 |
| `file_read` | 读取文件 | 🟢 低 |
| `file_write` | 写入文件 | 🟡 中 |
| `file_delete` | 删除文件 | 🔴 高 |
| `web_search` | 网络搜索 | 🟢 低 |
| `image_generate` | 生成图片 | 🟢 低 |

**示例**:
```yaml
permissions:
  - exec
  - web_fetch
  - canvas
```

---

### `max_context_tokens` (integer)
**用途**: 技能最大上下文占用

**规则**:
- 建议值：2000-10000
- 大型技能：≤20000
- 超过需拆分

**示例**:
```yaml
max_context_tokens: 5000
max_context_tokens: 10000
```

---

### `priority` (integer)
**用途**: 技能优先级

**选项**:
| 优先级 | 含义 | 卸载策略 |
|--------|------|---------|
| `1` | 高 | 最后卸载 |
| `2` | 中 | 正常卸载 |
| `3` | 低 | 优先卸载 |

**示例**:
```yaml
priority: 1  # 核心技能
priority: 2  # 普通技能
priority: 3  # 辅助技能
```

---

### `description` (string)
**用途**: 一行描述

**规则**: ≤100 字符

**示例**:
```yaml
description: Playwright 浏览器自动化技能
description: 知几-E 量化交易策略引擎
description: GMGN 链上交易执行技能
```

---

## 🏷️ 可选字段

### `tags` (array)
**用途**: 分类标签

**示例**:
```yaml
tags:
  - automation
  - browser
  - playwright
```

---

### `dependencies` (array)
**用途**: 依赖技能列表

**示例**:
```yaml
dependencies:
  - browser-automation
  - zhiji-e-data
```

---

### `config` (object)
**用途**: 默认配置参数

**示例**:
```yaml
config:
  browser: chromium
  headless: true
  timeout: 30000
  proxy: null
```

---

## 📝 完整示例

### 示例 1: 浏览器自动化
```yaml
---
skill: browser-automation
version: 1.0.0
author: 素问
created: 2026-04-03
updated: 2026-04-04
status: stable
triggers:
  - 浏览器
  - 网页自动化
  - Playwright
  - browser
  - web automation
  - 截图
permissions:
  - exec
  - web_fetch
  - canvas
max_context_tokens: 5000
priority: 2
description: Playwright 浏览器自动化技能
tags:
  - automation
  - browser
config:
  browser: chromium
  headless: true
  timeout: 30000
---

# 技能正文...
```

### 示例 2: 知几-E 策略
```yaml
---
skill: zhiji-e-strategy
version: 3.0.0
author: 知几
created: 2026-03-20
updated: 2026-04-01
status: stable
triggers:
  - 知几
  - 交易策略
  - Polymarket
  - 气象套利
  - quant trading
  - strategy
permissions:
  - exec
  - file_read
  - file_write
  - web_fetch
max_context_tokens: 8000
priority: 1
description: 知几-E 量化交易策略引擎
tags:
  - trading
  - quant
  - polymarket
dependencies:
  - zhiji-e-data
config:
  confidence_threshold: 0.96
  edge_threshold: 0.02
  position_sizing: quarter_kelly
---

# 技能正文...
```

### 示例 3: GMGN 交易
```yaml
---
skill: gmgn-swap
version: 1.0.0
author: 太一
created: 2026-03-27
updated: 2026-03-30
status: stable
triggers:
  - GMGN
  - 交易
  - swap
  - 币安
  - Solana
  - Base
permissions:
  - exec
  - message
max_context_tokens: 3000
priority: 1
description: GMGN 链上交易执行技能 [FINANCIAL EXECUTION]
tags:
  - trading
  - crypto
  - solana
  - base
config:
  default_chain: sol
  slippage: 1.0
  require_confirmation: true
---

# 技能正文...
```

---

## 🔧 验证脚本

```python
#!/usr/bin/env python3
# scripts/validate-skill-metadata.py

import yaml
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "skill", "version", "author", "created",
    "status", "triggers", "permissions",
    "max_context_tokens", "priority", "description"
]

VALID_STATUS = ["stable", "beta", "experimental", "deprecated"]
VALID_PERMISSIONS = [
    "exec", "web_fetch", "canvas", "message",
    "file_read", "file_write", "file_delete",
    "web_search", "image_generate"
]

def validate_skill(skill_path):
    """验证技能元数据"""
    content = Path(skill_path).read_text()
    
    if not content.startswith("---"):
        return False, "缺少 YAML Frontmatter"
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "YAML Frontmatter 格式错误"
    
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return False, f"YAML 解析错误：{e}"
    
    # 检查必填字段
    for field in REQUIRED_FIELDS:
        if field not in meta:
            return False, f"缺少必填字段：{field}"
    
    # 验证 status
    if meta["status"] not in VALID_STATUS:
        return False, f"无效 status: {meta['status']}"
    
    # 验证 permissions
    for perm in meta["permissions"]:
        if perm not in VALID_PERMISSIONS:
            return False, f"无效权限：{perm}"
    
    # 验证 priority
    if meta["priority"] not in [1, 2, 3]:
        return False, f"无效 priority: {meta['priority']}"
    
    # 验证 triggers 数量
    if len(meta["triggers"]) < 5:
        return False, f"triggers 过少 ({len(meta['triggers'])} < 5)"
    
    return True, "验证通过"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-skill-metadata.py <skill.md>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    valid, message = validate_skill(skill_path)
    
    if valid:
        print(f"✅ {skill_path}: {message}")
        sys.exit(0)
    else:
        print(f"❌ {skill_path}: {message}")
        sys.exit(1)
```

---

## 📊 技能索引自动生成

```python
#!/usr/bin/env python3
# scripts/generate-skill-index.py

import yaml
import json
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path(__file__).parent.parent / "skills"
OUTPUT_FILE = SKILLS_DIR / "index.json"

def parse_skill_meta(skill_path):
    """解析技能元数据"""
    content = skill_path.read_text()
    if not content.startswith("---"):
        return None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    return yaml.safe_load(parts[1])

def generate_index():
    """生成技能索引"""
    skills = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        meta = parse_skill_meta(skill_md)
        if meta:
            skills.append({
                "name": meta.get("skill", skill_dir.name),
                "version": meta.get("version", "0.0.0"),
                "author": meta.get("author", "unknown"),
                "status": meta.get("status", "unknown"),
                "triggers": meta.get("triggers", []),
                "permissions": meta.get("permissions", []),
                "priority": meta.get("priority", 2),
                "description": meta.get("description", ""),
                "path": str(skill_md.relative_to(SKILLS_DIR.parent)),
                "loaded": False,
                "last_used": None,
                "use_count": 0
            })
    
    index = {
        "skills": skills,
        "count": len(skills),
        "updated": datetime.now().isoformat()
    }
    
    OUTPUT_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"✅ 生成技能索引：{len(skills)} 个技能")
    return index

if __name__ == "__main__":
    generate_index()
```

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `constitution/skills/SKILL-METADATA.md` | 本文件 |
| `constitution/skills/SKILL-LIFECYCLE.md` | 生命周期管理 |
| `constitution/skills/PERMISSION-SCOPING.md` | 权限授予协议 |
| `scripts/validate-skill-metadata.py` | 验证脚本 |
| `scripts/generate-skill-index.py` | 索引生成 |

---

*创建时间：2026-04-04 | 太一 AGI · 能力涌现*
