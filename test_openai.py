import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return False
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, this is a test message."}
            ],
            max_tokens=5
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to OpenAI API: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection() 