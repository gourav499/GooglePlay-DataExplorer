import pandas as pd
import plotly.express as px
import random

# Sample list of countries
countries = ["USA", "India", "Brazil", "Germany", "UK", "Canada", "France", "Russia", "China", "Australia"]

# Load data
try:
    df = pd.read_csv("data/PlayStore_Data.csv")
except FileNotFoundError:
    print("Error: The file 'data/PlayStore_Data.csv' was not found. Please check the file path.")
    exit()

# Convert Installs to numeric
df["Installs"] = df["Installs"].str.replace(r"[^\d]", "", regex=True)  # Remove non-numeric characters
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")  # Convert to numbers, set errors to NaN
df = df.dropna(subset=["Installs"])  # Remove rows with NaN installs

# Get top 5 categories
top_categories = df.groupby("Category")["Installs"].sum().nlargest(5).reset_index()

# Assign random countries for testing
top_categories["Country"] = [random.choice(countries) for _ in range(len(top_categories))]

# Plot Choropleth Map
fig = px.choropleth(top_categories, 
                    locations="Country", 
                    locationmode="country names",
                    color="Installs", 
                    hover_name="Category",
                    title="Global Installs by App Category (Test Data)")

fig.show()
