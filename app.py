import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    calculate_summary,
    category_summary,
    monthly_summary,
    search_expenses,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SmartExpense AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.main{
    padding-top:1rem;
}

.stMetric{
    border-radius:10px;
    padding:10px;
}

footer{
    visibility:hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("💰 SmartExpense AI")

st.caption(
    "AI-powered Personal Expense Analytics Dashboard"
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Upload Expense Dataset")

st.sidebar.info(
"""
Required CSV columns:

• Date
• Amount
• Category
• Description
"""
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"],
)

# --------------------------------------------------
# Wait for Upload
# --------------------------------------------------

if uploaded_file is None:

    st.info(
        "Upload a CSV file to begin."
    )

    st.stop()

# --------------------------------------------------
# Safe Data Loading
# --------------------------------------------------

try:

    df = load_data(uploaded_file)

except Exception as e:

    st.error(
        "Unable to load dataset."
    )

    st.exception(e)

    st.stop()

# --------------------------------------------------
# Empty Dataset Check
# --------------------------------------------------

if df.empty:

    st.warning(
        "Dataset contains no valid records."
    )

    st.stop()
# --------------------------------------------------
# Dashboard Summary
# --------------------------------------------------

try:

    summary = calculate_summary(df)

except Exception as e:

    st.error(
        "Unable to calculate dashboard summary."
    )

    st.exception(e)

    st.stop()

st.subheader("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Expenses",
        f"₹{summary['Total Expense']:,.2f}",
    )

with col2:

    st.metric(
        "Average Expense",
        f"₹{summary['Average Expense']:,.2f}",
    )

with col3:

    st.metric(
        "Highest Expense",
        f"₹{summary['Highest Expense']:,.2f}",
    )

with col4:

    st.metric(
        "Transactions",
        summary["Transactions"],
    )

st.divider()

# --------------------------------------------------
# Category Summary
# --------------------------------------------------

try:

    category_df = category_summary(df)

except Exception as e:

    st.error(
        "Unable to generate category summary."
    )

    st.exception(e)

    category_df = pd.DataFrame(
        columns=[
            "Category",
            "Amount",
        ]
    )

st.subheader("📂 Category Summary")

st.dataframe(
    category_df,
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# Quick Statistics
# --------------------------------------------------

st.subheader("📈 Expense Statistics")

left, right = st.columns(2)

with left:

    st.write(
        f"**Date Range:** "
        f"{df['Date'].min().date()} → "
        f"{df['Date'].max().date()}"
    )

    st.write(
        f"**Unique Categories:** "
        f"{df['Category'].nunique()}"
    )

with right:

    st.write(
        f"**Average Daily Expense:** "
        f"₹{df.groupby(df['Date'].dt.date)['Amount'].sum().mean():,.2f}"
    )

    st.write(
        f"**Largest Single Expense:** "
        f"₹{df['Amount'].max():,.2f}"
    )

st.divider()
# --------------------------------------------------
# Search Expenses
# --------------------------------------------------

st.subheader("🔍 Search Expenses")

search_text = st.text_input(
    "Search by Category or Description",
    placeholder="Example: Food, Travel, Electricity",
)

try:

    filtered_df = search_expenses(
        df,
        search_text,
    ).reset_index(drop=True)

except Exception as e:

    st.error(
        "Unable to search expenses."
    )

    st.exception(e)

    filtered_df = df.copy().reset_index(drop=True)

# --------------------------------------------------
# Search Results
# --------------------------------------------------

st.write(
    f"Showing **{len(filtered_df):,}** expense record(s)."
)

if filtered_df.empty:

    st.warning(
        "No matching expenses found."
    )

else:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

# --------------------------------------------------
# Download Filtered Dataset
# --------------------------------------------------

try:

    csv = filtered_df.to_csv(
        index=False,
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv,
        file_name="filtered_expenses.csv",
        mime="text/csv",
    )

except Exception as e:

    st.error(
        "Unable to prepare CSV download."
    )

    st.exception(e)

st.divider()

# --------------------------------------------------
# Top Expenses
# --------------------------------------------------

st.subheader("💸 Top Expenses")

top_expenses = (
    filtered_df
    .sort_values(
        by="Amount",
        ascending=False,
    )
    .head(10)
)

if top_expenses.empty:

    st.info(
        "No expenses available."
    )

else:

    st.dataframe(
        top_expenses,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------

st.subheader("📄 Dataset Preview")

preview_rows = st.slider(
    "Rows to Preview",
    min_value=5,
    max_value=50,
    value=10,
)

st.dataframe(
    filtered_df.head(preview_rows),
    use_container_width=True,
    hide_index=True,
)

st.divider()
# --------------------------------------------------
# Interactive Charts
# --------------------------------------------------

st.subheader("📊 Expense Analytics")

# --------------------------------------------------
# Category-wise Spending
# --------------------------------------------------

try:

    if not category_df.empty:

        fig = px.pie(
            category_df,
            names="Category",
            values="Amount",
            title="Category-wise Spending",
            hole=0.45,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate Category chart."
    )

    st.exception(e)

# --------------------------------------------------
# Monthly Expense Trend
# --------------------------------------------------

try:

    monthly_df = monthly_summary(df)

    if not monthly_df.empty:

        fig = px.bar(
            monthly_df,
            x="Month",
            y="Amount",
            title="Monthly Expenses",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate Monthly Expense chart."
    )

    st.exception(e)

# --------------------------------------------------
# Expense Distribution
# --------------------------------------------------

try:

    fig = px.histogram(
        filtered_df,
        x="Amount",
        nbins=20,
        title="Expense Distribution",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:

    st.error(
        "Unable to generate Expense Distribution."
    )

    st.exception(e)

# --------------------------------------------------
# Daily Spending Trend
# --------------------------------------------------

try:

    daily_df = (
        filtered_df
        .groupby(
            filtered_df["Date"].dt.date,
            as_index=False,
        )["Amount"]
        .sum()
    )

    daily_df.columns = [
        "Date",
        "Amount",
    ]

    if not daily_df.empty:

        fig = px.line(
            daily_df,
            x="Date",
            y="Amount",
            title="Daily Spending Trend",
            markers=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate Daily Spending Trend."
    )

    st.exception(e)

# --------------------------------------------------
# Top Spending Categories
# --------------------------------------------------

try:

    top_categories = (
        filtered_df
        .groupby(
            "Category",
            as_index=False,
        )["Amount"]
        .sum()
        .sort_values(
            by="Amount",
            ascending=False,
        )
        .head(10)
    )

    if not top_categories.empty:

        fig = px.bar(
            top_categories,
            x="Category",
            y="Amount",
            title="Top Spending Categories",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate Category Analysis."
    )

    st.exception(e)

# --------------------------------------------------
# Expense Timeline
# --------------------------------------------------

try:

    timeline_df = (
        filtered_df
        .sort_values("Date")
    )

    fig = px.scatter(
        timeline_df,
        x="Date",
        y="Amount",
        color="Category",
        hover_data=[
            "Description",
        ],
        title="Expense Timeline",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:

    st.error(
        "Unable to generate Expense Timeline."
    )

    st.exception(e)

st.divider()
# --------------------------------------------------
# Expense Insights
# --------------------------------------------------

st.subheader("🧾 Expense Details")

display_df = filtered_df.reset_index(drop=True)

if display_df.empty:

    st.info(
        "No expense records available."
    )

else:

    selected_index = st.selectbox(
        "Select Expense",
        options=range(len(display_df)),
        format_func=lambda x:
            f"{display_df.iloc[x]['Date'].date()} | "
            f"{display_df.iloc[x]['Category']} | "
            f"₹{display_df.iloc[x]['Amount']:,.2f}",
    )

    expense = display_df.iloc[selected_index]

    col1, col2 = st.columns(2)

    with col1:

        st.write("### Expense Information")

        st.write(
            f"**Date:** {expense['Date'].date()}"
        )

        st.write(
            f"**Category:** {expense['Category']}"
        )

        st.write(
            f"**Amount:** ₹{expense['Amount']:,.2f}"
        )

        st.write(
            f"**Description:** {expense['Description']}"
        )

    with col2:

        st.write("### Expense Assessment")

        average = display_df["Amount"].mean()

        if expense["Amount"] >= average * 2:

            st.error(
                "This expense is significantly higher than your average spending."
            )

        elif expense["Amount"] >= average:

            st.warning(
                "This expense is above your average spending."
            )

        else:

            st.success(
                "This expense is below your average spending."
            )

        category_total = display_df[
            display_df["Category"] == expense["Category"]
        ]["Amount"].sum()

        st.write(
            f"**Total spent in this category:** ₹{category_total:,.2f}"
        )

st.divider()

# --------------------------------------------------
# Highest Spending Categories
# --------------------------------------------------

st.subheader("🏆 Highest Spending Categories")

top_categories = (
    display_df.groupby(
        "Category",
        as_index=False,
    )["Amount"]
    .sum()
    .sort_values(
        by="Amount",
        ascending=False,
    )
)

st.dataframe(
    top_categories,
    use_container_width=True,
    hide_index=True,
)

st.divider()
# --------------------------------------------------
# Dataset Health Report
# --------------------------------------------------

st.subheader("🩺 Dataset Health Report")

total_records = len(df)

missing_values = int(df.isna().sum().sum())

duplicate_rows = int(df.duplicated().sum())

invalid_amounts = int((df["Amount"] < 0).sum())

invalid_dates = int(df["Date"].isna().sum())

health_score = max(
    0,
    100
    - (
        missing_values
        + duplicate_rows
        + invalid_amounts
        + invalid_dates
    ),
)

health_score = min(100, health_score)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Records",
        total_records,
    )

    st.metric(
        "Missing Values",
        missing_values,
    )

with col2:

    st.metric(
        "Duplicate Rows",
        duplicate_rows,
    )

    st.metric(
        "Invalid Amounts",
        invalid_amounts,
    )

with col3:

    st.metric(
        "Invalid Dates",
        invalid_dates,
    )

    st.metric(
        "Dataset Quality",
        f"{health_score}%",
    )

st.divider()

# --------------------------------------------------
# Dataset Summary
# --------------------------------------------------

st.subheader("📋 Dataset Summary")

summary_df = pd.DataFrame(
    {
        "Metric": [
            "Rows",
            "Columns",
            "Categories",
            "Total Expenses",
            "Average Expense",
            "Largest Expense",
        ],
        "Value": [
            len(df),
            len(df.columns),
            df["Category"].nunique(),
            f"₹{df['Amount'].sum():,.2f}",
            f"₹{df['Amount'].mean():,.2f}",
            f"₹{df['Amount'].max():,.2f}",
        ],
    }
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "SmartExpense AI • Built with Streamlit, Pandas and Plotly"
)

















