import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Student Budget Tracker")

file = st.file_uploader("Upload your transactions CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.dataframe(df)

    by_cat = df.groupby("category")["amount"].sum().reset_index()
    st.plotly_chart(px.pie(by_cat, names="category", values="amount"))

    df["date"] = pd.to_datetime(df["date"])
    by_day = df.groupby("date")["amount"].sum().reset_index()
    fig = px.line(by_day, x="date", y="amount", title="Spending Over Time")
    st.plotly_chart(fig)

    total = df["amount"].sum()
    top = by_cat.sort_values("amount", ascending=False).iloc[0]
    share = top["amount"] / total * 100
    st.info(f"{top['category']} is your biggest category: {share:.0f}% of your spending.")

    # NEW: month over month
    df["month"] = df["date"].dt.to_period("M").astype(str)
    by_month = df.groupby("month")["amount"].sum()

    if len(by_month) >= 2:
        last = by_month.iloc[-1]
        prev = by_month.iloc[-2]
        change = (last - prev) / prev * 100
        if change > 0:
            st.warning(f"Spending went UP {change:.0f}% compared to last month.")
        else:
            st.success(f"Spending went DOWN {abs(change):.0f}% compared to last month.")