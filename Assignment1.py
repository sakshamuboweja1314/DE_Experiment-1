# Import libraries
import pandas as pd
import numpy as np
import re

# Read the CSV file
df = pd.read_csv('customers.csv')

# Remove duplicate rows
df = df.drop_duplicates()

# Function to check valid email syntax
def is_valid_email(email):
    if pd.isna(email):
        return False
    return re.match(r"[^@]+@[^@]+\.[^@]", str(email)) is not None

# Clean email column (replace invalid with NaN)
df['email'] = df['email'].apply(lambda x: x if is_valid_email(x) else np.nan)

# Handle invalid ages (<= 0 or NaN → replace with median)
valid_ages = df['age'].dropna()
valid_ages = valid_ages[valid_ages > 0]
median_age = valid_ages.median()
df['age'] = df['age'].apply(lambda x: median_age if pd.isna(x) or x <= 0 else x)

# Fill missing values for name and city
df['name'] = df['name'].fillna('Aditya')
df['city'] = df['city'].fillna('Pune')

# Fill missing/invalid email values with a default email
df['email'] = df['email'].fillna('abc@gmail.com')

# Save cleaned data to a new CSV
df.to_csv('customers_cleaned.csv', index=False)

print("✅ Data cleaning completed. Cleaned data saved to 'customers_cleaned.csv'.")
