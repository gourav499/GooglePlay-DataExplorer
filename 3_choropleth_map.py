import pandas as pd
import plotly.express as px
import datetime
import numpy as np

def format_large_numbers(value):
    """Format numbers into Millions (M) or Billions (B)."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return str(value)

def plot_choropleth(file_path, mapping_path, bypass_time=False):
    now = datetime.datetime.now().time()
    if not bypass_time and not (18 <= now.hour < 20):
        print("⏳ This visualization is only available from 6 PM to 8 PM IST")
        return

    df = pd.read_csv(file_path)
    df_mapping = pd.read_csv(mapping_path)

    df["Installs"] = df["Installs"].astype(str).str.replace(r"[^\d]", "", regex=True)
    df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")
    df.dropna(subset=["Installs"], inplace=True)

    excluded_letters = ("A", "C", "G", "S")
    df = df[~df["Category"].str.startswith(excluded_letters)]

    category_installs = df.groupby("Category")["Installs"].sum().reset_index()
    top5_categories = category_installs.nlargest(5, "Installs")

    df_mapping["Country"] = df_mapping["Country"].str.strip()
    df_top5 = top5_categories.merge(df_mapping, on="Category", how="left")
    df_top5["Country"].fillna("Unknown", inplace=True)
    df_top5["Formatted_Installs"] = df_top5["Installs"].apply(format_large_numbers)

    min_val = max(1_000_000, df_top5["Installs"].min())  # Ensure minimum scale is at least 1M
    max_val = df_top5["Installs"].max()

    tick_values = np.linspace(min_val, max_val, num=5)
    tick_labels = [format_large_numbers(v) for v in tick_values]

    fig = px.choropleth(
        df_top5,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Country",
        hover_data={"Formatted_Installs": True, "Category": True},  # Now correctly mapped
        title="Top 5 App Categories by Global Install Count (2025)",
        color_continuous_scale="hot"
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>"
                      "Country: %{hovertext}<br>"
                      "Installs: %{customdata[0]}<br>"
                      "Category: %{customdata[1]}"
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Installs",
            tickvals=tick_values.tolist(),
            ticktext=tick_labels,
            tickmode="array"
        ),
        geo=dict(showframe=False, showcoastlines=False)
    )

    fig.show()

if __name__ == "__main__":
    plot_choropleth("data/PlayStore_Data.csv", "data/category_country_mapping.csv")
