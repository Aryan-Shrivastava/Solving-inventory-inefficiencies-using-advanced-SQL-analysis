import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect('inventory.db')

# SQL query to calculate reorder points using historical 30-day sales trends
query = """
WITH recent_sales AS (
    SELECT 
        Product_ID,
        Store_ID,
        Date,
        Units_Sold
    FROM INVENTORY
    WHERE Date >= DATE((SELECT MAX(Date) FROM INVENTORY), '-30 day')
),
avg_sales AS (
    SELECT 
        Product_ID,
        Store_ID,
        AVG(Units_Sold) AS Avg_Daily_Sales
    FROM recent_sales
    GROUP BY Product_ID, Store_ID
),
latest_inventory AS (
    SELECT *
    FROM INVENTORY
    WHERE Date = (SELECT MAX(Date) FROM INVENTORY)
)
SELECT 
    l.Date,
    l.Store_ID,
    l.Product_ID,
    l.Inventory_Level,
    ROUND(a.Avg_Daily_Sales, 2) AS Avg_Daily_Sales,
    ROUND(a.Avg_Daily_Sales * 3, 2) AS Reorder_Point,
    CASE 
        WHEN l.Inventory_Level < (a.Avg_Daily_Sales * 3) THEN 1 
        ELSE 0 
    END AS Is_Low_Inventory
FROM latest_inventory l
JOIN avg_sales a ON l.Product_ID = a.Product_ID AND l.Store_ID = a.Store_ID
WHERE l.Inventory_Level < (a.Avg_Daily_Sales * 3);
"""

# Run the query and load the result into a DataFrame
reorder_df = pd.read_sql_query(query, conn)

# Display the output
print("\nLow Inventory Products (Based on 30-day Sales Trend & 3-Day Lead Time):")
print(reorder_df)

# Export to CSV
reorder_df.to_csv("low_inventory_trend_based.csv", index=False)

# Close the connection
conn.close()
