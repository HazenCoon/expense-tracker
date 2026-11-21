from pydantic import BaseModel
from typing import Literal


class TransactionCreate(BaseModel):
    amount: int
    transaction_type: Literal["expense", "income"]
    category: str
    date: str
    description: str | None = None
