"""
This script provides a simple way to inspect the contents of the SQLite database used in the FlowerClassifier application.
It displays all the tables in the database and the contents of the `training_images` table for debugging or monitoring purposes.
"""

import sqlite3

# Connect to the database
conn = sqlite3.connect("training_data.db")
cursor = conn.cursor()

# Display all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Display the contents of the training_images table
cursor.execute("SELECT * FROM training_images;")
rows = cursor.fetchall()
print("\nContents of the training_images table:")
for row in rows:
    print(row)

# Close the database connection
conn.close()