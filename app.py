import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("data.csv")

st.title("📊 Student Performance Analytics Dashboard")
st.write("This dashboard identifies at-risk students based on marks, attendance, and LMS logins.")

# Calculate Risk Score
df["RiskScore"] = (100 - df["Marks"])*0.4 + (100 - df["Attendance"])*0.4 + (50 - df["Logins"])*0.2

# Categorize Students
df["Status"] = df["RiskScore"].apply(lambda x: "High Risk" if x > 40 else ("Moderate Risk" if x > 25 else "Low Risk"))


# =======================
# Section 1: Dataset View
# =======================
st.header("📁 Student Dataset")
st.dataframe(df)


# =======================
# Section 2: Bar Charts
# =======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Marks Comparison")
    fig1 = px.bar(df, x="Name", y="Marks", color="Status", title="Marks of Students")
    st.plotly_chart(fig1)

with col2:
    st.subheader("Attendance Comparison")
    fig2 = px.bar(df, x="Name", y="Attendance", color="Status", title="Attendance % of Students")
    st.plotly_chart(fig2)


# =======================
# Section 3: Correlation Heatmap
# =======================
st.header("📌 Correlation Heatmap")
corr = df[["Marks", "Attendance", "Logins"]].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Between Marks, Attendance & Logins"
)
st.plotly_chart(fig_corr)


# =======================
# Section 4: Scatter Plot (Absentee Impact)
# =======================
st.header("📉 Absenteeism Impact on Marks")
fig_scatter = px.scatter(
    df,
    x="Attendance",
    y="Marks",
    color="Status",
    size="Logins",
    title="Impact of Attendance on Academic Performance"
)
st.plotly_chart(fig_scatter)


# =======================
# Section 5: At-Risk Students
# =======================
st.header("⚠️ At-Risk Students")

risk_students = df[df["Status"] == "High Risk"]

if len(risk_students) > 0:
    st.error("These students need immediate academic intervention.")
    st.dataframe(risk_students)
else:
    st.success("No high-risk students detected.")
