import pandas as pd
from pathlib import Path

# Path to data folder
data_folder = Path("data")

# Get all CSV files
csv_files = list(data_folder.glob("*.csv"))

processed_frames = []

for file in csv_files:
    # Read CSV file
    df = pd.read_csv(file)

    # ---- CLEAN & FILTER PRODUCT ----
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df = df[df["product"] == "pink morsel"]

    # ---- CLEAN PRICE COLUMN ----
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    # ---- ENSURE QUANTITY IS NUMERIC ----
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # ---- CREATE SALES COLUMN ----
    df["sales"] = df["quantity"] * df["price"]

    # ---- SELECT REQUIRED COLUMNS ----
    df = df[["sales", "date", "region"]]

    processed_frames.append(df)

# ---- COMBINE ALL FILES ----
final_df = pd.concat(processed_frames, ignore_index=True)

# ---- SAVE OUTPUT FILE ----
final_df.to_csv("processed_sales.csv", index=False)

print("Data processing complete.")
print(f"Total rows in output: {len(final_df)}")
print("Final file saved as processed_sales.csv")
