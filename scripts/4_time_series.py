import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pytz

def plot_time_series(file_path, override_time=False):
    # Time restriction (Only between 6 PM - 9 PM IST)
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(ist).time()
    
    if not override_time and not (18 <= now.hour < 21):
        print("⏳ This visualization is only available from 6 PM to 9 PM IST")
        return

    df = pd.read_csv(file_path)

    # Convert 'Last Updated' to datetime format
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

    # Clean 'Installs' column (Remove non-numeric values)
    df["Installs"] = (
        df["Installs"]
        .str.replace(r"[+,]", "", regex=True)  # Remove '+' and ',' characters
        .str.extract(r"(\d+)")  # Extract only numeric part
        .astype(float)  # Convert to float
    )

    # Remove NaN values in 'Installs'
    df = df.dropna(subset=["Installs"])

    # Convert 'Reviews' to numeric (removing commas)
    df["Reviews"] = df["Reviews"].astype(str).str.replace(",", "", regex=True).astype(float)

    # Apply filters
    df = df[
        df["Category"].str.startswith(("E", "C", "B")) &  # Category must start with E, C, B
        ~df["App"].str.startswith(("X", "Y", "Z")) &  # App name must not start with X, Y, Z
        (df["Reviews"] > 500)  # Reviews must be more than 500
    ]

    # Extract month and year
    df["Month"] = df["Last Updated"].dt.to_period("M")

    # Group by Month & Category
    category_trends = df.groupby(["Month", "Category"])["Installs"].sum().unstack()

    # Convert index to string for plotting
    months = category_trends.index.astype(str)

    # Plot Time Series
    plt.figure(figsize=(12, 6))

    for category in category_trends.columns:
        installs = category_trends[category].fillna(0)  # Replace NaN with 0

        # Identify months where installs increased >20% MoM
        growth = installs.pct_change().fillna(0) > 0.2

        plt.plot(months, installs, marker="o", linestyle="-", label=category)

        # Shade growth areas where MoM increase > 20%
        plt.fill_between(months, 0, installs, where=growth, color="gray", alpha=0.3)

    # Improve X-axis readability
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=9)

    # Set log scale if installs have large variations
    plt.yscale("log")

    plt.title("Monthly Installs Trend by Category")
    plt.xlabel("Month")
    plt.ylabel("Total Installs (Log Scale)")
    plt.legend(title="Category", fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()

# Testing
if __name__ == "__main__":
    plot_time_series("data/PlayStore_Data.csv")  # Allow testing anytime
