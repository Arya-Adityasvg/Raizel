from google_ai_integration import GoogleAIHelper

def main():
    # Initialize the Google AI helper
    ai_helper = GoogleAIHelper()
    
    # Example 1: Simple search
    print("\n=== Example 1: Simple Search ===")
    query = "What are the upcoming academic events?"
    print(f"Query: {query}")
    response = ai_helper.search(query)
    print(f"Response: {response}")
    
    # Example 2: Student-specific search
    print("\n=== Example 2: Student-Specific Search ===")
    student_query = "What are my current courses and grades?"
    registration_number = "REG2023001"
    print(f"Query: {student_query}")
    print(f"Registration Number: {registration_number}")
    response = ai_helper.search(student_query, registration_number)
    print(f"Response: {response}")
    
    # Example 3: Generate a summary
    print("\n=== Example 3: Generate a Summary ===")
    text = """
    The academic calendar for the current semester includes several important dates:
    - Mid-term exams: March 15-20, 2023
    - Spring break: April 3-7, 2023
    - Final exams: May 15-20, 2023
    - Commencement ceremony: May 25, 2023
    
    Students are advised to check their course syllabi for specific assignment deadlines
    and to register for courses by the end of the add/drop period on January 20, 2023.
    """
    print(f"Text to summarize: {text[:100]}...")
    summary = ai_helper.generate_summary(text, max_length=100)
    print(f"Summary: {summary}")
    
    # Example 4: Answer a question
    print("\n=== Example 4: Answer a Question ===")
    question = "What is the deadline for course registration?"
    print(f"Question: {question}")
    answer = ai_helper.answer_question(question)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main() 