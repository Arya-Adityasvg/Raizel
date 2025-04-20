import os
import sys
import subprocess
import webbrowser
from time import sleep

def check_dependencies():
    """Check if required packages are installed."""
    print("🔍 Checking dependencies...")
    try:
        import flask
        import pandas
        import google.generativeai
        import python_dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {str(e)}")
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n🔍 Checking .env file...")
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        if "GOOGLE_API_KEY" not in content:
            print("❌ GOOGLE_API_KEY not found in .env file")
            return False
    
    print("✅ .env file is properly configured")
    return True

def check_data_files():
    """Check if required data files exist."""
    print("\n🔍 Checking data files...")
    required_files = [
        "Students_Academic_Records.csv",
        "Academic_Calendar.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required data files are present")
    return True

def start_application():
    """Start the Flask application."""
    print("\n🚀 Starting the application...")
    
    # Open the application in the default browser
    def open_browser():
        sleep(2)  # Wait for the server to start
        webbrowser.open("http://127.0.0.1:3000")
    
    # Start the browser in a separate thread
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start the Flask application
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")

def main():
    """Main deployment function."""
    print("=" * 50)
    print("📦 Deploying Raizel Application")
    print("=" * 50)
    
    # Check all requirements
    if not all([
        check_dependencies(),
        check_env_file(),
        check_data_files()
    ]):
        print("\n❌ Deployment failed: Some requirements are not met")
        return
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main() 