"""
This script is used to inspect and display the contents of the SQLite database used in the FlowerClassifier project. 
It retrieves information about images stored in the database, including their labels, file paths, and training status.
"""

import sqlite3

# Path to the database
DB_PATH = "training_data.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Query all image records in the database
cursor.execute("SELECT id, image_path, label, added_at, used_in_training FROM training_images")
rows = cursor.fetchall()

# Display the results
if rows:
    print("Image records in the database:")
    print(f"{'ID':<5} {'Image Path':<50} {'Label':<15} {'Added At':<20} {'Used in Training':<15}")
    print("-" * 120)
    for row in rows:
        # Convert the used_in_training value to "Yes"/"No"
        used_in_training = "Yes" if row[4] == 1 else "No"
        print(f"{row[0]:<5} {row[1]:<50} {row[2]:<15} {row[3]:<20} {used_in_training:<15}")
else:
    print("No image records found in the database.")

# Close the database connection
conn.close()