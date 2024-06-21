# HyFish Models Deployment

## Table of Contents

1. [Project Overview](#1-project-overview)
1. [Prerequisites](#2-installation)
1. [Configuration](#configuration)
   - [Environment Variables](#environment-variables)
   - [GCP Credentials](#gcp-credentials)
1. [Accessing The Deployment](#accessing-the-deployment)

---

## 1. Project Overview

This project is a deployment for Machine Learning models used by HyFish app

## 2. Prerequisites

1. Git
1. Docker
1. Python 3.11 (Optional for Development / Local)

## 3. Configuration

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP servic account credentials file (`JSON`)
- `BUCKET_NAME`: GCP Cloud Storage Bucket name
- `CLASSIFIER_MODEL_PATH`: Path to Fish Classifier model file relative to GCP bucket (`H5`)
- `FRESHNESS_MODEL_PATH`: Path to Freshness Prediction model file relative to GCP bucket (`YOLO`)
- `TOXIC_MODEL_PATH`: Path to Toxic Classifier model file relative to GCP bucket (`H5`)
- `TOXIC_TOKENIZER_PATH`: Path to Tokenizer file for Toxic Classifier relative to GCP bucket (`Joblib`)
- `TF_ENABLE_ONEDNN_OPTS`: Set to `0` to turn off TensorFlow oneDNN optimizations

### GCP Credentials
Create a `service-account.json` file and place it in the `model-deployment` directory, it should contain the key from the service account that has storage admin permission to the GCS bucket.

## 4. Build and Run the project
- Development / Local

    create and use venv

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

    Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

    Run the project

    ```bash
    python run.py
    ```

- Production

    Clone the repository to your local machine:
    
    ```bash
    git clone https://github.com/hyfish-capstone-project/model-deployment.git
    cd model-deployment
    ```
    
    Build the Docker image
    
    ```bash
    docker build -t hyfish-model .
    ```
    
    Run the Docker Container
    
    ```bash
    docker run --net DOCKER_NETWORK_NAME --ip CUSTOM_INTERNAL_IP -d -p 5000:5000 --name hyfish-model-container hyfish-model
    ```

## 5. Accessing The Deployment
- Development / Local
    - Fish Classification URL: 
        
        `http://localhost:5000/api/predict`
    - Fish Freshness Detection URL: 
        
        `http://localhost:5000/api/freshness`
    - Toxic Classification URL: 
        
        `http://localhost:5000/api/toxic`

- Production
    - Fish Classification URL: 
        
        `http://CUSTOM_INTERNAL_IP:5000/api/predict`
    - Fish Freshness Detection URL: 
        
        `http://CUSTOM_INTERNAL_IP:5000/api/freshness`
    - Toxic Classification URL: 
        
        `http://CUSTOM_INTERNAL_IP:5000/api/toxic`