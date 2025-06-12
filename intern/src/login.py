import streamlit as st
import pandas as pd
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def login():
    # Background image setup
    background_image_path = r"C:\Users\SAS\OneDrive\Desktop\second\loginpic.jpg"
    if not os.path.exists(background_image_path):
        st.error(f" Background image not found at {background_image_path}")
        return

    background_base64 = get_base64_of_bin_file(background_image_path)

    # CSS for background and styling
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0,0,0,0.5)), url("data:image/png;base64,{background_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
        }}
        .title {{
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #00ffee;
            text-shadow: 2px 2px 8px #000;
            margin-top: 30px;
            margin-bottom: 0px;
        }}
        .form-container {{
            background: transparent;
            padding: 30px;
            border-radius: 20px;
            max-width: 500px;
            margin: 40px auto;
            box-shadow: none;
            color: white;
        }}
        .stTextInput > label,
        .stPasswordInput > label {{
            display: none !important;
        }}
        .stTextInput input, .stPasswordInput input {{
            background-color: #222 !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #00ffee;
        }}
        label, .css-1cpxqw2, .css-1y4p8pa {{
            font-weight: bold !important;
            color: white !important;
        }}
        .stRadio > div {{
            flex-direction: row;
            justify-content: center;
        }}
        button[kind="primary"] {{
            background-color: #00cc99;
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            margin-top: 10px;
        }}
        button[kind="primary"]:hover {{
            background-color: #00b386;
            transition: 0.3s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title
    st.markdown("<div class='title'> AI Exam Login Portal</div>", unsafe_allow_html=True)

    # Login Form
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)

    role = st.radio("🔑 Select Role", ["Admin", "Student"])
    username = st.text_input("", placeholder="🆔 Register Number (Student) /  (Admin)")
    password = st.text_input("", placeholder="🔒 Password ", type="password")

    if st.button("Login"):
        if role == "Admin":
            if username.lower() == "admin" and password == "admin123":
                st.success(" Login successful as Admin")
                st.session_state['role'] = "admin"
                st.session_state['username'] = "admin"
                st.rerun()
            else:
                st.error(" Invalid admin credentials.")
        elif role == "Student":
            try:
                student_df = pd.read_csv("data/student.csv")
                student_df.columns = student_df.columns.str.strip().str.replace(" ", "").str.lower()
                if {'registernumber', 'dob'}.issubset(student_df.columns):
                    matched = student_df[
                        (student_df['registernumber'].str.lower() == username.lower()) &
                        (student_df['dob'].astype(str) == password)
                    ]
                    if not matched.empty:
                        st.success(" Login successful as Student")
                        st.session_state['role'] = "student"
                        st.session_state['username'] = username.lower()
                        st.rerun()
                    else:
                        st.error(" Invalid student credentials.")
                else:
                    st.error(" CSV must contain 'Register Number' and 'DOB' columns.")
            except FileNotFoundError:
                st.error(" File not found: `data/student.csv`")
            except Exception as e:
                st.error(f" Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# Ensure login() runs without extra input field
if __name__ == "__main__":
    login()
