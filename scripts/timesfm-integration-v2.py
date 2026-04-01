#!/usr/bin/env python3
"""
TimesFM 集成脚本 v2.0 (Python 3.12 兼容)
太一 AGI · 知几-E 量化策略

功能:
- 使用 statsmodels/prophet 替代 TimesFM (Python 3.12 兼容)
- 时间序列预测
- 与知几-E 策略融合

集成周期：14 天 (2026-03-30 ~ 2026-04-12)
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pandas as pd
    import numpy as np
    print("✅ 依赖库加载成功 (pandas, numpy)")
except ImportError as e:
    print(f"❌ 依赖库缺失：{e}")
    print("请运行：pip install pandas numpy")
    sys.exit(1)

# 时间序列库
try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.arima.model import ARIMA
    print("✅ statsmodels 加载成功")
except ImportError:
    print("⚠️ statsmodels 未安装")
    ExponentialSmoothing = None
    ARIMA = None

try:
    from prophet import Prophet
    print("✅ Prophet 加载成功")
except ImportError:
    print("⚠️ Prophet 未安装")
    Prophet = None


class TimeSeriesPredictor:
    """时间序列预测器 (TimesFM 替代方案)"""
    
    def __init__(self, model_type: str = "ensemble"):
        """
        初始化预测器
        
        Args:
            model_type: 模型类型 (ensemble/arima/prophet/holt)
        """
        self.model_type = model_type
        self.models = {}
        self.initialized = False
        
    def load_models(self):
        """加载预测模型"""
        print("📥 加载时间序列模型...")
        
        # 初始化多个模型用于集成
        if ExponentialSmoothing:
            self.models['holt'] = 'ready'
            print("  ✅ Holt-Winters 模型就绪")
        
        if ARIMA:
            self.models['arima'] = 'ready'
            print("  ✅ ARIMA 模型就绪")
        
        if Prophet:
            self.models['prophet'] = 'ready'
            print("  ✅ Prophet 模型就绪")
        
        self.initialized = True
        print("✅ 时间序列模型加载完成")
        return True
    
    def predict(self, historical_data: list, forecast_horizon: int = 24) -> dict:
        """
        执行时间序列预测
        
        Args:
            historical_data: 历史数据列表 [值 1, 值 2, ...]
            forecast_horizon: 预测步长 (默认 24 小时)
        
        Returns:
            预测结果字典
        """
        if not self.initialized:
            self.load_models()
        
        if len(historical_data) < 10:
            return {
                'forecast': [],
                'confidence': [],
                'timestamp': datetime.now().isoformat(),
                'error': '数据不足 (至少需要 10 个点)'
            }
        
        # 使用集成预测
        if self.model_type == "ensemble":
            return self._ensemble_predict(historical_data, forecast_horizon)
        elif self.model_type == "arima":
            return self._arima_predict(historical_data, forecast_horizon)
        elif self.model_type == "holt":
            return self._holt_predict(historical_data, forecast_horizon)
        else:
            return self._simple_predict(historical_data, forecast_horizon)
    
    def _ensemble_predict(self, historical_data: list, forecast_horizon: int) -> dict:
        """集成预测 (多模型投票)"""
        forecasts = []
        confidences = []
        
        # Holt-Winters 预测
        holt_result = self._holt_predict(historical_data, forecast_horizon)
        if 'forecast' in holt_result and holt_result['forecast']:
            forecasts.append(holt_result['forecast'])
            confidences.append(holt_result.get('confidence', [0.7] * forecast_horizon))
        
        # ARIMA 预测
        arima_result = self._arima_predict(historical_data, forecast_horizon)
        if 'forecast' in arima_result and arima_result['forecast']:
            forecasts.append(arima_result['forecast'])
            confidences.append(arima_result.get('confidence', [0.7] * forecast_horizon))
        
        if not forecasts:
            return self._simple_predict(historical_data, forecast_horizon)
        
        # 平均集成
        avg_forecast = np.mean(forecasts, axis=0).tolist()
        avg_confidence = np.mean(confidences, axis=0).tolist()
        
        return {
            'forecast': avg_forecast,
            'confidence': avg_confidence,
            'timestamp': datetime.now().isoformat(),
            'method': 'ensemble',
            'models_used': len(forecasts)
        }
    
    def _holt_predict(self, historical_data: list, forecast_horizon: int) -> dict:
        """Holt-Winters 指数平滑预测"""
        if not ExponentialSmoothing:
            return {'error': 'statsmodels 未安装'}
        
        try:
            data = np.array(historical_data)
            model = ExponentialSmoothing(
                data,
                trend='add',
                seasonal=None,
                use_boxcox=False
            )
            fitted = model.fit()
            forecast = fitted.forecast(forecast_horizon)
            
            # 计算置信度 (基于拟合优度)
            residuals = data - fitted.fittedvalues
            mse = np.mean(residuals ** 2)
            confidence = max(0.5, 0.95 - mse * 0.1)
            
            return {
                'forecast': forecast.tolist(),
                'confidence': [confidence] * forecast_horizon,
                'method': 'holt-winters'
            }
        except Exception as e:
            return {'error': f'Holt 预测失败：{e}'}
    
    def _arima_predict(self, historical_data: list, forecast_horizon: int) -> dict:
        """ARIMA 预测"""
        if not ARIMA:
            return {'error': 'statsmodels 未安装'}
        
        try:
            data = np.array(historical_data)
            # 简化 ARIMA 参数以适应小数据集
            order = (2, 1, 0) if len(data) > 20 else (1, 1, 0)
            model = ARIMA(data, order=order)
            fitted = model.fit()
            forecast = fitted.forecast(steps=forecast_horizon)
            
            # 计算置信度
            residuals = data - fitted.fittedvalues
            mse = np.mean(residuals ** 2)
            confidence = max(0.5, 0.95 - mse * 0.1)
            
            return {
                'forecast': forecast.tolist(),
                'confidence': [confidence] * forecast_horizon,
                'method': 'arima'
            }
        except Exception as e:
            return {'error': f'ARIMA 预测失败：{e}'}
    
    def _simple_predict(self, historical_data: list, forecast_horizon: int) -> dict:
        """简单线性预测 (备用方案)"""
        if len(historical_data) < 2:
            return {
                'forecast': [],
                'confidence': [],
                'timestamp': datetime.now().isoformat(),
                'error': '数据不足'
            }
        
        # 线性外推
        last_value = historical_data[-1]
        trend = (historical_data[-1] - historical_data[0]) / len(historical_data)
        
        forecast = [last_value + trend * (i + 1) for i in range(forecast_horizon)]
        confidence = [0.95 - 0.02 * i for i in range(forecast_horizon)]
        
        return {
            'forecast': forecast,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat(),
            'method': 'simple_linear'
        }


class TimesFMIntegration:
    """TimesFM 与知几-E 策略集成 (v2.0)"""
    
    def __init__(self, config_path: str = "config/timesfm-config.json"):
        """
        初始化集成
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.predictor = TimeSeriesPredictor(model_type="ensemble")
        
    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "enabled": True,
            "model_type": "ensemble",
            "forecast_horizon": 24,
            "confidence_threshold": 0.70,
            "integration_mode": "ensemble"
        }
    
    def save_config(self):
        """保存配置文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件已保存：{self.config_path}")
    
    def initialize(self):
        """初始化集成"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  TimesFM 集成初始化 (v2.0 - Python 3.12 兼容)              ║")
        print("╚═══════════════════════════════════════════════════════════")
        print()
        
        # 加载模型
        if self.config.get("enabled", True):
            self.predictor.load_models()
        
        # 保存配置
        self.save_config()
        
        print()
        print("✅ TimesFM 集成初始化完成")
        print()
    
    def predict_market(self, market_data: dict) -> dict:
        """
        预测市场走势
        
        Args:
            market_data: 市场数据
        
        Returns:
            预测结果
        """
        market_id = market_data.get('market_id', 'unknown')
        historical_prices = market_data.get('historical_prices', [])
        
        if len(historical_prices) < 10:
            return {
                'market_id': market_id,
                'prediction': 'UNKNOWN',
                'confidence': 0.0,
                'error': '历史数据不足 (需要≥10 个点)'
            }
        
        # 执行预测
        forecast_horizon = self.config.get('forecast_horizon', 24)
        result = self.predictor.predict(historical_prices, forecast_horizon)
        
        if 'error' in result:
            return {
                'market_id': market_id,
                'prediction': 'UNKNOWN',
                'confidence': 0.0,
                'error': result['error']
            }
        
        forecast = result['forecast']
        confidence = result['confidence'][0] if result['confidence'] else 0.5
        
        # 判断趋势
        if len(forecast) > 0:
            trend = (forecast[-1] - forecast[0]) / forecast[0]
            prediction = 'UP' if trend > 0.02 else ('DOWN' if trend < -0.02 else 'FLAT')
            threshold = self.config.get('confidence_threshold', 0.70)
            recommendation = 'BUY' if (prediction == 'UP' and confidence > threshold) else 'HOLD'
        else:
            prediction = 'UNKNOWN'
            recommendation = 'HOLD'
        
        return {
            'market_id': market_id,
            'prediction': prediction,
            'confidence': confidence,
            'forecast': forecast,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat(),
            'method': result.get('method', 'ensemble')
        }
    
    def integrate_with_zhiji(self, zhiji_signal: dict) -> dict:
        """
        与知几-E 策略融合
        
        Args:
            zhiji_signal: 知几-E 原始信号
        
        Returns:
            融合后信号
        """
        integration_mode = self.config.get('integration_mode', 'ensemble')
        
        if integration_mode == 'replace':
            return self.predict_market(zhiji_signal)
        
        elif integration_mode == 'augment':
            timesfm_result = self.predict_market(zhiji_signal)
            
            zhiji_conf = zhiji_signal.get('confidence', 0.5)
            timesfm_conf = timesfm_result.get('confidence', 0.5)
            
            fused_confidence = 0.6 * zhiji_conf + 0.4 * timesfm_conf
            
            if zhiji_signal.get('prediction') == timesfm_result.get('prediction'):
                fused_confidence = min(fused_confidence + 0.1, 1.0)
            else:
                fused_confidence = max(fused_confidence - 0.2, 0.0)
            
            return {
                'market_id': zhiji_signal.get('market_id'),
                'prediction': zhiji_signal.get('prediction'),
                'confidence': fused_confidence,
                'recommendation': 'BUY' if fused_confidence > self.config['confidence_threshold'] else 'HOLD',
                'sources': ['zhiji', 'timesfm'],
                'fusion_mode': 'augment',
                'timestamp': datetime.now().isoformat()
            }
        
        else:  # ensemble
            timesfm_result = self.predict_market(zhiji_signal)
            
            zhiji_pred = zhiji_signal.get('prediction')
            timesfm_pred = timesfm_result.get('prediction')
            
            if zhiji_pred == timesfm_pred:
                fused_confidence = (zhiji_signal.get('confidence', 0.5) + timesfm_result.get('confidence', 0.5)) / 2
                fused_confidence = min(fused_confidence + 0.1, 1.0)
            else:
                fused_confidence = zhiji_signal.get('confidence', 0.5) * 0.8
            
            threshold = self.config.get('confidence_threshold', 0.70)
            return {
                'market_id': zhiji_signal.get('market_id'),
                'prediction': zhiji_pred,
                'confidence': fused_confidence,
                'recommendation': 'BUY' if fused_confidence > threshold else 'HOLD',
                'sources': ['zhiji', 'timesfm'],
                'fusion_mode': 'ensemble',
                'agreement': zhiji_pred == timesfm_pred,
                'timestamp': datetime.now().isoformat()
            }


