# TimesFM 配置
TIMESFM_ENABLED = True
try:
    import timesfm
    print(f"✅ TimesFM 已加载 (v{timesfm.__version__ if hasattr(timesfm, '__version__') else '2.0.0'})")
except ImportError:
    print("⚠️  TimesFM 未安装，使用 v3.0 策略")
    TIMESFM_ENABLED = False
