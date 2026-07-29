import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Date",
    "Amount",
    "Category",
    "Description",
]


def load_data(uploaded_file):
    """
    Safely load and validate expense data.
    """

    if uploaded_file is None:
        raise ValueError(
            "No CSV file uploaded."
        )

    try:

        df = pd.read_csv(uploaded_file)

    except Exception as e:

        raise ValueError(
            f"Unable to read CSV: {e}"
        )

    if df.empty:

        raise ValueError(
            "Uploaded CSV is empty."
        )

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce",
    )

    df["Category"] = (
        df["Category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["Description"] = (
        df["Description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df = df.dropna(
        subset=[
            "Date",
            "Amount",
        ]
    )

    df["Amount"] = df["Amount"].clip(
        lower=0
    )

    df = df.reset_index(
        drop=True
    )

    return df


def calculate_summary(df):
    """
    Safely calculate dashboard summary.
    """

    if df.empty:

        return {
            "Total Expense": 0.0,
            "Average Expense": 0.0,
            "Highest Expense": 0.0,
            "Transactions": 0,
        }

    return {

        "Total Expense":
            float(df["Amount"].sum()),

        "Average Expense":
            float(df["Amount"].mean()),

        "Highest Expense":
            float(df["Amount"].max()),

        "Transactions":
            int(len(df)),
    }


def category_summary(df):
    """
    Expense totals by category.
    """

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Category",
                "Amount",
            ]
        )

    return (

        df.groupby(
            "Category",
            dropna=False,
        )["Amount"]

        .sum()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )


def monthly_summary(df):
    """
    Monthly expense totals.
    """

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Month",
                "Amount",
            ]
        )

    temp = df.copy()

    temp["Month"] = (

        temp["Date"]

        .dt.to_period("M")

        .astype(str)

    )

    return (

        temp.groupby(
            "Month",
            as_index=False,
        )["Amount"]

        .sum()

        .sort_values(
            "Month"
        )

    )


def search_expenses(df, keyword):
    """
    Safe category/description search.
    """

    if df.empty:

        return df

    if keyword is None:

        return df

    keyword = str(keyword).strip()

    if keyword == "":

        return df

    keyword = keyword.lower()

    category = (

        df["Category"]

        .fillna("")

        .astype(str)

        .str.lower()

    )

    description = (

        df["Description"]

        .fillna("")

        .astype(str)

        .str.lower()

    )

    return df[

        category.str.contains(
            keyword,
            regex=False,
            na=False,
        )

        |

        description.str.contains(
            keyword,
            regex=False,
            na=False,
        )

    ]
