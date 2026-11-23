from pydantic import BaseModel
from typing import Literal
from datetime import date


class TransactionCreate(BaseModel):
    amount: int
    transaction_type: Literal["expense", "income"]
    category: str
    date: date
    description: str | None = None
