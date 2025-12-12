from pydantic import BaseModel
from datetime import datetime


class TokenBalanceResponse(BaseModel):
    balance: int
    total_used: int
    percentage_remaining: float


class TokenHistoryItem(BaseModel):
    id: int
    request_type: str
    tokens_used: int
    prompt: str
    created_at: datetime
    status: str
    
    class Config:
        from_attributes = True
