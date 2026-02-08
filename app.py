import streamlit as st
import pandas as pd
import plotly.express as px

from database import create_tables
from auth import register_user, login_user
from expenses import add_expense, get_expenses
from analytics import spending_insights

st.set_page_config(page_title="Smart Expense Tracker", layout="wide")
create_tables()

# Session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------- AUTH ----------
st.title("💰 Smart Expense Tracker")

if st.session_state.user_id is None:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.rerun()

            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

# ---------- MAIN APP ----------
else:
    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.rerun()


    st.header("➕ Add Expense")
    col1, col2, col3 = st.columns(3)

    with col1:
        amount = st.number_input("Amount", min_value=0.0)
    with col2:
        category = st.selectbox("Category", ["Food", "Travel", "Rent", "Shopping", "Other"])
    with col3:
        date = st.date_input("Date")

    desc = st.text_input("Description")

    if st.button("Add Expense"):
        add_expense(st.session_state.user_id, amount, category, str(date), desc)
        st.success("Expense added!")

    # ---------- DASHBOARD ----------
    st.header("📊 Analytics Dashboard")
    df = get_expenses(st.session_state.user_id)

    if df.empty:
        st.info("No expenses yet")
    else:
        df["date"] = pd.to_datetime(df["date"])

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.pie(
                df,
                values="amount",
                names="category",
                title="Spending by Category"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
            monthly.index = monthly.index.astype(str)
            st.line_chart(monthly)

        # ---------- INSIGHTS ----------
        st.header("🧠 Smart Insights")
        insights = spending_insights(df)
        for i in insights:
            st.write(i)
