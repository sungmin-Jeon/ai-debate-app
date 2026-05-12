from typing import Dict, List, TypedDict

class AgentType:
    PRO = "PRO_AGENT"  # 찬성
    CON = "CON_AGENT"   # 반대
    JUDGE = "JUDGE_AGENT"   # 심판

    @classmethod
    def to_korean(cls, role: str) -> str:
        if role == cls.PRO:
            return "찬성"
        elif role == cls.CON:
            return "반대"
        elif role == cls.JUDGE:
            return "심판"
        else:
            return role

# 토론 진행 데이터 형식 정의       
class DebateState(TypedDict):

    topic: str
    messages: List[Dict]
    current_round: int
    max_rounds: int