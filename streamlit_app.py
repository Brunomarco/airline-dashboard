import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Airline Pricing Dashboard")

# Load Excel file from GitHub using requests
url = "https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/raw/main/Marken%20RFP%20Airline%20Bids%20Consolidated.xlsx"
response = requests.get(url)
xls = pd.ExcelFile(BytesIO(response.content))

# Load sheet
df = xls.parse("Airline Bids")

# Preprocess
df = df[['Origin Airport', 'Destination Airport', 'Airline', 'Min Charge2']].dropna()
df.rename(columns={
    'Origin Airport': 'Origin',
    'Destination Airport': 'Destination',
    'Min Charge2': 'Price'
}, inplace=True)

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df = df.dropna(subset=['Price'])

# Filters
origin = st.selectbox("Select Origin", df['Origin'].unique())
destination = st.selectbox("Select Destination", df[df['Origin'] == origin]['Destination'].unique())

# Filtered data
filtered = df[(df['Origin'] == origin) & (df['Destination'] == destination)]

if len(filtered) > 0:
    # Percentile-based color classification
    percentiles = filtered['Price'].rank(pct=True)
    filtered['Color'] = percentiles.apply(lambda x: 'Green' if x <= 0.2 else 'Orange' if x <= 0.7 else 'Red')

    # Color map
    color_map = {'Green': 'green', 'Orange': 'orange', 'Red': 'red'}
    bar_colors = filtered['Color'].map(color_map)

    # Plot
    plt.figure(figsize=(10,6))
    sns.barplot(data=filtered, x='Airline', y='Price', palette=bar_colors)
    plt.title(f"{origin} → {destination} Price Comparison")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    st.pyplot(plt)
else:
    st.write("No data available for selected route.")
