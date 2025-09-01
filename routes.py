from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from models import User, Transaction
from schemas import UserBase, UserOut, WalletBalance, AddMoneyResponse, TransactionBase, TransactionOut, TransferCreate, TransferOut
from database import get_db
from sqlalchemy.future import select
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter()

# Get user by ID
@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "balance": user.balance,
        "created_at": user.created_at,
    }

# Put user by ID
@router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: UserBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return HTTP_200_OK
    

# Get user wallet balance
@router.get("/wallet/{user_id}/balance", response_model=WalletBalance)
async def get_wallet_balance(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
            "user_id":user.id,
            "balance": user.balance,
            "last_updated": user.updated_at,
            }

# Post add money to wallet
@router.post("/wallet/{user_id}/add-money", response_model=AddMoneyResponse)
async def add_money_to_wallet(user_id: str, transaction_data: TransactionBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if transaction_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if round(transaction_data.amount, 2) != transaction_data.amount:
        raise HTTPException(status_code=400, detail="Amount must be up to 2 decimal places only")
    user.balance += transaction_data.amount
    # ensure user.balance is updated in db
    await db.refresh(user)
    new_transaction = Transaction(
        user_id=user_id,
        transaction_type="CREDIT",
        amount=transaction_data.amount,
        description=transaction_data.description,
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return {
        "transaction_id":transaction_data.reference_transaction_id,
        "user_id":user_id,
        "amount":transaction_data.amount,
        "new_balance": user.balance,
        "transaction_type":"CREDIT",
    }

# Post widhdraw money from wallet
@router.post("/wallet/{user_id}/withdraw")
async def withdraw_money_from_wallet(user_id: str, transaction_data: TransactionBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if transaction_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if round(transaction_data.amount, 2) != transaction_data.amount:
        raise HTTPException(status_code=400, detail="Amount must be up to 2 decimal places only")
    if user.balance < transaction_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    user.balance -= transaction_data.amount
    # ensure user.balance is updated in db
    await db.refresh(user)
    new_transaction = Transaction(
        user_id=user_id,
        transaction_type="DEBIT",
        amount=transaction_data.amount,
        description=transaction_data.description,
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return HTTP_201_CREATED

# Get user transaction history with pagination
@router.get("/transactions/{user_id}?page={page}&limit={limit}", response_model=TransactionOut)
async def get_transaction_history(user_id: str, page: int = 1, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    offset = (page - 1) * limit
    result = await db.execute(select(Transaction).where(user_id==user_id).offset(offset).limit(limit))
    transactions = result.scalars().all()
    return {
        "transactions": transactions,
        "total": len(transactions),
        "page": page,
        "limit": limit
    }

# Get transaction detail by ID
@router.get("/transactions/detail/{transaction_id}", response_model=TransactionBase)
async def get_transaction_detail(transaction_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(id==transaction_id))
    transaction = result.scalars().first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Post transactions with userid, transaction type (CREDIT|DEBIT), amount, description
# @router.post("/transactions/", response_model=TransactionBase)
# async def create_transaction(transaction_data: TransactionBase, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(User).where(id==transaction_data.user_id))
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if transaction_data.amount <= 0:
#         raise HTTPException(status_code=400, detail="Amount must be positive")
#     if round(transaction_data.amount, 2) != transaction_data.amount:
#         raise HTTPException(status_code=400, detail="Amount must be up to 2 decimal places only")
#     if transaction_data.transaction_type == "DEBIT" and user.balance < transaction_data.amount:
#         raise HTTPException(status_code=400, detail="Insufficient balance")
#     if transaction_data.transaction_type == "CREDIT":
#         user.balance += transaction_data.amount
#     elif transaction_data.transaction_type == "DEBIT":
#         user.balance -= transaction_data.amount
#     else:
#         raise HTTPException(status_code=400, detail="Invalid transaction type")
#     new_transaction = Transaction(
#         user_id=transaction_data.user_id,
#         transaction_type=transaction_data.transaction_type,
#         amount=transaction_data.amount,
#         description=transaction_data.description,
#         reference_transaction_id=transaction_data.reference_transaction_id,
#         recipient_user_id=transaction_data.recipient_user_id
#     )
#     db.add(new_transaction)
#     await db.commit()
#     await db.refresh(new_transaction)
#     #update balance in user wallet
#     await db.refresh(user)
#     return new_transaction

# Post transfer money to another user with sender_user_id, recipient_user_id, amount, description
@router.post("/transfer", response_model=TransferCreate)
async def transfer_money(sender_user_id: str, recipient_user_id: str, amount: float, description: str, db: AsyncSession = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if round(amount, 2) != amount:
        raise HTTPException(status_code=400, detail="Amount must be up to 2 decimal places only")
    result = await db.execute(select(User).where(id==sender_user_id))
    sender = result.scalars().first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    result = await db.execute(select(User).where(id==recipient_user_id))
    recipient = result.scalars().first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    sender.balance -= amount
    recipient.balance += amount
    # ensure balances are updated in db
    await db.refresh(sender)
    await db.refresh(recipient)
    new_transaction = Transaction(
        user_id=sender_user_id,
        transaction_type="DEBIT",
        amount=amount,
        description=description,
        recipient_user_id=recipient_user_id
    )
    new_transaction_recipient = Transaction(
        user_id=recipient_user_id,
        transaction_type="CREDIT",
        amount=amount,
        description=description,
        reference_transaction_id=new_transaction.id,
        recipient_user_id=sender_user_id
    )
    db.add(new_transaction)
    db.add(new_transaction_recipient)
    await db.commit()
    await db.refresh(new_transaction)
    return {
        "transfer_id": new_transaction.id,
        "sender_transaction_id": new_transaction.id,
        "recipient_transaction_id": new_transaction.id,
        "amount": amount,
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance,
        "status": "completed"
    }
    
# Get transfer detail by ID
@router.get("/transfer/{transfer_id}", response_model=TransferOut)
async def get_transfer_detail(transfer_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(id==transfer_id))
    transaction = result.scalars().first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transfer not found")
    if not transaction.recipient_user_id:
        raise HTTPException(status_code=400, detail="Not a transfer transaction")
    return transaction