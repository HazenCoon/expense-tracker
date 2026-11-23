import sqlite3
from pathlib import Path


def get_connection():
    data_directory = Path("data")
    data_directory.mkdir(exist_ok=True)
    return sqlite3.connect(data_directory / "expense_tracker.db")


def create_table():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY,
                amount INTEGER NOT NULL CHECK(amount>0),
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income','expense')),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        """)
        connection.commit()
    finally:
        connection.close()


def add_transaction(amount, transaction_type, category, date, description=None):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
                    INSERT INTO transactions(
                    amount,
                    transaction_type,
                    category,
                    date,
                    description
                )
                VALUES(?,?,?,?,?)""",
            (amount, transaction_type, category, date, description),
        )
        connection.commit()
    finally:
        connection.close()


def get_transactions():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
            id,
            amount,
            transaction_type,
            category,
            date,
            description
            FROM transactions
            ORDER BY date DESC, id DESC
    """)
        data = cursor.fetchall()
    finally:
        connection.close()
    return data
