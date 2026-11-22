from fastapi.testclient import TestClient
import app.database as database


def test_pages_returns_category_filter_and_category(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "Noch keine Buchungen vorhanden" in response.text
    assert 'src="/static/category-filter.js"' in response.text
    assert 'data-transaction-type="income"' in response.text
    assert 'data-transaction-type="expense"' in response.text
    assert 'type="radio" name="transaction_type" value="expense"' in response.text
    assert 'type="radio" name="transaction_type" value="income"' in response.text


def test_post_transactions_form_converts_to_int(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app, follow_redirects=False) as client:
        post = client.post(
            "/transactions/form",
            data={
                "amount": "25.00",
                "transaction_type": "expense",
                "category": "Lebensmittel",
                "date": "2026-04-01",
                "description": "Test Konvertierung in Cent",
            },
        )
        assert post.status_code == 303
        response = client.get("/transactions")
        assert response.json() == [
            [
                1,
                2500,
                "expense",
                "Lebensmittel",
                "2026-04-01",
                "Test Konvertierung in Cent",
            ]
        ]


def test_post_transaction_form_rejects_category_for_wrong_type(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app, follow_redirects=False) as client:
        response = client.post(
            "/transactions/form",
            data={
                "amount": "32.00",
                "transaction_type": "expense",
                "category": "Gehalt",
                "date": "2025-02-15",
                "description": "Ungültige Kombination",
            },
        )
        assert response.status_code == 422
        assert client.get("/transactions").json() == []


def test_post_transaction_form_rejects_zero_amount(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app, follow_redirects=False) as client:
        response = client.post(
            "/transactions/form",
            data={
                "amount": "0.00",
                "transaction_type": "expense",
                "category": "Lebensmittel",
                "date": "2026-12-12",
                "description": "Ungültiger Betrag",
            },
        )

        assert response.status_code == 422
        assert client.get("/transactions").json() == []


def test_post_transaction_form_rejects_more_than_two_decimal_places(
    tmp_path, monkeypatch
):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    from app.main import app

    with TestClient(app, follow_redirects=False) as client:
        response = client.post(
            "/transactions/form",
            data={
                "amount": "1700.219",
                "transaction_type": "income",
                "category": "Sonstiges",
                "date": "2026-06-06",
                "description": "Ungültiger Betrag",
            },
        )

        assert response.status_code == 422
        assert client.get("/transactions").json() == []
