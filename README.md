Vehicle Registration Analytics Dashboard
This project is an interactive web dashboard built with Python and Streamlit to analyze vehicle registration data from an investor's perspective. It provides key metrics like Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth and allows users to filter data dynamically.

# 🚀 Setup and Installation
Follow these steps to set up and run the project locally.

# 1. Prerequisites
Python 3.8 or newer

pip package manager

# 2. Clone the Repository
git https://github.com/shishupalsahu/Vehiclytics.git 
Network URL : http://192.168.43.218:8501
cd Vehiclytics

# 3. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

On Windows:

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

python -m venv venv
source venv/bin/activate

# 4. Install Dependencies
Install the necessary Python libraries using pip:

pip install pandas streamlit plotly

# 5. Generate Sample Data
The dashboard uses a generated sample dataset. Run the following script first to create the data.csv file.

python create_data.py

# 6. Run the Dashboard
Once the data is generated, launch the Streamlit application:

streamlit run app.py

Your web browser should automatically open a new tab with the running dashboard.

# 📊 Data Assumptions
This dashboard currently uses a generated sample dataset (data.csv) for demonstration and reliability purposes, as live government data sources can be inconsistent.

The data mimics real-world vehicle registration information and has the following structure:

Date: The date of registration (YYYY-MM-DD).

Manufacturer: The name of the vehicle manufacturer (e.g., "Maruti", "Hero").

Category: The vehicle type (e.g., "4W", "2W").

Registrations: The number of vehicles registered on that day for the given manufacturer.

# 🗺️ Feature Roadmap
This project has a solid foundation. If development were to continue, here are some potential features and improvements for the future:

# Backend & Data
Live Data Integration: Replace the static data.csv with a live data source by building a robust web scraper (BeautifulSoup, Scrapy) or connecting to an official API if one becomes available.

Database Integration: Store the collected data in a scalable database like PostgreSQL or a data warehouse to handle larger datasets and more complex queries efficiently.

Automated Data Pipeline: Create a scheduled job (e.g., using cron or Airflow) to automatically fetch and update the data daily.

# Frontend & Analytics
Advanced Metrics: Introduce more sophisticated investor metrics like rolling averages, market share analysis, and volatility calculations.

Predictive Analytics: Incorporate a forecasting model (e.g., using Prophet or ARIMA) to predict future registration trends.

Export Functionality: Add buttons to allow users to download charts as images or export the filtered data as a CSV file.

User Authentication: Implement a user login system to allow for saved filter presets and personalized dashboards.
