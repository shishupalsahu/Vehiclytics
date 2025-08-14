# create_data.py

import pandas as pd
import numpy as np

# Define the parameters for our data
np.random.seed(42)
date_range = pd.to_datetime(pd.date_range(start="2022-01-01", end="2024-12-31", freq='D'))
manufacturers = ["Maruti", "Hyundai", "Tata", "Mahindra", "Kia", "Toyota", "Honda", "Hero", "Bajaj", "TVS"]
categories = {
    "Maruti": "4W", "Hyundai": "4W", "Tata": "4W", "Mahindra": "4W", "Kia": "4W", "Toyota": "4W", "Honda": "4W",
    "Hero": "2W", "Bajaj": "2W", "TVS": "2W"
}

# Generate data
data = []
for date in date_range:
    # Randomly select a few manufacturers to have registrations each day
    num_mfg_per_day = np.random.randint(5, len(manufacturers) + 1)
    mfg_today = np.random.choice(manufacturers, size=num_mfg_per_day, replace=False)
    
    for mfg in mfg_today:
        category = categories.get(mfg, "Other")
        # Base registrations + seasonality (sine wave) + random noise
        base_regs = 150 if category == '4W' else 300
        seasonality = int(50 * np.sin(2 * np.pi * date.dayofyear / 365))
        noise = np.random.randint(-20, 20)
        registrations = max(0, base_regs + seasonality + noise)
        
        data.append([date, mfg, category, registrations])

# Create DataFrame
df = pd.DataFrame(data, columns=["Date", "Manufacturer", "Category", "Registrations"])

# Save to CSV
df.to_csv('data.csv', index=False)

print("Successfully created data.csv with sample vehicle registration data.")