import streamlit as st
import pandas as pd

# Title
st.title("Airline Pricing Dashboard")

# Load Excel
url = "https://raw.githubusercontent.com/Brunomarco/airline-dashboard/main/arken RFP Airline Bids Consolidated.xlsx"
df = pd.read_excel(url, sheet_name="Airline Bids")

# Filter columns
df = df[["Origin Airport", "Destination Airport", "Airline", "Min Charge2", "Percentage", "Colour"]]
df.dropna(subset=["Min Charge2"], inplace=True)

# Convert price to float
df["Price"] = df["Min Charge2"].replace('[\$,]', '', regex=True).astype(float)

# Sidebar filters
origin = st.sidebar.selectbox("Select Origin", sorted(df["Origin Airport"].unique()))
destination = st.sidebar.selectbox("Select Destination", sorted(df[df["Origin Airport"] == origin]["Destination Airport"].unique()))

# Filter by route
filtered_df = df[(df["Origin Airport"] == origin) & (df["Destination Airport"] == destination)]

# Show data
st.write(f"### Airlines flying from {origin} to {destination}")
st.dataframe(filtered_df[["Airline", "Price", "Colour", "Percentage"]])

# Bar chart
color_map = {"Green": "green", "Orange": "orange", "Red": "red"}
bar_colors = filtered_df["Colour"].map(color_map)

st.bar_chart(
    data=filtered_df.set_index("Airline")["Price"],
    use_container_width=True
)