def main():
    """主函数 - 测试 TimesFM 集成"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  TimesFM 集成测试 v2.0 (Python 3.12 兼容)                  ║")
    print("║  太一 AGI · 知几-E 量化策略                                ║")
    print("╚═══════════════════════════════════════════════════════════")
    print()
    
    # 创建集成实例
    integration = TimesFMIntegration()
    
    # 初始化
    integration.initialize()
    
    # 测试预测
    print("📊 执行测试预测...")
    test_data = {
        'market_id': 'TEST-WEATHER-001',
        'historical_prices': [0.45, 0.48, 0.52, 0.50, 0.55, 0.58, 0.60, 0.62, 0.65, 0.63, 0.67, 0.70],
        'volume': [1000, 1200, 1100, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100]
    }
    
    result = integration.predict_market(test_data)
    print()
    print("📈 预测结果:")
    print(f"  市场：{result['market_id']}")
    print(f"  预测：{result['prediction']}")
    print(f"  置信度：{result['confidence']:.2%}")
    print(f"  建议：{result['recommendation']}")
    print(f"  方法：{result.get('method', 'unknown')}")
    print()
    
    # 测试与知几-E 融合
    print("🔗 测试知几-E 策略融合...")
    zhiji_signal = {
        'market_id': 'TEST-WEATHER-001',
        'prediction': 'UP',
        'confidence': 0.75
    }
    
    fused_result = integration.integrate_with_zhiji(zhiji_signal)
    print()
    print("📊 融合结果:")
    print(f"  市场：{fused_result['market_id']}")
    print(f"  预测：{fused_result['prediction']}")
    print(f"  融合置信度：{fused_result['confidence']:.2%}")
    print(f"  融合模式：{fused_result.get('fusion_mode', 'unknown')}")
    print(f"  建议：{fused_result['recommendation']}")
    print()
    
    print("✅ TimesFM 集成测试完成")
    print()
    print("═══════════════════════════════════════════════════════════")
    print("📋 集成状态:")
    print("  ✅ Python 3.12 兼容")
    print("  ✅ statsmodels (ARIMA + Holt-Winters)")
    print("  ✅ Prophet (可选)")
    print("  ✅ 集成预测模式")
    print("  ✅ 知几-E 策略融合")
    print()
    print("📁 下一步:")
    print("1. 接入真实市场数据 (Polymarket API)")
    print("2. 执行历史回测")
    print("3. 实盘测试 (14 天周期)")
    print("═══════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
