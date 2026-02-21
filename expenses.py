import pandas as pd
from database import get_connection

def add_expense(user_id, amount, category, date, desc):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO expenses (user_id, amount, category, description, date)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, category, desc, date))

    conn.commit()
    conn.close()


def get_expenses(user_id):
    conn = get_connection()
    df = pd.read_sql_query(
        """
        SELECT expense_id, amount, category, description, date
        FROM expenses
        WHERE user_id=?
        """,
        conn,
        params=(user_id,)
    )
    conn.close()
    return df


def update_expense(expense_id, amount, category, date, desc):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE expenses
    SET amount=?, category=?, description=?, date=?
    WHERE expense_id=?
    """, (amount, category, desc, date, expense_id))

    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
    conn.commit()
    conn.close()