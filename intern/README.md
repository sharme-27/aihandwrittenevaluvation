# 📄 AI-Based Handwritten Answer Evaluation System

## ✨ Project Overview

This project is an **AI-powered handwritten answer sheet evaluator** that leverages **OCR (Optical Character Recognition)** to extract text from scanned images of student answer sheets and matches them against predefined keywords uploaded by the admin.

✅ **Admin uploads**:  
- Keywords per subject  
- Student answer sheet images  

✅ **System does**:  
- Text extraction via **EasyOCR**  
- Keyword-based mark calculation  
- CSV storage of evaluation  
- Marksheet generation as downloadable **PDF**  

✅ **Student can**:  
- Log in using register number and DOB  
- View evaluated marks  
- Download official PDF marksheet  

---

## 🚀 Tech Stack

| Component     | Technology Used              |
|---------------|------------------------------|
| Frontend      | Streamlit                    |
| Backend       | Python                       |
| OCR Engine    | EasyOCR                      |
| PDF Generator | FPDF                         |
| Database      | CSV / optionally Firestore   |
| Cloud Storage | Google Cloud Storage (GCS)   |

---

## 📁 Features

### 👨‍💼 Admin Dashboard:
- Upload keywords (CSV) for each subject
- Upload student handwritten answer sheets
- Automatically evaluate using OCR
- Marks calculated based on keyword matches
- Results stored in `marks_data.csv`

### 🎓 Student Dashboard:
- Student login via Register Number + DOB
- View subject-wise marks
- See Pass/Fail status
- Download PDF marksheet

### 📝 PDF Marksheet:
- Includes:
  - College Name
  - University Name
  - Student Register Number
  - Subject-wise marks
  - Pass/Fail status
  - Overall Result
  - Logo

---

## 🖼 Screenshots

| Login Page                          | Admin Panel                          | Student Dashboard                    |
|------------------------------------|--------------------------------------|--------------------------------------|
| ![login](screenshots/login.png)    | ![admin](screenshots/admin.png)      | ![student](screenshots/student.png)  |

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/ai-handwritten-evaluator.git
cd ai-handwritten-evaluator

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
