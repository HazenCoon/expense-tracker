from fastapi import APIRouter, Form, HTTPException
from app.database import get_transactions, add_transaction
from app.schemas import TransactionCreate
from decimal import Decimal
from fastapi.responses import RedirectResponse
from app.services import CATEGORIES_BY_TYPE

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


@router.post("/transactions/form")
def create_transaction_from_form(
    amount: Decimal = Form(...),
    transaction_type: str = Form(...),
    category: str = Form(...),
    date: str = Form(...),
    description: str | None = Form(None),
):
    if transaction_type not in CATEGORIES_BY_TYPE:
        raise HTTPException(status_code=422, detail="Ungültige Buchungsart.")
    if category not in CATEGORIES_BY_TYPE[transaction_type]:
        raise HTTPException(
            status_code=422, detail="Diese Kategorie passt nicht zur Buchungsart."
        )
    if amount <= 0:
        raise HTTPException(
            status_code=422, detail="Der Betrag muss größer als 0 sein."
        )
    amount_in_cents = amount * 100
    if amount_in_cents != amount_in_cents.to_integral_value():
        raise HTTPException(
            status_code=422,
            detail="Der Betrag darf höchstens zwei Nachkommastellen haben.",
        )

    add_transaction(
        int(amount_in_cents),
        transaction_type,
        category,
        date,
        description,
    )
    return RedirectResponse(url="/", status_code=303)
