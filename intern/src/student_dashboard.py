import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
import tempfile

# ---------- PDF Generator ----------
class PDFWithWatermark(FPDF):
    def header(self):
        # Watermark (center of page)
        try:
            self.image("logo.jpg", x=55, y=90, w=100, h=100)
        except:
            pass  # If logo not found, skip

def generate_marksheet_pdf(reg_no, student_name, student_rows):
    pdf = PDFWithWatermark()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Stella Maris College", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "Beauroi University", ln=1, align='C')
    pdf.ln(10)

    # Student Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, f"Register Number: {reg_no}", ln=1)
    pdf.cell(100, 10, f"Name: {student_name}", ln=1)
    pdf.ln(5)

    # Table headers
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Subject", 1)
    pdf.cell(40, 10, "Marks", 1)
    pdf.cell(40, 10, "Status", 1, ln=1)

    # Table rows
    pdf.set_font("Arial", '', 12)
    total = 0
    passed_all = True
    for _, row in student_rows.iterrows():
        subject = row.get("subject", "N/A").capitalize()
        marks = int(row.get("marks", 0))
        status = "Pass" if marks >= 30 else "Fail"
        if marks < 30:
            passed_all = False
        total += marks
        pdf.cell(80, 10, subject, 1)
        pdf.cell(40, 10, str(marks), 1)
        pdf.cell(40, 10, status, 1, ln=1)

    # Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.ln(5)
    max_marks = 50 * len(student_rows)
    overall_status = "Pass" if passed_all else "Fail"
    pdf.cell(100, 10, f"Total Marks: {total} / {max_marks}", ln=1)
    pdf.cell(100, 10, f"Overall Result: {overall_status}", ln=1)

    # Save PDF
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# ---------- Streamlit Dashboard ----------
def student_dashboard():
    st.markdown("<div class='custom-title'> Student Dashboard</div>", unsafe_allow_html=True)

    reg_no = st.session_state.get("username")
    if not reg_no:
        reg_no = st.text_input("Enter your Register Number")

    if not reg_no:
        st.warning("Please enter your Register Number.")
        return

    try:
        df_marks = pd.read_csv("marks_data.csv")
        df_students = pd.read_csv("student.csv")

        # Clean column names
        df_marks.columns = df_marks.columns.str.strip().str.lower().str.replace(" ", "")
        df_students.columns = df_students.columns.str.strip().str.lower().str.replace(" ", "")

        if 'registernumber' not in df_marks.columns or 'registernumber' not in df_students.columns:
            st.error("Required column 'RegisterNumber' not found.")
            return

        student_rows = df_marks[df_marks['registernumber'].str.lower() == reg_no.lower()]
        student_info = df_students[df_students['registernumber'].str.lower() == reg_no.lower()]

        if student_rows.empty or student_info.empty:
            st.warning("Record not found.")
            return

        student_name = student_info.iloc[0]['name']
        st.success(f" Record found for {student_name}")
        st.dataframe(student_rows)

        if st.button(" Download Marksheet (PDF)"):
            pdf_path = generate_marksheet_pdf(reg_no, student_name, student_rows)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇ Download PDF",
                    data=f,
                    file_name=f"{reg_no}_marksheet.pdf",
                    mime="application/pdf"
                )

    except FileNotFoundError as e:
        st.error(f" File not found: {e.filename}")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------- Run ----------
if "rerun_triggered" not in st.session_state:
    st.session_state["rerun_triggered"] = True
    st.rerun()
else:
    student_dashboard()
