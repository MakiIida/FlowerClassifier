"""
This script serves as the main interface for the FlowerClassifier project, implemented using Streamlit.
It allows users to:
- Upload flower images for classification.
- View prediction results with confidence scores.
- Submit images for model retraining to improve performance.
Additionally, the script displays summaries of the training and validation datasets in a sidebar.
"""

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime
import sqlite3
import os
import uuid

# SQLite database configuration
DB_PATH = "training_data.db"
TRAIN_DIR = "./train_data"
VAL_DIR = "./val_data"

def initialize_database():
    """
    Initializes the SQLite database. Creates the 'training_images' table
    if it does not already exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            label TEXT,
            added_at TIMESTAMP,
            used_in_training BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database (only executed once)
initialize_database()

# Set up the Streamlit page title
st.title("Flower Classifier")
st.write("Upload an image of a flower, and we'll classify it into one of the flower categories!")

# Load the TensorFlow model
model_path = "./flowers_SavedModel"  # Path to the trained model
loaded_model = tf.saved_model.load(model_path)
inference_function = loaded_model.signatures["serving_default"]

# Define flower class names
class_names = ["Daisy", "Dandelion", "Rose", "Sunflower", "Tulip"]

# Function to summarize dataset contents
def data_summary(data_dir, data_type):
    """
    Summarizes the number of images per class in the given dataset directory.
    Displays the results in the Streamlit interface.
    """
    data_counts = {}
    for label in class_names:
        label_dir = os.path.join(data_dir, label)
        if os.path.exists(label_dir):
            data_counts[label] = len(os.listdir(label_dir))
        else:
            data_counts[label] = 0
    st.subheader(f"{data_type} Data Summary")
    for label, count in data_counts.items():
        st.write(f"{label}: {count} images")

# Display summaries for training and validation datasets in the sidebar
with st.sidebar:
    st.subheader("Data Summaries")
    data_summary(TRAIN_DIR, "Train")
    data_summary(VAL_DIR, "Validation")

# File uploader for user input
uploaded_file = st.file_uploader("Upload a flower image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    image_display = image.resize((500, 500))
    st.image(image_display, caption="Uploaded Image", use_container_width=50)

    # Preprocess the image for model inference
    image = image.resize((150, 150))  # Resize image to 150x150 pixels
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Prediction button
    if st.button("Predict"):
        st.write("Analyzing the image...")

        # Run inference using the model
        tensor_input = tf.convert_to_tensor(image_array, dtype=tf.float32)
        prediction = inference_function(tensor_input)
        prediction = list(prediction.values())[0].numpy()

        # Extract the predicted class and confidence
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_names[predicted_class_index]
        confidence = prediction[0][predicted_class_index]
        current_time_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]

        # Display the prediction result
        result = {
            "label": int(predicted_class_index),
            "confidence": float(confidence),
            "prediction": predicted_class,
            "timestamp": current_time_iso
        }
        st.write("Prediction:")
        st.json(result)

    # Feedback mechanism for retraining
    st.write("Not happy with the prediction? Let us know to improve the model!")
    label = st.selectbox("Select the correct label:", class_names)
    if st.button("Submit for Training"):
        try:
            # Save the image locally to the training queue directory
            unique_id = str(uuid.uuid4())
            filename = f"{label}_{unique_id}.jpg"
            filepath = os.path.join("./training_queue", filename)
            image.save(filepath)

            # Insert image details into the database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO training_images (image_path, label, added_at)
                VALUES (?, ?, ?)
            ''', (filepath, label, datetime.now()))
            conn.commit()
            conn.close()

            st.success(f"Image submitted for training: {filename}")
        except Exception as e:
            st.error(f"Error: {str(e)}")