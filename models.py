from pydantic import BaseModel, Field
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class User:
    id:int
    username:str
    email:str
    password:str
    phone_number:str
    balance:float
    created_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    transactions = relationship("Transaction", back_populates="user")

class Transaction:
    id:int
    user_id:int
    transaction_type:str
    amount:float
    description:str
    reference_transaction_id:int
    recipient_user_id:int
    created_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))