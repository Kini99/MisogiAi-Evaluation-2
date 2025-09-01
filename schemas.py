from typing import Optional
from sqlalchemy import DateTime
from database import Base

class UserBase(Base):
    username: str
    email: str
    password: str
    phone_number: str
    balance: float
    created_at: Optional[DateTime] = None
    updated_at: Optional[DateTime] = None

class UserOut(UserBase):
    user_id: int
    username:str
    email:str
    phone_number: str
    balance: float
    created_at: Optional[DateTime] = None
    
class WalletBalance(Base):
    user_id: int
    balance: float
    last_updated: Optional[DateTime] = None
    
class AddMoneyResponse(Base):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

class TransactionBase(Base):
    user_id: int
    transaction_type: str
    amount: float
    description: str
    reference_transaction_id: int
    recipient_user_id:int
    created_at: Optional[DateTime] = None
    
class TransactionOut(Base):
    transactions: list[TransactionBase]
    total: int
    page: int
    limit: int
    
class TransferCreate(Base):
    transfer_id: int
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str
    
class TransferOut(Base):
    transfer_id: int
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str
    status: str
    created_at: Optional[DateTime] = None