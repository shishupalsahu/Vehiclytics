# app.py (Corrected)

import streamlit as st
import pandas as pd
from datetime import timedelta

# --- Page Setup ---
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    # Add Year and Quarter columns for easy filtering and calculations
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q')
    return df

df = load_data('data.csv')

# --- Main Dashboard ---
st.title("Vehicle Registrations Dashboard")

# --- Sidebar for Filters ---
st.sidebar.header("Filters")

# Date Range Selection
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date, end_date = date_range

# Vehicle Category Selection
category_options = ['All'] + sorted(df['Category'].unique().tolist())
category = st.sidebar.selectbox(
    "Select Vehicle Category",
    options=category_options
)

# Manufacturer Selection
manufacturer_options = ['All'] + sorted(df['Manufacturer'].unique().tolist())
manufacturer = st.sidebar.selectbox(
    "Select Manufacturer",
    options=manufacturer_options
)


# --- Filtering Data ---
# Start with the full dataframe and apply filters sequentially
filtered_df = df.copy()

# Apply date filter
if start_date and end_date:
    filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)]

# Apply category filter
if category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == category]

# Apply manufacturer filter
if manufacturer != 'All':
    filtered_df = filtered_df[filtered_df['Manufacturer'] == manufacturer]


# --- Metric Calculations ---
def calculate_growth(current_period_sum, previous_period_sum):
    if previous_period_sum is None or previous_period_sum == 0:
        return None
    return ((current_period_sum - previous_period_sum) / previous_period_sum) * 100

# YoY Calculation
previous_year_start = start_date.replace(year=start_date.year - 1)
previous_year_end = end_date.replace(year=end_date.year - 1)

current_period_regs = filtered_df['Registrations'].sum()

# Filter for the previous year's data using the original dataframe
previous_year_df = df[
    (df['Date'].dt.date >= previous_year_start) & (df['Date'].dt.date <= previous_year_end)
]
# Apply the same category/manufacturer filters to the comparison period
if category != 'All':
    previous_year_df = previous_year_df[previous_year_df['Category'] == category]
if manufacturer != 'All':
    previous_year_df = previous_year_df[previous_year_df['Manufacturer'] == manufacturer]
    
previous_year_regs = previous_year_df['Registrations'].sum()
yoy_growth = calculate_growth(current_period_regs, previous_year_regs)

# QoQ Calculation (Comparing the last quarter of the selection to the one before it)
if not filtered_df.empty:
    last_quarter = filtered_df['Date'].dt.to_period('Q').max()
    current_quarter_regs = filtered_df[filtered_df['Date'].dt.to_period('Q') == last_quarter]['Registrations'].sum()
    
    previous_quarter = last_quarter - 1
    previous_quarter_df = df[df['Date'].dt.to_period('Q') == previous_quarter]
    if category != 'All':
        previous_quarter_df = previous_quarter_df[previous_quarter_df['Category'] == category]
    if manufacturer != 'All':
        previous_quarter_df = previous_quarter_df[previous_quarter_df['Manufacturer'] == manufacturer]

    previous_quarter_regs = previous_quarter_df['Registrations'].sum()
    qoq_growth = calculate_growth(current_quarter_regs, previous_quarter_regs)
else:
    qoq_growth = None


# --- Display Metrics ---
col1, col2 = st.columns(2)

with col1:
    if yoy_growth is not None:
        # CORRECTED VARIABLE NAME
        st.metric(label="YoY Growth", value=f"{yoy_growth:.1f}%", delta=f"{yoy_growth:.1f}%")
    else:
        st.metric(label="YoY Growth", value="N/A")

with col2:
    if qoq_growth is not None:
        # CORRECTED VARIABLE NAME
        st.metric(label="QoQ Growth", value=f"{qoq_growth:.1f}%", delta=f"{qoq_growth:.1f}%")
    else:
        st.metric(label="QoQ Growth", value="N/A")


# We will hide the raw data table in the next step, but leave it for now for verification.
st.subheader("Filtered Data Sample")
st.dataframe(filtered_df)