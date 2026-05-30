import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from model import predict_category

# ==========================
# TITLE
# ==========================

st.title("💰 AI-Powered Personal Finance Tracker")

# ==========================
# ADD TRANSACTION
# ==========================

st.header("➕ Add Transaction")

date = st.date_input("Date")

transaction_type = st.selectbox(
    "Type",
    ["Income", "Expense"]
)

description = st.text_input(
    "Description"
)

predicted_category = "Other"

if description:
    predicted_category = predict_category(
        description
    )

st.write(
    f"🤖 Predicted Category: **{predicted_category}**"
)

amount = st.number_input(
    "Amount",
    min_value=0.0
)

# ==========================
# SAVE TRANSACTION
# ==========================

if st.button("Add Transaction"):

    new_transaction = pd.DataFrame({
        "Date": [date],
        "Type": [transaction_type],
        "Category": [predicted_category],
        "Amount": [amount],
        "Description": [description]
    })

    try:
        old_data = pd.read_csv(
            "transactions.csv"
        )
    except:
        old_data = pd.DataFrame(
            columns=[
                "Date",
                "Type",
                "Category",
                "Amount",
                "Description"
            ]
        )

    updated_data = pd.concat(
        [old_data, new_transaction],
        ignore_index=True
    )

    updated_data.to_csv(
        "transactions.csv",
        index=False
    )

    st.success(
        "✅ Transaction Saved!"
    )

# ==========================
# LOAD DATA
# ==========================

try:
    data = pd.read_csv(
        "transactions.csv"
    )
except:
    data = pd.DataFrame(
        columns=[
            "Date",
            "Type",
            "Category",
            "Amount",
            "Description"
        ]
    )

# ==========================
# DASHBOARD
# ==========================

income = data[
    data["Type"] == "Income"
]["Amount"].sum()

expense = data[
    data["Type"] == "Expense"
]["Amount"].sum()

savings = income - expense

st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Total Income",
        f"₹{income:.2f}"
    )

with col2:
    st.metric(
        "💸 Total Expense",
        f"₹{expense:.2f}"
    )

with col3:
    st.metric(
        "🏦 Savings",
        f"₹{savings:.2f}"
    )

# ==========================
# TRANSACTION HISTORY
# ==========================

st.header("📜 Transaction History")

st.dataframe(
    data,
    use_container_width=True
)

# ==========================
# DELETE TRANSACTION
# ==========================

st.subheader("🗑 Delete Transaction")

if not data.empty:

    transaction_index = st.selectbox(
        "Select Transaction",
        data.index
    )

    if st.button(
        "Delete Transaction"
    ):

        data = data.drop(
            transaction_index
        )

        data.to_csv(
            "transactions.csv",
            index=False
        )

        st.success(
            "Transaction Deleted!"
        )

        st.rerun()

# ==========================
# EXPORT CSV
# ==========================

st.subheader("📥 Export Report")

csv = data.to_csv(
    index=False
)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="finance_report.csv",
    mime="text/csv"
)

# ==========================
# PIE CHART
# ==========================

expense_data = data[
    data["Type"] == "Expense"
]

if not expense_data.empty:

    st.header(
        "📊 Expense Breakdown"
    )

    category_expense = (
        expense_data
        .groupby("Category")
        ["Amount"]
        .sum()
    )

    fig, ax = plt.subplots()

    ax.pie(
        category_expense,
        labels=category_expense.index,
        autopct="%1.1f%%"
    )

    ax.axis("equal")

    st.pyplot(fig)

# ==========================
# EXPENSE TREND
# ==========================

if not expense_data.empty:

    st.header(
        "📈 Expense Trend"
    )

    expense_data = expense_data.copy()

    expense_data["Date"] = pd.to_datetime(
        expense_data["Date"]
    )

    daily_expense = (
        expense_data
        .groupby("Date")
        ["Amount"]
        .sum()
    )

    fig, ax = plt.subplots()

    ax.plot(
        daily_expense.index,
        daily_expense.values,
        marker="o"
    )

    ax.set_title(
        "Expense Trend"
    )

    ax.set_xlabel(
        "Date"
    )

    ax.set_ylabel(
        "Amount (₹)"
    )

    st.pyplot(fig)

st.header("🎯 Monthly Budget Tracker")

budget = st.number_input(
    "Set Monthly Budget (₹)",
    min_value=0.0,
    value=10000.0
)

remaining = budget - expense

usage_percent = (
    (expense / budget) * 100
    if budget > 0
    else 0
)

st.progress(
    min(int(usage_percent), 100)
)

st.write(
    f"Budget Used: {usage_percent:.1f}%"
)

st.write(
    f"Remaining Budget: ₹{remaining:.2f}"
)

if usage_percent >= 90:
    st.warning(
        "⚠️ You have used more than 90% of your budget!"
    )

st.sidebar.title("💰 Finance Tracker")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Transaction"]
)