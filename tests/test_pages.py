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
