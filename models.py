from pydantic import Field
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User:
    id:int = Field(primary_key=True)
    username:str = Field(unique=True, nullable=False)
    email:str = Field(unique=True, nullable=False)
    password:str = Field(nullable=False)
    phone_number:str
    balance:float = Field(default=0.0)
    created_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    transactions = relationship("Transaction", back_populates="user")

class Transaction:
    id:int = Field(primary_key=True)
    user_id:int
    transaction_type:str = Field(nullable=False, only=["CREDIT", "DEBIT", "TRANSFER_IN", "TRANSFER_OUT"]) 
    amount:float
    description:str
    reference_transaction_id:int
    recipient_user_id:int
    created_at:DateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="transactions")