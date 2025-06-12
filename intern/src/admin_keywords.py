import streamlit as st
import pandas as pd
import easyocr
import numpy as np
import cv2
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from src.merge_results import merge_results

# Load model and vectorizer
base_path = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_path, "ml_model.pkl"))
vectorizer = joblib.load(os.path.join(base_path, "vectorizer.pkl"))

# OCR using EasyOCR
def extract_text_easyocr(image_file):
    reader = easyocr.Reader(['en'])
    bytes_data = image_file.read()
    np_array = np.frombuffer(bytes_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    result = reader.readtext(image, detail=0)
    return " ".join(result)

# Evaluate text using ML model
def evaluate_text_ml(extracted_text):
    X = vectorizer.transform([extracted_text])
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0].max()
    return prediction, round(probability * 100, 2)

# Main Admin Dashboard
def admin_dashboard():
    st.header("🧠 Admin Dashboard - ML-based Evaluation")

    keyword_file = st.file_uploader("📄 Upload Keywords (CSV or TXT)", type=["csv", "txt"])
    student_reg = st.text_input("🎓 Enter Student Register Number")
    image_file = st.file_uploader("🖼️ Upload Answer Sheet Image", type=["jpg", "jpeg", "png"])

    if st.button("🚀 Submit for Evaluation"):
        if keyword_file and student_reg and image_file:
            if not student_reg.startswith("student"):
                st.error("❌ Register number must start with 'student'")
                return

            extracted_text = extract_text_easyocr(image_file)
            prediction, confidence = evaluate_text_ml(extracted_text)

            st.success(f"✅ Evaluation Complete for {student_reg}")
            st.write(f"📊 Prediction: {'Correct' if prediction == 1 else 'Incorrect'}")
            st.write(f"📈 Confidence: {confidence}%")

            marks = 10 if prediction == 1 else 0

            result_data = {
                "RegisterNo": student_reg,
                "Marks": marks
            }

            result_df = pd.DataFrame([result_data])

            # Save or append the result to CSV (ensure header only once)
            result_file = "ml_evaluation_result.csv"
            if os.path.exists(result_file):
                result_df.to_csv(result_file, mode='a', index=False, header=False)
            else:
                result_df.to_csv(result_file, index=False)

        else:
            st.warning("⚠️ Please upload all required files and fill the register number.")

    # Add a button to merge results with student data
    st.markdown("---")
    st.subheader("📎 Merge Evaluation with Student Data")
    if st.button("📂 Merge and Save Results"):
        try:
            merge_results()
            st.success("✅ Student data and marks merged into `marks_data.csv` successfully!")
        except Exception as e:
            st.error(f"❌ Error during merging: {e}")
