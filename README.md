# Network Security Phishing Detection

This is an end-to-end Machine Learning project designed to identify and classify phishing websites. It implements a complete data pipeline from ingestion to validation, transformation, and model training.

## Project Overview

The project is structured as a pipeline to predict whether a website is legitimate or a phishing attempt based on various network and website characteristics. The project automates the entire machine learning lifecycle, making it scalable and robust.

### Pipeline Stages

1. **Data Ingestion**
   - Retrieves raw network security and phishing data from a MongoDB database.
   - Splits the dataset into training and testing sets.
   - Saves the split datasets to the artifacts directory.

2. **Data Validation**
   - Validates the incoming datasets against a predefined schema.yaml to ensure correct data types and columns.
   - Computes and checks for data drift between training and testing sets, generating a report.yaml.

3. **Data Transformation**
   - Handles missing values using a K-Nearest Neighbors (KNN) Imputer.
   - Preprocesses and scales features for the machine learning models.
   - Saves the transformation object as a pickle file and the transformed data as numpy arrays.

4. **Model Training**
   - Trains classification models on the transformed training dataset.
   - Evaluates performance against target metrics and checks for overfitting/underfitting.
   - Saves the final model as a pickle file.

---

## Directory Structure

```text
NetworkSecurity/
├── data_schema/
│   └── schema.yaml
├── Network_Data/
│   └── phisingData.csv
├── networksecurity/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── constant/
│   │   └── training_pipeline/
│   │       └── __init__.py
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   ├── exception/
│   │   └── exception.py
│   ├── logging/
│   │   └── logger.py
│   ├── pipeline/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── main_utils/
│   │   │   └── utils.py
│   │   └── ml_utils/
│   └── __init__.py
├── main.py
├── mongoDB_push_data.py
├── setup.py
├── requirements.txt
└── .env
```

## Project Workflow and Data Flow

```text
+-----------------------+
|     Network_Data/     |
|   phisingData.csv     |
+-----------+-----------+
            |
            | (mongoDB_push_data.py)
            v
+-----------------------+
|     MongoDB Atlas     |
|   (Database/Table)    |
+-----------+-----------+
            |
            | (Data Ingestion)
            v
+-----------------------+
|     Data Ingestion    | ---> Splitted Train / Test Data
+-----------+-----------+
            |
            | (Data Validation)
            v
+-----------------------+
|    Data Validation    | ---> Drift Analysis & Schema Validation
+-----------+-----------+
            |
            | (Data Transformation)
            v
+-----------------------+
|  Data Transformation  | ---> KNN Imputation, Scaling & Preprocessing
+-----------+-----------+
            |
            | (Model Trainer)
            v
+-----------------------+
|     Model Trainer     | ---> Evaluated Model Artifact (model.pkl)
+-----------------------+
```

---

## Installation and Setup

### Prerequisites

- Python 3.8 or above
- A running MongoDB instance (local or Atlas)

### Steps

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd NetworkSecurity
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package and dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your MongoDB connection string (replacing `<username>` and `<password>` with your actual MongoDB Atlas database credentials):
   ```env
   MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
   
   > [!IMPORTANT]
   > Do not commit the `.env` file to your GitHub repository. The `.gitignore` file is configured to exclude `.env` to prevent sensitive database credentials from being pushed to public repositories.


---

## How to Run

1. **Extract and Push Data to MongoDB:**
   Run the following script to load the raw CSV data into your MongoDB database:
   ```bash
   python mongoDB_push_data.py
   ```

2. **Run the Training Pipeline:**
   Execute the entire end-to-end pipeline (Data Ingestion, Validation, Transformation, and Model Training):
   ```bash
   python main.py
   ```
