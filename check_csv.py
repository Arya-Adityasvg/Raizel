import pandas as pd
import os
import sys

def check_csv_file(file_path):
    """Check if a CSV file exists and is properly formatted."""
    try:
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        # Try to read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if df.empty:
            return False, f"File is empty: {file_path}"
        
        # Return success with the number of rows and columns
        return True, f"Success! {file_path} has {len(df)} rows and {len(df.columns)} columns"
    except Exception as e:
        return False, f"Error reading {file_path}: {str(e)}"

def main():
    """Check all required CSV files."""
    csv_files = [
        'Students_Academic_Records.csv',
        'Academic_Calendar.csv',
        'SubjectWise_Marks.csv',
        'Student_Course_Details.csv'
    ]
    
    print("Checking CSV files...")
    print("-" * 50)
    
    all_files_exist = True
    all_files_valid = True
    
    for file in csv_files:
        exists, message = check_csv_file(file)
        if not exists:
            all_files_exist = False
            all_files_valid = False
            print(f"❌ {message}")
        else:
            print(f"✅ {message}")
    
    print("-" * 50)
    
    if all_files_exist and all_files_valid:
        print("All CSV files are present and properly formatted.")
        return 0
    else:
        print("Some CSV files are missing or improperly formatted.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 