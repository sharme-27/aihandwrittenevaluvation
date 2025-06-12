import streamlit as st
import pandas as pd
import numpy as np
import os
import easyocr
from PIL import Image

def admin_dashboard():
    # ----- CSS Styling Fixes -----
    st.markdown("""
        <style>
        .stApp {
            background-color: #f3f8ff;
            font-family: 'Segoe UI', sans-serif;
            color: #000000;
        }
        .title {
            text-align: center;
            font-size: 36px;
            color: #002b5c;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .block-box {
            background-color: #e9f1ff;
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #aac8ff;
            margin-bottom: 40px;
        }
        .stTextInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #003366;
            border-radius: 8px;
            padding: 10px;
        }
        .stFileUploader {
            border: 1px solid #0066cc !important;
            border-radius: 10px;
            background-color: #ffffff;
        }
        .stButton>button {
            background-color: #007acc;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #005fa3;
        }
        h5 {
            font-size: 20px;
            color: #003366;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'> Admin Dashboard — AI Answer Evaluation</div>", unsafe_allow_html=True)

    if "keywords" not in st.session_state:
        st.session_state["keywords"] = {}

    subjects = ["English", "Maths", "Science"]

    # ---------- Keyword Upload ----------
    st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    st.markdown("###  Upload Evaluation Keywords for Each Subject", unsafe_allow_html=True)

    for subject in subjects:
        st.markdown(f"#### {subject.capitalize()} Keywords CSV", unsafe_allow_html=True)
        uploaded_csv = st.file_uploader(f"Upload CSV for {subject}", type=["csv"], key=subject)
        if uploaded_csv:
            df = pd.read_csv(uploaded_csv)
            if "Keywords" not in df.columns:
                st.error(f" {subject} CSV must have a column named 'Keywords'")
            else:
                st.session_state["keywords"][subject] = df["Keywords"].str.lower().tolist()
                st.success(f" {subject.capitalize()} keywords uploaded successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Answer Upload & Evaluation ----------
    st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    st.markdown("###  Upload Answer Sheets and Evaluate", unsafe_allow_html=True)

    reg_no = st.text_input("Enter Student Register Number", key="register_number")

    uploaded_images = {}
    for subject in subjects:
        uploaded_images[subject] = st.file_uploader(
            f"Upload {subject} Answer Sheet", type=["png", "jpg", "jpeg"], key=subject + "_img"
        )

    if st.button("Evaluate Student") and reg_no:
        if all(subj in st.session_state["keywords"] for subj in subjects) and all(uploaded_images.values()):
            results = []
            reader = easyocr.Reader(['en'])

            for subject in subjects:
                image = Image.open(uploaded_images[subject])
                text = " ".join(reader.readtext(np.array(image), detail=0)).lower()
                keywords = st.session_state["keywords"][subject]
                matched = [kw for kw in keywords if kw in text]

                total_keywords = len(keywords)
                marks_per_keyword = 50 / total_keywords if total_keywords > 0 else 0
                marks = round(len(matched) * marks_per_keyword)
                status = "Pass" if marks >= 30 else "Fail"

                results.append({"Subject": subject, "Marks": marks, "Status": status})
                st.markdown(f"###  {subject.capitalize()}: **{marks}/50** — {status}")
                st.markdown("**Matched Keywords:**")
                st.json(matched)

            # Save result
            marks_file = "marks_data.csv"
            result_df = pd.DataFrame(results)
            result_df["Register Number"] = reg_no

            if os.path.exists(marks_file):
                existing_df = pd.read_csv(marks_file)
                existing_df = existing_df[existing_df["Register Number"] != reg_no]
                updated_df = pd.concat([existing_df, result_df], ignore_index=True)
            else:
                updated_df = result_df

            updated_df.to_csv(marks_file, index=False)
            st.success(" Evaluation completed and saved to `marks_data.csv`.")
        else:
            st.error(" Upload all keyword files and answer sheets.")

    st.markdown("</div>", unsafe_allow_html=True)

# Run
if __name__ == "__main__":
    admin_dashboard()
