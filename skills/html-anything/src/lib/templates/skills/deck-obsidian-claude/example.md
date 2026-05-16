01 / 08

● OBSIDIAN × CLAUDE · 第二大脑

# 把 Obsidian 和 Claude 拧成 一条神经

不是又一个 AI 笔记插件 —— 是让 Claude 真正理解你 vault 的结构、链接、双向引用，
然后在你想写东西之前就把资料准备好。

🧠 Markdown-native
⚡ MCP-ready
🔗 双链理解

02 / 08

● CHAPTER 01

# Why not Notion?

当你的知识多到会互相引用时，
「文件夹」就不够了，「数据库」也不是答案。

03 / 08

● COMPARE

## Notion vs Obsidian · 对 AI 友好度

NOTION

#### 数据库原生

适合结构化任务、团队协作，但是——
• AI 要走 API，拿不到实时全文
• 嵌套块结构复杂，token 成本高
• 本地化差，没法当长期记忆

OBSIDIAN

#### 纯 Markdown + 双链

对 AI 天生友好 ——
• 所有东西就是文件，Claude 直接读
• 双链 = 天然 graph，抽实体几乎零成本
• 离线、可 git、可 diff、可回滚

💡 **关键洞察：**AI 不需要「更聪明的数据库」，它需要「能被它自己读懂的文件系统」。

04 / 08

● SETUP · 4 STEPS

## 从 0 到第一次「AI 写笔记」

1

#### 装 Obsidian + 开 Local REST API 插件

社区插件，一个勾就开。它让外部进程能 read/write 你的 vault。

2

#### 接 Claude Desktop + obsidian-mcp server

MCP 一个配置文件就能接，token 填 vault 的 api key。

3

#### 装 5 个 obsidian-skills

markdown / bases / canvas / cli / defuddle —— 让 Claude 知道怎么正确使用 Obsidian。

4

#### 让 Claude 自己整理一次

「帮我把最近 10 篇笔记里的重复概念合并，生成一张新的 MOC」—— 90 秒出结果。

05 / 08

● MCP CONFIG

## claude\_desktop\_config.json

```
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "xxxxxxxxxxxxxxxx",
        "OBSIDIAN_HOST": "http://127.0.0.1:27123"
      }
    }
  }
}
```

重启 Claude Desktop，输入 **/mcp**，你会看到 obsidian 已连。

06 / 08

● 3 MONTHS IN

## 跑了 90 天，我的 vault 数据

1,842

notes in vault

6.3k

backlinks (由 AI 自动补)

-74%

找资料平均耗时

最大收益不是「AI 帮我写」，而是「AI 帮我把旧笔记重新连起来」—— 每周 30 分钟，vault 就会主动生长。

07 / 08

● CTA · 今晚可以做

> 不要再找「AI 笔记应用」了。
> 你要的是一个 文件夹 + 一条神经。

— 我自己，用了 90 天后

⬇ obsidian.md
⬇ Claude Desktop
⬇ obsidian-mcp
⬇ obsidian-skills × 5

08 / 08

Thanks.

配置模板、skill manifest、我的 vault 结构图都在 **github.com/lewis/obsidian-claude**