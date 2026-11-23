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


def test_post_transactions_rejects_category_for_wrong_type(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        response = client.post(
            "/transactions",
            json={
                "amount": 2500,
                "transaction_type": "expense",
                "category": "Gehalt",
                "date": "2026-11-22",
                "description": "Ungültige Kombination",
            },
        )
        transactions = client.get("/transactions").json()
        assert response.status_code == 422
        assert transactions == []


def test_post_transactions_rejects_amount_zero(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        response = client.post(
            "/transactions",
            json={
                "amount": 0,
                "transaction_type": "expense",
                "category": "Lebensmittel",
                "date": "2026-10-20",
                "description": "Ungültige Eingabe in amount",
            },
        )
        transactions = client.get("/transactions").json()
        assert response.status_code == 422
        assert transactions == []


def test_post_transactions_rejects_invalid_date(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        response = client.post(
            "/transactions",
            json={
                "amount": 1000,
                "transaction_type": "expense",
                "category": "Lebensmittel",
                "date": "2026-99-99",
                "description": "Ungültiges Datum",
            },
        )
        transactions = client.get("/transactions").json()
        assert response.status_code == 422
        assert transactions == []
