from app.routers import transactions
import app.database as database
from fastapi.testclient import TestClient


def test_get_transactions_returns_empty_list(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []


def test_post_transactions_saves_transaction(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        post = client.post(
            "/transactions",
            json={
                "amount": 2500,
                "transaction_type": "income",
                "category": "Gehalt",
                "date": "2026-08-13",
                "description": "Test post_transactions",
            },
        )
        response = client.get("/transactions")
    assert post.status_code == 201
    assert response.json() == [
        [
            1,
            2500,
            "income",
            "Gehalt",
            "2026-08-13",
            "Test post_transactions",
        ]
    ]


def test_post_transactions_rejects_invalid_transaction_type(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        post = client.post(
            "/transactions",
            json={
                "amount": 61000,
                "transaction_type": "transfer",
                "category": "Gehalt",
                "date": "2025-03-07",
                "description": "Test post_transactions with wrong transaction-type",
            },
        )
        response = client.get("/transactions")
    assert post.status_code == 422
    assert response.json() == []
