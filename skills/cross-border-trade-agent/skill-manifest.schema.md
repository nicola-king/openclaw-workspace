{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "太一 Skill 注册元数据标准",
  "description": "所有 Agent 能力标准化注册格式，驱动 Skill Registry 动态发现和路由",
  "type": "object",
  "required": ["id", "name", "version", "description", "owner", "triggers", "input_schema", "output_schema"],
  "properties": {
    "id": {
      "type": "string",
      "description": "唯一标识符，格式: {module}.{action}",
      "pattern": "^[a-z][a-z0-9-]+\\.[a-z][a-z0-9-]+$",
      "examples": ["guike-zhilu.outreach", "intelligence-hub.market-analysis"]
    },
    "name": {
      "type": "string",
      "description": "中文名称",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "description": "语义化版本号",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "description": {
      "type": "string",
      "description": "功能描述（一句话）"
    },
    "owner": {
      "type": "string",
      "description": "所属 Bot：知几 | 山木 | 素问 | 罔两 | 庖丁 | 太一",
      "enum": ["知几", "山木", "素问", "罔两", "庖丁", "太一"]
    },
    "triggers": {
      "type": "array",
      "description": "触发关键词，用于意图匹配",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 1
    },
    "input_schema": {
      "type": "object",
      "description": "输入参数定义，key=参数名, value=类型+说明",
      "additionalProperties": { "type": "string" }
    },
    "output_schema": {
      "type": "object",
      "description": "输出结构定义",
      "additionalProperties": { "type": "string" }
    },
    "dependencies": {
      "type": "array",
      "description": "运行依赖的模块ID列表",
      "items": { "type": "string" },
      "uniqueItems": true
    },
    "execution_mode": {
      "type": "string",
      "description": "执行模式",
      "enum": ["synchronous", "asynchronous", "streaming"]
    },
    "cost_estimate": {
      "type": "string",
      "description": "预估消耗",
      "enum": ["low", "medium", "high"]
    },
    "entry_point": {
      "type": "string",
      "description": "入口文件路径（相对 skill 根目录）",
      "examples": ["modules/intelligence-hub/core.py"]
    },
    "config_schema": {
      "type": "object",
      "description": "配置项定义",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "default": {},
          "description": { "type": "string" }
        }
      }
    }
  }
}
