import pandas as pd


def load_data(uploaded_file):
    """Load expense data from a CSV file."""
    return pd.read_csv(uploaded_file, parse_dates=["Date"])


def calculate_summary(df):
    """Calculate total expenses and transaction statistics."""

    total_expense = df["Amount"].sum()
    average_expense = df["Amount"].mean()
    highest_expense = df["Amount"].max()
    transaction_count = len(df)

    return {
        "Total Expense": total_expense,
        "Average Expense": average_expense,
        "Highest Expense": highest_expense,
        "Transactions": transaction_count,
    }


def category_summary(df):
    """Summarize expenses by category."""

    return (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def monthly_summary(df):
    """Summarize expenses by month."""

    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return (
        df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )


def search_expenses(df, keyword):
    """Filter expenses by category or description."""

    if not keyword:
        return df

    keyword = keyword.lower()

    return df[
        df["Category"].astype(str).str.lower().str.contains(keyword)
        | df["Description"].astype(str).str.lower().str.contains(keyword)
    ]
