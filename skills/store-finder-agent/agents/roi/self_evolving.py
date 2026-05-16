"""
ROI模型自进化 — 实际开店数据反馈闭环
LightGBM增量训练 → 更新后的ROI预测模型
"""
def update_roi_model_with_feedback(existing_model, feedback_df):
    """
    根据开店实际收益数据，更新ROI预测模型
    """
    X_new = feedback_df[["area", "rent", "foot_traffic", "competitors_count"]]
    y_new = feedback_df["actual_roi"]
    existing_model.add_valid_data(X_new, y_new)
    existing_model.train(num_boost_round=50)
    return existing_model

def simulate_roi(model, candidate_df, scenarios: list) -> list:
    """
    多场景ROI预测
    scenarios: [{'foot_traffic': val, 'rent': val}, ...]
    """
    results = []
    for s in scenarios:
        df_copy = candidate_df.copy()
        for k, v in s.items():
            df_copy[k] = v
        df_copy['predicted_roi'] = model.predict(
            df_copy[["area", "rent", "foot_traffic", "competitors_count"]]
        )
        results.append(df_copy[['name', 'predicted_roi']])
    return results
