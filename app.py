import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the stock data CSV file
csv_file_path = "stock_data.csv"
df = pd.read_csv(csv_file_path)

# Convert 'Timestamp' to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Convert price and volume columns to numeric
df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values
df.dropna(inplace=True)

# Sort data by timestamp
df.sort_values(by='Timestamp', inplace=True)

# Streamlit UI
st.set_page_config(page_title="Stock Data Analysis", layout="wide")
st.title("📈 Stock Data Analysis App")
st.sidebar.header("Filter Options")

# Date range filter
date_range = st.sidebar.date_input("Select Date Range", [df['Timestamp'].min().date(), df['Timestamp'].max().date()])
filtered_df = df[(df['Timestamp'].dt.date >= date_range[0]) & (df['Timestamp'].dt.date <= date_range[1])]

# Display data
tab1, tab2 = st.tabs(["📊 Charts", "📄 Raw Data"])

with tab1:
    st.subheader("Stock Price Trends")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(filtered_df['Timestamp'], filtered_df['Close'], marker='o', linestyle='-', color='b', label='Close Price')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Closing Price")
    ax.set_title("Stock Closing Price Over Time")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Trading Volume")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(filtered_df['Timestamp'], filtered_df['Volume'], color='g', label='Volume Traded')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Volume")
    ax.set_title("Stock Trading Volume Over Time")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    st.subheader("Raw Stock Data")
    st.dataframe(filtered_df, use_container_width=True)

st.success("Analysis Complete! Use the filters to adjust the view.")

