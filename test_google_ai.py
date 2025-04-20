import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_google_ai_connection():
    """Test the connection to Google AI API."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            print("❌ Error: API key not configured")
            print("Please follow these steps:")
            print("1. Go to https://makersuite.google.com/app/apikey")
            print("2. Sign in with your Google account")
            print("3. Click 'Create API Key'")
            print("4. Copy the generated API key")
            print("5. Update the GOOGLE_API_KEY in your .env file")
            return False
        
        # Configure the Google AI client
        genai.configure(api_key=api_key)
        
        # Test the connection with a simple query
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        response = model.generate_content("Hello, are you working?")
        
        if response and response.text:
            print("✅ Successfully connected to Google AI!")
            print("Response:", response.text)
            return True
        else:
            print("❌ Error: No response from Google AI")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Google AI: {str(e)}")
        return False

if __name__ == "__main__":
    test_google_ai_connection() 