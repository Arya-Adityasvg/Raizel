import os
import sys
import subprocess
import pandas as pd
import requests
import json
import time
import webbrowser
from pathlib import Path

def check_python_installation():
    """Check if Python is installed and accessible."""
    print("Checking Python installation...")
    try:
        python_version = subprocess.check_output(["py", "--version"], stderr=subprocess.STDOUT).decode().strip()
        print(f"✅ Python is installed: {python_version}")
        return True
    except Exception as e:
        print(f"❌ Python is not accessible: {str(e)}")
        print("Please install Python from https://www.python.org/downloads/")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\nChecking dependencies...")
    required_packages = [
        "flask", "flask-login", "werkzeug", "flask-socketio", "python-socketio",
        "pandas", "numpy", "SpeechRecognition", "pyttsx3", "python-dotenv",
        "requests", "beautifulsoup4", "nltk", "wikipedia-api", "google-api-python-client"
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            all_installed = False
    
    if not all_installed:
        print("\nInstalling missing dependencies...")
        try:
            subprocess.check_call(["py", "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
        except Exception as e:
            print(f"❌ Error installing dependencies: {str(e)}")
            return False
    
    return True

def check_csv_files():
    """Check if all required CSV files exist and are properly formatted."""
    print("\nChecking CSV files...")
    required_csv_files = [
        "Students_Academic_Records.csv",
        "Academic_Calendar.csv",
        "SubjectWise_Marks.csv",
        "Student_Course_Details.csv"
    ]
    
    all_files_exist = True
    all_files_valid = True
    
    for file in required_csv_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
            try:
                df = pd.read_csv(file)
                if df.empty:
                    print(f"❌ {file} is empty")
                    all_files_valid = False
                else:
                    print(f"✅ {file} has {len(df)} rows and {len(df.columns)} columns")
            except Exception as e:
                print(f"❌ Error reading {file}: {str(e)}")
                all_files_valid = False
        else:
            print(f"❌ {file} does not exist")
            all_files_exist = False
    
    if not all_files_exist:
        print("\nSome CSV files are missing. Please ensure all required CSV files are present.")
        return False
    
    if not all_files_valid:
        print("\nSome CSV files are not properly formatted. Please check the file formats.")
        return False
    
    return True

def check_server_running():
    """Check if the Flask server is running."""
    print("\nChecking if the server is running...")
    try:
        response = requests.get("http://127.0.0.1:3000/", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        return False

def start_server():
    """Start the Flask server."""
    print("\nStarting the Flask server...")
    try:
        # Create a new process to run the server
        server_process = subprocess.Popen(["py", "app.py"], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         text=True)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the server is running
        if check_server_running():
            print("✅ Server started successfully")
            return server_process
        else:
            print("❌ Failed to start the server")
            server_process.terminate()
            return None
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        return None

def open_browser():
    """Open the application in the default browser."""
    print("\nOpening the application in your default browser...")
    try:
        webbrowser.open("http://127.0.0.1:3000")
        print("✅ Browser opened successfully")
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {str(e)}")
        return False

def main():
    """Run all diagnostic checks and fix issues."""
    print("=" * 50)
    print("RAIZEL DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Check Python installation
    if not check_python_installation():
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check CSV files
    if not check_csv_files():
        return 1
    
    # Check if server is running
    server_running = check_server_running()
    
    # Start server if not running
    server_process = None
    if not server_running:
        server_process = start_server()
        if not server_process:
            return 1
    
    # Open browser
    open_browser()
    
    print("\n" + "=" * 50)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 50)
    print("\nIf you're still experiencing issues, please try the following:")
    print("1. Check your firewall settings and ensure port 3000 is not blocked")
    print("2. Try using a different browser")
    print("3. Restart your computer and try again")
    print("4. Check if any antivirus software is blocking the application")
    
    # Keep the script running if we started the server
    if server_process:
        print("\nPress Ctrl+C to stop the server and exit...")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 