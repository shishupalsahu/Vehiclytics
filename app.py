import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

#  Page Setup 
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Data Loading 
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q')
    return df

df = load_data('data.csv')

#  Main Dashboard 
st.title("Vehicle Registrations Dashboard")

#   Sidebar for Filters  
st.sidebar.header("Filters")

# Date Range Selection
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()), 
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

#   Filtering Data  
filtered_df = df.copy()

if start_date and end_date:
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)
    ]

if category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == category]

if manufacturer != 'All':
    filtered_df = filtered_df[filtered_df['Manufacturer'] == manufacturer]

#   Metric Calculations  
def calculate_growth(current_period_sum, previous_period_sum):
    if previous_period_sum is None or previous_period_sum == 0:
        return None
    return ((current_period_sum - previous_period_sum) / previous_period_sum) * 100

# YoY Calculation
previous_year_start = start_date.replace(year=start_date.year - 1)
previous_year_end = end_date.replace(year=end_date.year - 1)
current_period_regs = filtered_df['Registrations'].sum()

previous_year_df = df[
    (df['Date'].dt.date >= previous_year_start) & (df['Date'].dt.date <= previous_year_end)
]
if category != 'All':
    previous_year_df = previous_year_df[previous_year_df['Category'] == category]
if manufacturer != 'All':
    previous_year_df = previous_year_df[previous_year_df['Manufacturer'] == manufacturer]

previous_year_regs = previous_year_df['Registrations'].sum()
yoy_growth = calculate_growth(current_period_regs, previous_year_regs)

# QoQ Calculation
if not filtered_df.empty:
    last_quarter_of_selection = pd.to_datetime(end_date).to_period('Q')
    current_quarter_regs = filtered_df[filtered_df['Date'].dt.to_period('Q') == last_quarter_of_selection]['Registrations'].sum()

    previous_quarter = last_quarter_of_selection - 1
    previous_quarter_df = df[df['Date'].dt.to_period('Q') == previous_quarter]
    if category != 'All':
        previous_quarter_df = previous_quarter_df[previous_quarter_df['Category'] == category]
    if manufacturer != 'All':
        previous_quarter_df = previous_quarter_df[previous_quarter_df['Manufacturer'] == manufacturer]

    previous_quarter_regs = previous_quarter_df['Registrations'].sum()
    qoq_growth = calculate_growth(current_quarter_regs, previous_quarter_regs)
else:
    qoq_growth = None
    
#   Display Metrics  
st.header("Growth Metrics")
col1, col2 = st.columns(2)

with col1:
    if yoy_growth is not None:
        st.metric(label="YoY Growth", value=f"{yoy_growth:.1f}%", delta=f"{yoy_growth:.1f}%")
    else:
        st.metric(label="YoY Growth", value="N/A")

with col2:
    if qoq_growth is not None:
        st.metric(label="QoQ Growth", value=f"{qoq_growth:.1f}%", delta=f"{qoq_growth:.1f}%")
    else:
        st.metric(label="QoQ Growth", value="N/A")


#   Visualizations  
st.header("Data Visualizations")
col1_viz, col2_viz = st.columns(2)

with col1_viz:
    st.subheader("Vehicle Registrations by Category")
    # Prepare data for line chart
    category_trend = filtered_df.groupby(['Date', 'Category'])['Registrations'].sum().reset_index()
    fig_category = px.line(category_trend, x='Date', y='Registrations', color='Category',
                           labels={'Registrations': 'Number of Registrations'})
    fig_category.update_layout(legend_title_text='Category')
    st.plotly_chart(fig_category, use_container_width=True)

with col2_viz:
    st.subheader("Registrations by Manufacturer")
    # Prepare data for bar chart
    manufacturer_regs = filtered_df.groupby('Manufacturer')['Registrations'].sum().sort_values(ascending=True).reset_index()
    fig_manufacturer = px.bar(manufacturer_regs.tail(10), x='Registrations', y='Manufacturer', orientation='h',
                              labels={'Registrations': 'Total Registrations'})
    st.plotly_chart(fig_manufacturer, use_container_width=True)