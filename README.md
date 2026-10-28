Email Shield — Email Spam Detection System

Deployment files:
- app.py: Streamlit web application
- model/spam_model.pkl: trained machine-learning pipeline
- requirements.txt: Python dependencies

Deploy with Streamlit Community Cloud by selecting app.py as the main file.

Note: The model was saved with scikit-learn 1.9.1, so this deployment bundle pins that version.
The original training script and datasets are not included because the live app uses the saved model and does not need to retrain.
