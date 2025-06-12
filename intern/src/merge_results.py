import pandas as pd

def merge_results():
    try:
        students = pd.read_csv("student.csv")
        results = pd.read_csv("ml_evaluation_result.csv")

        # Merge both on RegisterNo
        merged = pd.merge(students, results, on="RegisterNo", how="inner")

        # Save it to marks_data.csv
        merged.to_csv("marks_data.csv", index=False)
        print("✅ Merge successful. File saved as marks_data.csv")
    except Exception as e:
        print(f"❌ Error during merge: {e}")
