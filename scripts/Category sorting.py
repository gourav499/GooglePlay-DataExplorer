import pandas as pd

# Load both CSV files
playstore_df = pd.read_csv("PlayStore_Data.csv")  # Adjust the path if needed
mapping_df = pd.read_csv("scripts/category_country_mapping.csv")  # Ensure this file exists

# Merge them on 'Category'
merged_df = pd.merge(playstore_df, mapping_df, on="Category", how="inner")  

# Check the new dataframe
print(merged_df.head())  

# Save merged file (optional)
merged_df.to_csv("scripts/Merged_PlayStore_Data.csv", index=False)

print(merged_df.columns)  # Ensure 'Country' exists
