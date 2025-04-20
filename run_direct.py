import os
import sys
import subprocess

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the voice_chatbot.py file
script_path = os.path.join(current_dir, "voice_chatbot.py")

# Try to run the script
try:
    print(f"Attempting to run: {script_path}")
    subprocess.run([sys.executable, script_path], check=True)
except Exception as e:
    print(f"Error: {e}")
    
input("Press Enter to exit...") 