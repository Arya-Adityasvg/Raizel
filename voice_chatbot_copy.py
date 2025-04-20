import speech_recognition as sr
import pyttsx3 as tts
import time
import os
from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup as bs
import re
import sys
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
import urllib.parse
import wikipedia
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import glob

class Raizel:
    def __init__(self):
        try:
            # Download required NLTK data
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('punkt')
                nltk.download('stopwords')

            # Initialize speech recognizer with optimized settings
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 3000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8  # Reduced for faster response
            
            # Initialize text-to-speech engine
            self.engine = tts.init()
            
            # Set voice properties for Hugh Jackman-like voice
            voices = self.engine.getProperty('voices')
            male_voice = None
            for voice in voices:
                if "male" in voice.name.lower():
                    male_voice = voice
                    break
            
            if male_voice:
                self.engine.setProperty('voice', male_voice.id)
                self.engine.setProperty('rate', 145)
                self.engine.setProperty('volume', 0.9)
                print("Voice set to male voice successfully!")
            else:
                print("No male voice found, using default voice")
                self.engine.setProperty('voice', voices[0].id)
                self.engine.setProperty('rate', 145)
                self.engine.setProperty('volume', 0.9)
            
            # Load environment variables if any
            load_dotenv()
            
            # Load CSV files
            self.load_csv_files()
            
            # Dictionary of responses with more natural language
            self.responses = {
                "hello": "Hello! I'm Raizel, your AI assistant. How can I help you today?",
                "hi": "Hi there! How can I assist you?",
                "hey": "Hey! What can I do for you?",
                "how are you": "I'm functioning perfectly, thank you for asking!",
                "what's your name": "I'm Raizel, your AI assistant. I can help you search the internet and answer your questions!",
                "goodbye": "Goodbye! Have a great day!",
                "bye": "See you later!",
                "search": "Let me search that for you.",
                "default": "I'm not sure about that. Would you like me to search the internet for more information?"
            }
            
            # Search keywords for better command recognition
            self.search_keywords = [
                "search", "find", "look up", "what is", "who is", 
                "tell me about", "explain", "define", "meaning of"
            ]
            
            # CSV-related keywords
            self.csv_keywords = [
                "student", "academic", "marks", "grades", "course",
                "subject", "calendar", "record", "performance"
            ]
            
            print("Raizel initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing Raizel: {str(e)}")
            sys.exit(1)

    def load_csv_files(self):
        """Load all CSV files in the workspace"""
        try:
            self.csv_data = {}
            csv_files = glob.glob("*.csv")
            
            for file in csv_files:
                try:
                    df = pd.read_csv(file)
                    self.csv_data[file] = df
                    print(f"Successfully loaded {file}")
                except Exception as e:
                    print(f"Error loading {file}: {str(e)}")
            
            if not self.csv_data:
                print("Warning: No CSV files were loaded successfully")
        except Exception as e:
            print(f"Error loading CSV files: {str(e)}")

    def query_csv_data(self, query):
        """Query the loaded CSV data based on user input"""
        try:
            query = query.lower()
            results = []
            
            # Check each CSV file for relevant information
            for file_name, df in self.csv_data.items():
                # Convert column names to lowercase for case-insensitive matching
                columns = [col.lower() for col in df.columns]
                
                # Check if query matches any column names
                matching_columns = [col for col in columns if query in col]
                
                if matching_columns:
                    # Get the first few rows of matching columns
                    for col in matching_columns:
                        original_col = df.columns[columns.index(col)]
                        sample_data = df[original_col].head(3).to_string()
                        results.append(f"In {file_name}, {col} data: {sample_data}")
            
            if results:
                return "\n".join(results)
            else:
                return None
        except Exception as e:
            print(f"Error querying CSV data: {str(e)}")
            return None

    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_relevant_content(self, soup):
        """Extract relevant content from webpage"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'aside']):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        text = self.clean_text(text)
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        # Remove short sentences and clean them
        sentences = [s.strip() for s in sentences if len(s.split()) > 5]
        
        return sentences

    def find_best_answer(self, query, sentences):
        """Find the most relevant sentence based on the query"""
        # Clean the query
        query = self.clean_text(query.lower())
        query_words = set(query.split())
        
        # Remove stopwords from query
        stop_words = set(stopwords.words('english'))
        query_words = query_words - stop_words
        
        best_score = 0
        best_sentence = None
        
        for sentence in sentences:
            sentence = sentence.lower()
            # Count matching words
            score = sum(1 for word in query_words if word in sentence)
            if score > best_score:
                best_score = score
                best_sentence = sentence
        
        return best_sentence

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            # Search Wikipedia
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=2)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple matches, use the first option
            return wikipedia.summary(e.options[0], sentences=2)
        except wikipedia.exceptions.PageError:
            return None
        except Exception as e:
            print(f"Wikipedia search error: {str(e)}")
            return None

    def search_google(self, query):
        """Search using Google Custom Search API"""
        try:
            # Get API key and CSE ID from environment variables
            api_key = os.getenv('GOOGLE_API_KEY')
            cse_id = os.getenv('GOOGLE_CSE_ID')
            
            if not api_key or not cse_id:
                return "Google search is not configured. Please set up API credentials in the .env file."
                
            # Build the service
            service = build('customsearch', 'v1', developerKey=api_key)
            
            # Execute the search
            result = service.cse().list(q=query, cx=cse_id, num=3).execute()
            
            if 'items' in result:
                # Get the snippet from the first result
                return result['items'][0]['snippet']
            
            return None
            
        except HttpError as e:
            print(f"Google search error: {str(e)}")
            return None
        except Exception as e:
            print(f"Google search error: {str(e)}")
            return None

    def search_internet(self, query):
        """Search the internet using multiple sources"""
        try:
            # Format the search query
            search_query = query
            if not any(word in query.lower() for word in ["what", "who", "how", "when", "where", "why"]):
                search_query = f"what is {query}"
            
            # Try Wikipedia first
            wiki_result = self.search_wikipedia(search_query)
            if wiki_result:
                return f"According to Wikipedia, {wiki_result}"
            
            # If Wikipedia fails, try Google
            google_result = self.search_google(search_query)
            if google_result:
                return f"According to Google, {google_result}"
            
            return "I couldn't find any information about that. Would you like to try a different search?"
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return "I encountered an error while searching. Please try again."

    def process_voice_input(self, audio_file_path):
        """Process voice input from a file and return the response"""
        try:
            print(f"Opening audio file: {audio_file_path}")
            with sr.AudioFile(audio_file_path) as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Recording audio...")
                audio = self.recognizer.record(source)
                print("Sending to Google Speech Recognition...")
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized text: {text}")
                return self.get_response(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "I couldn't understand the audio. Could you please try again?"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {str(e)}")
            return f"Could not request results from Google Speech Recognition service; {str(e)}"
        except Exception as e:
            print(f"Error processing voice input: {str(e)}")
            import traceback
            traceback.print_exc()
            return "Sorry, I encountered an error processing your voice input. Please try again."

    def listen(self):
        """Listen for voice input and return the recognized text"""
        try:
            with sr.Microphone() as source:
                print("\nListening... (speak now)")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    # Wait for user to speak
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Process the audio
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text.lower()
                    
                except sr.WaitTimeoutError:
                    print("No speech detected within timeout period.")
                    return None
                    
                except sr.UnknownValueError:
                    print("I couldn't understand that. Could you please repeat?")
                    return None
                    
                except sr.RequestError:
                    print("I'm having trouble connecting to the speech service. Please check your internet connection.")
                    return None
                    
        except Exception as e:
            print(f"Error during listening: {str(e)}")
            return None

    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"Raizel: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during speech: {str(e)}")

    def get_response(self, text):
        """Get appropriate response based on input text"""
        if not text:
            return self.responses["default"]
            
        # Check for CSV-related queries
        if any(keyword in text.lower() for keyword in self.csv_keywords):
            csv_result = self.query_csv_data(text)
            if csv_result:
                return csv_result
            
        # Check for search-related keywords
        for keyword in self.search_keywords:
            if keyword in text:
                query = text.split(keyword)[-1].strip()
                return self.search_internet(query)
            
        # Check for other predefined responses
        for key in self.responses:
            if key in text:
                return self.responses[key]
                
        return self.responses["default"]

    def run(self):
        """Main loop for the chatbot with improved error handling"""
        try:
            self.speak("Hello! I'm Raizel, your AI assistant. I can help you search the internet and answer your questions. How can I assist you today?")
            
            while True:
                # Wait for user input
                text = self.listen()
                
                if text:
                    if any(word in text for word in ["goodbye", "bye", "exit", "quit"]):
                        self.speak(self.responses["goodbye"])
                        break
                        
                    response = self.get_response(text)
                    self.speak(response)
                
                # Add a small delay between iterations
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            self.speak("Goodbye! Have a great day!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self.speak("I encountered an error. Please restart me.")

if __name__ == "__main__":
    try:
        raizel = Raizel()
        raizel.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1) 
        