
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("media_data_processed.csv")
df['Date'] = pd.to_datetime(df['Date'])

st.title("📊 Marketing Performance Dashboard")

# Filters
vendor = st.selectbox("Select Vendor", options=df['Vendor'].unique())
campaign = st.selectbox("Select Campaign", options=df['Campaign'].unique())
date_range = st.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

# Filter data
mask = (
    (df['Vendor'] == vendor) &
    (df['Campaign'] == campaign) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
)
filtered_df = df[mask]

# KPIs
st.subheader("Key Performance Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("CTR", f"{filtered_df['CTR'].mean():.2%}")
col2.metric("CPC", f"${filtered_df['CPC'].mean():.2f}")
col3.metric("CPA", f"${filtered_df['CPA'].mean():.2f}")

# Time series chart
fig = px.line(filtered_df, x='Date', y='Conversions', title='Conversions Over Time')
st.plotly_chart(fig, use_container_width=True)

# Metric comparison
st.subheader("Campaign Performance Breakdown")
st.dataframe(filtered_df[['Date', 'Impressions', 'Clicks', 'Spend', 'Conversions', 'CTR', 'CPC', 'CPA']])
