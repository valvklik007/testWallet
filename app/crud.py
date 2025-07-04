from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from fastapi import HTTPException
from uuid import UUID
from .models import Wallet
from .schemas import OperationType



async def create_wallet(session: AsyncSession) -> Wallet:
    try:
        wallet = Wallet(balance=0)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail="Error creating wallet"
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail="Unexpected error creating wallet"
        )



async def get_wallet(session: AsyncSession, wallet_id: UUID) -> Wallet:
    stmt = select(Wallet).where(Wallet.id == wallet_id)
    result = await session.execute(stmt)
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet



async def operate_wallet(session: AsyncSession, wallet_id: UUID, operation: OperationType, amount: float):
    async with session.begin():
        wallet = await session.get(Wallet, wallet_id, with_for_update=True)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        decimal_amount = Decimal(str(amount))

        if operation == OperationType.withdraw:
            if wallet.balance < decimal_amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance -= decimal_amount
        else:
            wallet.balance += decimal_amount

        session.add(wallet)
    return wallet