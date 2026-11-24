from fastapi import FastAPI, Request
from app.database import create_table, get_transactions
from app.routers.transactions import router as transactions_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.services import CATEGORIES_BY_TYPE
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
create_table()
app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def format_german_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return value


templates.env.filters["german_date"] = format_german_date

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(transactions_router)


@app.get("/")
def read_root(request: Request):
    error_message = None
    if request.query_params.get("error") == "invalid_date":
        error_message = "Bitte geben Sie ein gültiges Datum ein."
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "transactions": get_transactions(),
            "categories_by_type": CATEGORIES_BY_TYPE,
            "error": error_message,
            "today": datetime.today().date().isoformat(),
        },
    )
