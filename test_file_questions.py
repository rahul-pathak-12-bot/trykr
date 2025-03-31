import os
import requests
import json
import argparse
from pathlib import Path

# Base URL for the API
API_URL = "http://localhost:8000/api/"

# Test cases with questions and associated files
TEST_CASES = [
    {
        "name": "CSV Extract",
        "question": "Download and unzip file which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?",
        "file_path": "test_files/csv_extract/sample.zip"
    },
    {
        "name": "Prettier NPX",
        "question": "Let's make sure you know how to use npx and prettier. Download . In the directory where you downloaded it, make sure it is called README.md, and run npx -y prettier@3.4.2 README.md | sha256sum. What is the output of the command?",
        "file_path": "test_files/prettier_npx/README.md"
    }
    # Add more test cases as needed
]

def setup_folders():
    """Create the necessary folder structure if it doesn't exist"""
    folders = [
        "test_files",
        "test_files/csv_extract",
        "test_files/prettier_npx",
        "test_files/other_files"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        
    print("Folder structure created. Please place your test files in the appropriate folders.")
    print("Example paths:")
    print("  - CSV Extract: test_files/csv_extract/sample.zip")
    print("  - Prettier NPX: test_files/prettier_npx/README.md")

def test_case(case_name=None):
    """Run a specific test case or all test cases"""
    if case_name:
        # Run only the specified test case
        cases = [case for case in TEST_CASES if case["name"].lower() == case_name.lower()]
        if not cases:
            print(f"No test case found with name: {case_name}")
            print(f"Available test cases: {', '.join(case['name'] for case in TEST_CASES)}")
            return
    else:
        # Run all test cases
        cases = TEST_CASES
    
    for case in cases:
        print(f"\nTesting: {case['name']}")
        print("-" * 50)
        
        # Check if the file exists
        file_path = Path(case["file_path"])
        if not file_path.exists():
            print(f"Error: File not found at {file_path}")
            print(f"Please place your test file at this location and try again.")
            continue
        
        # Prepare the request
        files = {
            'file': open(file_path, 'rb'),
            'question': (None, case["question"])
        }
        
        try:
            # Send the request
            print(f"Sending request to {API_URL} with file: {file_path.name}")
            response = requests.post(API_URL, files=files)
            
            # Print the response
            print(f"Status code: {response.status_code}")
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            except:
                print(f"Response text: {response.text}")
        except Exception as e:
            print(f"Error sending request: {e}")
        finally:
            # Close the file
            files['file'].close()

def main():
    parser = argparse.ArgumentParser(description="Test file-based questions against the API")
    parser.add_argument("--setup", action="store_true", help="Set up the folder structure")
    parser.add_argument("--test", help="Run a specific test case by name", default=None)
    
    args = parser.parse_args()
    
    if args.setup:
        setup_folders()
    else:
        # Make sure the API is running
        try:
            response = requests.get(API_URL.replace("/api/", "/health"))
            if response.status_code != 200:
                print("Warning: API may not be running. Please start the API server first.")
        except:
            print("Warning: API may not be running. Please start the API server first.")
        
        # Run the test(s)
        test_case(args.test)

if __name__ == "__main__":
    main()