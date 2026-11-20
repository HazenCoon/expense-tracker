from fastapi import FastAPI
from app.database import create_table

create_table()
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Expense Tracker is running"}
