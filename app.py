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