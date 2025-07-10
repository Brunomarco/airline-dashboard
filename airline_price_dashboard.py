import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Airline Pricing Dashboard")

# ✅ Load Excel from local file (uploaded into GitHub repo)
df = pd.read_excel("Marken RFP Airline Bids Consolidated.xlsx", sheet_name="Airline Bids", engine="openpyxl")

# ✅ Clean and prepare
df = df[['Origin Airport', 'Destination Airport', 'Airline', 'Min Charge2']].dropna()
df = df.rename(columns={
    'Origin Airport': 'Origin',
    'Destination Airport': 'Destination',
    'Min Charge2': 'Price'
})
df['Price'] = df['Price'].astype(float)

# ✅ Sidebar filters
origins = df['Origin'].unique()
destinations = df['Destination'].unique()

selected_origin = st.sidebar.selectbox("Select Origin", sorted(origins))
filtered_dest = df[df['Origin'] == selected_origin]['Destination'].unique()
selected_destination = st.sidebar.selectbox("Select Destination", sorted(filtered_dest))

# ✅ Filtered data
route_df = df[(df['Origin'] == selected_origin) & (df['Destination'] == selected_destination)]

if not route_df.empty:
    # Classify into percentiles
    percentiles = route_df['Price'].rank(pct=True)
    route_df['Percentile'] = percentiles
    route_df['Color'] = percentiles.apply(lambda p: 'green' if p <= 0.2 else 'orange' if p <= 0.7 else 'red')

    st.write(f"### Prices from {selected_origin} to {selected_destination}")
    st.dataframe(route_df)

    # Plot
    plt.figure(figsize=(10, 5))
    bar_colors = route_df.sort_values('Price')['Color'].tolist()
    sns.barplot(data=route_df.sort_values('Price'), x='Airline', y='Price', palette=bar_colors)
    plt.title(f"Airline Prices: {selected_origin} → {selected_destination}")
    plt.xticks(rotation=45)
    plt.ylabel("Price (USD)")
    plt.xlabel("Airline")
    st.pyplot(plt.gcf())
else:
    st.warning("No data available for this route.")
