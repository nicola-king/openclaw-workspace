"""
共情路由策略
目标：情感感知模型选择，提供更有温度的响应
"""

from typing import Dict, Any, List, Tuple


class EmpathyRouter:
    """共情路由器"""
    
    # 情感关键词分类
    EMOTION_KEYWORDS = {
        'negative': ['难过', '伤心', '沮丧', '焦虑', '压力', '累', '烦', '失望', '痛苦', '绝望'],
        'positive': ['开心', '高兴', '兴奋', '满意', '幸福', '快乐', '棒', '好'],
        'neutral': ['平静', '一般', '还行', '普通'],
    }
    
    # 情感强度分数
    EMOTION_INTENSITY = {
        'negative': -0.8,
        'positive': 0.6,
        'neutral': 0.0,
    }
    
    def __init__(self):
        self.empathy_config = {
            'warm_tone': True,
            'longer_response': True,
            'validate_feelings': True,
        }
    
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """
        检测文本情感
        
        Returns:
            (情感类型，强度分数)
        """
        scores = {}
        
        for emotion_type, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[emotion_type] = score
        
        # 确定主导情感
        max_emotion = max(scores, key=scores.get)
        max_score = scores[max_emotion]
        
        if max_score == 0:
            return 'neutral', 0.0
        
        intensity = self.EMOTION_INTENSITY[max_emotion] * min(1.0, max_score / 3)
        return max_emotion, intensity
    
    def route(self, task_info: Dict[str, Any]) -> str:
        """
        根据情感信息选择最合适的模型
        
        Args:
            task_info: 任务信息 {type, complexity, token_estimate, text}
        
        Returns:
            模型名称
        """
        text = task_info.get('text', '')
        
        # 检测情感
        emotion, intensity = self.detect_emotion(text)
        
        # 负面情感 → 使用主力模型，确保高质量共情响应
        if emotion == 'negative':
            return 'bailian/qwen3.5-plus'
        
        # 正面情感 → 可以使用本地模型
        if emotion == 'positive' and task_info.get('complexity') == 'easy':
            return 'local/qwen2.5:7b'
        
        # 中性/默认 → 主力模型
        return 'bailian/qwen3.5-plus'
    
    def get_empathy_config(self, emotion: str, intensity: float) -> Dict[str, Any]:
        """
        获取共情配置
        
        Returns:
            共情配置字典
        """
        config = self.empathy_config.copy()
        
        # 根据情感调整配置
        if emotion == 'negative':
            config['warm_tone'] = True
            config['longer_response'] = intensity < -0.5  # 更强烈的负面情感需要更长响应
            config['validate_feelings'] = True
            config['offer_support'] = True
        elif emotion == 'positive':
            config['warm_tone'] = True
            config['celebrate'] = True
            config['longer_response'] = False
        
        return config
    
    def enhance_prompt(self, original_prompt: str, emotion: str, intensity: float) -> str:
        """
        增强提示词，添加共情指导
        
        Args:
            original_prompt: 原始提示词
            emotion: 情感类型
            intensity: 情感强度
        
        Returns:
            增强后的提示词
        """
        if emotion == 'negative':
            prefix = "请表现出理解和关心，语气温和 supportive。"
            if intensity < -0.5:
                prefix += "用户情绪较低，请提供更多情感支持和鼓励。"
            return f"{prefix}\n\n{original_prompt}"
        
        elif emotion == 'positive':
            prefix = "请分享用户的喜悦，语气轻快积极。"
            return f"{prefix}\n\n{original_prompt}"
        
        return original_prompt
