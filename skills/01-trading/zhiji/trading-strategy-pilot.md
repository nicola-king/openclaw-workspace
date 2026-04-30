# P7 · 交易策略试点方案

**版本**: v0.1  
**创建**: 2026-03-25 16:51  
**执行**: 知几 + 素问  
**优先级**: P7

---

## 🎯 目标

试点 Self-Improving 机制，让知几-E 通过 diff 对比学习 SAYELF 的交易决策模式。

---

## 📋 试点流程

### Step 1: 知几生成交易信号

```python
知几-E 分析气象数据 + 市场赔率
    ↓
生成交易信号（置信度/下注金额/方向）
    ↓
发送给 SAYELF（微信/Telegram）
    ↓
等待确认或调整
```

### Step 2: SAYELF 调整决策

```
SAYELF 收到交易信号
    ↓
评估风险/调整参数
    ↓
确认执行或修改（如：置信度 96%→98%，下注¥5→¥10）
    ↓
系统自动保存两版
```

### Step 3: diff 对比学习

```
diff-learner.py 对比两版信号
    ↓
提取调整模式（决策规则）
    ↓
宪法审查（风控检查）
    ↓
写入知几策略文件
    ↓
下次生成改进信号
```

---

## 🔧 技术实现

### 组件 1: 信号版本追踪器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/zhiji/signal-tracker.py

import json
from pathlib import Path
from datetime import datetime

class SignalTracker:
    """交易信号版本追踪器"""
    
    def __init__(self):
        self.history_dir = Path.home() / ".taiyi" / "output-history" / "zhiji"
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def save_signal_pair(self, session_id, original_signal, modified_signal):
        """保存原始和修改后的交易信号"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存原始信号
        original_path = self.history_dir / f"{timestamp}_original.json"
        with open(original_path, "w", encoding="utf-8") as f:
            json.dump({
                "type": "original",
                "session": session_id,
                "timestamp": datetime.now().isoformat(),
                "signal": original_signal
            }, f, indent=2, ensure_ascii=False)
        
        # 保存修改信号
        modified_path = self.history_dir / f"{timestamp}_modified.json"
        with open(modified_path, "w", encoding="utf-8") as f:
            json.dump({
                "type": "modified",
                "original": original_path.name,
                "session": session_id,
                "timestamp": datetime.now().isoformat(),
                "signal": modified_signal
            }, f, indent=2, ensure_ascii=False)
        
        return original_path, modified_path
    
    def get_signal_pairs(self, limit=10):
        """获取成对的信号记录"""
        pairs = []
        originals = sorted(self.history_dir.glob("*_original.json"))
        
        for original in originals[-limit:]:
            modified = original.with_name(original.stem.replace("_original", "_modified") + ".json")
            if modified.exists():
                with open(original, "r") as f:
                    orig_data = json.load(f)
                with open(modified, "r") as f:
                    mod_data = json.load(f)
                
                pairs.append({
                    "original": orig_data["signal"],
                    "modified": mod_data["signal"],
                    "timestamp": orig_data["timestamp"]
                })
        
        return pairs
```

### 组件 2: 交易规则提取器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/zhiji/trading-rule-extractor.py

import json
from pathlib import Path

class TradingRuleExtractor:
    """交易规则提取器"""
    
    def __init__(self):
        self.rules_file = Path.home() / ".taiyi" / "zhiji-trading-rules.json"
        self.rules = self._load_rules()
    
    def _load_rules(self):
        """加载现有规则"""
        if self.rules_file.exists():
            with open(self.rules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def extract_from_adjustment(self, original, modified):
        """从参数调整中提取交易规则"""
        rules = []
        
        # 置信度调整
        if "confidence" in original and "confidence" in modified:
            diff = modified["confidence"] - original["confidence"]
            if abs(diff) >= 0.02:  # 2% 以上调整
                rules.append({
                    "type": "confidence_adjustment",
                    "pattern": f"置信度调整 {diff*100:+.1f}%",
                    "original": original["confidence"],
                    "modified": modified["confidence"],
                    "description": self._describe_confidence_adjustment(diff)
                })
        
        # 下注金额调整
        if "stake" in original and "stake" in modified:
            diff = modified["stake"] - original["stake"]
            if abs(diff) >= 5:  # ¥5 以上调整
                rules.append({
                    "type": "stake_adjustment",
                    "pattern": f"下注金额调整 ¥{diff:+.0f}",
                    "original": original["stake"],
                    "modified": modified["stake"],
                    "description": self._describe_stake_adjustment(diff)
                })
        
        # 方向调整
        if "direction" in original and "direction" in modified:
            if original["direction"] != modified["direction"]:
                rules.append({
                    "type": "direction_reversal",
                    "pattern": f"方向反转：{original['direction']} → {modified['direction']}",
                    "description": "完全反转交易方向（高风险信号）"
                })
        
        return rules
    
    def _describe_confidence_adjustment(self, diff):
        """描述置信度调整原因"""
        if diff > 0:
            return "SAYELF 认为信号更强，提高置信度"
        else:
            return "SAYELF 认为信号较弱，降低置信度"
    
    def _describe_stake_adjustment(self, diff):
        """描述下注金额调整原因"""
        if diff > 0:
            return "SAYELF 增加下注金额（风险承受能力强）"
        else:
            return "SAYELF 减少下注金额（风险控制）"
```

---

## 📊 试点计划

### 第 1 周：数据收集

**目标**: 收集 10+ 组交易信号调整

| 信号类型 | 数量 | 状态 |
|---------|------|------|
| 气象套利信号 | 5 个 | 🟡 待收集 |
| 鲸鱼跟随信号 | 3 个 | 🟡 待收集 |
| 其他交易信号 | 2 个 | 🟡 待收集 |

### 第 2 周：规则提取

**目标**: 提取 10+ 条交易决策规则

| 规则类型 | 预期数量 | 说明 |
|---------|---------|------|
| 置信度调整 | 5 条 | 学习风险判断 |
| 下注金额调整 | 3 条 | 学习仓位管理 |
| 方向反转 | 2 条 | 学习反向思维 |

### 第 3 周：策略更新

**目标**: 更新知几-E 策略文件

- [ ] 写入规则到策略配置
- [ ] 测试改进效果
- [ ] 实盘验证（如授权）

### 第 4 周：迭代优化

**目标**: 持续改进策略

- [ ] 分析规则准确率
- [ ] 回测验证效果
- [ ] 优化策略参数

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-050` | 信号版本追踪器 | ✅ 完成 | 16:51 |
| `TASK-20260325-051` | 交易规则提取器 | ✅ 完成 | 16:51 |
| `TASK-20260325-052` | 数据收集（10+ 组） | 🟡 待执行 | - |
| `TASK-20260325-053` | 规则提取（10+ 条） | 🟡 待执行 | - |
| `TASK-20260325-054` | 策略文件更新 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:51 | 执行：知几 + 素问*
