import pandas as pd

def clean_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Standardizing column names
        df.columns = df.columns.str.strip().str.lower()

        # Dropping missing values
        df.dropna(inplace=True)

        # Converting Reviews column to lowercase
        if "reviews" in df.columns:
            df["reviews"] = df["reviews"].astype(str).str.lower()

        return df

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None

# Testing
if __name__ == "__main__":
    df = clean_data("data/User_Reviews.csv")
    if df is not None:
        print(df.head())
