# 📚 太一智慧库

> **创建时间**: 2026-04-12 23:58  
> **内容**: 道家智慧 + 佛家智慧  
> **推送时间**: 每日早晨 8:00

---

## 🌅 每日道家智慧

**来源**: Dao.Agent  
**经典**: 道德经、庄子、列子  
**推送时间**: 每日 08:00

**今日智慧**:
```
查看：dao_wisdom_today.md
```

**历史记录**:
```
查看：dao_wisdom_history.json
```

---

## 🌸 每日佛家智慧

**来源**: 悟.Agent (Satori Agent)  
**经典**: 心经、金刚经、六祖坛经等 10 部  
**推送时间**: 每日 08:00

**今日智慧**:
```
查看：buddhist_wisdom_today.md
```

**历史记录**:
```
查看：buddhist_wisdom_history.json
```

---

## 📅 推送配置

**Crontab 配置**:
```bash
# 每日 08:00 - 道家 + 佛家智慧推送
0 8 * * * /home/nicola/.openclaw/workspace/scripts/daily-wisdom-push.sh
```

**手动执行**:
```bash
# 道家智慧
python3 /home/nicola/.openclaw/workspace/skills/dao-agent/daily_dao_wisdom.py

# 佛家智慧
python3 /home/nicola/.openclaw/workspace/skills/wu-enlightenment/daily_buddhist_wisdom.py

# 两者都推送
bash /home/nicola/.openclaw/workspace/scripts/daily-wisdom-push.sh
```

---

## 📊 智慧统计

**道家智慧**:
- 经典：3 部 (道德经、庄子、列子)
- 句子：20+ 句
- 推送：每日 1 句

**佛家智慧**:
- 经典：6 部 (心经、金刚经、六祖坛经等)
- 句子：20+ 句
- 推送：每日 1 句

---

## 🔗 相关链接

**Dao.Agent**:
```
https://github.com/nicola-king/dao.agent
```

**悟.Agent (Satori Agent)**:
```
https://github.com/nicola-king/satori-agent
```

---

**📚 太一智慧库 - 每日启迪心灵！**

**太一 AGI · 2026-04-12**
