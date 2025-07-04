from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
# from models import Wallet


class OperationType(str, Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class OperationRequest(BaseModel):
    operationType: OperationType
    amount: float = Field(..., gt=0)


class WalletResponse(BaseModel):
    wallet_id: UUID
    balance: float