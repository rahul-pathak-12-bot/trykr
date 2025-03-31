# test_handlers.py
from app.question_handlers import identify_question_type, handle_question

# Test cases for each question type
test_cases = [
    {
        "name": "VS Code command",
        "question": "Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below. What is the output of code -s?",
        "expected_type": "vscode_command",
        "expected_answer_start": "Version:          Code 1.96.4"
    },
    {
        "name": "HTTP request",
        "question": "Running uv run --with httpie -- https [URL] installs the Python package httpie and sends a HTTPS request to the URL. Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 23f2000798@ds.study.iitm.ac.in. What is the JSON output of the command?",
        "expected_type": "httpie_request",
        "expected_answer_start": '{\n  "args": {'
    },
    {
        "name": "Prettier NPX",
        "question": "Let's make sure you know how to use npx and prettier. Download . In the directory where you downloaded it, make sure it is called README.md, and run npx -y prettier@3.4.2 README.md | sha256sum. What is the output of the command?",
        "expected_type": "prettier_npx",
        "expected_answer_start": "7b7eb59f381d8c51e21d2a431977c6ae2fce64c7f9b54cffb7d01a59548b9433"
    },
    {
        "name": "Google Sheets formula",
        "question": "Let's make sure you can write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel) =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 15, 0), 1, 10)) What is the result?",
        "expected_type": "google_sheets_formula",
        "expected_answer_start": "150"
    },
    {
        "name": "Excel formula",
        "question": "Let's make sure you can write formulas in Excel. Type this formula into Excel. Note: This will ONLY work in Office 365. =SUM(TAKE(SORTBY({11,1,3,0,12,2,11,9,2,12,2,4,1,14,8,2}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 3)) What is the result?",
        "expected_type": "excel_formula",
        "expected_answer_start": "4"
    }
]

def run_tests():
    print("Testing question handlers...")
    print("-" * 50)
    
    passed = 0
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['name']}")
        
        question = test_case["question"]
        expected_type = test_case["expected_type"]
        expected_answer_start = test_case["expected_answer_start"]
        
        # Test question type identification
        identified_type = identify_question_type(question)
        type_correct = identified_type == expected_type
        
        # Test answer generation
        answer = handle_question(question, identified_type)
        answer_correct = answer and answer.startswith(expected_answer_start)
        
        print(f"  Question type identification: {'✓' if type_correct else '✗'}")
        print(f"  Answer generation: {'✓' if answer_correct else '✗'}")
        
        if not type_correct:
            print(f"  Expected type: {expected_type}, Got: {identified_type}")
        
        if not answer_correct:
            print(f"  Expected answer to start with: {expected_answer_start}")
            print(f"  Got answer: {answer[:100]}...")
        
        if type_correct and answer_correct:
            passed += 1
    
    print("\n" + "-" * 50)
    print(f"Test results: {passed}/{len(test_cases)} tests passed")

if __name__ == "__main__":
    run_tests()