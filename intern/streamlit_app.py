import streamlit as st
from src.login import login
from src.admin_dashboard import admin_dashboard
from src.student_dashboard import student_dashboard

def main():
    if 'role' not in st.session_state:
        login()
    elif st.session_state['role'] == 'admin':
        admin_dashboard()
    elif st.session_state['role'] == 'student':
        student_dashboard()

if __name__ == '__main__':
    main()
