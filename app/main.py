from fastapi import FastAPI
from app.database import create_table
from app.routers.transactions import router as transactions_router

create_table()
app = FastAPI()
app.include_router(transactions_router)


@app.get("/")
def read_root():
    return {"message": "Expense Tracker is running"}
