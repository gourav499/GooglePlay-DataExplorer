import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import webbrowser
import os



# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Analysis Dashboard</title>
</head>
<body>
    <h1>App Analysis Dashboard</h1>
    <div>
        <h2>Scatter Plot: Revenue vs Installs (Paid Apps)</h2>
        <img src="scatter_plot.png" alt="Scatter Plot">
    </div>
    <div>
        <h2>Choropleth Map: Top 5 Categories by Installs</h2>
        <iframe src="choropleth.html" width="100%" height="500"></iframe>
    </div>
    <div>
        <h2>Time Series: Monthly Installs Trend</h2>
        <img src="time_series.png" alt="Time Series Plot">
    </div>
</body>
</html>
"""

 

def format_large_numbers(value):
    if pd.isna(value):
        return "0"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return str(value)

def plot_scatter(df):
    df_paid = df[df['Type'] == 'Paid'].copy()
    df_paid['Installs'] = pd.to_numeric(df_paid['Installs'].astype(str).str.replace(r'[^0-9]', '', regex=True), errors='coerce')
    df_paid['Price'] = pd.to_numeric(df_paid['Price'].astype(str).str.replace(r'[^0-9.]', '', regex=True), errors='coerce')
    df_paid.dropna(subset=['Installs', 'Price'], inplace=True)
    df_paid['Revenue'] = df_paid['Installs'] * df_paid['Price']
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(data=df_paid, x=df_paid["Installs"] / 1e6, y=df_paid["Revenue"], hue=df_paid["Category"], palette="Set2")
    sns.regplot(data=df_paid, x=df_paid["Installs"] / 1e6, y=df_paid["Revenue"], scatter=False, color="black", line_kws={"linestyle": "dashed"})
    plt.xlabel("Number of Installs (in millions)")
    plt.ylabel("Revenue (in $)")
    plt.title("Revenue vs Installs (Paid Apps)", fontweight="bold")
    plt.legend(title="App Category", bbox_to_anchor=(1.05, 1.05), loc="upper left", fontsize=8)
    plt.subplots_adjust(left=0.15, right=0.75)
    plt.savefig("scatter_plot.png")
    plt.close()

def plot_choropleth(df, mapping_path):
    df_mapping = pd.read_csv(mapping_path)
    df["Installs"] = pd.to_numeric(df["Installs"].astype(str).str.replace(r'[^0-9]', '', regex=True), errors='coerce')
    df.dropna(subset=["Installs"], inplace=True)
    df_mapping["Country"] = df_mapping["Country"].str.strip()
    df_top5 = df.groupby("Category")["Installs"].sum().reset_index().nlargest(5, "Installs")
    df_top5 = df_top5.merge(df_mapping, on="Category", how="left")
    df_top5["Country"] = df_top5["Country"].fillna("Unknown")
    df_top5["Formatted_Installs"] = df_top5["Installs"].apply(format_large_numbers)
    fig = px.choropleth(
        df_top5, locations="Country", locationmode="country names", color="Installs", hover_name="Country",
        hover_data={"Formatted_Installs": True, "Category": True}, title="Top 5 App Categories by Global Install Count (2025)",
        color_continuous_scale="hot"
    )
    fig.write_html("choropleth.html")

def plot_time_series(df):
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    df["Installs"] = pd.to_numeric(df["Installs"].astype(str).str.replace(r'[^0-9]', '', regex=True), errors='coerce')
    df.dropna(subset=["Installs"], inplace=True)
    df["Month"] = df["Last Updated"].dt.to_period("M")
    category_trends = df.groupby(["Month", "Category"])["Installs"].sum().unstack()
    months = category_trends.index.astype(str)
    plt.figure(figsize=(12, 6))
    for category in category_trends.columns:
        installs = category_trends[category].fillna(0)
        plt.plot(months, installs, marker="o", linestyle="-", label=category)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=9)
    plt.yscale("log")
    plt.title("Monthly Installs Trend by Category")
    plt.xlabel("Month")
    plt.ylabel("Total Installs (Log Scale)")
    plt.legend(title="Category", fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig("time_series.png")
    plt.close()


if __name__ == "__main__":
    # Get the script's directory (so the paths stay correct no matter where you run it)
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    data_dir = os.path.join(script_dir, "../data")  # Moves up one level to the "data" folder

    # Use relative paths
    playstore_path = os.path.join(data_dir, "PlayStore_Data.csv")
    mapping_path = os.path.join(data_dir, "category_country_mapping.csv")

    # Load the data
    df = pd.read_csv(playstore_path)
    plot_scatter(df)
    plot_choropleth(df, mapping_path)
    plot_time_series(df)

    with open("dashboard.html", "w") as f:
        f.write(html_template)

    print("✅ Dashboard generated successfully!")
    webbrowser.open("file://" + os.path.abspath("dashboard.html"))  
