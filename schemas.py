
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phone_number: Optional[str] = None
    balance: Optional[float] = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: Optional[str] = None
    balance: float
    created_at: Optional[datetime] = None

class WalletBalance(BaseModel):
    user_id: int
    balance: float
    last_updated: Optional[datetime] = None

class AddMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

class TransactionBase(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    reference_transaction_id: Optional[int] = None
    recipient_user_id: Optional[int] = None
    created_at: Optional[datetime] = None

class TransactionOut(BaseModel):
    transactions: List[TransactionBase]
    total: int
    page: int
    limit: int

class TransferCreate(BaseModel):
    transfer_id: int
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str
    
class TransferOut(BaseModel):
    transfer_id: int
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None