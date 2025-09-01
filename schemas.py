from pydantic import BaseModel
from typing import Optional
from sqlalchemy import DateTime

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    balance: float
    created_at: Optional[DateTime] = None
    updated_at: Optional[DateTime] = None
        
class TransactionBase(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    description: str
    reference_transaction_id: int
    recipient_user_id:int
    created_at: Optional[DateTime] = None