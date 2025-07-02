import sqlite3
import pandas as pd

conn = sqlite3.connect("inventory.db")

# Stockout Rate per Product per Store
stockout_query = """
WITH stock_status AS (
    SELECT Product_ID, Store_ID,
           COUNT(*) AS Total_Records,
           SUM(CASE WHEN Inventory_Level = 0 THEN 1 ELSE 0 END) AS Stockout_Count
    FROM INVENTORY
    GROUP BY Product_ID, Store_ID
)
SELECT 
    Product_ID, Store_ID,
    Total_Records,
    Stockout_Count,
    ROUND(100.0 * Stockout_Count / Total_Records, 2) AS Stockout_Rate_Percent
FROM stock_status;
"""
stockout_df = pd.read_sql_query(stockout_query, conn)
print("\n Stockout Rate Report:")
print(stockout_df)
stockout_df.to_csv("kpi_stockout_rate.csv", index=False)


# Inventory Age (days since last Units_Sold > 0)
inventory_age_query = """
WITH last_sold AS (
    SELECT Product_ID, Store_ID, MAX(Date) AS Last_Sale_Date
    FROM INVENTORY
    WHERE Units_Sold > 0
    GROUP BY Product_ID, Store_ID
)
SELECT 
    i.Product_ID,
    i.Store_ID,
    julianday(MAX(i.Date)) - julianday(l.Last_Sale_Date) AS Inventory_Age_Days
FROM INVENTORY i
JOIN last_sold l ON i.Product_ID = l.Product_ID AND i.Store_ID = l.Store_ID
GROUP BY i.Product_ID, i.Store_ID;
"""
inventory_age_df = pd.read_sql_query(inventory_age_query, conn)
print("\nInventory Age Report (days since last sale):")
print(inventory_age_df)
inventory_age_df.to_csv("kpi_inventory_age.csv", index=False)


# Average Stock Level per Product per Store
avg_stock_query = """
SELECT 
    Product_ID,
    Store_ID,
    ROUND(AVG(Inventory_Level), 2) AS Avg_Inventory_Level
FROM INVENTORY
GROUP BY Product_ID, Store_ID;
"""
avg_stock_df = pd.read_sql_query(avg_stock_query, conn)
print("\nAverage Stock Level Report:")
print(avg_stock_df)
avg_stock_df.to_csv("kpi_avg_stock_level.csv", index=False)

# Close connection
conn.close()
