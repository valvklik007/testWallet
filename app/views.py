from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .database import sessionLocal
from .schemas import OperationRequest, WalletResponse
from . import crud


router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


async def get_session() -> AsyncSession:
    async with sessionLocal() as session:
        yield session


#Создать кошелек
@router.get("/create", response_model=WalletResponse)
async def create_wallets(session: AsyncSession = Depends(get_session)):
    wallet = await crud.create_wallet(session)
    return WalletResponse(wallet_id=wallet.id, balance=float(wallet.balance))


#Перевод
@router.post("/{wallet_id}/operation", response_model=WalletResponse)
async def wallet_operation(wallet_id: UUID, data: OperationRequest, session: AsyncSession = Depends(get_session)):
    wallet = await crud.operate_wallet(session, wallet_id, data.operationType, data.amount)
    return WalletResponse(wallet_id=wallet.id, balance=float(wallet.balance))


#Баланс
@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(wallet_id: UUID, session: AsyncSession = Depends(get_session)):
    wallet = await crud.get_wallet(session, wallet_id)
    return WalletResponse(wallet_id=wallet.id, balance=float(wallet.balance))