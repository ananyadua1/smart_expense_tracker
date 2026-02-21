import sqlite3

def get_connection():
    return sqlite3.connect("expenses.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash BLOB
    )
    """)

    # Expenses table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # NEW: Monthly Budget Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS monthly_budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        month TEXT,
        budget REAL,
        UNIQUE(user_id, month)
    )
    """)

    conn.commit()
    conn.close()