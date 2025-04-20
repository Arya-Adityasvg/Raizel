# Google AI Integration for Raizel

This document explains how to set up and use the Google AI integration for the Raizel application.

## Setup

1. **Get a Google API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the API key

2. **Configure the API Key**:
   - Open the `.env` file in your project directory
   - Replace `your_api_key_here` with your actual Google API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Testing the Integration

To test if your Google AI integration is working correctly, run:

```
python test_google_ai.py
```

If successful, you should see a message like:
```
✅ Google AI connection successful!
Response: Hello! How can I assist you today?
```

## Using the Google AI Integration

The `GoogleAIHelper` class provides several methods for interacting with Google's Generative AI:

### 1. Search

```python
from google_ai_integration import GoogleAIHelper

# Initialize the helper
ai_helper = GoogleAIHelper()

# Simple search
response = ai_helper.search("What are the upcoming academic events?")
print(response)

# Student-specific search
response = ai_helper.search("What are my current courses and grades?", registration_number="REG2023001")
print(response)
```

### 2. Generate Summary

```python
text = "Your long text here..."
summary = ai_helper.generate_summary(text, max_length=150)
print(summary)
```

### 3. Answer Question

```python
answer = ai_helper.answer_question("What is the deadline for course registration?")
print(answer)
```

## Example Script

Run the example script to see all features in action:

```
python example_google_ai.py
```

## Troubleshooting

If you encounter issues:

1. **API Key Invalid**: Make sure you've correctly copied your API key to the `.env` file
2. **Connection Issues**: Check your internet connection
3. **Rate Limiting**: Google AI has rate limits. If you hit them, wait a few minutes and try again

## Additional Resources

- [Google AI Documentation](https://ai.google.dev/docs)
- [Gemini Pro Model](https://ai.google.dev/models/gemini)
- [Google AI Studio](https://makersuite.google.com/) 