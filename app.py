import streamlit as st
import pandas as pd
import plotly.express as px
import time

from database import create_tables, get_connection
from auth import register_user, login_user
from expenses import add_expense, get_expenses

st.set_page_config(page_title="Smart Expense Tracker", layout="wide")
create_tables()

# ---------------- SESSION ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- STYLES ----------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #0b1a2a;
    padding-top: 40px;
}
div[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #cbd5e1 !important;
    text-align: left !important;
    padding: 14px 20px !important;
    font-size: 18px !important;
}
div[data-testid="stSidebar"] button:hover {
    background-color: #1e293b !important;
    color: white !important;
}
.section-box {
    background: #111827;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 30px;
}
.kpi-card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}
.kpi-title {
    font-size: 14px;
    color: #9ca3af;
}
.kpi-value {
    font-size: 28px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Expense Tracker")

# ---------------- ANIMATION FUNCTION ----------------
def animated_card(title, value, color):
    placeholder = st.empty()
    steps = 40

    for i in range(steps + 1):
        animated_value = value * (i / steps)
        placeholder.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value" style="color:{color}">
                ₹ {animated_value:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.01)

# ---------------- BUDGET FUNCTIONS ----------------
def set_monthly_budget(user_id, month, budget):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO monthly_budgets (user_id, month, budget)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, month)
    DO UPDATE SET budget=excluded.budget
    """, (user_id, month, budget))
    conn.commit()
    conn.close()

def get_monthly_budget(user_id, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT budget FROM monthly_budgets
    WHERE user_id=? AND month=?
    """, (user_id, month))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

# ---------------- AUTH ----------------
if st.session_state.user_id is None:

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
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
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

# ---------------- MAIN APP ----------------
else:

    if st.sidebar.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.sidebar.button("📋 Manage", use_container_width=True):
        st.session_state.page = "Manage"

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.rerun()

    df = get_expenses(st.session_state.user_id)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    # ================= DASHBOARD =================
    if st.session_state.page == "Dashboard":

        if df.empty:
            st.info("No expenses yet.")
        else:

            # -------- UPDATED MONTH DROPDOWN --------
            month_values = sorted(df["date"].dt.strftime("%Y-%m").unique())
            month_display = [
                pd.to_datetime(m).strftime("%B %Y") for m in month_values
            ]

            current_month = pd.Timestamp.today().strftime("%Y-%m")

            if current_month in month_values:
                default_index = month_values.index(current_month)
            else:
                default_index = len(month_values) - 1

            selected_display = st.selectbox(
                "Select Month",
                month_display,
                index=default_index
            )

            selected_month = month_values[
                month_display.index(selected_display)
            ]

            # -------- FILTER --------
            filtered_df = df[
                df["date"].dt.strftime("%Y-%m") == selected_month
            ]

            current_budget = get_monthly_budget(
                st.session_state.user_id,
                selected_month
            )

            total_spent = filtered_df["amount"].sum()
            remaining = (current_budget - total_spent) if current_budget else 0
            percent_used = ((total_spent / current_budget) * 100) if current_budget else 0

            # -------- SECTION 1 --------
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("📈 Monthly Budget Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                animated_card("Monthly Budget",
                              current_budget if current_budget else 0,
                              "#3b82f6")

            with col2:
                animated_card("Total Spent",
                              total_spent,
                              "#f59e0b")

            with col3:
                color = "#10b981" if remaining >= 0 else "#ef4444"
                animated_card("Remaining",
                              remaining,
                              color)

            if current_budget:
                st.progress(min(percent_used / 100, 1.0))
                st.write(f"**{percent_used:.1f}% of budget used**")

            st.markdown('</div>', unsafe_allow_html=True)

            # -------- SECTION 2 --------
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("📊 Detailed Analytics")

            col1, col2 = st.columns(2)

            col1.plotly_chart(
                px.pie(filtered_df,
                       values="amount",
                       names="category",
                       title="Spending by Category"),
                use_container_width=True
            )

            col2.plotly_chart(
                px.bar(filtered_df.groupby("category")["amount"].sum().reset_index(),
                       x="category",
                       y="amount",
                       title="Category Totals"),
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            col1.plotly_chart(
                px.area(filtered_df.groupby(
                    filtered_df["date"].dt.date)["amount"].sum().reset_index(),
                        x="date",
                        y="amount",
                        title="Daily Trend"),
                use_container_width=True
            )

            col2.plotly_chart(
                px.bar(filtered_df.sort_values(
                    "amount", ascending=False).head(5),
                       x="amount",
                       y="description",
                       orientation="h",
                       title="Top 5 Expenses"),
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # -------- OVERALL MONTHLY TREND --------
            st.subheader("📉 Overall Monthly Spending Trend")

            monthly_all = df.groupby(
                df["date"].dt.to_period("M")
            )["amount"].sum()

            st.plotly_chart(
                px.line(x=monthly_all.index.astype(str),
                        y=monthly_all.values,
                        markers=True,
                        title="Monthly Spending (All Months)"),
                use_container_width=True
            )

    # ================= MANAGE =================
    if st.session_state.page == "Manage":

        st.header("📋 Manage")

        st.subheader("➕ Add Expense")

        col1, col2, col3 = st.columns(3)

        with col1:
            amount = st.number_input("Amount", min_value=0.0)
        with col2:
            category = st.selectbox(
                "Category",
                ["Food", "Travel", "Rent", "Shopping", "Other"]
            )
        with col3:
            date = st.date_input("Date")

        desc = st.text_input("Description")

        if st.button("Add Expense"):
            formatted_date = date.strftime("%Y-%m-%d")
            add_expense(
                st.session_state.user_id,
                amount,
                category,
                formatted_date,
                desc
            )
            st.success("Expense added!")
            st.rerun()

        st.markdown("---")

        st.subheader("💳 Manage Monthly Budgets")

        month_options = sorted(df["date"].dt.strftime("%Y-%m").unique()) if not df.empty else [pd.Timestamp.today().strftime("%Y-%m")]

        selected_budget_month = st.selectbox(
            "Select Month to Edit Budget",
            month_options
        )

        existing_budget = get_monthly_budget(
            st.session_state.user_id,
            selected_budget_month
        )

        budget_input = st.number_input(
            "Monthly Budget",
            min_value=0.0,
            value=float(existing_budget) if existing_budget else 0.0
        )

        if st.button("Save / Update Budget"):
            set_monthly_budget(
                st.session_state.user_id,
                selected_budget_month,
                budget_input
            )
            st.success(f"Budget updated for {selected_budget_month}!")
            st.rerun()

        st.markdown("---")

        st.subheader("📑 Expense Records")

        if not df.empty:
            st.dataframe(
                df.drop(columns=["expense_id"]),
                use_container_width=True
            )
        else:
            st.info("No records yet.")