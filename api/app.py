#!/usr/bin/env python3
"""
情景模式 API 服务
FastAPI 实现

端点：
- POST /api/v1/analyze - 分析用户问题
- GET /api/v1/skills/{skill_id} - 获取 Skill 详情
- POST /api/v1/skills/{skill_id}/unlock - 解锁 Skill (付费)
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
from pathlib import Path
from datetime import datetime
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.decision_agent import DecisionAgent

app = FastAPI(
    title="情景模式 API",
    description="64×6=384 Skills 决策引擎",
    version="2.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
agent = None


def get_agent() -> DecisionAgent:
    """获取 Decision Agent 单例"""
    global agent
    if agent is None:
        agent = DecisionAgent()
    return agent


# 数据模型
class AnalyzeRequest(BaseModel):
    """分析请求"""
    user_input: str
    test_type: Optional[str] = "quick"  # quick/standard/deep


class AnalyzeResponse(BaseModel):
    """分析响应"""
    state: Dict
    stage: Dict
    skill_preview: Dict  # 免费预览
    skill_full: Optional[Dict]  # 完整内容 (付费后)
    confidence: float
    upsell: Dict
    timestamp: str


class UnlockRequest(BaseModel):
    """解锁请求"""
    skill_id: str
    payment_token: str  # 支付凭证


class UnlockResponse(BaseModel):
    """解锁响应"""
    success: bool
    skill: Optional[Dict]
    message: str


# API 端点
@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "情景模式 API",
        "version": "2.0",
        "description": "64×6=384 Skills 决策引擎",
        "endpoints": [
            "POST /api/v1/analyze",
            "GET /api/v1/skills/{skill_id}",
            "POST /api/v1/skills/{skill_id}/unlock"
        ]
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "skills_loaded": len(get_agent().skills) if get_agent() else 0
    }


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_user_input(request: AnalyzeRequest):
    """
    分析用户输入，返回 State + Stage + Skill
    
    分层返回策略：
    - 免费层：State 识别 + Stage 判断
    - ¥1 层：Stage 详细解释
    - ¥9.9 层：完整 Skill 行动方案
    """
    
    agent = get_agent()
    
    # 执行分析
    result = agent.analyze(request.user_input)
    
    # 构建响应
    state = result['state']
    stage = result['stage']
    skill = result['skill']
    
    # 免费预览（部分信息）
    skill_preview = {}
    if skill:
        skill_preview = {
            "id": skill['id'],
            "state_name": skill['state_name'],
            "stage": skill['stage'],
            "decision": skill['decision'],
            # 隐藏具体行动，引导付费
            "action_count": len(skill['action']),
            "has_psychology": True
        }
    
    # 付费引导
    upsell = {
        "tiers": [
            {
                "name": "免费",
                "price": 0,
                "content": "状态识别 + 阶段判断",
                "unlocked": True
            },
            {
                "name": "阶段解读",
                "price": 1.0,
                "content": "阶段详细解释 + 心理学解读",
                "unlocked": False,
                "unlock_action": "POST /api/v1/stage/{state_id}/{stage}/unlock"
            },
            {
                "name": "完整方案",
                "price": 9.9,
                "content": "完整行动方案 + 避免事项 + 3 重心理学解读",
                "unlocked": False,
                "unlock_action": f"POST /api/v1/skills/{skill['id']}/unlock" if skill else None
            },
            {
                "name": "会员",
                "price": 19.0,
                "price_unit": "月",
                "content": "384 Skills 无限访问 + 用户轨迹追踪",
                "unlocked": False,
                "unlock_action": "POST /api/v1/membership/unlock"
            }
        ]
    }
    
    return AnalyzeResponse(
        state=state,
        stage=stage,
        skill_preview=skill_preview,
        skill_full=None,  # 付费后返回
        confidence=result['confidence'],
        upsell=upsell,
        timestamp=result['timestamp']
    )


@app.get("/api/v1/skills/{skill_id}")
async def get_skill_preview(skill_id: str):
    """
    获取 Skill 预览（免费）
    """
    
    agent = get_agent()
    skill = agent.skills.get(skill_id)
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # 返回预览（隐藏核心内容）
    preview = {
        "id": skill['id'],
        "state_name": skill['state_name'],
        "stage": skill['stage'],
        "stage_name": skill['stage_name'],
        "type": skill['type'],
        "theme": skill['theme'],
        "situation": skill['situation'],
        "decision": skill['decision'],
        # 隐藏行动和心理学解读
        "action_count": len(skill['action']),
        "avoid_count": len(skill['avoid']),
        "has_psychology": True,
        "price_tier": skill['metadata']['price_tier'],
        "unlock_price": 9.9
    }
    
    return preview


@app.post("/api/v1/skills/{skill_id}/unlock", response_model=UnlockResponse)
async def unlock_skill(skill_id: str, request: UnlockRequest):
    """
    解锁完整 Skill（付费）
    
    验证支付凭证，返回完整 Skill 内容
    """
    
    agent = get_agent()
    skill = agent.skills.get(skill_id)
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # TODO: 验证支付凭证
    # 这里简化处理，实际应该调用支付 API 验证
    payment_valid = validate_payment(request.payment_token, skill_id)
    
    if not payment_valid:
        return UnlockResponse(
            success=False,
            skill=None,
            message="支付凭证无效"
        )
    
    # 返回完整 Skill
    return UnlockResponse(
        success=True,
        skill=skill,
        message="解锁成功"
    )


@app.get("/api/v1/states")
async def list_states():
    """
    获取所有状态列表（免费）
    """
    
    agent = get_agent()
    
    states = []
    for skill_id, skill in agent.skills.items():
        state_info = {
            "id": skill['state_id'],
            "name": skill['state_name'],
            "type": skill['type'],
            "theme": skill['theme']
        }
        if state_info not in states:
            states.append(state_info)
    
    return {
        "total": len(states),
        "states": states
    }


@app.get("/api/v1/states/{state_id}/stages")
async def list_state_stages(state_id: str):
    """
    获取某个状态的所有阶段（免费）
    """
    
    agent = get_agent()
    
    stages = []
    for skill_id, skill in agent.skills.items():
        if skill['state_id'] == state_id:
            stage_info = {
                "stage": skill['stage'],
                "stage_name": skill['stage_name'],
                "skill_id": skill['id'],
                "theme": skill['theme']
            }
            stages.append(stage_info)
    
    # 按阶段排序
    stages.sort(key=lambda x: x['stage'])
    
    return {
        "state_id": state_id,
        "total": len(stages),
        "stages": stages
    }


# 辅助函数
def validate_payment(payment_token: str, skill_id: str) -> bool:
    """
    验证支付凭证
    
    TODO: 实现真实的支付验证逻辑
    目前简化为总是成功（测试用）
    """
    
    # 测试用：特定 token 总是成功
    if payment_token.startswith("test_"):
        return True
    
    # TODO: 调用微信支付/支付宝 API 验证
    # 实际应该：
    # 1. 验证 token 有效性
    # 2. 检查是否已支付
    # 3. 检查金额是否匹配
    
    return False


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    print("🚀 情景模式 API 启动...")
    agent = get_agent()
    print(f"✅ 加载 {len(agent.skills)} 个 Skills")
    print("✅ API 就绪")


# 运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
