#-------------------------------------------
# Arjun Singh 
# IIT Ropar AI & ML Minor
# Ni. Name Monster Developer
#--------------------------------------------

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')



#### EDA ####
# ------------------------------
# Step 1: Load Dataset
# ------------------------------
df = pd.read_csv("investments_VC.csv", encoding='ISO-8859-1')
df.columns = df.columns.str.strip()
df['funding_total_usd'] = df['funding_total_usd'].astype(str)
df['funding_total_usd'] = df['funding_total_usd'].str.replace(',', '')
df['funding_total_usd'] = df['funding_total_usd'].str.replace(' ', '')
df['funding_total_usd'] = df['funding_total_usd'].replace('?', np.nan)
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')
df['funding_total_usd'] = df['funding_total_usd'].fillna(df['funding_total_usd'].median())

# Clean Data
df.drop(['status', 'region', 'state_code', 'permalink', 'homepage_url',
         'founded_at', 'founded_month', 'founded_quarter', 'founded_year'],
        axis=1, inplace=True)

df['category_list'] = df['category_list'].fillna("Unknown")
df['country_code'] = df['country_code'].fillna("Unknown")
df['city'] = df['city'].fillna("Unknown")
df['main_category'] = df['category_list'].apply(lambda x: x.split('|')[0] if '|' in x else x)
df['funding_million_usd'] = df['funding_total_usd'] / 1_000_000

df.to_csv("clean.csv", index=False)

