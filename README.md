# FlowerClassifier

## Project Overview

The Flower Classifier is a machine learning-based application designed to classify images of flowers into predefined categories, including Daisy, Dandelion, Rose, Sunflower and Tulip. This project provides an interactive web interface built with Streamlit, allowing users to upload flower images for classification. Additionally, users can contribute to improving the model by submitting mislabeled or new images for retraining. The application also offers features for dataset management, such as viewing summaries of training and validation data, and ensuring the integrity of the training pipeline.

Key features include:

- Image Classification: Upload flower images to get accurate predictions.
- Model Retraining: Enhance the model by submitting images for retraining.
- Dataset Insights: View statistics for the training and validation datasets.
- Streamlined Workflow: Manage training data with an organized pipeline for queuing and archiving images.

---

## Dataset
This project uses the [Flower Dataset](https://www.kaggle.com/datasets/abhayayare/flower-dataset) from Kaggle.  
The dataset is licensed under [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/), which permits unrestricted use, modification, and distribution.  
The data is freely available for download on Kaggle.

---

## Setup and Usage Instructions

Below is the step-by-step guide to setting up and using the FlowerClassifier project. 

1. **Navigate to the project directory:**
```bash
   cd ~/code/FlowerClassifier
``` 

2. Activate the virtual environment: The .venv directory contains the project's virtual environment, used to isolate Python dependencies to avoid conflicts with other projects or global installations. The required dependencies are listed in the requirements.txt file. To activate the virtual environment, use the following commands:

On Windows: source .venv/Scripts/activate
On macOS/Linux: source .venv/bin/activate

3. Start Streamlit and verify functionality. You can start the Streamlit application to ensure that the interface works as expected. Use either of the following commands:

With Docker Compose: docker-compose -f docker-compose-flower.yml up --build
Without Docker Compose: streamlit run app.py

4. Access the Streamlit application. Open your browser and navigate to:

http://localhost:8501

5. Check the database status before retraining. Run the following command to inspect the database:

python check_database.py

Results: This script displays all images in the database and their status. Verify that images intended for retraining are marked as Used in Training: No.

6. Check file integrity. Verify that all images in the database exist in either the training_queue or training_archive directories:

python check_file_integrity.py

Results: If files are missing, inspect potential discrepancies between the database and directories.

7. Run the retraining process. Start retraining the machine learning model:

python retrain_model.py

8. Check the database status after retraining. After retraining, verify the updated database status:

python check_database.py

Results: Confirm that the images used for retraining are now marked as Used in Training: Yes.

9. Verify file transfers. Ensure that images used for retraining have been moved to the training_archive directory:

python check_file_integrity.py

Results: Images used in retraining should no longer be present in the training_queue directory but should be moved to the training_archive.

The training_queue serves as a staging area for images awaiting retraining.
The training_archive stores images that have already been used for retraining.


10. Stop the containers. If running the project with Docker Compose, shut down the containers with the following command:

docker-compose -f docker-compose-flower.yml down

---

## Project File Descriptions

.venv - The .venv directory contains the project's virtual environment.

flowers_SavedModel - This directory contains the pre-trained TensorFlow model used for flower classification. It is utilized by the application to predict flower categories and supports further retraining with new data.

train_data - This directory contains the training dataset, organized into subdirectories by flower class. These images are used to train and improve the machine learning model.

training_archive - This directory serves as a storage location for images that have already been used in the model retraining process. Once images in the training queue are processed, they are moved here to keep the training queue organized. 

training_queue - This directory acts as a staging area for images submitted for model retraining. Images are stored here temporarily until they are processed and moved to the training_archive directory after retraining.

val_data - This directory contains the validation dataset, organized into subdirectories by flower class. These images are used to evaluate the model's performance after training, ensuring it generalizes well to unseen data. 

app.py - This file contains the Streamlit-based web interface for the flower classifier.

check_database.py - This script allows users to inspect the contents of the SQLite database.

check_file_integrity.py - This script ensures the integrity of image files by verifying their presence in the database's referenced directories and reporting any discrepancies.

docker-compose-flowerclassifier.yml - This file configures the FlowerClassifier application as a Docker service, enabling the application to be built, deployed, and run with defined settings, including port mapping and restart policies.

Dockerfile - Defines a Docker container for the FlowerClassifier application, setting up the Python environment, dependencies, and Streamlit on port 8501.

inspect_database.py - Displays the structure and contents of the SQLite database, listing all tables and the data in the training_images table.

requirements.txt - Lists all the Python dependencies required for the FlowerClassifier application. Use pip install -r requirements.txt to install the necessary libraries.

retrain_model.py - Automates the retraining of the machine learning model by processing new images submitted through the application. This script updates the model, moves processed images to an archive, and ensures the database remains consistent.

training_data.db - This SQLite database stores metadata about the images used in the training pipeline. It tracks each image's path, label, timestamp, and training status to ensure efficient and consistent model updates.