import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("inventory.db")

# SQL query for inventory turnover analysis
query = """
SELECT 
    Product_ID,
    Store_ID,
    ROUND(SUM(Units_Sold), 2) AS Total_Units_Sold,
    ROUND(AVG(Inventory_Level), 2) AS Avg_Inventory_Level,
    CASE 
        WHEN AVG(Inventory_Level) > 0 THEN ROUND(SUM(Units_Sold) / AVG(Inventory_Level), 2)
        ELSE NULL
    END AS Inventory_Turnover
FROM INVENTORY
GROUP BY Product_ID, Store_ID;
"""

# Execute query and load result into a DataFrame
turnover_df = pd.read_sql_query(query, conn)

# Display result
print("\nInventory Turnover Analysis:")
print(turnover_df)

# Export to CSV
turnover_df.to_csv("inventory_turnover.csv", index=False)

# Close the database connection
conn.close()
