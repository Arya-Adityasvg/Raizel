import requests
import json
import sys
import os

def check_server_running():
    """Check if the Flask server is running."""
    try:
        response = requests.get('http://127.0.0.1:3000/')
        return True, "Server is running"
    except requests.exceptions.ConnectionError:
        return False, "Server is not running. Please start the Flask application."

def check_chat_endpoint():
    """Check if the chat endpoint is working."""
    try:
        test_message = {
            "message": "Hello",
            "registration_number": "REG2023001"
        }
        response = requests.post(
            'http://127.0.0.1:3000/chat',
            json=test_message
        )
        if response.status_code == 200:
            return True, "Chat endpoint is working"
        else:
            return False, f"Chat endpoint returned status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to chat endpoint"

def check_dashboard_data():
    """Check if dashboard data can be retrieved."""
    try:
        response = requests.get('http://127.0.0.1:3000/dashboard/REG2023001')
        if response.status_code == 200:
            data = response.json()
            return True, "Dashboard data retrieved successfully"
        else:
            return False, f"Dashboard endpoint returned status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to dashboard endpoint"

def main():
    """Run all checks and report results."""
    print("Running diagnostic checks...")
    print("-" * 50)
    
    # Check server
    server_ok, server_msg = check_server_running()
    print(f"{'✅' if server_ok else '❌'} Server Status: {server_msg}")
    
    if not server_ok:
        print("\nPlease start the Flask application using:")
        print("python app.py")
        return 1
    
    # Check chat endpoint
    chat_ok, chat_msg = check_chat_endpoint()
    print(f"{'✅' if chat_ok else '❌'} Chat Endpoint: {chat_msg}")
    
    # Check dashboard data
    dashboard_ok, dashboard_msg = check_dashboard_data()
    print(f"{'✅' if dashboard_ok else '❌'} Dashboard Data: {dashboard_msg}")
    
    print("-" * 50)
    
    if server_ok and chat_ok and dashboard_ok:
        print("All systems are working correctly!")
        return 0
    else:
        print("\nSome issues were found. Please check the error messages above.")
        print("\nTroubleshooting steps:")
        print("1. Ensure all CSV files are present and properly formatted")
        print("2. Check if the Flask application is running")
        print("3. Verify that port 3000 is not being used by another application")
        print("4. Check your firewall settings")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 