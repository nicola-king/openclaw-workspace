# Learning Agent - 强化学习智能体

> **版本**: 1.0.0  
> **创建时间**: 2026-04-15 00:35  
> **职责**: 从历史数据学习，优化调度策略  
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 强化学习优化调度策略

**学习方法**:
- Q-learning 强化学习
- 经验回放 (Experience Replay)
- 策略梯度优化
- 超参数自动调整

---

## 🧠 学习能力

### 1. Q-learning 核心

```python
# Q 值更新公式
Q(s,a) ← Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]

参数:
- α (学习率): 0.1
- γ (折扣因子): 0.9
- ε (探索率): 0.1→0.01 (衰减)
```

### 2. 状态空间

```python
state = (
    目标进度，      # 0.0-2.0
    时间戳，        # 0-23 小时
    资源使用率，    # 0.0-1.0
    连续成功，      # 0-10
    执行频率，      # 1-12 次/天
)
```

### 3. 动作空间

```python
action = (
    执行频率，      # 30min/1h/2h/4h
    并发数，        # 1/2/3
    资源分配，      # 256MB/512MB/1GB
)
```

### 4. 奖励函数

```python
reward = (
    目标达成率 * 0.5 +    # 50%
    执行成功率 * 0.3 +    # 30%
    资源效率 * 0.2        # 20%
)
```

---

## 📋 专业能力

### 1. 强化学习

- ✅ Q-learning 核心
- ✅ 经验回放
- ✅ ε-greedy 策略
- ✅ Q-table 持久化

### 2. 策略优化

- ✅ 历史数据分析
- ✅ 最优策略提取
- ✅ 策略效果评估
- ✅ 自动策略更新

### 3. 模型管理

- ✅ Q-table 保存/加载
- ✅ 训练进度追踪
- ✅ 模型版本管理
- ✅ 性能指标监控

---

## 🔧 配置说明

配置文件位于 `config/learning-config.json`:

```json
{
  "learning_rate": 0.1,
  "discount_factor": 0.9,
  "exploration_rate": 0.1,
  "exploration_decay": 0.995,
  "min_exploration": 0.01,
  "replay_buffer_size": 1000,
  "batch_size": 32,
  "training_frequency": 100
}
```

---

## 🚀 使用说明

### 训练模型

```bash
# 开始训练
python3 skills/learning-agent/src/learner.py --train

# 查看训练进度
python3 skills/learning-agent/src/learner.py --status
```

### 使用模型

```bash
# 获取最优动作
python3 skills/learning-agent/src/learner.py --get-action --state <state>

# 评估策略
python3 skills/learning-agent/src/learner.py --evaluate
```

---

## 📊 学习进度

### 训练目标

| 指标 | 目标 | 当前 |
|------|------|------|
| 训练轮次 | 1000 | 0 |
| 平均奖励 | >0.8 | 0.0 |
| 收敛轮次 | <500 | - |
| 策略稳定性 | >95% | - |

### 预期效果

```
训练后:
✅ 目标达成率提升 30%+
✅ 执行效率提升 50%+
✅ 资源浪费减少 40%+
✅ 人工干预减少 90%+
```

---

## 🧪 测试

```bash
# 运行测试
pytest skills/learning-agent/tests/

# 测试 Q-learning
python3 skills/learning-agent/tests/test_qlearning.py
```

---

## 📝 变更日志

### v1.0.0 (2026-04-15)

- ✅ 初始版本
- ✅ Q-learning 核心
- ✅ 经验回放
- ✅ 策略优化
- ✅ 模型管理

---

*太一 AGI · Learning Agent · 2026-04-15*
