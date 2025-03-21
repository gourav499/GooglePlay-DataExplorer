# Google Play Store Data Analytics & Visualization

## Project Overview
This project is a **real-time Google Play Store data analytics** application that processes, analyzes, and visualizes app installation trends worldwide. The project involves **data cleaning, merging, and advanced visualizations**, including:

- **Scatter Plot** (App installs vs. Ratings)
- **Choropleth Map** (Installs per country for top app categories)
- **Time-Series Line Chart** (Installs over time)
- **Full Integration into a Website** for live analytics

The goal is to help businesses, developers, and analysts understand how different app categories perform globally.

---

## Project Structure
```
📁 GooglePlay_Analytics
│── 📂 data                # Raw and cleaned datasets
│   │── category_country_mapping.csv
│   │── PlayStore_Data.csv
    │── User_Reviews.csv
│── 📂 scripts             # Python scripts for analysis
│   │── _Analysis.Final.py        # Runs all visualizations together
    │── data_cleaning.py
│   │── data_merging.py
│   │── scatter_plot.py
│   │── choropleth_map.py
│   │── time_series_chart.py
│── 📂 templets             # Frontend files for web integration
│── 📂 README.md              # Project documentation (this file)
```

---

## Features & Functionality
- **Automated Data Cleaning**
  - Converts `Installs` column to numeric values
  - Removes duplicate entries and missing data
- **Data Merging & Aggregation**
  - Merges Play Store data with country-category mapping
  - Aggregates installs for top 5 app categories per country
- **Interactive Visualizations**
  - **Scatter Plot:** Shows correlation between installs and ratings
  - **Choropleth Map:** Global view of installs per country
  - **Time-Series Chart:** Displays app installs over time
- **Website Integration**
  - Fully responsive and mobile-friendly

---

## Data Sources
- **Google Play Store Dataset:** `PlayStore_Data.csv`
- **Country Mapping Dataset:** `category_country_mapping.xlsx`
- Data has been processed and transformed for accurate insights

---

## Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/gourav499/GooglePlay_Analytics.git
cd GooglePlay_Analytics
```
### 2️⃣ Install Dependencies
Ensure you have Python installed, then install required libraries:
```bash
pip install pandas numpy plotly openpyxl flask matplotlib.pyplot seaborn datetime pytz

```
### 3️⃣ Run the Scripts
To clean and merge data:
```bash
python scripts/1_data_cleaning.py
python scripts/data_merging.py
```
To generate visualizations:
```bash
python scripts/2_scatter_plot.py
python scripts/3_choropleth_map.py
python scripts/4_time_series_chart.py
```
To run all visualizations together:
```bash
python scripts/_Analysis.Final
```

---

## How to View the Dashboard
1. Run the script to generate `dashboard.html`.
2. Open the file in a browser manually or let the script do it for you.

---

## Challenges & Solutions
✅ **Non-numeric `Installs` values** → Cleaned using regex & converted to integers  
✅ **Country name mismatches** → Standardized names to match Plotly's format  
✅ **Missing category-country mappings** → Filled gaps with 'Unknown' to avoid errors  
✅ **Choropleth map only showing some countries** → Fixed merge logic & ensured all entries were included  
✅ **Saudi Arabia appearing black in map** → Normalized install values for better color scaling  

---

## Contributing
Want to improve this project? Feel free to:
- Fork the repository
- Make your changes in a new branch
- Submit a pull request

---

## License
This project is **open-source** under the MIT License. Feel free to use and modify it for your own purposes.

---

## Contact
For any questions, feel free to reach out:
📧 Email: gouravtiwari499@gmail.com  
🌍 GitHub: [your-username](https://github.com/gourav499)  
🚀 Live Project URL: [Open Dashboard](file:///C:/Users/Gourav%20Tiwari/Desktop/Google-Play-Analytics/dashboard.html)

Happy coding! 🎉

