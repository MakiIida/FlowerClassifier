# FlowerClassifier/app.py

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime

# Set up the Streamlit page title
st.title("Flower Classifier")
st.write("Upload an image of a flower, and we'll classify it into one of the flower categories!")

# Load the TensorFlow model
model_path = "./flowers_SavedModel"  # Path to the trained model
loaded_model = tf.saved_model.load(model_path)
inference_function = loaded_model.signatures["serving_default"]

# Define class names
class_names = ["Daisy", "Dandelion", "Rose", "Sunflower", "Tulip"]

# File uploader for image input
uploaded_file = st.file_uploader("Upload a flower image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    image_display = image.resize((500, 500))
    st.image(image_display, caption="Uploaded Image", use_container_width=50)

    # Preprocess the image
    image = image.resize((150, 150))  # Resize image to 150x150 pixels
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Add a button for prediction
    if st.button("Predict"):
        st.write("Analyzing the image...")

        # Perform inference using the model
        tensor_input = tf.convert_to_tensor(image_array, dtype=tf.float32)
        prediction = inference_function(tensor_input)
        prediction = list(prediction.values())[0].numpy()

        predicted_class_index = np.argmax(prediction)
        predicted_class = class_names[predicted_class_index]
        confidence = prediction[0][predicted_class_index]
        current_time_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]

        # Display prediction results
        result = {
            "label": int(predicted_class_index),
            "confidence": float(confidence),
            "prediction": predicted_class,
            "timestamp": current_time_iso
        }
        st.write("Prediction:")
        st.json(result)

    # Add feedback for model improvement
    st.write("Not happy with the prediction? Let us know to improve the model!")
    label = st.selectbox("Select the correct label:", class_names)
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! The model will be improved.")