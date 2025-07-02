import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')

# 1. Stock Level per Product per Store
query1 = """
SELECT Store_ID, Product_ID, SUM(Inventory_Level) AS Stock_Level
FROM INVENTORY
GROUP BY Store_ID, Product_ID;
"""
df1 = pd.read_sql_query(query1, conn)
print("\n1. Stock Level per Product per Store:")
print(df1)
df1.to_csv("stock_per_store.csv", index=False)

# 2. Total Stock per Product (Warehouse View)
query2 = """
SELECT Product_ID, SUM(Inventory_Level) AS Total_Stock
FROM INVENTORY
GROUP BY Product_ID;
"""
df2 = pd.read_sql_query(query2, conn)
print("\n2. Total Stock per Product:")
print(df2)
df2.to_csv("total_stock_per_product.csv", index=False)

# 3. Stock by Region (joining STORES table)
query3 = """
SELECT s.Region, i.Product_ID, SUM(i.Inventory_Level) AS Regional_Stock
FROM INVENTORY i
JOIN STORES s ON i.Store_ID = s.Store_ID
GROUP BY s.Region, i.Product_ID;
"""
df3 = pd.read_sql_query(query3, conn)
print("\n3. Stock by Region:")
print(df3)
df3.to_csv("stock_by_region.csv", index=False)

# Close the connection
conn.close()
