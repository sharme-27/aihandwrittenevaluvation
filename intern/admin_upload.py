import streamlit as st
import pandas as pd

st.title("Admin - Upload Marks")

reg_no = st.text_input("Enter Register Number")
student_name = st.text_input("Student Name")
year = st.selectbox("Year", ["1", "2", "3"])
major = st.text_input("Major")
marks = st.number_input("Enter Marks", 0, 100)

if st.button("Submit"):
    new_data = {
        "RegisterNo": reg_no,
        "Name": student_name,
        "Year": year,
        "Major": major,
        "Marks": marks
    }
    
    try:
        df = pd.read_csv("marks_data.csv")
        df = df[df["RegisterNo"] != reg_no]  # Remove old entry
    except FileNotFoundError:
        df = pd.DataFrame()
    
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv("marks_data.csv", index=False)
    st.success("Marks submitted!")
