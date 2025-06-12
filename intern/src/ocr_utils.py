import easyocr
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_text_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    return ' '.join(result)

def predict_marks(text):
    with open("src/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("src/ml_model.pkl", "rb") as f:
        model = pickle.load(f)
    features = vectorizer.transform([text])
    return round(float(model.predict(features)[0]), 2)
