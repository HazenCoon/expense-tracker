from fastapi import FastAPI, Request
from app.database import create_table, get_transactions
from app.routers.transactions import router as transactions_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.services import CATEGORIES_BY_TYPE

BASE_DIR = Path(__file__).resolve().parent
create_table()
app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(transactions_router)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "transactions": get_transactions(),
            "categories_by_type": CATEGORIES_BY_TYPE,
        },
    )
