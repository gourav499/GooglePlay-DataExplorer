import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_scatter(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Filter only paid apps
    df_paid = df[df['Type'] == 'Paid'].copy()

    # Convert 'Installs' to numeric (remove non-numeric characters like '+', ',')
    df_paid['Installs'] = df_paid['Installs'].str.replace(r'[+,]', '', regex=True).astype(float)

    # Ensure 'Price' column is properly cleaned and converted to float
    df_paid['Price'] = df_paid['Price'].astype(str).str.replace(r'[$]', '', regex=True).astype(float)

    # Calculate revenue (Revenue = Installs * Price)
    df_paid['Revenue'] = df_paid['Installs'] * df_paid['Price']

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=df_paid,
        x=df_paid["Installs"] / 1e6,  # Convert installs to millions
        y=df_paid["Revenue"],
        hue=df_paid["Category"],  # Color by category
        palette="Set2"
    )

    # Add a trendline
    sns.regplot(
        data=df_paid,
        x=df_paid["Installs"] / 1e6,
        y=df_paid["Revenue"],
        scatter=False,
        color="black",
        line_kws={"linestyle": "dashed"}
    )

    # Labels and title
    plt.xlabel("Number of Installs (in millions)")
    plt.ylabel("Revenue (in $)")
    plt.title("Revenue vs Installs (Paid Apps)", fontweight="bold")

    # Adjust legend position
    plt.legend(title="App Category", bbox_to_anchor=(1.05, 1.05), loc="upper left", fontsize=8)
    
    # plt.subplots_adjust(left=0.15, right=0.75)  # Moves the plot to the left
    plt.subplots_adjust(left=0.15, right=0.75)  # Moves the plot to the left


    plt.show()

# Example usage (replace with your actual file path)
plot_scatter("data/PlayStore_Data.csv")
