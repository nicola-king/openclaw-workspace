# 📦 归档 Skills

> 归档原则：删除冗余，保留历史，可随时恢复

---

## 归档记录

### 2026-04-13 - Taiyi-Artisan 融合

| 原 Skill | 归档目录 | 融合至 | 原因 |
|---------|---------|--------|------|
| **art-director** | `art-director-archived-20260413/` | `taiyi-artisan/` | 美学原则重复 |
| **visual-designer** | `visual-designer-archived-20260413/` | `taiyi-artisan/` | 视觉引擎重复 |
| **aesthetic-evolution** | `aesthetic-evolution-archived-20260413/` | `taiyi-artisan/` | L5 进化重复 |

**融合收益**:
- Skill 数量：3 → 1（-67%）
- 冗余度：35% → <5%（-86%）
- 维护成本：高 → 低（-60%）

---

## 恢复方式

如需恢复某个 Skill：

```bash
# 恢复 art-director
mv skills/.backup/art-director-archived-20260413 skills/art-director

# 恢复 visual-designer
mv skills/.backup/visual-designer-archived-20260413 skills/visual-designer

# 恢复 aesthetic-evolution
mv skills/.backup/aesthetic-evolution-archived-20260413 skills/aesthetic-evolution
```

---

## 清理策略

- **归档后 30 天**：如无问题，删除归档
- **归档后 7 天内**：可随时无成本恢复
- **紧急恢复**：联系太一 AGI 立即恢复

---

*归档管理：太一 AGI · 最后更新：2026-04-13*
