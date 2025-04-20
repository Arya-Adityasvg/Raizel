import os
import json
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GoogleAIHelper:
    def __init__(self):
        """Initialize the Google AI client."""
        # Get API key from environment variables
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            print("Please add your Google API key to the .env file")
            print("Example: GOOGLE_API_KEY=your_api_key_here")
            return
        
        # Configure the Google AI client
        genai.configure(api_key=api_key)
        
        # Set up the model
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        print("Google AI initialized successfully")
        
        # Load CSV data for context
        self.load_csv_data()
    
    def load_csv_data(self):
        """Load CSV data for context-aware responses."""
        self.csv_data = {}
        csv_files = [
            'Students_Academic_Records.csv',
            'Academic_Calendar.csv',
            'SubjectWise_Marks.csv',
            'Student_Course_Details.csv'
        ]
        
        for file in csv_files:
            try:
                if os.path.exists(file):
                    df = pd.read_csv(file)
                    self.csv_data[file] = df
                    print(f"Loaded {file} for context")
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
    
    def get_student_context(self, registration_number):
        """Get context about a specific student."""
        context = ""
        
        # Get student profile
        if 'Students_Academic_Records.csv' in self.csv_data:
            student_data = self.csv_data['Students_Academic_Records.csv']
            student = student_data[student_data['Registration_Number'] == registration_number]
            if not student.empty:
                student_info = student.iloc[0].to_dict()
                context += f"Student Profile: {json.dumps(student_info)}\n\n"
        
        # Get student marks
        if 'SubjectWise_Marks.csv' in self.csv_data:
            marks_data = self.csv_data['SubjectWise_Marks.csv']
            student_marks = marks_data[marks_data['Registration_Number'] == registration_number]
            if not student_marks.empty:
                marks_info = student_marks.to_dict('records')
                context += f"Student Marks: {json.dumps(marks_info)}\n\n"
        
        # Get student courses
        if 'Student_Course_Details.csv' in self.csv_data:
            course_data = self.csv_data['Student_Course_Details.csv']
            student_courses = course_data[course_data['Registration_Number'] == registration_number]
            if not student_courses.empty:
                courses_info = student_courses.to_dict('records')
                context += f"Student Courses: {json.dumps(courses_info)}\n\n"
        
        return context
    
    def get_academic_calendar(self):
        """Get academic calendar information."""
        if 'Academic_Calendar.csv' in self.csv_data:
            calendar_data = self.csv_data['Academic_Calendar.csv']
            return json.dumps(calendar_data.to_dict('records'))
        return ""
    
    def search(self, query, registration_number=None):
        """
        Search using Google AI with context from CSV data.
        
        Args:
            query (str): The search query
            registration_number (str, optional): Student registration number for personalized context
            
        Returns:
            str: The response from Google AI
        """
        try:
            # Prepare context from CSV data
            context = ""
            if registration_number:
                context = self.get_student_context(registration_number)
            
            calendar_info = self.get_academic_calendar()
            if calendar_info:
                context += f"Academic Calendar: {calendar_info}\n\n"
            
            # Create the prompt with context
            prompt = f"""You are Raizel, an AI academic assistant. 
            Use the following context to provide accurate and helpful responses:
            
            {context}
            
            If the query is about academic information, use the context provided.
            If the query is general knowledge, use your own knowledge.
            Always be helpful, concise, and accurate.
            
            Query: {query}"""
            
            # Generate response using Google AI
            response = self.model.generate_content(prompt)
            
            # Return the response text
            return response.text
            
        except Exception as e:
            print(f"Error in Google AI search: {str(e)}")
            return f"I encountered an error while searching: {str(e)}"
    
    def generate_summary(self, text, max_length=150):
        """
        Generate a concise summary of the provided text.
        
        Args:
            text (str): The text to summarize
            max_length (int): Maximum length of the summary
            
        Returns:
            str: The generated summary
        """
        try:
            # Create the prompt
            prompt = f"Please summarize the following text in {max_length} characters or less:\n\n{text}"
            
            # Generate summary using Google AI
            response = self.model.generate_content(prompt)
            
            # Return the summary
            return response.text
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return f"I encountered an error while summarizing: {str(e)}"
    
    def answer_question(self, question, registration_number=None):
        """
        Answer a specific question using Google AI with context.
        
        Args:
            question (str): The question to answer
            registration_number (str, optional): Student registration number for personalized context
            
        Returns:
            str: The answer from Google AI
        """
        try:
            # Prepare context from CSV data
            context = ""
            if registration_number:
                context = self.get_student_context(registration_number)
            
            # Create the prompt with context
            prompt = f"""You are Raizel, an AI academic assistant. 
            Use the following context to provide accurate and helpful responses:
            
            {context}
            
            Answer the question based on the context if it's about academic information.
            If the question is about general knowledge, use your own knowledge.
            Always be helpful, concise, and accurate.
            
            Question: {question}"""
            
            # Generate response using Google AI
            response = self.model.generate_content(prompt)
            
            # Return the response text
            return response.text
            
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return f"I encountered an error while answering your question: {str(e)}"

# Example usage
if __name__ == "__main__":
    ai_helper = GoogleAIHelper()
    
    # Example search
    query = "What are the upcoming academic events?"
    print(f"Query: {query}")
    print(f"Response: {ai_helper.search(query)}")
    
    # Example with student context
    student_query = "What are my current courses and grades?"
    registration_number = "REG2023001"
    print(f"\nQuery: {student_query}")
    print(f"Response: {ai_helper.search(student_query, registration_number)}") 