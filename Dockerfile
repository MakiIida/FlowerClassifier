# This Dockerfile is used to containerize the FlowerClassifier application.
# It defines the environment, installs dependencies, and sets up the 
# application to run on a lightweight Python-based Docker container.

# Base image with Python 3.11 slim version
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache for dependencies
COPY requirements.txt .

# Install dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining application files into the container
COPY . .

# Install additional utilities (like ping for debugging, optional)
RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose port 8501 for Streamlit (not 8000, since your CMD specifies 8501)
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]