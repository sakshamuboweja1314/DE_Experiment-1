
# Libraries
import pandas as pd
import numpy as np
import re

# Read the CSV file
df = pd.read_csv('employee_data.csv')

# Remove duplicate rows
df = df.drop_duplicates()

# Function to check valid email syntax
def is_valid_email(email):
    if pd.isna(email):
        return False
    return re.match(r"[^@]+@[^@]+\.[^@]", str(email)) is not None

# Clean invalid emails (replace with NaN)
df['email'] = df['email'].apply(lambda x: x if is_valid_email(x) else np.nan)

# Fill missing email values
df['email'] = df['email'].fillna('abc@gmail.com')

# Handle invalid salaries (<=0 or NaN → replace with median)
valid_salary = df['salary'].dropna()
valid_salary = valid_salary[valid_salary > 0]
median_salary = valid_salary.median()
df['salary'] = df['salary'].apply(lambda x: median_salary if pd.isna(x) or x <= 0 else x)

# Function to clean and standardize department names
def clean_depart(dept):
    if pd.isna(dept):
        return dept
    dept = str(dept).strip()
    dept_lower = dept.lower()
    if dept_lower in ['hr', 'human resources']:
        return 'Human Resources'
    elif dept_lower in ['it', 'information technology']:
        return 'Information Technology'
    elif dept_lower == 'finance':
        return 'Finance'
    else:
        return dept.title()

# Apply department cleaning (make sure column name matches your CSV!)
df['department'] = df['department'].apply(clean_depart)

# Fill missing values for name and joining date
df['name'] = df['name'].fillna('Unknown')
df['joining_date'] = df['joining_date'].fillna('Unknown')

# Save cleaned data
df.to_csv('employee_cleaned.csv', index=False)

print("✅ Data cleaning completed. Cleaned data saved to 'employee_cleaned.csv'.")
