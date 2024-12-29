# FlowerClassifier

## Project Overview

The Flower Classifier is a machine learning-based application designed to classify images of flowers into predefined categories: Daisy, Dandelion, Rose, Sunflower and Tulip. At its core, the project utilizes a custom-trained neural network model, which I personally developed and fine-tuned using a dataset of flower images. This neural network forms the backbone of the classifier, enabling accurate predictions for the specified flower categories.

The application features an interactive web interface built with Streamlit, allowing users to upload flower images for classification. Users can also contribute to improving the model by submitting mislabeled or new images for retraining. Additionally, the project includes robust tools for dataset management, offering functionality to view training and validation dataset summaries and maintain the integrity of the training pipeline.

### Detailed Overview of Features:

- **Image Classification** Upload flower images to the application and receive accurate predictions powered by the custom-trained neural network model.

- **Model Retraining** Submit new or mislabeled images to improve the model's accuracy through the integrated retraining pipeline.

- **Dataset Insights** Easily monitor and manage the project’s datasets by viewing summaries of the training and validation data, including class distribution and image counts.

- **Streamlined Workflow** The application organizes data management efficiently, with separate pipelines for queuing and archiving images used in retraining.

## Dataset
This project uses the [Flower Dataset](https://www.kaggle.com/datasets/abhayayare/flower-dataset) from Kaggle.  
The dataset is licensed under [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/), which permits unrestricted use, modification and distribution.  
The data is freely available for download on Kaggle.

## Setup and Usage Instructions

To test the FlowerClassifier project, clone the Git repository and follow the steps in this README file. 

**1. Clone the repository from GitHub**
```bash
   git clone https://github.com/MakiIida/FlowerClassifier.git
``` 

**2. Navigate to the project directory**
```bash
   cd FlowerClassifier
``` 
**3. Activate the virtual environment**
The `.venv` directory contains the project's virtual environment, which is used to isolate Python dependencies and avoid conflicts with other projects or global installations. The required dependencies are listed in the `requirements.txt` file. To activate the virtual environment, use the following commands:

On Windows:
```bash
source .venv/Scripts/activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```
**4. Install the required libraries**
Install all necessary dependencies listed in `requirements.txt` to ensure the project runs correctly. Use the following command:

```bash
   pip install -r requirements.txt
```  

**5. Start Streamlit and verify functionality**
You can start the Streamlit application to ensure that the interface works as expected. Use either of the following commands:

With Docker Compose:
```bash
docker-compose -f docker-compose-flower.yml up --build
```

Without Docker Compose: 
```bash
streamlit run app.py
```

**6. Access the Streamlit application**
Open your browser and navigate to the following URL:

[http://localhost:8501](http://localhost:8501)

**7. Check the database status before retraining**
Run the following command to inspect the database:

```bash
python check_database.py
```

Results: This script displays all images in the database and their status. Verify that images intended for retraining are marked as Used in Training: No.

**8. Check file integrity**
Verify that all images in the database exist in either the `training_queue` or `training_archive` directories:

```bash
python check_file_integrity.py
```

Results: If files are missing, inspect potential discrepancies between the database and directories.

**9. Run the retraining process**
Start retraining the machine learning model:

```bash
python retrain_model.py
```

**10. Check the database status after retraining**
After retraining, verify the updated database status:

```bash
python check_database.py
```

Results: Confirm that the images used for retraining are now marked as Used in Training: Yes.

**11. Verify file transfers**
Ensure that images used for retraining have been moved to the `training_archive` directory:

```bash
python check_file_integrity.py
```

Results: Images used in retraining should no longer be present in the `training_queue` directory but should be moved to the `training_archive`.

The training_queue serves as a staging area for images awaiting retraining.
The training_archive stores images that have already been used for retraining.

**12. Stop the application**
If running the project with Docker Compose, shut down the containers with the following command:

```bash
docker-compose -f docker-compose-flower.yml down
```
If you started the application directly with Streamlit, stop the process by pressing Ctrl + C in the terminal where Streamlit is running.

## Project File Descriptions

`.venv` - The `.venv` directory contains the project's virtual environment.

`flowers_SavedModel` - This directory contains the pre-trained TensorFlow model used for flower classification. It is utilized by the application to predict flower categories and supports further retraining with new data.

`train_data` - This directory contains the training dataset, organized into subdirectories by flower class. These images are used to train and improve the machine learning model.

`training_archive` - This directory serves as a storage location for images that have already been used in the model retraining process. Once images in the training queue are processed, they are moved here to maintain organization. 

`training_queue` - This directory acts as a staging area for images submitted for model retraining. Images are stored here temporarily until they are processed and moved to the training_archive directory after retraining.

`val_data` - This directory contains the validation dataset, organized into subdirectories by flower class. These images are used to evaluate the model's performance after training, ensuring it generalizes well to unseen data. 

`app.py` - This file contains the Streamlit-based web interface for the flower classifier.

`check_database.py` - This script allows users to inspect the contents of the SQLite database.

`check_file_integrity.py` - This script ensures the integrity of image files by verifying their presence in the database's referenced directories and reporting any discrepancies.

`docker-compose-flowerclassifier.yml` - This file configures the FlowerClassifier application as a Docker service, enabling the application to be built, deployed and run with defined settings, including port mapping and restart policies.

`Dockerfile` - Defines a Docker container for the FlowerClassifier application, setting up the Python environment, dependencies and Streamlit on port 8501.

`inspect_database.py` - Displays the structure and contents of the SQLite database, listing all tables and the data in the training_images table.

`requirements.txt` - Lists all the Python dependencies required for the FlowerClassifier application. Use pip install -r requirements.txt to install the necessary libraries.

`retrain_model.py` - Automates the retraining of the machine learning model by processing new images submitted through the application. This script updates the model, moves processed images to an archive and ensures the database remains consistent.

`training_data.db` - This SQLite database stores metadata about the images used in the training pipeline. It tracks each image's path, label, timestamp and training status to ensure efficient and consistent model updates.

Note on `training_archive` and `training_queue` directories:
The `training_archive` and `training_queue` directories are dynamically managed by the application during the retraining process. The `training_queue` serves as a staging area for new images awaiting retraining, while the `training_archive` stores images that have already been processed. These directories function as temporary storage locations and are automatically created and updated by the application at runtime.