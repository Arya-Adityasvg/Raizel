import pandas as pd
import os

def test_csv_files():
    csv_files = [
        'Students_Academic_Records.csv',
        'Academic_Calendar.csv',
        'SubjectWise_Marks.csv',
        'Student_Course_Details.csv'
    ]
    
    for file in csv_files:
        try:
            print(f"Testing {file}...")
            df = pd.read_csv(file)
            print(f"Successfully loaded {file} with {len(df)} rows and {len(df.columns)} columns")
            print(f"Columns: {df.columns.tolist()}")
            print(f"First row: {df.iloc[0].to_dict()}")
            print("-" * 50)
        except Exception as e:
            print(f"Error loading {file}: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")
    test_csv_files() 