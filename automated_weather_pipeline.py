
""""
Automated Weather Data Cleaning Pipeline
----------------------------------------

Description: This script automates the ingestion, cleaning, and merging of 
multi-source historical weather data (CSV, JSON, and Excel). 

It performs schema alignment, handles missing values, removes duplicates, 
and produces a consolidated 'Final_Dataset.csv' for downstream analysis.

Author: Bayan Aldoghan
"""



import os
import pandas as pd


# Locate our directory
script_dir = os.path.dirname(os.path.abspath(__file__))


# Load the raw files exactly as they are upstream
df_temp = pd.read_csv(os.path.join(script_dir, 'source_temperature.csv'))
df_env = pd.read_json(os.path.join(script_dir, 'source_environmental.json'))
df_summary = pd.read_excel(os.path.join(script_dir, 'source_summary.xlsx'))



# --- STEP 1: LOOK AT WHAT IS INSIDE EACH FILE ---
# Available Columns per File:
print(f"CSV Temperature Columns: {list(df_temp.columns)}")
print(f"JSON Environmental Columns: {list(df_env.columns)}")
print(f"Excel Summary Columns: {list(df_summary.columns)}")
print()
print()

# Data Frames Inspection
print(df_temp.head(3).to_string(index=False))
print()
print(df_env.head(3).to_string(index=False))
print()
print(df_summary.head(3).to_string(index=False))
print()



# --- STEP 2: INVESTIGATE THE COMMON KEY & FORMATS ---
print(f"CSV Date Sample:  '{df_temp['Formatted Date'].iloc[0]}' (Type: {df_temp['Formatted Date'].dtype})")
print(f"JSON Date Sample: '{df_env['Formatted Date'].iloc[0]}' (Type: {df_env['Formatted Date'].dtype})")
print(f"Excel Date Sample:'{df_summary['Formatted Date'].iloc[0]}' (Type: {df_summary['Formatted Date'].dtype})")
print()
print()

# Date Standardization (Schema Alignment)
df_temp['Formatted Date'] = pd.to_datetime(df_temp['Formatted Date'], utc=True)
df_env['Formatted Date'] = pd.to_datetime(df_env['Formatted Date'], utc=True)
df_summary['Formatted Date'] = pd.to_datetime(df_summary['Formatted Date'], utc=True)

# Verify 'Formatted Date' Type
print(f"CSV Date Sample:  '{df_temp['Formatted Date'].iloc[0]}' (Type: {df_temp['Formatted Date'].dtype})")
print(f"JSON Date Sample: '{df_env['Formatted Date'].iloc[0]}' (Type: {df_env['Formatted Date'].dtype})")
print(f"Excel Date Sample:'{df_summary['Formatted Date'].iloc[0]}' (Type: {df_summary['Formatted Date'].dtype})")
print()
print()




# --- STEP 3: Data Cleaning (Data Audit) ---

# 1. Missing data Inspection
print(df_temp.isnull().sum())
print(df_env.isnull().sum())
print(df_summary.isnull().sum())
print()
print()

# Filling missing data
df_summary['Precip Type'] = df_summary['Precip Type'].fillna('Unknown')
print(df_summary.isnull().sum())
print()
print()


# 2. Data types Inspection
print("CSV Data Types")
print(df_temp.dtypes)
print("JSON Data Types")
print(df_env.dtypes)
print("Excel Data Types")
print(df_summary.dtypes)
print()
print()



# 3. Duplicate Records Inspection
print("Checking for Duplicate Timestamps:")
print(f"CSV Duplicate Rows: {df_temp.duplicated(subset=['Formatted Date']).sum()}")
print(f"JSON Duplicate Rows: {df_env.duplicated(subset=['Formatted Date']).sum()}")
print(f"Excel Duplicate Rows: {df_summary.duplicated(subset=['Formatted Date']).sum()}")
print()
print()

# Fixing Deduplication 
df_temp = df_temp.drop_duplicates(subset=['Formatted Date'])
df_env = df_env.drop_duplicates(subset=['Formatted Date'])
df_summary = df_summary.drop_duplicates(subset=['Formatted Date'])

print(f"CSV Duplicate Rows: {df_temp.duplicated(subset=['Formatted Date']).sum()}")
print(f"JSON Duplicate Rows: {df_env.duplicated(subset=['Formatted Date']).sum()}")
print(f"Excel Duplicate Rows: {df_summary.duplicated(subset=['Formatted Date']).sum()}")
print()
print()



# 4. Outlier & Range Inspection
print("Statistical Range Check:")
print("Temperature Numeric Ranges:")
print(df_temp[['Temperature (C)', 'Apparent Temperature (C)']].describe().loc[['min', 'max']])
print("Environmental Numeric Ranges:")
print(df_env[['Humidity', 'Wind Speed (km/h)']].describe().loc[['min', 'max']])
print()
print()



# 5. Text Standardization
df_summary['Summary'] = df_summary['Summary'].str.strip()
df_summary['Precip Type'] = df_summary['Precip Type'].str.strip()






# --- STEP 4: Combining Disparate Silos Into A Final Single Dataset ---

# 1. First Join: Merge CSV (df_temp) and JSON (df_env) data
merged_step1 = pd.merge(df_temp, df_env, on='Formatted Date', how='inner')

# 2. Second Join: Merge the remaining Excel (df_summary) data to complete the set
df_final = pd.merge(merged_step1, df_summary, on='Formatted Date', how='inner')

print(f"Data Relational Join Complete.")
print()
print()





# --- STEP 5: DISPLAYING AND LOADING THE FINAL HIGH-QUALITY OUTPUT ---

# Final Dataset Inspection

print(f"Final Dataset Dimension: {df_final.shape[0]} Rows x {df_final.shape[1]} Columns.")
print(df_final.head(10).to_string(index=False))

# Loading The Clean Final Dataset 
df_final.to_csv(os.path.join(script_dir, 'Final_Dataset.csv'), index=False)




