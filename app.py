# app.py

import streamlit as st
import pandas as pd

# --- Page Setup ---
# The st.set_page_config command should be the first Streamlit command in your script.
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide"
)

# --- Data Loading ---
# We use a caching decorator to load the data only once, which improves performance.
@st.cache_data
def load_data(path):
    """
    Loads the vehicle registration data from a CSV file.
    """
    df = pd.read_csv(path)
    # Convert 'Date' column to datetime objects for proper filtering and plotting
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Load the data
df = load_data('data.csv')


# --- Main Dashboard ---
st.title("Vehicle Registrations Dashboard")

st.markdown("This dashboard provides an investor-focused view of vehicle registration data.")

# Display a sample of the data to verify it's loaded correctly.
st.subheader("Raw Data Sample")
st.dataframe(df.head())