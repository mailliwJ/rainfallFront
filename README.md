# Rainfall Application
This project is a full-stack web application for predicting rainfall using climatic data. It consists of:
- Backend: A Flask API for making rainfall predictions, retraining the model, and saving updated data.
- Frontend: A Streamlit app for user interaction, including uploading data, retraining the model, and viewing evaluation metrics.

# Features

## Fronend
Interactive UI built with Streamlit which allow users to:
- Input climatic parameters to predict rainfall.
- Upload new datasets to retrain the model.
- Compare model performance on old and updated datasets.
- Save updated models and datasets if performance improves.

## Backend
Flask API endpoints for:
- /predict: Predict rainfall using climatic parameters.
- /retrain_save: Upload new data, retrain the model and save updated models and datasets after evaluation.

Offers integration with pre-trained models and scalable infrastructure.

## Project Structure

## Setup Instructions

## Usage
1. Make Predictions
- Go to the "Predict" section in the Streamlit app.
- Enter climatic parameters (e.g., cloud cover, sunshine, temperature).
- Click "Predict Rainfall" to get the predicted rainfall in mm.
2. Retrain the Model
- Go to the "Retrain Model" section.
- Upload a CSV file containing the new dataset.
- Click "Retrain & Evaluate" to compare metrics on the original and updated datasets.
3. Save Updated Model
- If the updated model performs better, click "Save Dataset and Retrain Model" to update the backend.

## API Endpoints

|Endpoint	   |Method	|Description|
|--------------|--------|-|
|/predict	   |POST	|Predict rainfall based on climatic parameters|
|/retrain_save |POST	|Evaluate model metrics using an uploaded dataset|
|/retrain_save |PUT	    |Save updated datasets and models after retraining|

## Technologies Used
Frontend: Streamlit
Backend: Flask
Machine Learning: Scikit-Learn
Deployment: PythonAnywhere, Streamlit Community Cloud
Version Control: GitHub

## Example CSV File
An example dataset for retraining:

|date    |cloud_cover|sunshine|global_radiation|max_temp|mean_temp|min_temp|precipitation|pressure|snow_depth|
|--------|-----------|--------|----------------|--------|---------|--------|-------------|--------|----------|
|19790101|2.0        |7.0     |52.0            |2.3     |-4.1     |-7.5    |0.4          |101900  |9.0       |
|19790102|6.0        |1.7     |27.0            |1.6     |-2.6     |-7.5    |0.0          |102530  |8.0       |

