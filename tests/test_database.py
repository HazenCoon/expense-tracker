import app.database as database
import sqlite3
import pytest


def test_get_transactions_returns_saved_transaction(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    database.add_transaction(250000, "income", "Gehalt", "2026-11-20", "pytest-Test")

    assert database.get_transactions() == [
        (1, 250000, "income", "Gehalt", "2026-11-20", "pytest-Test")
    ]


def test_get_transactions_returns_empty_list(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()

    assert database.get_transactions() == []


def test_add_transactions_rejects_zero_amount(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)

    database.create_table()
    with pytest.raises(sqlite3.IntegrityError):
        database.add_transaction(0, "income", "Gehalt", "2026-10-19", "Test add 0")
