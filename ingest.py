import pandas as pd
import sqlite3

# Load the CSV
csv_file = 'inventory_forecasting.csv'  # Change this to your actual file name
df = pd.read_csv(csv_file)

# Rename columns for SQL compatibility
df.columns = [col.strip().replace(' ', '_').replace('/', '_') for col in df.columns]

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create tables based on the ER diagram
cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUCT (
    Product_ID TEXT PRIMARY KEY,
    Category TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS STORES (
    Store_ID TEXT PRIMARY KEY,
    Region TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DATES (
    Date TEXT PRIMARY KEY,
    Weather_Condition TEXT,
    Holiday_Promotion TEXT,
    Seasonality TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS INVENTORY (
    Date TEXT,
    Store_ID TEXT,
    Product_ID TEXT,
    Inventory_Level INTEGER,
    Units_Sold INTEGER,
    Units_Ordered INTEGER,
    Demand_Forecast REAL,
    Price REAL,
    Discount REAL,
    Competitor_Pricing REAL,
    Promotion_Flag TEXT,
    PRIMARY KEY (Date, Store_ID, Product_ID),
    FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID),
    FOREIGN KEY (Store_ID) REFERENCES STORES(Store_ID),
    FOREIGN KEY (Date) REFERENCES DATES(Date)
);
""")

# Populate PRODUCT table
product_df = df[['Product_ID', 'Category']].drop_duplicates()
product_df.to_sql('PRODUCT', conn, if_exists='replace', index=False)

# Populate STORES table
store_df = df[['Store_ID', 'Region']].drop_duplicates()
store_df.to_sql('STORES', conn, if_exists='replace', index=False)

# Populate DATES table
dates_df = df[['Date', 'Weather_Condition', 'Holiday_Promotion', 'Seasonality']].drop_duplicates()
dates_df.to_sql('DATES', conn, if_exists='replace', index=False)

# Add Promotion_Flag based on Holiday_Promotion (can be customized)
df['Promotion_Flag'] = df['Holiday_Promotion'].apply(lambda x: 'Yes' if pd.notna(x) and x != 'None' else 'No')

# Populate INVENTORY table
inventory_df = df[['Date', 'Store_ID', 'Product_ID', 'Inventory_Level', 'Units_Sold',
                   'Units_Ordered', 'Demand_Forecast', 'Price', 'Discount',
                   'Competitor_Pricing', 'Promotion_Flag']]

inventory_df.to_sql('INVENTORY', conn, if_exists='append', index=False)

# Commit and close connection
conn.commit()
conn.close()

print("Data successfully loaded into SQLite database.")
