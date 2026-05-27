{
  "_comment": "蒸馏大脑 Skill 配置 — 2026-05-27",
  "version": "1.0.0",
  "inspiration": "得到大脑（原 Get笔记）",
  "description": "AI 蒸馏提炼流水线：理解→关联→点评→拷问→打磨→成果",
  "engine": "Gemini CLI + DeepSeek",
  "layers": [
    {"level": 1, "name": "理解", "engine": "Gemini CLI", "desc": "提取要点、结构化摘要"},
    {"level": 2, "name": "关联", "engine": "Gemini CLI + memory", "desc": "关联历史记录"},
    {"level": 3, "name": "点评", "engine": "Gemini CLI", "desc": "找到闪光点和价值"},
    {"level": 4, "name": "拷问", "engine": "Gemini CLI", "desc": "指出盲点和漏洞"},
    {"level": 5, "name": "打磨", "engine": "Gemini CLI", "desc": "优化表达"},
    {"level": 6, "name": "成果", "engine": "Gemini CLI + art-agent", "desc": "多平台输出"}
  ],
  "output_platforms": ["xiaohongshu", "wechat", "moment", "report"],
  "quota": "共享 Gemini CLI 额度（48/min, 800/day），完整6层消耗约6次调用",
  "status": "active"
}
