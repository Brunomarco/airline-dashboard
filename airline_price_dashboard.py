
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_names = excel_file.sheet_names
    sheet = st.selectbox("Select a sheet", sheet_names)
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # Preprocess the data
    df = df[['Origin Airport', 'Destination Airport', 'Airline', 'Min Charge2']]
    df = df.rename(columns={
        'Origin Airport': 'Origin',
        'Destination Airport': 'Destination',
        'Min Charge2': 'Price'
    })
    df = df.dropna(subset=['Price'])
    df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)

    # Dropdowns for filtering
    origins = sorted(df['Origin'].dropna().unique())
    selected_origin = st.selectbox("Select Origin Airport", origins)

    destinations = sorted(df[df['Origin'] == selected_origin]['Destination'].dropna().unique())
    selected_destination = st.selectbox("Select Destination Airport", destinations)

    # Filtered data
    filtered_df = df[(df['Origin'] == selected_origin) & (df['Destination'] == selected_destination)]

    if not filtered_df.empty and len(filtered_df) > 1:
        # Classification
        percentiles = filtered_df['Price'].rank(pct=True)
        filtered_df['Rating'] = percentiles.apply(
            lambda p: 'Green' if p <= 0.2 else 'Orange' if p <= 0.7 else 'Red'
        )

        color_map = {'Green': 'green', 'Orange': 'orange', 'Red': 'red'}
        filtered_df = filtered_df.sort_values('Price')

        # Plot
        st.subheader(f"Flight Prices: {selected_origin} → {selected_destination}")
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = sns.barplot(
            data=filtered_df,
            x='Airline',
            y='Price',
            palette=[color_map[c] for c in filtered_df['Rating']]
        )
        ax.set_ylabel("Price (USD)")
        ax.set_xlabel("Airline")
        ax.set_title(f"Airline Price Comparison: {selected_origin} → {selected_destination}")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Not enough data for selected route.")
