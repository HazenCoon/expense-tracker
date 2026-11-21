from fastapi import APIRouter
from app.database import get_transactions, add_transaction
from app.schemas import TransactionCreate

router = APIRouter()


@router.get("/transactions")
def read_transactions():
    return get_transactions()


@router.post("/transactions", status_code=201)
def create_transactions(transaction: TransactionCreate):
    add_transaction(
        transaction.amount,
        transaction.transaction_type,
        transaction.category,
        transaction.date,
        transaction.description,
    )
    return {"message": "Transaktion erfolgreich gespeichert!"}
