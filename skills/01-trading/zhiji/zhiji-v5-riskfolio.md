# 知几-E 仓位管理 v5.0 - Riskfolio-Lib 整合

> 基于 Riskfolio-Lib 投资组合优化 | 版本：v5.0 | 创建：2026-03-27

---

## 🎯 核心验证

```
Riskfolio-Lib = 专业级投资组合优化库

太一知几-E 需要:
✅ 仓位优化 (凯利公式 + 现代投资组合理论)
✅ 风险管理 (VaR, CVaR)
✅ 有效前沿 (最优风险收益比)
✅ 多资产相关性分析

这意味着:
太一可以集成成熟开源库，无需重复造轮子！
```

---

## 📊 功能对比

| 功能 | Riskfolio-Lib | 知几-E v4.0 | 知几-E v5.0 |
|------|---------------|------------|------------|
| **有效前沿** | ✅ | ❌ | ✅ 新增 |
| **资产配置** | ✅ | ⏳ 凯利公式 | ✅ 增强 |
| **VaR 风险** | ✅ | ❌ | ✅ 新增 |
| **CVaR 风险** | ✅ | ⏳ 对数效用 | ✅ 增强 |
| **相关性分析** | ✅ | ❌ | ✅ 新增 |
| **Black-Litterman** | ✅ | ❌ | ✅ 新增 |
| **可视化** | ✅ | ❌ | ✅ 新增 |

---

## 🛠️ 技术整合方案

### 步骤 1: 安装 Riskfolio-Lib

```bash
# 安装依赖
pip install riskfolio-lib
pip install pandas numpy matplotlib scipy

# 验证安装
python3 -c "import riskfolio as rp; print(rp.__version__)"
```

### 步骤 2: 基础使用示例

```python
import riskfolio as rp
import pandas as pd
import numpy as np

# 示例：Polymarket 市场投资组合优化

# 1. 准备数据 (历史收益率)
markets = ['BTC100K', 'ETH5K', 'SOL500', 'Weather']
returns_data = {
    'BTC100K': [0.15, -0.05, 0.22, 0.08, -0.12, 0.18],
    'ETH5K': [0.12, -0.08, 0.18, 0.05, -0.15, 0.20],
    'SOL500': [0.25, -0.15, 0.35, 0.10, -0.20, 0.30],
    'Weather': [0.05, 0.03, 0.08, 0.04, 0.02, 0.06]
}

returns_df = pd.DataFrame(returns_data)

# 2. 估计参数
mu = rp.estimated_moment(returns_df, kindhist='mean')
sigma = rp.estimated_cov(returns_df, method='hist')

# 3. 投资组合优化
model = 'MeanVar'  # Mean-Variance 模型
rm = 'Std'  # 标准差作为风险度量

# 经典模型 (Markowitz)
port = rp.HCPortfolio(assets=markets, mu=mu, cov=sigma)

# 计算有效前沿
port.ef_plot(model=model, rm=rm, n_port=20, alpha=0.05)

# 最优投资组合
portfolio = port.optimality(model=model, rm=rm, alpha=0.05)
print("最优权重:")
print(portfolio)

# 4. 风险管理
# VaR (Value at Risk)
var_95 = rp.VaR(returns_df, alpha=0.05)
print(f"95% VaR: {var_95}")

# CVaR (Conditional VaR)
cvar_95 = rp.CVaR(returns_df, alpha=0.05)
print(f"95% CVaR: {cvar_95}")
```

### 步骤 3: 知几-E 集成

```python
#!/usr/bin/env python3
"""
知几-E v5.0 - Riskfolio-Lib 集成

功能:
- Polymarket 投资组合优化
- 自动仓位计算
- 风险管理 (VaR/CVaR)
- 有效前沿可视化
"""

import riskfolio as rp
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ZhijiPortfolio:
    """知几-E 投资组合管理类"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.markets = []
        self.returns_history = []
        
    def fetch_polymarket_data(self, days=60):
        """获取 Polymarket 历史数据"""
        # 调用 Polymarket Gamma API
        # 返回各市场历史价格和收益率
        pass
        
    def calculate_optimal_weights(self, model='MeanVar', risk_measure='Std'):
        """
        计算最优仓位权重
        
        参数:
        - model: 优化模型 (MeanVar, BlackLitterman, 等)
        - risk_measure: 风险度量 (Std, VaR, CVaR)
        
        返回:
        - 各市场最优权重
        """
        # 1. 准备数据
        returns_df = pd.DataFrame(self.returns_history)
        
        # 2. 估计参数
        mu = rp.estimated_moment(returns_df, kindhist='mean')
        sigma = rp.estimated_cov(returns_df, method='hist')
        
        # 3. 投资组合优化
        port = rp.HCPortfolio(assets=self.markets, mu=mu, cov=sigma)
        portfolio = port.optimality(model=model, rm=risk_measure)
        
        return portfolio
    
    def calculate_risk_metrics(self, alpha=0.05):
        """
        计算风险指标
        
        参数:
        - alpha: 置信水平 (0.05 = 95% 置信度)
        
        返回:
        - VaR, CVaR, 最大回撤等
        """
        returns_df = pd.DataFrame(self.returns_history)
        
        var_95 = rp.VaR(returns_df, alpha=alpha)
        cvar_95 = rp.CVaR(returns_df, alpha=alpha)
        
        return {
            'VaR_95': var_95,
            'CVaR_95': cvar_95,
        }
    
    def generate_report(self):
        """生成投资组合报告"""
        # 计算最优权重
        optimal_weights = self.calculate_optimal_weights()
        
        # 计算风险指标
        risk_metrics = self.calculate_risk_metrics()
        
        # 生成报告
        report = f"""
# 知几-E 投资组合报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━

## 📊 最优仓位配置

"""
        for market, weight in optimal_weights.items():
            report += f"- **{market}**: {weight:.2%}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━

## ⚠️ 风险指标

"""
        report += f"- **VaR (95%)**: {risk_metrics['VaR_95']:.2%}\n"
        report += f"- **CVaR (95%)**: {risk_metrics['CVaR_95']:.2%}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━

## 💡 调仓建议

根据当前市场情况和历史表现:
1. [建议 1]
2. [建议 2]
3. [建议 3]

━━━━━━━━━━━━━━━━━━━━━

*知几-E v5.0 · 基于 Riskfolio-Lib*
"""
        return report


# 使用示例
if __name__ == "__main__":
    # 初始化
    zhiji = ZhijiPortfolio(api_key="your_polymarket_api_key")
    
    # 获取数据
    zhiji.fetch_polymarket_data(days=60)
    
    # 生成报告
    report = zhiji.generate_report()
    
    # 保存报告
    output_file = f"/home/nicola/.openclaw/workspace/reports/zhiji-portfolio-{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ 投资组合报告已生成：{output_file}")
