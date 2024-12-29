"""
This script is used to validate the integrity of image files referenced in the SQLite database.
It checks whether the images exist in the designated directories (`training_queue` or `training_archive`) 
and provides detailed reports on any missing files.
"""

import os
import sqlite3

# Database path and directory paths
DB_PATH = "training_data.db"
QUEUE_PATH = "./training_queue"
ARCHIVE_PATH = "./training_archive"

# Connect to the database and retrieve image paths
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT image_path FROM training_images")
rows = cursor.fetchall()
conn.close()

# Check all images in the database and verify their location
missing_in_queue = []
missing_in_archive = []
for row in rows:
    file_path = row[0]
    # Check if the file is missing from the training_queue directory
    if not os.path.exists(os.path.join(QUEUE_PATH, os.path.basename(file_path))):
        missing_in_queue.append(file_path)
    # Check if the file is missing from the training_archive directory
    if not os.path.exists(os.path.join(ARCHIVE_PATH, os.path.basename(file_path))):
        missing_in_archive.append(file_path)

# Print missing files with clear messages
if missing_in_queue or missing_in_archive:
    if missing_in_queue:
        print("Following files are missing from the training_queue directory:")
        for file in missing_in_queue:
            print(file)
    if missing_in_archive:
        print("\nFollowing files are missing from the training_archive directory:")
        for file in missing_in_archive:
            print(file)
else:
    print("All files in the database exist in either the training_queue or training_archive directory.")
