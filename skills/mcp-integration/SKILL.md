# 太一 MCP 集成 (Taiyi MCP Integration)

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **类别**: 集成/协议/扩展
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: Model Context Protocol (MCP) 集成，实现太一系统与外部 AI 工具的标准化通信

**适用场景**:
- 与 Claude Desktop 集成
- 与 Cursor IDE 集成
- 与各类 MCP 客户端通信
- 标准化工具调用接口
- 上下文共享与同步

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    太一系统 (Taiyi System)                │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 跨境贸易 │  │ 旅游探路 │  │ OSINT   │  │ TTS     │   │
│  │ Agent   │  │ Agent   │  │ Agent   │  │ Agent   │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │         │
│       └────────────┴────────────┴────────────┘         │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              MCP 集成层 (MCP Integration)          │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 工具注册  │  │ 上下文   │  │ 资源管理  │      │   │
│  │  │ Tools    │  │ Context  │  │ Resources│      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 提示模板  │  │ 采样控制  │  │ 协议转换  │      │   │
│  │  │ Prompts  │  │ Sampling │  │ Adapter  │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              MCP 客户端 (MCP Clients)              │   │
│  │                                                  │   │
│  │  Claude Desktop │ Cursor │ VS Code │ 其他客户端 │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 核心组件

### 1. 工具注册 (Tools)

**功能**: 注册太一系统能力为 MCP 工具

**支持工具**:
| 工具 | 说明 | 对应Agent |
|------|------|---------|
| `search` | 全网搜索 | 共享搜索服务 |
| `cross_border_trade` | 跨境贸易分析 | 跨境贸易Agent |
| `travel_plan` | 旅游规划 | 旅游探路者 |
| `osint_scan` | 数字足迹扫描 | Maigret |
| `tts_synthesize` | 语音合成 | MOSS-TTS |
| `geo_audit` | GEO审计 | GEO模块 |
| `system_status` | 系统状态 | 太一 |

### 2. 上下文管理 (Context)

**功能**: 管理 MCP 会话上下文

**支持功能**:
- 会话状态保持
- 历史记录管理
- 上下文压缩
- 多轮对话支持

### 3. 资源管理 (Resources)

**功能**: 暴露系统内部资源

**支持资源**:
| 资源 | URI | 说明 |
|------|-----|------|
| 系统状态 | `taiyi://status` | 实时系统状态 |
| Agent列表 | `taiyi://agents` | 可用Agent列表 |
| 技能目录 | `taiyi://skills` | 技能清单 |
| 宪法文件 | `taiyi://constitution` | 太一宪法 |
| 记忆文件 | `taiyi://memory` | 系统记忆 |

---

## 🚀 使用方式

### 1. 配置 MCP Server

```json
// mcp-config.json
{
  "mcpServers": {
    "taiyi": {
      "command": "python3",
      "args": [
        "/home/sayelf/.openclaw/workspace/skills/mcp-integration/mcp_server.py"
      ],
      "env": {
        "TAIYI_WORKSPACE": "/home/sayelf/.openclaw/workspace"
      }
    }
  }
}
```

### 2. 在 Claude Desktop 中使用

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "taiyi": {
      "command": "python3",
      "args": [
        "/home/sayelf/.openclaw/workspace/skills/mcp-integration/mcp_server.py"
      ]
    }
  }
}
```

### 3. 工具调用示例

```python
# MCP 客户端调用示例
async def use_taiyi_tools():
    # 调用搜索工具
    result = await client.call_tool(
        "search",
        {"query": "smart water bottle", "agent_type": "cross_border_trade"}
    )
    
    # 调用跨境贸易分析
    result = await client.call_tool(
        "cross_border_trade",
        {"product": "智能水杯", "country": "US"}
    )
    
    # 获取系统状态
    result = await client.read_resource("taiyi://status")
```

---

## 📡 系统内部信息集成

### 信息来源

太一 MCP 集成采用系统内部信息:

```
系统内部信息
├── Agent能力
│   ├── 跨境贸易 - 选品/物流/市场分析
│   ├── 旅游探路 - 行程规划/票价查找
│   ├── OSINT - 用户名扫描/数字足迹
│   └── TTS - 语音合成/克隆
├── 系统状态
│   ├── CPU/内存/磁盘
│   ├── Agent运行状态
│   └── 任务队列
├── 知识库
│   ├── 宪法文件
│   ├── 技能文档
│   └── 历史记忆
└── 配置信息
    ├── 环境变量
    ├── 配置文件
    └── 用户偏好
```

---

## 🔒 安全与权限

### 访问控制

| 级别 | 权限 | 说明 |
|------|------|------|
| 公开 | 只读 | 系统状态、技能列表 |
| 标准 | 调用 | 搜索、旅游规划 |
| 高级 | 管理 | 跨境贸易、OSINT |
| 管理员 | 全部 | 系统配置、代码执行 |

### 认证方式

```python
# Token 认证
headers = {"Authorization": "Bearer taiyi_xxxxxxxx"}

# 或环境变量
os.environ["TAIYI_MCP_TOKEN"] = "taiyi_xxxxxxxx"
```

---

## 📁 文件结构

```
skills/mcp-integration/
├── SKILL.md                          # 技能说明
├── mcp_server.py                     # MCP Server实现
├── tools/                            # 工具实现
│   ├── __init__.py
│   ├── search_tool.py                # 搜索工具
│   ├── trade_tool.py                 # 跨境贸易工具
│   ├── travel_tool.py                # 旅游工具
│   ├── osint_tool.py                 # OSINT工具
│   └── system_tool.py                # 系统工具
├── resources/                        # 资源实现
│   ├── __init__.py
│   ├── status_resource.py            # 状态资源
│   ├── agent_resource.py             # Agent资源
│   └── memory_resource.py            # 记忆资源
├── prompts/                          # 提示模板
│   └── system_prompts.yaml           # 系统提示
├── config.yaml                       # 配置文件
└── test_client.py                    # 测试客户端
```

---

## 🔄 与现有系统集成

### 已集成
- ✅ 共享搜索服务 - `search` 工具
- ✅ 跨境贸易Agent - `cross_border_trade` 工具
- ✅ 旅游探路者 - `travel_plan` 工具
- ✅ Maigret - `osint_scan` 工具
- ✅ MOSS-TTS - `tts_synthesize` 工具
- ✅ 系统监控 - `system_status` 工具

### 待集成
- 🟡 飞书集成 - 消息推送工具
- 🟡 GitHub集成 - 代码管理工具
- 🟡 反爬工具包 - 爬虫工具

---

## 🎯 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 多模态支持 | P1 | 图片/音频处理 |
| 流式响应 | P1 | SSE 实时推送 |
| 分布式部署 | P2 | 多实例负载均衡 |
| 插件系统 | P2 | 第三方工具接入 |
| 审计日志 | P2 | 操作记录追踪 |

---

*太一 AGI · MCP 集成技能 v1.0*
*创建时间: 2026-05-04*
*核心能力: 标准化协议 · 工具暴露 · 上下文共享*
