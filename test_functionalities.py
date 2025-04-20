from google_ai_integration import GoogleAIHelper

def test_functionalities():
    print("🔍 Testing Google AI Integration Functionalities")
    print("=" * 50)
    
    # Initialize the AI helper
    ai = GoogleAIHelper()
    
    # Test 1: Basic Question
    print("\n1. Testing Basic Question:")
    question = "What is the importance of education?"
    print(f"Question: {question}")
    response = ai.answer_question(question)
    print(f"Response: {response}")
    
    # Test 2: Student Information Query
    print("\n2. Testing Student Information Query:")
    reg_number = "REG2023001"  # John Doe from Computer Science
    question = "What is the CGPA of the student with registration number REG2023001?"
    print(f"Question (for student {reg_number}): {question}")
    response = ai.search(question, reg_number)
    print(f"Response: {response}")
    
    # Test 3: Academic Calendar Query
    print("\n3. Testing Academic Calendar Query:")
    question = "What are the upcoming events in March 2024?"
    print(f"Question: {question}")
    response = ai.search(question)
    print(f"Response: {response}")
    
    # Test 4: Text Summarization
    print("\n4. Testing Text Summarization:")
    text = """
    The academic calendar shows several important events:
    Mid-Term Exams on March 15, 2024
    Spring Break starting March 25, 2024
    Project Submissions due on April 10, 2024
    Final Exams beginning May 1, 2024
    And Summer Break starting May 15, 2024
    """
    print("Original Text:", text)
    summary = ai.generate_summary(text, max_length=100)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    test_functionalities() 