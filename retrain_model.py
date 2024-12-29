"""
This script is responsible for retraining the machine learning model using new images submitted for training. 
It updates the model with new data, archives the used images, and ensures the database reflects the updated state.
"""

import os

# Suppress TensorFlow warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import sqlite3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.layers import TFSMLayer
import shutil

# Paths for database, model, and directories
DB_PATH = "training_data.db"
MODEL_PATH = "./flowers_SavedModel"
TRAINING_QUEUE_DIR = "./training_queue"
ARCHIVE_DIR = "./training_archive"

# Class names
class_names = ["Daisy", "Dandelion", "Rose", "Sunflower", "Tulip"]

def retrain_model():
    # Create archive directory if it doesn't exist
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
        print(f"Created archive directory at {ARCHIVE_DIR}")

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch images not yet used for training
    cursor.execute('''
        SELECT id, image_path, label
        FROM training_images
        WHERE used_in_training = 0
        LIMIT 5
    ''')
    images = cursor.fetchall()

    if len(images) < 5:
        print("Not enough images for retraining. At least 5 are required.")
        conn.close()
        return

    # Load images and their labels
    training_data = []
    training_labels = []
    for image_id, image_path, label in images:
        # Check if the file exists before processing
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}. Skipping...")
            continue

        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
        img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        training_data.append(img_array)
        training_labels.append(class_names.index(label))

        # Update database to mark the image as used
        cursor.execute('''
            UPDATE training_images
            SET used_in_training = 1
            WHERE id = ?
        ''', (image_id,))
        conn.commit()
        # Print confirmation of database update
        print(f"Updated database: set used_in_training = Yes for image ID {image_id}")

        # Move the image to the archive directory
        destination_path = os.path.join(ARCHIVE_DIR, os.path.basename(image_path))
        shutil.move(image_path, destination_path)
        print(f"Moved {image_path} to {destination_path}")

    if len(training_data) < 5:
        print("Not enough valid images for retraining after validation.")
        conn.close()
        return

    # Convert data to TensorFlow format
    training_data = tf.convert_to_tensor(training_data, dtype=tf.float32)
    training_labels = tf.convert_to_tensor(training_labels, dtype=tf.int32)

    # Load the existing model for inference
    base_model = tf.keras.Sequential([
        tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint='serving_default')
    ])

    # Define a function to handle TFSMLayer output
    def extract_tensor(inputs):
        # Extract the output using the specified key (assuming the key is "output_0")
        return inputs["output_0"]

    # Define a new model with additional layers for retraining
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.Lambda(extract_tensor),  # Use Lambda to extract tensor from TFSMLayer output
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(class_names), activation='softmax')  # Output layer for the classes
    ])

    # Compile the model for retraining
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Train the model with the new data
    model.fit(training_data, training_labels, epochs=5)

    # Save the updated model
    model.save(MODEL_PATH)
    print("Model retrained and saved successfully!")

    # Close the database connection
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    retrain_model()