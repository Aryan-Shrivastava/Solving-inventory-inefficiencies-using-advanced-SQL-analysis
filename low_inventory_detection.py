import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('inventory.db')

# SQL Query for low inventory detection using average daily sales and reorder point
query = """
WITH avg_sales AS (
    SELECT Product_ID, AVG(Units_Sold) AS Avg_Daily_Sales
    FROM INVENTORY
    GROUP BY Product_ID
)
SELECT 
    i.Date,
    i.Store_ID,
    i.Product_ID,
    i.Inventory_Level,
    ROUND(a.Avg_Daily_Sales, 2) AS Avg_Daily_Sales,
    ROUND(a.Avg_Daily_Sales * 3, 2) AS Reorder_Point,
    (i.Inventory_Level < a.Avg_Daily_Sales * 3) AS Is_Low_Inventory
FROM INVENTORY i
JOIN avg_sales a ON i.Product_ID = a.Product_ID
WHERE i.Inventory_Level < (a.Avg_Daily_Sales * 3);
"""

# Run the query and load into DataFrame
low_inventory_df = pd.read_sql_query(query, conn)

# Display the result
print("Low Inventory Items (Based on Avg Daily Sales x 3-Day Lead Time):")
print(low_inventory_df)

# Export to CSV
low_inventory_df.to_csv("low_inventory_alerts.csv", index=False)

# Close connection
conn.close()
