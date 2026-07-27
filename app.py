import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    calculate_summary,
    category_summary,
    monthly_summary,
    search_expenses,
)

st.set_page_config(
    page_title="SmartExpense AI",
    page_icon="💸",
    layout="wide",
)

st.title("💸 SmartExpense AI")
st.caption("AI-Powered Personal Expense Tracker")

uploaded_file = st.file_uploader(
    "Upload your expense CSV file",
    type=["csv"],
)

if uploaded_file:

    df = load_data(uploaded_file)

    st.subheader("Expense Data")
    st.dataframe(df, use_container_width=True)

    st.divider()

    summary = calculate_summary(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Expense",
        f"₹{summary['Total Expense']:,.2f}",
    )

    col2.metric(
        "Average Expense",
        f"₹{summary['Average Expense']:,.2f}",
    )

    col3.metric(
        "Highest Expense",
        f"₹{summary['Highest Expense']:,.2f}",
    )

    col4.metric(
        "Transactions",
        summary["Transactions"],
    )

    st.divider()

    st.subheader("Search Expenses")

    keyword = st.text_input(
        "Search by category or description"
    )

    filtered = search_expenses(df, keyword)

    st.dataframe(filtered, use_container_width=True)

    st.divider()

    st.subheader("Expense by Category")

    category = category_summary(filtered)

    pie = px.pie(
        category,
        names="Category",
        values="Amount",
        hole=0.4,
    )

    st.plotly_chart(
        pie,
        use_container_width=True,
    )

    st.subheader("Monthly Expenses")

    monthly = monthly_summary(filtered)

    bar = px.bar(
        monthly,
        x="Month",
        y="Amount",
    )

    st.plotly_chart(
        bar,
        use_container_width=True,
    )

    st.subheader("Download Filtered Data")

    st.download_button(
        "Download CSV",
        filtered.to_csv(index=False),
        file_name="filtered_expenses.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to begin.")
