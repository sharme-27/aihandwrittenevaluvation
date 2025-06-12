import pandas as pd
import os

def merge_results():
    student_file = "data/student_data.csv"
    eval_file = "data/ml_evaluation_results.csv"
    out_file = "data/marks_data.csv"

    if os.path.exists(student_file) and os.path.exists(eval_file):
        students = pd.read_csv(student_file)
        results = pd.read_csv(eval_file)
        merged = pd.merge(students, results, on="RegisterNo", how="inner")
        merged.to_csv(out_file, index=False)
