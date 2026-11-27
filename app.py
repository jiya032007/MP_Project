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
    st.plotly_chart(px.pie(by_cat, names="category", values="amount",
                       color_discrete_sequence=px.colors.sequential.RdPu))

    df["date"] = pd.to_datetime(df["date"])
    by_day = df.groupby("date")["amount"].sum().reset_index()
    fig = px.line(by_day, x="date", y="amount", title="Spending Over Time")
    st.plotly_chart(fig)

    total = df["amount"].sum()
    top = by_cat.sort_values("amount", ascending=False).iloc[0]
    share = top["amount"] / total * 100
    st.info(f"{top['category']} is your biggest category: {share:.0f}% of your spending.")