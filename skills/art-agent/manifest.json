{
  "name": "art-agent",
  "version": "2.1.0",
  "description": "太一美学引擎 v2.0 - 模块化、自进化的艺术 Agent 集群",
  "author": "太一 AGI",
  "license": "MIT",
  "updated": "2026-04-26",
  "modules": {
    "aesthetic-filter": {
      "version": "2.0.0",
      "path": "modules/aesthetic-filter",
      "dependencies": [],
      "description": "美学过滤器：为太一系统所有输出提供艺术处理，保证高品质交付"
    },
    "aesthetic-scorer": {
      "version": "1.0.0",
      "path": "modules/aesthetic-scorer",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "美学评分引擎：多维度质量评估 (可读性/一致性/美学/功能性/结构性/语义性)"
    },
    "aesthetics-engine": {
      "version": "1.0.0",
      "path": "modules/aesthetics-engine",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "美学引擎：美学决策 + 风格系统 + 自进化"
    },
    "output-enhancer": {
      "version": "1.0.0",
      "path": "core/output_enhancer",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "输出增强器：安全的美化处理器，只处理明确传入的文件路径"
    },
    "taiyi-artisan": {
      "version": "1.0.0",
      "path": "modules/taiyi-artisan",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "太一艺境：艺术创作引擎，风格应用与艺术创作"
    },
    "taiyi-design": {
      "version": "1.0.0",
      "path": "modules/taiyi-design",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "太一设计系统：设计规范与组件库"
    },
    "brand-guardian": {
      "version": "1.0.0",
      "path": "modules/brand-guardian",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "品牌守护者：品牌一致性检查与风格统一"
    },
    "ui-designer": {
      "version": "1.0.0",
      "path": "modules/ui-designer",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "UI 设计器：界面生成与布局优化"
    },
    "ux-writer": {
      "version": "1.0.0",
      "path": "modules/ux-writer",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "UX 写作助手：文案生成与优化"
    },
    "visual-api": {
      "version": "1.0.0",
      "path": "modules/visual-api",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "视觉 API：图像生成、编辑、分析"
    },
    "visual-narrative": {
      "version": "1.0.0",
      "path": "modules/visual-narrative",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "视觉叙事：数据故事化，将数据转化为有故事性的视觉呈现"
    },
    "chart-generator": {
      "version": "1.0.0",
      "path": "modules/chart-generator",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "图表生成：文字转图表/流程图/信息图"
    },
    "card-generator": {
      "version": "1.0.0",
      "path": "modules/card-generator",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "卡片生成：信息卡片/知识卡片/报告卡片"
    },
    "3d-generator": {
      "version": "1.0.0",
      "path": "modules/3d-generator",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "3D 生成：文字转 3D 模型"
    },
    "visual-workflow": {
      "version": "1.0.0",
      "path": "modules/visual-workflow",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "可视化工作流：自动视觉工作流编排"
    },
    "design-system": {
      "version": "1.0.0",
      "path": "modules/design-system",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "设计系统：设计 Token/UI 组件/样式规范"
    },
    "design-agent": {
      "version": "1.0.0",
      "path": "modules/design-agent",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "设计 Agent：侘寂美学研究 (从 05-content 迁移)"
    },
    "content-creator": {
      "version": "1.0.0",
      "path": "modules/content-creator",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "内容创作器：内容生成与优化 (从 05-content 迁移)"
    },
    "self-evolution": {
      "version": "1.0.0",
      "path": "modules/self-evolution",
      "dependencies": [
        "aesthetic-filter"
      ],
      "description": "自进化系统：宪法学习循环 + Elon 五步算法 + 进化指标追踪"
    }
  },
  "shared": {
    "api": "shared/api",
    "utils": "shared/utils"
  },
  "core": {
    "output-enhancer": "core/output_enhancer.py"
  },
  "install": {
    "script": "deploy/install.sh",
    "update": "deploy/update.sh"
  },
  "principles": {
    "modular": "每个模块可独立作为 skill 或 agent 发布",
    "safe": "美化只处理明确指定的文件，绝不自动扫描 workspace",
    "self-evolving": "所有模块支持自进化 (记录版本和改进历史)"
  }
}